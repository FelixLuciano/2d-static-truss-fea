from typing import List, Tuple, Type

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Colormap, TwoSlopeNorm

from .beam import Beam
from .force import Force
from .node import Node


class Plot():
    def execute(
        self,
        show_nodes: bool,
        show_labels: bool,
        color: str,
        values: np.ndarray,
        cmap: Type[Colormap],
        norm: Type[TwoSlopeNorm],
        scale_label: str,
    ):
        if values is not None:
            self._execute_color_scale(values, cmap, norm, scale_label)

        for beam in self.beams:
            label = (
                None
                if not show_labels
                else values[beam.id]
                if values is not None
                else beam.length
            )

            Plot._execute_beam(beam, color, label)

        if show_nodes:
            for node in self.nodes:
                Plot._execute_node(node, zorder=2)

    def _execute_color_scale(
        self,
        values: np.ndarray,
        cmap: Type[Colormap],
        norm: Type[TwoSlopeNorm],
        label: str,
    ):
        if norm is None:
            norm = TwoSlopeNorm(
                vmin=values.min(),
                vcenter=0.0,
                vmax=values.max(),
            )

        for beam in self.beams:
            value = values[beam.id]
            color = cmap(norm(value))

            beam.set_color(color)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

        plt.colorbar(sm, label=label)

    @staticmethod
    def _execute_beam(beam: Beam, color: str, label: str):

        plt.plot(
            [beam.node1.x, beam.node2.x],
            [beam.node1.y, beam.node2.y],
            c=color or beam.color,
        )

        if label != None:
            Plot._execute_beam_label(beam, label)

    @staticmethod
    def _execute_beam_label(beam: Beam, label: str):
        cx, cy = beam.center
        alpha = np.degrees(beam.angle)

        if alpha < -90 and alpha > -270:
            alpha += 180

        plt.text(
            cx,
            cy,
            f"{label:.2f}",
            horizontalalignment="center",
            verticalalignment="center",
            rotation=alpha,
        )

    @staticmethod
    def _execute_node(node: Node, zorder: int):
        dx, dy = node.displacement.vec
        marker = "X" if dx and dy else ">" if dx else "^" if dy else "o"

        plt.scatter([node.x], [node.y], c="#27B", marker=marker, zorder=zorder)

        if len(node.forces) > 0:
            Plot._execute_node_force((node.x, node.y), node.resultant_force, zorder + 1)

    @staticmethod
    def _execute_node_force(origin: Tuple[float, float], force: Force, zorder: int):
        arrow = mpl.markers.MarkerStyle(marker=5)
        arrow._transform = arrow.get_transform().rotate_deg(force.angle)

        plt.scatter(
            [origin[0]], [origin[1]], c="#B22", marker=arrow, s=100, zorder=zorder
        )
