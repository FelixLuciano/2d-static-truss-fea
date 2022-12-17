from matplotlib import pyplot as plt
from matplotlib import patches

from truss_fea import Truss, Material


plt.style.use('seaborn-v0_8')


if __name__ == "__main__":
    bar = Truss()
    material = Material(200_000_000, 0.02)
    node1 = bar.make_node(0, 0)
    node2 = bar.make_node(1, 0)
    node3 = bar.make_node(2, 0)
    beam1 = bar.make_beam(node1, node2)
    beam2 = bar.make_beam(node2, node3)

    node1.displacement.set_x().set_y()
    node3.apply_force(50_000, 0)

    plt.figure(figsize=(5, 5))

    ax = plt.axes()
    ax.add_patch(patches.Rectangle((-1, -1), 1, 2, color="#BBB"))

    plt.title("Bar example")
    plt.xlabel("Length [m]")
    plt.ylabel("Height [m]")
    bar.plot()
    plt.savefig('examples/bar.png', bbox_inches="tight")
