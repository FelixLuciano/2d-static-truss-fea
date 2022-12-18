from typing import List

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt

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

    def apply_force(self, x: float, y: float):
        force = Force(x, y)

        self.add_force(force)

        return force

    def get_resultant_force(self):
        Rx = 0
        Ry = 0

        for force in self.forces:
            Rx += force.x
            Ry += force.y

        return Force(Rx, Ry)

    def plot(self, show_nodes: bool, zorder: int, *args, **kwargs):
        dx, dy = self.displacement.get_axis()

        if dx and dy:
            marker = "X"
        elif dx:
            marker = ">"
        elif dy:
            marker = "^"
        elif show_nodes:
            marker = "o"
        else:
            marker = "none"

        plt.scatter(
            [self.x], [self.y], c="#27B", marker=marker, zorder=zorder, *args, **kwargs
        )

        if show_nodes and len(self.forces) > 0:
            resultant = self.get_resultant_force()
            theta = np.degrees(np.arctan2(resultant.y, resultant.x))

            t = mpl.markers.MarkerStyle(marker=5)
            t._transform = t.get_transform().rotate_deg(theta)

            plt.scatter(
                [self.x], [self.y], c="#B22", marker=t, s=100, zorder=zorder + 1
            )
