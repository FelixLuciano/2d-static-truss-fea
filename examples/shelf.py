from matplotlib import pyplot as plt
from matplotlib import patches

from truss_fea import Truss, Material, Solve


plt.style.use('seaborn-v0_8')


if __name__ == "__main__":
    MASS = 50   # in Kg
    G = 9.81    # gravitational acceleration

    wood = Material(95_000_000, 0.02)
    steel = Material(200_000_000, 0.01)
    rope = Material(9_000_000, 0.001)

    shelf = Truss()
    node1 = shelf.make_node(0, 0)
    node2 = shelf.make_node(1, 0)
    node3 = shelf.make_node(0, -1)
    node4 = shelf.make_node(0, 2)

    beam1 = shelf.make_beam(node1, node2).set_material(wood)
    beam3 = shelf.make_beam(node2, node3).set_material(steel)
    beam4 = shelf.make_beam(node2, node4).set_material(rope)

    node1.displacement.set_x().set_y()
    node2.apply_force(0, -(MASS * G))
    node3.displacement.set_x().set_y()
    node4.displacement.set_x().set_y()

    solution = Solve(shelf).execute()

    plt.figure(figsize=(5, 5))

    ax = plt.axes()
    ax.add_patch(patches.Rectangle((.5, 0), .5, 1, color="#CCC"))
    ax.add_patch(patches.Rectangle((-.5, -1.5), .5, 4, color="#CCC"))

    plt.title("Shelf example")
    plt.xlabel("Length [m]")
    plt.ylabel("Height [m]")
    shelf.plot(color="#BBB", show_lengths=False, show_nodes=False)
    solution.plot_force(label="Internal force [N]", show_lengths=False)
    plt.savefig('examples/shelf.png', bbox_inches="tight")