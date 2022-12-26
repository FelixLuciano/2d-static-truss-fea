from copy import deepcopy

import numpy as np

from .method import Method


class Solve:
    internal_deformation: np.ndarray
    internal_tension: np.ndarray
    internal_forces: np.ndarray

    def __init__(self):
        self.solution = self

    def execute(self, charge: float, method: Method, tolerance: float):
        self.solution = deepcopy(self)

        self._execute_rigidity()
        self._execute_mask()
        self._execute_forces(charge)
        self._execute_displacement(method, tolerance)
        self._execute_reactions()
        self._execute_internal_deformation()
        self._execute_internal_tension()
        self._execute_internal_force()

        return self

    def plot_deformation(self, *args, **kwargs):
        self.solution.plot(values=self.internal_deformation, *args, **kwargs)

    def plot_tension(self, *args, **kwargs):
        self.solution.plot(values=self.internal_tension, *args, **kwargs)

    def plot_force(self, *args, **kwargs):
        self.solution.plot(values=self.internal_forces, *args, **kwargs)

    def _execute_mask(self):
        self._mask = np.array(
            [node.displacement.vec for node in self.solution.nodes]
        ).flatten()
        self._mask_n = np.bitwise_not(self._mask)

    def _execute_rigidity(self):
        size = len(self.solution.nodes)
        K = np.zeros((size * 2, size * 2))

        for beam in self.solution.beams:
            Ke = beam.rigidity
            i1 = beam.node1.id * 2
            i2 = beam.node2.id * 2

            K[i1 : i1 + 2, i1 : i1 + 2] += Ke[0:2, 0:2]
            K[i1 : i1 + 2, i2 : i2 + 2] += Ke[0:2, 2:4]
            K[i2 : i2 + 2, i1 : i1 + 2] += Ke[2:4, 0:2]
            K[i2 : i2 + 2, i2 : i2 + 2] += Ke[2:4, 2:4]

        self._rigidity = K

    def _execute_forces(self, charge: float):
        F = []

        for node in self.solution.nodes:
            R = node.resultant_force

            F.append(R.x)
            F.append(R.y)

        self._forces = np.array(F) * charge

    def _execute_displacement(self, method: Method, tolerance: float):
        u = np.zeros(self._rigidity.shape[1])

        u[self._mask_n] = method.solve(
            k=self._rigidity[self._mask_n][:, self._mask_n],
            y=self._forces[self._mask_n],
            tolerance=tolerance,
        )

        for beam in self.solution.beams:
            i1 = beam.node1.id * 2
            i2 = beam.node2.id * 2

            beam.node1.x += u[i1]
            beam.node1.y += u[i1 + 1]
            beam.node2.x += u[i2]
            beam.node2.y += u[i2 + 1]

        self._displacement = u

    def _execute_reactions(self):
        self._forces[self._mask] = np.matmul(self._rigidity, self._displacement)[
            self._mask
        ]

    def _execute_internal_deformation(self):
        deformations = []

        for beam in self.solution.beams:
            i1 = beam.node1.id * 2
            i2 = beam.node2.id * 2
            u1 = self._displacement[i1 : i1 + 2]
            u2 = self._displacement[i2 : i2 + 2]
            deformation = beam.get_deformation(u1, u2)

            deformations.append(deformation)

        self.internal_deformation = np.array(deformations)

    def _execute_internal_tension(self):
        self.internal_tension = np.array(
            [
                deformation * beam.material.elasticity
                for deformation, beam in zip(
                    self.internal_deformation, self.solution.beams
                )
            ]
        )

    def _execute_internal_force(self):
        self.internal_forces = np.array(
            [
                tension * beam.material.area
                for tension, beam in zip(self.internal_tension, self.solution.beams)
            ]
        )
