import os
import threading
import asyncio
import time
from datetime import datetime
import keyboard  # pip install keyboard
from eigenlib.utils.audio_io import AudioIO
from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
from typing import Optional
from eigenlib.utils.notion_io import NotionIO

NOTION_AVAILABLE = True


class Transcriptor:
    def __init__(self, output_dir, block_duration=60, sample_rate=48000, compression='medium',
                 to_notion=False, notion_page_id="23d2a599e98580d6b20dc30f999a1a2c"):
        """
        Args:
            output_dir (str): Carpeta donde se guardarán las transcripciones y audios.
            block_duration (int): Duración en segundos de cada bloque de grabación.
            sample_rate (int): Frecuencia de muestreo de grabación.
            compression (str): Nivel de compresión para los bloques de audio.
            to_notion (bool): Si True, sube las transcripciones a Notion.
            notion_page_id (str): ID de la página de Notion donde subir transcripciones.
        """
        self.output_dir = output_dir
        self.block_duration = block_duration
        self.sample_rate = sample_rate
        self.compression = compression
        self.to_notion = to_notion
        self.notion_page_id = notion_page_id

        os.makedirs(self.output_dir, exist_ok=True)

        # Clases auxiliares
        self.audio_handler = AudioIO(sample_rate=self.sample_rate)
        self.transcriber = OAIWhisperSTTClass()

        # Configurar Notion si está habilitado
        self.notion_manager = None
        if self.to_notion:
            if NOTION_AVAILABLE:
                try:
                    self.notion_manager = NotionIO()
                    print("✅ Notion configurado correctamente")
                except Exception as e:
                    print(f"⚠️ Error configurando Notion: {e}")
                    self.to_notion = False
            else:
                print("⚠️ notion-client no disponible. Instalé con: pip install notion-client")
                self.to_notion = False

        # Estado de la grabación
        self.is_recording = False
        self.should_exit = False

        # Control de hilos y asyncio
        self.loop = None
        self.background_thread = None
        self.recording_thread = None

        # Para manejar el último bloque
        self.pending_tasks = []

        # Control de sesión para Notion
        self.current_session_started = False
        self.notion_upload_lock = threading.Lock()  # Para evitar uploads concurrentes

    def _start_event_loop(self):
        """Inicia el event loop en un hilo separado."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _submit_async(self, coro):
        """Enviar una tarea al loop asincrónico desde un hilo externo."""
        if self.loop and not self.loop.is_closed():
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)
            self.pending_tasks.append(future)
            return future
        return None

    def _create_session_title(self) -> str:
        """Crea un título para la sesión actual con fecha y hora."""
        now = datetime.now()
        # Días de la semana en español
        days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        day_name = days[now.weekday()]

        return f"{day_name} {now.strftime('%d/%m/%Y - %H:%M')}"

    async def _upload_to_notion(self, text: str, is_session_start: bool = False, block_timestamp: str = None):
        """Sube contenido a Notion de forma asíncrona e inmediata."""
        if not self.to_notion or not self.notion_manager:
            return

        # Usar lock para evitar uploads concurrentes que puedan causar problemas
        with self.notion_upload_lock:
            try:
                if is_session_start:
                    # Crear título de sesión
                    session_title = self._create_session_title()
                    print(f"📝 Creando sesión en Notion: {session_title}")
                    success = self.notion_manager.write_heading(self.notion_page_id, session_title, level=2)
                    if success:
                        print(f"✅ Nueva sesión creada en Notion: {session_title}")
                    else:
                        print("❌ Error creando título de sesión en Notion")
                elif text and text.strip() and not text.startswith("[ERROR"):
                    # Subir inmediatamente cada transcripción con timestamp
                    timestamp_str = f"[{datetime.now().strftime('%H:%M:%S')}]" if block_timestamp else ""
                    formatted_text = f"{timestamp_str} {text.strip()}" if timestamp_str else text.strip()

                    print(f"📝 Subiendo a Notion: {formatted_text[:100]}...")
                    success = self.notion_manager.write_text(self.notion_page_id, formatted_text)

                    if success:
                        print(f"✅ Transcripción subida a Notion ({len(formatted_text)} caracteres)")
                    else:
                        print("❌ Error subiendo transcripción a Notion")
                        # Reintentar una vez más
                        print("🔄 Reintentando subida a Notion...")
                        time.sleep(1)
                        success_retry = self.notion_manager.write_text(self.notion_page_id, formatted_text)
                        if success_retry:
                            print("✅ Transcripción subida en segundo intento")
                        else:
                            print("❌ Fallo definitivo subiendo a Notion")
                elif text and text.startswith("[ERROR"):
                    print(f"⚠️ No se sube error de transcripción a Notion: {text}")
                else:
                    print(f"⚠️ Texto vacío o inválido, no se sube a Notion: '{text}'")

            except Exception as e:
                print(f"❌ Error en upload a Notion: {e}")
                import traceback
                print(f"❌ Traceback completo: {traceback.format_exc()}")

    async def _process_block(self, block_data, block_rate, timestamp):
        """Procesar un bloque: guardar y transcribir."""
        print(f"🔄 Procesando bloque {timestamp}...")

        try:
            # 1. Guardar archivo de audio
            audio_filename = os.path.join(self.output_dir, f"audio_{timestamp}.mp3")
            self.audio_handler.save(audio_filename, source=(block_data, block_rate),
                                    bitrate_compression=self.compression)
            print(f"💾 Audio guardado: {audio_filename}")

            # 2. Transcribir
            print(f"🎯 Iniciando transcripción para bloque {timestamp}...")
            try:
                text = self.transcriber.run(audio_filename)
                print(f"📝 Transcripción completada: '{text[:100]}...'")
            except Exception as e:
                text = f"[ERROR en transcripción: {e}]"
                print(f"❌ Error en transcripción: {e}")

            # 3. Guardar transcripción
            txt_filename = os.path.join(self.output_dir, f"transcripcion_{timestamp}.txt")
            with open(txt_filename, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"✅ Bloque {timestamp} procesado. Audio y transcripción guardados.")

            # 4. Subir INMEDIATAMENTE a Notion si está habilitado y hay texto válido
            if self.to_notion and text and text.strip() and not text.startswith("[ERROR"):
                print(f"📤 Enviando a Notion inmediatamente...")
                await self._upload_to_notion(text.strip(), is_session_start=False, block_timestamp=timestamp)
            elif self.to_notion and text.startswith("[ERROR"):
                print(f"⚠️ No se envía error de transcripción a Notion")
            elif self.to_notion:
                print(f"⚠️ Texto vacío o inválido, no se envía a Notion: '{text}'")

        except Exception as e:
            print(f"❌ Error procesando bloque {timestamp}: {e}")
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")

    def _record_loop(self):
        """Graba en bloques sucesivos hasta que se detenga."""
        print(f"🎙️ Grabación iniciada. Bloques de {self.block_duration}s")

        try:
            while self.is_recording:
                print(f"🔴 Iniciando nuevo bloque de {self.block_duration}s...")

                # Iniciar grabación del bloque
                self.audio_handler.start_recording()

                # Esperar la duración del bloque o hasta que se detenga
                start_time = time.time()
                while time.time() - start_time < self.block_duration and self.is_recording:
                    time.sleep(0.1)  # Check más frecuente para respuesta rápida

                # Obtener el bloque grabado
                block_data = self.audio_handler.stop_recording()

                if block_data is not None:
                    print(f"🎵 Bloque de audio capturado, comprimiendo...")
                    # Comprimir bloque
                    compressed = self.audio_handler.compress(compression=self.compression)
                    if compressed is not None:
                        block_data, block_rate = compressed
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Incluir milisegundos
                        print(f"📦 Bloque comprimido, enviando a procesar: {timestamp}")
                        # Procesar de forma asíncrona
                        self._submit_async(self._process_block(block_data, block_rate, timestamp))
                    else:
                        print("❌ Error comprimiendo bloque de audio")
                else:
                    print("❌ No se pudo obtener datos del bloque de audio")

        except Exception as e:
            print(f"❌ Error en el bucle de grabación: {e}")
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")

        print("🛑 Grabación detenida.")

    def _start_recording(self):
        """Inicia la grabación en un hilo separado."""
        if not self.is_recording:
            print("🚀 Iniciando grabación...")
            self.is_recording = True
            self.current_session_started = True

            # Crear título de sesión en Notion si está habilitado
            if self.to_notion:
                print("📝 Creando título de sesión en Notion...")
                self._submit_async(self._upload_to_notion("", is_session_start=True))

            self.recording_thread = threading.Thread(target=self._record_loop, daemon=True)
            self.recording_thread.start()
            print("✅ Grabación iniciada correctamente")

    def _stop_recording(self):
        """Detiene la grabación y espera a que terminen las tareas pendientes."""
        if self.is_recording:
            print("⏹️ Deteniendo grabación...")
            self.is_recording = False

            # Esperar a que termine el hilo de grabación
            if self.recording_thread and self.recording_thread.is_alive():
                print("⏳ Esperando que termine el hilo de grabación...")
                self.recording_thread.join(timeout=5)

            # Esperar a que terminen todas las tareas de procesamiento
            if self.pending_tasks:
                print(f"⏳ Esperando a que terminen {len(self.pending_tasks)} transcripciones...")
                completed = 0
                for task in self.pending_tasks:
                    try:
                        task.result(timeout=30)  # Timeout de 30 segundos por tarea
                        completed += 1
                        print(f"✅ Transcripción {completed}/{len(self.pending_tasks)} completada")
                    except Exception as e:
                        print(f"⚠️ Error esperando tarea: {e}")
                self.pending_tasks.clear()

            # Reset session state
            self.current_session_started = False

            print("✅ Grabación completamente detenida.")

    def _cleanup(self):
        """Limpia recursos antes de salir."""
        print("🧹 Limpiando recursos...")

        # Detener grabación si está activa
        if self.is_recording:
            self._stop_recording()

        # Cerrar el event loop
        if self.loop and not self.loop.is_closed():
            self.loop.call_soon_threadsafe(self.loop.stop)

        # Esperar a que termine el hilo del event loop
        if self.background_thread and self.background_thread.is_alive():
            self.background_thread.join(timeout=3)

    def _print_status(self):
        """Muestra el estado actual de la aplicación."""
        notion_status = "📝 Notion ON" if self.to_notion else "📝 Notion OFF"
        pending_tasks_count = len(self.pending_tasks)
        tasks_info = f" | 📋 {pending_tasks_count} tareas pendientes" if pending_tasks_count > 0 else ""

        if self.is_recording:
            print(f"🔴 GRABANDO | {notion_status}{tasks_info} | Presiona CTRL+ALT+S para detener | ESC para salir")
        else:
            print(f"⚪ PARADO | {notion_status}{tasks_info} | Presiona CTRL+ALT+R para grabar | ESC para salir")

    def run(self):
        """Ejecuta la aplicación principal que espera teclas."""
        print("=" * 70)
        print("🎙️  APLICACIÓN DE TRANSCRIPCIÓN")
        if self.to_notion:
            print(f"📝 Notion habilitado - Página: {self.notion_page_id}")
        print("=" * 70)
        print("Controles:")
        print("  CTRL+ALT+R : Iniciar grabación")
        print("  CTRL+ALT+S : Detener grabación")
        print("  ESC        : Salir de la aplicación")
        print("=" * 70)

        # Iniciar el event loop en background
        self.background_thread = threading.Thread(target=self._start_event_loop, daemon=True)
        self.background_thread.start()

        # Esperar a que el loop esté listo
        time.sleep(0.5)

        self._print_status()

        try:
            while not self.should_exit:
                # Iniciar grabación
                if keyboard.is_pressed("ctrl+alt+r") and not self.is_recording:
                    self._start_recording()
                    time.sleep(0.5)  # Evitar rebotes
                    self._print_status()

                # Detener grabación
                if keyboard.is_pressed("ctrl+alt+s") and self.is_recording:
                    self._stop_recording()
                    self._print_status()
                    time.sleep(0.5)  # Evitar rebotes

                # Salir de la aplicación
                if keyboard.is_pressed("esc"):
                    print("🚪 Saliendo de la aplicación...")
                    self.should_exit = True
                    break

                time.sleep(0.1)  # Reducir uso de CPU

        except KeyboardInterrupt:
            print("\n🛑 Interrupción por teclado detectada.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        finally:
            self._cleanup()
            print("👋 Aplicación finalizada correctamente.")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    app = Transcriptor(
        output_dir="./data/processed/audios",
        block_duration=30,
        sample_rate=48000,
        compression="high",
        to_notion=True,
        notion_page_id="23d2a599e98580d6b20dc30f999a1a2c"
    )
    app.run()