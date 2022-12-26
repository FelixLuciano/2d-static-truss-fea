import numpy as np

from .material import Material
from .node import Node


class Beam:
    id: int = None
    node1: Node
    node2: Node
    material: Material
    color: str

    def __init__(self, node1: Node, node2: Node, color: str = "#BBB"):
        self.node1 = node1
        self.node2 = node2
        self.color = color

    @property
    def center(self):
        cx = (self.node1.x + self.node2.x) / 2
        cy = (self.node1.y + self.node2.y) / 2

        return cx, cy

    @property
    def length(self):
        return self.node1.get_distance_from(self.node2)

    @property
    def angle(self):
        return self.node1.get_angle_from(self.node2)

    @property
    def sin_cos(self):
        dx = self.node2.x - self.node1.x
        dy = self.node2.y - self.node1.y
        l = np.sqrt(dx**2 + dy**2)

        return dy / l, dx / l

    @property
    def rigidity(self):
        longitudinal_rigidity = (
            self.material.elasticity * self.material.area / self.length
        )
        sin, cos = self.sin_cos
        axis = np.array(
            [
                [cos, sin, 0.0, 0.0],
                [0.0, 0.0, cos, sin],
            ]
        )
        signal = np.array(
            [
                [1.0, -1.0],
                [-1.0, 1.0],
            ]
        )

        return np.matmul(np.matmul(axis.T * longitudinal_rigidity, signal), axis)

    def set_material(self, material: Material):
        self.material = material

        return self

    def set_color(self, color: str):
        self.color = color

        return self

    def get_deformation(self, u1, u2):
        sin, cos = self.sin_cos
        vec = [-cos, -sin, cos, sin]
        pos = [u1[0], u1[1], u2[0], u2[1]]

        return np.dot(vec / self.length, pos)
