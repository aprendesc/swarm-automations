
import psutil
import time
from dotenv import load_dotenv
from swarmautomations.modules.session_recorder import SessionRecorder

load_dotenv()

# Tu configuración existente
raw_page_id = '27c2a599-e985-802d-9432-f6a6fbab7105'
page_id = '2742a599-e985-8023-a111-d9972ae4f61a'

class TeamsMonitor:
    def __init__(self):
        self.sm = None
        self.recording = False

    def count_teams_windows(self):
        """Cuenta las ventanas de Microsoft Teams abiertas"""
        teams_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'teams' in proc.info['name'].lower() or 'ms-teams' in proc.info['name'].lower():
                    teams_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return teams_count

    def start_recording(self):
        """Inicia la grabación"""
        if not self.recording:
            self.sm = SessionRecorder(raw_page_id=raw_page_id, page_id=page_id)
            self.sm.start(chunk_seconds=20, summarize=True)
            self.recording = True
            print("🔴 Grabación iniciada - Detectadas múltiples ventanas de Teams")

    def stop_recording(self):
        """Detiene la grabación"""
        if self.recording and self.sm:
            self.sm.stop()
            self.recording = False
            print("⏹️ Grabación detenida - Solo queda una ventana de Teams")

    def monitor(self):
        """Monitorea continuamente las ventanas de Teams"""
        print("🔍 Monitoreando ventanas de Microsoft Teams...")

        while True:
            teams_windows = self.count_teams_windows()
            print(f"Ventanas de Teams detectadas: {teams_windows}")

            # Trigger START: Más de 2 ventanas
            if teams_windows > 2 and not self.recording:
                self.start_recording()

            # Trigger STOP: Solo 1 ventana (o ninguna)
            elif teams_windows <= 1 and self.recording:
                self.stop_recording()

            time.sleep(5)  # Revisa cada 5 segundos

if __name__ == "__main__":
    monitor = TeamsMonitor()
    try:
        monitor.monitor()
    except KeyboardInterrupt:
        print("\n🛑 Monitoreo detenido")
        if monitor.recording:
            monitor.stop_recording()
