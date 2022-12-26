from typing import List, Type

import numpy as np
from matplotlib.colors import Colormap, TwoSlopeNorm
from  matplotlib import pyplot as plt

from .beam import Beam
from .material import Material
from .method import Method, GaussSeidel_method
from .node import Node
from .solve import Solve
from .plot import Plot


class Truss(Solve, Plot):
    nodes: List[Node]
    beams: List[Beam]
    material: Material

    def __init__(self):
        Solve.__init__(self)
        Plot.__init__(self)

        self.nodes = []
        self.beams = []
        self.material = None

    def add_node(self, node: Node):
        last_id = Truss._get_last_id(self.nodes)

        if node not in self.nodes:
            node.id = last_id + 1

            self.nodes.append(node)

        return self

    def add_beam(self, beam: Beam):
        last_id = Truss._get_last_id(self.beams)

        if beam not in self.beams:
            beam.id = last_id + 1

            self.add_node(beam.node1).add_node(beam.node2)
            self.beams.append(beam)

        return self

    def add_truss(self, truss: Type["Truss"]):
        for beam in truss.beams:
            self.add_beam(beam)

        return self

    def make_node(self, x: float, y: float):
        node = Node(x, y)

        self.add_node(node)

        return node

    def make_beam(self, node1: Node, node2: Node):
        beam = Beam(node1, node2).set_material(self.material)

        self.add_beam(beam)

        return beam

    def set_material(self, material: Material):
        self.material = material

        for beam in self.beams:
            beam.set_material(self.material)

        return self

    def solve(self, charge: float = 1.0, method: Method = GaussSeidel_method, tolerance: float = 1e-5):
        Solve.execute(self, charge, method, tolerance)

    def plot(
        self,
        show_nodes: bool = True,
        show_labels: bool = True,
        color: str = None,
        values: np.ndarray = None,
        cmap: Type[Colormap] = plt.cm.rainbow,
        norm: Type[TwoSlopeNorm] = None,
        scale_label: str = None,
    ):
        Plot.execute(self, show_nodes, show_labels, color, values, cmap, norm, scale_label)

    @staticmethod
    def execute():
        pass

    @staticmethod
    def _get_last_id(collection):
        return collection[-1].id if len(collection) > 0 else -1
