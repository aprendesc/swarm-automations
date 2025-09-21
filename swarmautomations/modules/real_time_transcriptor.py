import os
import threading
import time
from datetime import datetime
from typing import Optional

import keyboard  # pip install keyboard
import pyautogui  # pip install pyautogui
import pyperclip  # pip install pyperclip

from eigenlib.utils.audio_io import AudioIO
from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass


class RealTimeTranscriptor:
    """Transcripción de voz con toggle usando la tecla º.

    Flujo:
      1. Al presionar º por primera vez comienza la grabación.
      2. Al presionar º por segunda vez se detiene, se procesa el audio y se
         escribe la transcripción donde esté el cursor.
    """

    def __init__(
            self,
            sample_rate: int = 48_000,
            temp_audio_dir: Optional[str] = None,
    ) -> None:
        self.sample_rate = sample_rate
        self.temp_audio_dir = temp_audio_dir or os.path.join(
            os.path.expanduser("~"), "tmp_rt_transcriptions"
        )
        os.makedirs(self.temp_audio_dir, exist_ok=True)

        self.audio_io = AudioIO(sample_rate=sample_rate)
        self.stt = OAIWhisperSTTClass()

        self._recording = False
        self._lock = threading.Lock()

        # Configuramos pyautogui para mayor velocidad
        pyautogui.PAUSE = 0.01

        # Registramos evento de teclado para la tecla º
        keyboard.on_press_key("º", self._on_toggle_key_press)
        print(
            "[RealTimeTranscriptor] Presiona º para iniciar/detener la grabación y transcribir."
        )

    # ------------------------------------------------------------------
    # Keyboard callbacks
    # ------------------------------------------------------------------

    def _on_toggle_key_press(self, e):
        with self._lock:
            if not self._recording:
                self._start_recording()
            else:
                # Lanzamos la transcripción en un hilo aparte para no bloquear
                threading.Thread(target=self._stop_and_transcribe, daemon=True).start()

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------

    def _start_recording(self):
        try:
            self.audio_io.start_recording()
            self._recording = True
            self._t_start = time.time()
            print("[RealTimeTranscriptor] Grabando...")
        except Exception as exc:
            print(f"[RealTimeTranscriptor] Error al iniciar la grabación: {exc}")

    def _stop_and_transcribe(self):
        try:
            audio_chunk = self.audio_io.stop_recording()
        except Exception as exc:
            print(f"[RealTimeTranscriptor] Error al detener la grabación: {exc}")
            audio_chunk = None
        self._recording = False

        if audio_chunk is None:
            print("[RealTimeTranscriptor] No se capturó audio válido.")
            return

        # Guardamos audio temporal
        fname = datetime.now().strftime("rt_%Y%m%d_%H%M%S.mp3")
        fpath = os.path.join(self.temp_audio_dir, fname)
        try:
            self.audio_io.save(
                fpath,
                (audio_chunk, self.sample_rate),
                bitrate_compression="medium",
            )
        except Exception as exc:
            print(f"[RealTimeTranscriptor] Error al guardar audio temporal: {exc}")
            return

        # Transcripción
        try:
            transcription = self.stt.run(fpath)
        except Exception as exc:
            print(f"[RealTimeTranscriptor] Error durante la transcripción: {exc}")
            transcription = ""

        # Escribimos texto usando portapapeles (más rápido y mejor para español)
        if transcription:
            dur = time.time() - self._t_start
            print(f"[RealTimeTranscriptor] ({dur:.1f}s) -> {transcription}")
            self._paste_text(transcription + " ")

        # Limpieza
        try:
            os.remove(fpath)
        except OSError:
            pass

    def _paste_text(self, text: str):
        """Pega texto usando el portapapeles (rápido y compatible con español)."""
        try:
            # Guardamos el contenido actual del portapapeles
            original_clipboard = pyperclip.paste()

            # Copiamos nuestro texto al portapapeles
            pyperclip.copy(text)

            # Pegamos con Ctrl+V
            pyautogui.hotkey('ctrl', 'v')

            # Restauramos el contenido original del portapapeles
            pyperclip.copy(original_clipboard)

        except Exception as exc:
            print(f"[RealTimeTranscriptor] Error al pegar texto: {exc}")
            # Fallback: usar typewrite simple
            try:
                pyautogui.typewrite(text)
            except Exception as exc2:
                print(f"[RealTimeTranscriptor] Error en fallback: {exc2}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def wait(self):
        """Mantiene el script vivo (Ctrl+C para salir)."""
        print("[RealTimeTranscriptor] Esperando eventos… (Ctrl+C para salir)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[RealTimeTranscriptor] Finalizando…")
            # Si queda una grabación en marcha la procesamos
            with self._lock:
                if self._recording:
                    self._stop_and_transcribe()