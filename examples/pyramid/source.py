from matplotlib import pyplot as plt
from truss_fea import Truss, Material, Solve


plt.style.use("seaborn-v0_8")


if __name__ == "__main__":
    with open("examples/pyramid/entry.txt", "r") as entry:
        pyramid = Truss()

        mode = 1
        for line in entry.readlines():
            arg = line.strip("\n").split(" ")

            if arg[0] == "":
                mode +=1
                continue

            if mode == 1:
                x, y, displace_x, displace_y, force_x, force_y = map(float, arg)
                node = pyramid.make_node(x, y)

                if bool(displace_x) == 0:
                    node.displacement.set_x()
                if bool(displace_y) == 0:
                    node.displacement.set_y()

                if force_x != 0.0 and force_y != 0.0:
                    node.apply_force(force_x, force_y)

            elif mode == 2:
                node1_id, node2_id, area, young_modulus = arg
                node1 = pyramid.nodes[int(node1_id) - 1]
                node2 = pyramid.nodes[int(node2_id) - 1]
                beam = pyramid.make_beam(node1, node2)
                material = Material(float(young_modulus), float(area))

                beam.set_material(material)

            elif mode == 3:
                pass

        solution = Solve(pyramid).execute()
    
        plt.figure(figsize=(10, 2))
        plt.title("Pyramid example")
        plt.xlabel("Length [mm]")
        plt.ylabel("Height [mm]")
        plt.axis("equal")
        solution.plot_force(label="Internal force [N]")
        plt.savefig("examples/pyramid/output.png", bbox_inches="tight")
