import numpy as np
from matplotlib import pyplot as plt

from .node import Node
from .material import Material


class Beam:
    id:int = None
    material:Material

    def __init__(self, node1: Node, node2: Node):
        self.node1 = node1
        self.node2 = node2

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
        rigidity = self.material.elasticity * self.material.area / self.length
        s, c = self.sin_cos
        a = np.array([ [c, s, 0, 0],
                       [0, 0, c, s], ])
        b = np.array([ [1.0, -1.0],
                       [-1.0, 1.0], ])

        return np.matmul(np.matmul(a.T * rigidity,  b), a)

    def get_deformation(self, u1, u2):
        s, c = self.sin_cos
        vec = [-c, -s, c, s]
        pos = [u1[0], u1[1], u2[0], u2[1]]

        return np.dot(vec / self.length, pos)

    def set_material(self, material:Material):
        self.material = material

        return self

    def plot(self, show_lengths:bool, *args, **kwargs):
        mx = (self.node1.x + self.node2.x) / 2
        my = (self.node1.y + self.node2.y) / 2
        alpha = np.degrees(self.angle)

        if alpha < -90 and alpha > -270:
            alpha += 180

        plt.plot(
            [self.node1.x, self.node2.x], [self.node1.y, self.node2.y], *args, **kwargs
        )

        if show_lengths:
            plt.text(
                mx,
                my,
                f"{self.length:.2f}",
                horizontalalignment="center",
                verticalalignment="center",
                rotation=alpha,
            )
