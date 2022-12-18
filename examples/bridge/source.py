from copy import deepcopy
from typing import List

import numpy as np
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from truss_fea import Beam, Material, Node, Solve, Truss


plt.style.use("seaborn-v0_8")


class Bridge(Truss):
    arc: List[Beam]
    deck: List[Beam]
    pillars: List[Beam]
    trelices: List[Beam]
    base: List[Beam]

    def __init__(self, deck1: Node, deck2: Node, base1: Node, base2: Node, steps: int):
        super().__init__()

        self.arc = []
        self.deck = []
        self.pillars = []
        self.trelices = []
        self.base = []

        self._make_arc(deck1, deck2, steps)
        self._make_deck()
        self._make_pillars()
        self._make_trelices()
        self._make_base(base1, base2)

    def _make_arc(self, node1: Node, node2: Node, steps: int):
        def cicloid(theta: float, length: float):
            r = length / (2 * np.pi)
            x = r * (theta - np.sin(theta))
            y = r * (1 - np.cos(theta))

            return x, y

        length = node1.get_distance_from(node2)
        alpha = node1.get_angle_from(node2)

        node0 = node1
        for theta in np.linspace(0, 2 * np.pi, steps)[1:-1]:
            x, y = cicloid(theta, length)
            node = self.make_node(x + node1.x, y + node1.y).rotate_by(alpha, node1)
            beam = self.make_beam(node0, node)
            node0 = node

            self.arc.append(beam)

        beam = self.make_beam(node0, node2)

        self.arc.append(beam)

    def _make_deck(self):
        origin = self.arc[0].node1
        end = self.arc[-1].node2
        alpha = origin.get_angle_from(end)

        node0 = origin
        for beam in self.arc[:-1]:
            beam.node1.rotate_by(-alpha, origin)

            node = self.make_node(beam.node2.x, origin.y)
            beam = self.make_beam(node0, node)

            self.deck.append(beam)
            beam.node1.rotate_by(alpha, origin)
            node.rotate_by(alpha, origin)

            node0 = node

        beam = self.make_beam(node0, end)

        self.deck.append(beam)

    def _make_pillars(self):
        for beam1, beam2 in zip(self.arc, self.deck):
            node1 = beam1.node1
            node2 = beam2.node1

            if node1 != node2:
                pillar = self.make_beam(node1, node2)

                self.pillars.append(pillar)

    def _make_trelices(self):
        for beam1, beam2 in zip(self.pillars[1:], self.pillars[:-1]):
            trelice1 = self.make_beam(beam1.node1, beam2.node2)
            trelice2 = self.make_beam(beam1.node2, beam2.node1)

            self.trelices.append(trelice1)
            self.trelices.append(trelice2)

    def _make_base(self, node1: Node, node2: Node):
        meam = len(self.deck) // 2

        for deck_beam in self.deck[1 : meam + 1]:
            beam = self.make_beam(node1, deck_beam.node1)

            self.base.append(beam)

        for deck_beam in self.deck[meam:-1]:
            beam = self.make_beam(node2, deck_beam.node2)

            self.base.append(beam)


def make_bridge():
    LOAD = 120 # kg
    G = 9.81 # m/s²
    MDF_YOUNG_MODULUS = 21_000_000

    node1 = Node(0, 0)
    node2 = Node(400, 0)
    node3 = Node(0, -60)
    node4 = Node(400, -60)
    node5 = Node(-60, 0)
    node6 = Node(460, 0)

    MDF = Material(MDF_YOUNG_MODULUS * 1E-3**2 / 1E-3, 3*15)
    bridge = Bridge(node1, node2, node3, node4, steps=8).set_material(MDF)

    bridge.make_beam(node5, bridge.arc[0].node2)
    bridge.make_beam(node6, bridge.arc[-1].node1)

    node1.displacement.set_x().set_y()
    node2.displacement.set_x().set_y()
    node3.displacement.set_x().set_y()
    node4.displacement.set_x().set_y()
    node5.displacement.set_x().set_y()
    node6.displacement.set_x().set_y()

    bridge.arc[3].node1.apply_force(0, LOAD * -G / 2)
    bridge.arc[3].node2.apply_force(0, LOAD * -G / 2)

    return bridge


def plot(bridge, solution):
    ax = plt.axes()
    ax.add_patch(patches.Rectangle((-70, -70), 70, 70, color="#BBB"))
    ax.add_patch(patches.Rectangle((400, -70), 70, 70, color="#BBB"))

    plt.title("Bridge example")
    plt.xlabel("Length [mm]")
    plt.ylabel("Height [mm]")

    bridge.plot(color="#BBB", show_lengths=False, show_nodes=False)
    solution.plot_force(label="Internal force [N]", show_lengths=False, show_nodes=True)
    plt.tight_layout()


if __name__ == "__main__":
    bridge = make_bridge()
    solution = Solve(bridge)
    fig = plt.figure(figsize=(14, 5))

    frames = []

    def animate(i):
        fig.clear()

        if i < 30:
            solution.execute()
            plot(bridge, solution)

            frames.append(deepcopy(solution))
        else:
            plot(bridge, frames[30 - i - 1])


    ani = FuncAnimation(fig, animate, frames=60)

    ani.save("examples/bridge/output.gif", fps=30)
