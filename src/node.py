from typing import List

import numpy as np

from .displacement import Displacement
from .force import Force


class Node:
    id: int
    x: float
    y: float
    forces: List[Force]
    displacement: Displacement

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.forces = []
        self.displacement = Displacement()

    @property
    def resultant_force(self):
        r_x = 0
        r_y = 0

        for force in self.forces:
            r_x += force.x
            r_y += force.y

        return Force(r_x, r_y)

    def get_distance_from(self, node):
        return np.hypot(self.x - node.x, self.y - node.y)

    def get_angle_from(self, node):
        dx = self.x - node.x
        dy = self.y - node.y

        return np.arctan2(dy, dx) - np.pi

    def rotate_by(self, theta: float, origin):
        x = self.x - origin.x
        y = self.y - origin.y

        self.x = origin.x + x * np.cos(theta) - y * np.sin(theta)
        self.y = origin.y + x * np.sin(theta) + y * np.cos(theta)

        return self

    def add_force(self, force: Force):
        if force not in self.forces:
            self.forces.append(force)

        return self

    def apply_force(self, x: float, y: float):
        force = Force(x, y)

        self.add_force(force)

        return force
