from copy import deepcopy

import matplotlib.colors
import numpy as np
from matplotlib import pyplot as plt

from .method import GaussSeidel_method, Method
from .truss import Truss


class Solve:
    mask: np.ndarray
    mask_: np.ndarray
    rigidity: np.ndarray
    forces: np.ndarray
    displacement: np.ndarray
    internal_deformation: np.ndarray
    internal_tension: np.ndarray
    internal_forces: np.ndarray
    output: Truss

    def __init__(self, truss: Truss, method: Method = GaussSeidel_method):
        self.output = deepcopy(truss)
        self.method = method

    def execute(self, tol: float = 1e-5):
        self._execute_rigidity()
        self._execute_mask()
        self._execute_forces()
        self._execute_displacement(self.method, tol)
        self._execute_reactions()
        self._execute_internal_deformation()
        self._execute_internal_tension()
        self._execute_internal_force()

        return self

    def plot_deformation(self, label: str = None, cmap=plt.cm.rainbow, *args, **kwargs):
        self._plot(self.internal_deformation, label, cmap, *args, **kwargs)

    def plot_tension(self, label: str = None, cmap=plt.cm.rainbow, *args, **kwargs):
        self._plot(self.internal_tension, label, cmap, *args, **kwargs)

    def plot_force(self, label: str = None, cmap=plt.cm.rainbow, *args, **kwargs):
        self._plot(self.internal_forces, label, cmap, *args, **kwargs)

    def plot(self, *args, **kwargs):
        self.output.plot(*args, **kwargs)

    def _plot(self, attr: np.ndarray, label: str, cmap, *args, **kwargs):
        norm = matplotlib.colors.Normalize(vmin=attr.min(), vmax=attr.max())
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

        for beam in self.output.beams:
            value = attr[beam.id - 1]
            color = cmap(norm(value))

            beam.set_color(color)

        self.plot(*args, **kwargs)
        plt.colorbar(sm, label=label)

    def get_reactions(self):
        return self.forces[self.mask]

    def _execute_mask(self):
        self.mask = np.array(
            [node.displacement.get_axis() for node in self.output.nodes]
        ).flatten()
        self.mask_ = np.bitwise_not(self.mask)

    def _execute_rigidity(self):
        size = len(self.output.nodes)
        K = np.zeros((size * 2, size * 2))

        for beam in self.output.beams:
            Ke = beam.rigidity
            i1 = (beam.node1.id - 1) * 2
            i2 = (beam.node2.id - 1) * 2

            K[i1 : i1 + 2, i1 : i1 + 2] += Ke[0:2, 0:2]
            K[i1 : i1 + 2, i2 : i2 + 2] += Ke[0:2, 2:4]
            K[i2 : i2 + 2, i1 : i1 + 2] += Ke[2:4, 0:2]
            K[i2 : i2 + 2, i2 : i2 + 2] += Ke[2:4, 2:4]

        self.rigidity = K

    def _get_masked_rigidity(self, mask):
        return self.rigidity[mask][:, mask]

    def _execute_forces(self):
        F = []

        for node in self.output.nodes:
            r = node.get_resultant_force()

            F.append(r.x)
            F.append(r.y)

        self.forces = np.array(F)

    def _execute_displacement(self, method, tol: float):
        u = np.zeros(self.rigidity.shape[1])

        u[self.mask_] = method.solve(
            k=self._get_masked_rigidity(self.mask_), y=self.forces[self.mask_], tol=tol
        )

        for beam in self.output.beams:
            i1 = (beam.node1.id - 1) * 2
            i2 = (beam.node2.id - 1) * 2

            beam.node1.x += u[i1]
            beam.node1.y += u[i1 + 1]
            beam.node2.x += u[i2]
            beam.node2.y += u[i2 + 1]

        self.displacement = u

    def _execute_reactions(self):
        self.forces[self.mask] = np.matmul(self.rigidity, self.displacement)[self.mask]

    def _execute_internal_deformation(self):
        deformations = []

        for beam in self.output.beams:
            i1 = (beam.node1.id - 1) * 2
            i2 = (beam.node2.id - 1) * 2
            u1 = self.displacement[i1 : i1 + 2]
            u2 = self.displacement[i2 : i2 + 2]
            deformation = beam.get_deformation(u1, u2)

            deformations.append(deformation)

        self.internal_deformation = np.array(deformations)

    def _execute_internal_tension(self):
        tensions = []

        for deformation, beam in zip(self.internal_deformation, self.output.beams):
            tension = deformation * beam.material.elasticity

            tensions.append(tension)

        self.internal_tension = np.array(tensions)

    def _execute_internal_force(self):
        forces = []

        for tension, beam in zip(self.internal_tension, self.output.beams):
            force = tension * beam.material.area

            forces.append(force)

        self.internal_forces = np.array(forces)
