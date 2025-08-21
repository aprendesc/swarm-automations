import os
from datetime import datetime
import keyboard
import tempfile
import subprocess
from eigenlib.audio.audio_mixer_recorder import AudioMixerRecorder
from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
from eigenlib.utils.notion_utils import NotionUtilsClass

class CallRecordingPipelineClass:
    def __init__(self):
        pass

    # ---------------------------------------------------------------------
    # Helper: compress audio (high quality → 16k bitrate MP3)
    # ---------------------------------------------------------------------
    def _compress_audio(self, input_path: str) -> str:
        """Compress `input_path` to a temporary MP3 (high settings) and return its path."""
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp_file.close()
        tmp_path = tmp_file.name

        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-c:a", "libmp3lame",
            "-b:a", "16k",
            "-ac", "1",
            "-ar", "11025",
            "-map_metadata", "-1",
            "-f", "mp3",
            tmp_path,
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print("⚠️  Error al comprimir el audio, se enviará el original:", e)
            return input_path

        return tmp_path

    def run(self):
        # Instancias de grabación, STT y Notion
        mixer = AudioMixerRecorder()
        whisper_model = OAIWhisperSTTClass()
        NU = NotionUtilsClass()

        # ID de la página de Notion donde acumulamos las transcripciones
        page_id = "23d2a599e98580178243d907aa70218b"

        print("============================================")
        print("  Ctrl+Alt+R → Iniciar grabación")
        print("        Esc   → Detener, transcribir y subir a Notion")
        print("  Ctrl+C o cierre de ventana → Salir")
        print("============================================\n")

        try:
            while True:
                # Esperamos al atajo para empezar a grabar
                keyboard.wait("ctrl+alt+r")
                output_path = self.formatear_nombre_por_fecha()
                mixer.archivo_salida = output_path
                mixer.start()
                print(f"Grabando... (archivo → {output_path})")

                # Esperamos a que el usuario presione ESC
                keyboard.wait("esc")
                mixer.stop()
                print("Grabación detenida. Procesando audio...\n")

                # ---------------------------------------------------------
                # 1) Comprimir antes de transcribir
                # ---------------------------------------------------------
                audio_a_transcribir = self._compress_audio(output_path)

                # 2) Transcribir con Whisper
                try:
                    transcription = whisper_model.run(audio_a_transcribir, engine='cloud')
                    print("Transcripción obtenida:")
                    print(transcription, "\n")
                except Exception as e:
                    print("⚠️ Error al transcribir el audio:", e)
                    continue  # saltamos la parte de Notion y volvemos a esperar el siguiente Ctrl+Alt+R

                # 3) Leer contenido previo de la página de Notion
                try:
                    contenido_actual = NU.read(page_id=page_id)
                except Exception as e:
                    print("⚠️ Error al leer página de Notion:", e)
                    contenido_actual = ""

                # 4) Acumular la transcripción y escribir de nuevo
                try:
                    texto_a_escribir = transcription
                    max_longitud = 1500

                    # Divide el texto en bloques de máximo 1500 caracteres sin cortar palabras
                    def dividir_en_bloques(texto, max_long):
                        bloques = []
                        while len(texto) > max_long:
                            # Buscar el último espacio dentro del límite para no cortar palabras
                            corte = texto.rfind(' ', 0, max_long)
                            if corte == -1:
                                corte = max_long  # Si no hay espacio, corta de todos modos
                            bloques.append(texto[:corte].strip())
                            texto = texto[corte:].lstrip()
                        if texto:
                            bloques.append(texto.strip())
                        return bloques

                    bloques = dividir_en_bloques(texto_a_escribir, max_longitud)

                    for i, bloque in enumerate(bloques):
                        NU.write(page_id=page_id, texto=bloque)
                    print("✅ Transcripción subida y acumulada en Notion.\n")
                except Exception as e:
                    print("⚠️ Error al escribir en Notion:", e)

                print("Vuelve a pulsar Ctrl+Alt+R para otra grabación.\n")

        except KeyboardInterrupt:
            print("\nSaliendo...")
            if mixer.is_recording:
                mixer.stop()

    def formatear_nombre_por_fecha(self, base_path='./data/curated/automations_app_call_recording') -> str:
        """Genera un string tipo './data/curated/domingo_21_julio_2025_13_35.flac'"""
        dias_semana = [
            "lunes", "martes", "miércoles", "jueves",
            "viernes", "sábado", "domingo"
        ]
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre",
            "noviembre", "diciembre"
        ]
        ahora = datetime.now()
        dia_sem = dias_semana[ahora.weekday()]
        dia_num = ahora.day
        mes = meses[ahora.month - 1]
        ano = ahora.year
        hora = ahora.hour
        minuto = ahora.minute

        # Aseguramos que la carpeta existe
        os.makedirs(base_path, exist_ok=True)

        nombre = f"{dia_sem}_{dia_num}_{mes}_{ano}_{hora:02d}_{minuto:02d}.flac"
        return os.path.join(base_path, nombre)
