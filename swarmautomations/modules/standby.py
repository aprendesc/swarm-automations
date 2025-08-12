import time
import math
import pyautogui as pg

class StandbyClass:
    def __init__(self, interval=5, radius=50, steps=64):
        self.interval, self.radius, self.steps = interval, radius, steps

    def _circle(self, cx, cy, dur=3):
        for i in range(self.steps):
            a = 2*math.pi*i/self.steps
            pg.moveTo(cx + self.radius*math.cos(a), cy + self.radius*math.sin(a), dur/self.steps)

    def run(self):
        while True:
            x0, y0 = pg.position()
            time.sleep(self.interval)
            if (x0, y0) == pg.position():
                print('Standby detected...')
                self._circle(x0, y0)
