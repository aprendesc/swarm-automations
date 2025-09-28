import time
from eigenlib.utils.audio_io import AudioIO
from eigenlib.utils.notion_io import NotionIO
import tempfile
from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
from datetime import datetime
from eigenlib.genai.utils.llm_client import LLMClient
from eigenlib.genai.utils.memory import Memory
import threading
import os

class SessionRecorder:
    def __init__(self, raw_page_id=None, page_id=None):
        self.audio_handler = AudioIO(sample_rate=48000)
        self.raw_page_id = raw_page_id
        self.page_id = page_id
        self.stt = OAIWhisperSTTClass()
        self.notion_utils = NotionIO()
        self.recording = False
        self.recording_thread = None
        self.transcriptions = []
        self.chunk_start_time = None

    def start(self, chunk_seconds=20, summarize=True):
        """Inicia la grabación con volcado de mensajes cada chunk_second segundos."""
        self.summarize = summarize
        if self.recording:
            print("La grabación ya está en curso.")
            return

        self.recording = True
        self.transcriptions = []  # Reset transcriptions for new session
        print(f"Iniciando grabación con chunks de {chunk_seconds} segundos...")

        # Iniciar el thread de grabación
        self.recording_thread = threading.Thread(
            target=self.record_chunk,
            args=(chunk_seconds,),
            daemon=True
        )
        self.recording_thread.start()

    def stop(self):
        """Para de grabar, procesa el último chunk pendiente y sumariza las transcripciones acumuladas."""
        if not self.recording:
            print("No hay grabación en curso.")
            return

        print("Deteniendo grabación...")
        self.recording = False

        # Esperar a que termine el thread actual si existe
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=10)

        # Procesar el último chunk de audio si hay algo grabado
        self._process_final_chunk()

        # Combinar todas las transcripciones
        if not self.transcriptions:
            print("No hay transcripciones para procesar.")
            return

        transcription = "\n".join(self.transcriptions)
        print("Procesando resumen...")

        # SUMMARIZATION
        if self.summarize:
            memory = Memory()
            system_prompt = """
    Eres un asistente especializado en resumir transcripciones de reuniones obtenidas con Whisper, que pueden contener errores de transcripción y no están diarizadas por participante. 
    Tu misión es: 
    Corrección y claridad: Corrige los errores de transcripción, ortografía, gramática y expresiones mal reconocidas, asegurando que el texto final sea fluido, natural y preciso. 
    Estructuración del contenido: Resume la reunión de forma clara y organizada. 
    Divide el contenido en secciones temáticas o puntos principales.
    Cuando el tema lo requiera, desarrolla explicaciones detalladas para que cualquier lector pueda comprender la conversación sin haber asistido a la reunión. 
    Registro de acuerdos y acciones: Identifica y lista de manera explícita: 
    Decisiones tomadas Tareas pendientes (To-Dos) con responsables sugeridos si es posible Próximos pasos 
    Detección de incertidumbres y dudas: Señala posibles malentendidos, fragmentos poco claros en la transcripción, o temas que podrían necesar aclaración en la siguiente reunión.  
    Formula estas dudas de manera explícita como recomendaciones para mejorar la comprensión y la calidad futura. 
    Formato final esperado: Resumen ejecutivo breve (2–5 líneas, visión general) 
    Desarrollo estructurado (temas tratados en viñetas o secciones) 
    Lista de acuerdos To-Dos y próximos pasos Dudas / puntos de mejora para la próxima reunión 
    Mantén siempre un tono profesional, claro y neutral."""
            memory.log(role="system", modality="text", content=system_prompt, channel="SUMMARIZER")
            memory.log(role="user", modality="text", content=transcription, channel="SUMMARIZER")
            answer = LLMClient(client='oai_1').run(memory.history, model='gpt-4o')

            # UPLOAD TO NOTION
            content = f"""
    # {datetime.now().strftime("%A %Y-%m-%d %H:%M:%S")}
    {answer}
    """
            self.notion_utils.write_page_content(page_id=page_id, markdown_content=content, clear_existing=False)
            print("Resumen guardado en Notion.")

    def _process_final_chunk(self):
        """Procesa el último fragmento de audio pendiente cuando se para la grabación."""
        try:
            print("Procesando último fragmento de audio...")

            # Detener la grabación y obtener el audio
            self.audio_handler.stop_recording()
            audio_comprimido = self.audio_handler.compress(compression='medium')
            tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            self.audio_handler.save(tmp.name, source=audio_comprimido)

            # TRANSCRIPTION del último fragmento - SIEMPRE procesar
            transcription = self.stt.run(audio_path=tmp.name)

            # Guardar transcripción SIEMPRE, aunque esté vacía o sea corta
            self.transcriptions.append(transcription)

            # UPLOAD TO NOTION
            content = f"""
{transcription}
"""
            self.notion_utils.write_page_content(page_id=raw_page_id, markdown_content=content, clear_existing=False)
            print(f"Último fragmento procesado: '{transcription[:50]}...'")

            # Limpiar archivo temporal
            try:
                os.unlink(tmp.name)
            except:
                pass

        except Exception as e:
            print(f"Error procesando último fragmento: {e}")

    def record_chunk(self, chunk_seconds=20):
        """RECORDING - Graba en chunks continuos hasta que se pare la sesión"""
        date_header = f"""
# {datetime.now().strftime("%A %Y-%m-%d %H:%M:%S")}"""
        self.notion_utils.write_page_content(page_id=raw_page_id, markdown_content=date_header, clear_existing=False)

        # Iniciar la grabación INMEDIATAMENTE
        self.audio_handler.start_recording(mic_volume=0.8, loopback_volume=1.0)
        self.chunk_start_time = time.time()

        while self.recording:
            try:
                # Esperar hasta completar el chunk o hasta que se pare la grabación
                elapsed = 0
                while elapsed < chunk_seconds and self.recording:
                    time.sleep(0.1)  # Verificar cada 100ms si debemos parar
                    elapsed = time.time() - self.chunk_start_time

                # Si se paró la grabación antes de completar el chunk,
                # salir del bucle - el último fragmento se procesará en _process_final_chunk()
                if not self.recording:
                    break

                # Completamos un chunk, procesarlo
                self.audio_handler.stop_recording()
                audio_comprimido = self.audio_handler.compress(compression='medium')
                tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                self.audio_handler.save(tmp.name, source=audio_comprimido)

                # TRANSCRIPTION
                transcription = self.stt.run(audio_path=tmp.name)

                # Guardar transcripción para el resumen final
                self.transcriptions.append(transcription)

                # UPLOAD TO NOTION
                content = f"""
{transcription}
"""
                self.notion_utils.write_page_content(page_id=raw_page_id, markdown_content=content,
                                                     clear_existing=False)

                # Limpiar archivo temporal
                try:
                    os.unlink(tmp.name)
                except:
                    pass

                # Continuar con la siguiente grabación si aún estamos activos
                if self.recording:
                    self.audio_handler.start_recording(mic_volume=0.8, loopback_volume=1.0)
                    self.chunk_start_time = time.time()

            except Exception as e:
                print(f"Error durante la grabación: {e}")
                if self.recording:  # Solo continuar si seguimos grabando
                    time.sleep(1)  # Pequeña pausa antes de reintentar
                    try:
                        # Intentar reiniciar la grabación
                        self.audio_handler.start_recording(mic_volume=0.8, loopback_volume=1.0)
                        self.chunk_start_time = time.time()
                    except:
                        print("No se pudo reiniciar la grabación")
                        break

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    raw_page_id = '27c2a599-e985-802d-9432-f6a6fbab7105'
    page_id = '2742a599-e985-8023-a111-d9972ae4f61a'
    sm = SessionRecorder(raw_page_id=raw_page_id, page_id=page_id)
    sm.start(chunk_seconds=20, summarize=True)
    time.sleep(35)
    sm.stop()
