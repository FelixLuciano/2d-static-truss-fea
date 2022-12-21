from typing import List

import numpy as np

from .beam import Beam
from .material import Material
from .node import Node


class Truss:
    nodes: List[Node]
    beams: List[Beam]
    material: Material

    def __init__(self):
        self.nodes = []
        self.beams = []
        self.material = None

    def add_node(self, node: Node):
        last_id = self.nodes[-1].id if len(self.nodes) > 0 else 0

        if node not in self.nodes:
            node.id = last_id + 1

            self.nodes.append(node)

        return self

    def add_beam(self, beam: Beam):
        last_id = self.beams[-1].id if len(self.beams) > 0 else 0

        if beam not in self.beams:
            beam.id = last_id + 1

            self.add_node(beam.node1).add_node(beam.node2)
            self.beams.append(beam)

        return self

    def add_truss(self, truss):
        for node in truss.nodes:
            self.add_node(node)

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

    def plot(self, show_nodes=True, show_labels=True, labels:List[str|int|float]=None, zorder=1, *args, **kwargs):
        for i, beam in enumerate(self.beams):
            label = None if not show_labels else labels[i] if labels is not None else beam.length

            beam.plot(label=label, zorder=zorder, *args, **kwargs)

        for node in self.nodes:
            node.plot(show_nodes=show_nodes, zorder=zorder + 1)
