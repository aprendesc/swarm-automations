import pyautogui as pg
import time

class StandbyClass:
    def __init__(self, interval=20):
        self.interval = interval  # tiempo entre simulaciones en segundos

    def simulate_activity(self):
        # Mover el mouse 1px a la derecha y volver
        x, y = pg.position()
        pg.moveTo(x + 1, y)
        pg.moveTo(x, y)

        # Presionar y soltar Shift
        pg.press('shift')

    def run(self):
        while True:
            self.simulate_activity()
            print("Actividad simulada para Teams y sistema.")
            time.sleep(self.interval)
