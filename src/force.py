import numpy as np


class Force:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def norm(self):
        return np.hypot(self.x, self.y)
