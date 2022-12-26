import numpy as np


class Force:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def norm(self):
        return np.hypot(self.x, self.y)

    @property
    def angle(self):
        return np.degrees(np.arctan2(self.y, self.x))
