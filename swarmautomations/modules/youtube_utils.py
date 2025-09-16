import os
import subprocess
import time
import random
from yt_dlp import YoutubeDL

class YoutubeUtilsClass:
    def __init__(
            self,
            quiet: bool = True,
            no_warnings: bool = True,
    ):
        """
        Parámetros:
        ----------
        quiet : bool
            Suprime salida estándar de yt_dlp.
        no_warnings : bool
            Suprime advertencias de yt_dlp.
        """
        self.quiet = quiet
        self.no_warnings = no_warnings
        # Ajusta la ruta a tu binario de ffmpeg si es necesario
        self.ffmpeg_path = 'C:/ffmpeg-2025-07-01-git-11d1b71c31-essentials_build/bin/ffmpeg.exe'

    def _get_random_user_agent(self):
        """Retorna un User-Agent aleatorio para evitar detección."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        return random.choice(user_agents)

    def _get_base_options(self, output_dir: str, filename: str):
        """Configuración base de yt_dlp con medidas anti-detección."""
        return {
            "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
            "outtmpl": os.path.join(output_dir, f"{filename}.%(ext)s"),
            "quiet": self.quiet,
            "no_warnings": self.no_warnings,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "no_playlist": True,
            "extract_flat": False,

            # Headers anti-detección
            "http_headers": {
                "User-Agent": self._get_random_user_agent(),
                "Referer": "https://www.youtube.com/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            },

            # Configuraciones adicionales anti-bot
            "extractor_retries": 3,
            "fragment_retries": 3,
            "retry_sleep_functions": {
                "http": lambda n: min(4 ** n, 60),
                "fragment": lambda n: min(4 ** n, 60),
                "extractor": lambda n: min(2 ** n, 10)
            },

            # Simular comportamiento de navegador
            "sleep_interval": 1,
            "max_sleep_interval": 5,
            "sleep_interval_subtitles": 1,
        }

    def download_audio_with_fallback(
            self,
            video_url: str,
            output_dir: str,
            filename: str = "original_audio",
            compress: bool = False,
            compression_level: str = "high",
            max_retries: int = 3
    ) -> str:
        """
        Descarga audio con múltiples estrategias de fallback para evitar 403.

        Parámetros:
        -----------
        video_url : str
            URL del vídeo de YouTube.
        output_dir : str
            Carpeta donde guardar el audio.
        filename : str
            Nombre base del fichero sin extensión.
        compress : bool
            Si True, aplica compresión FFmpeg.
        compression_level : str
            Nivel de compresión: "low", "medium", "high", "extreme"
        max_retries : int
            Número máximo de intentos con diferentes estrategias.

        Retorna:
        --------
        str
            Ruta completa al archivo descargado.
        """
        os.makedirs(output_dir, exist_ok=True)

        strategies = [
            #self._strategy_cookies,
            #self._strategy_proxy_simulation,
            #self._strategy_age_gate_bypass,
            self._strategy_minimal_format
        ]

        last_error = None

        for attempt in range(max_retries):
            for i, strategy in enumerate(strategies):
                try:
                    if not self.quiet:
                        print(f"Intento {attempt + 1}, Estrategia {i + 1}: {strategy.__name__}")

                    # Espera aleatoria entre intentos
                    if attempt > 0 or i > 0:
                        sleep_time = random.uniform(2, 6)
                        time.sleep(sleep_time)

                    ydl_opts = strategy(output_dir, filename)

                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)

                    # Si llegamos aquí, la descarga fue exitosa
                    ext = info.get("ext", "")
                    downloaded_path = os.path.join(output_dir, f"{filename}.{ext}")

                    if compress:
                        return self._compress_audio(downloaded_path, output_dir, filename, compression_level)

                    return downloaded_path

                except Exception as e:
                    last_error = e
                    if not self.quiet:
                        print(f"Estrategia {i + 1} falló: {str(e)}")
                    continue

        # Si todas las estrategias fallaron
        raise Exception(f"Todas las estrategias fallaron. Último error: {last_error}")

    def _strategy_cookies(self, output_dir: str, filename: str):
        """Estrategia 1: Usar cookies simuladas y configuración estándar mejorada."""
        opts = self._get_base_options(output_dir, filename)
        opts.update({
            # Simular cookies de sesión
            "http_headers": {
                **opts["http_headers"],
                "Cookie": "CONSENT=YES+cb.20210328-17-p0.en+FX+854; YSC=DwKYllHNwuw; VISITOR_INFO1_LIVE=jMbHaoYJoXI"
            }
        })
        return opts

    def _strategy_proxy_simulation(self, output_dir: str, filename: str):
        """Estrategia 2: Simular diferentes configuraciones de proxy."""
        opts = self._get_base_options(output_dir, filename)
        opts.update({
            "http_headers": {
                **opts["http_headers"],
                "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "X-Real-IP": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            },
            # Usar extractor específico
            "force_generic_extractor": False,
        })
        return opts

    def _strategy_age_gate_bypass(self, output_dir: str, filename: str):
        """Estrategia 3: Bypass para contenido con restricción de edad."""
        opts = self._get_base_options(output_dir, filename)
        opts.update({
            # Configuraciones para bypass de age gate
            "age_limit": 99,
            "http_headers": {
                **opts["http_headers"],
                "Cookie": "PREF=f1=50000000&f6=8&hl=en-US&f5=30&f4=4000000; CONSENT=YES+cb"
            }
        })
        return opts

    def _strategy_minimal_format(self, output_dir: str, filename: str):
        """Estrategia 4: Formato mínimo y configuración simplificada."""
        opts = self._get_base_options(output_dir, filename)
        opts.update({
            # Formato más simple
            "format": "worst[ext=webm]/worst",
            "prefer_free_formats": True,
            # Reducir timeouts
            "socket_timeout": 30,
            "http_headers": {
                "User-Agent": self._get_random_user_agent(),
                "Accept": "*/*"
            }
        })
        return opts

    def _compress_audio(self, downloaded_path: str, output_dir: str, filename: str, compression_level: str):
        """Comprime el audio descargado."""
        compression_configs = {
            "low": {
                "codec": "libmp3lame",
                "ext": "mp3",
                "bitrate": "48k",
                "channels": "2",
                "sample_rate": "22050"
            },
            "medium": {
                "codec": "libmp3lame",
                "ext": "mp3",
                "bitrate": "32k",
                "channels": "1",
                "sample_rate": "16000"
            },
            "high": {
                "codec": "libmp3lame",
                "ext": "mp3",
                "bitrate": "16k",
                "channels": "1",
                "sample_rate": "11025"
            },
            "extreme": {
                "codec": "libmp3lame",
                "ext": "mp3",
                "bitrate": "8k",
                "channels": "1",
                "sample_rate": "8000"
            }
        }

        config = compression_configs.get(compression_level, compression_configs["high"])
        compressed_path = os.path.join(output_dir, f"{filename}_compressed.{config['ext']}")

        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i", downloaded_path,
            "-c:a", config["codec"],
            "-b:a", config["bitrate"],
            "-ac", config["channels"],
            "-ar", config["sample_rate"],
            "-f", config["ext"],
            "-map_metadata", "-1",
            compressed_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            if not self.quiet:
                orig_size = os.path.getsize(downloaded_path)
                comp_size = os.path.getsize(compressed_path)
                print(f"Compresión completada. Original: {orig_size} bytes, Comprimido: {comp_size} bytes")
                reduction = (1 - comp_size / orig_size) * 100
                print(f"Reducción de tamaño: {reduction:.1f}%")

            # Reemplazar original por comprimido
            os.remove(downloaded_path)
            final_path = os.path.join(output_dir, f"{filename}.{config['ext']}")
            os.rename(compressed_path, final_path)
            return final_path

        except subprocess.CalledProcessError as e:
            print(f"Error en la compresión: {e}")
            print(f"Stderr: {e.stderr}")
            return downloaded_path

    def download_audio(
            self,
            video_url: str,
            output_dir: str,
            filename: str = "original_audio",
            compress: bool = False,
            compression_level: str = "high"
    ) -> str:
        """
        Método de compatibilidad que usa la nueva implementación con fallback.
        Mantiene la misma interfaz que el método original.
        """
        return self.download_audio_with_fallback(
            video_url=video_url,
            output_dir=output_dir,
            filename=filename,
            compress=compress,
            compression_level=compression_level
        )

    def get_file_size_mb(self, file_path: str) -> float:
        """
        Obtiene el tamaño del archivo en MB.

        Parámetros:
        -----------
        file_path : str
            Ruta al archivo.

        Retorna:
        --------
        float
            Tamaño del archivo en MB.
        """
        if os.path.exists(file_path):
            return os.path.getsize(file_path) / (1024 * 1024)
        return 0.0

    def update_ytdlp(self):
        """
        Actualiza yt-dlp a la versión más reciente.
        Ejecuta: pip install --upgrade yt-dlp
        """
        try:
            result = subprocess.run(
                ["pip", "install", "--upgrade", "yt-dlp"],
                capture_output=True,
                text=True,
                check=True
            )
            print("yt-dlp actualizado correctamente")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error actualizando yt-dlp: {e}")
            print(f"Stderr: {e.stderr}")
