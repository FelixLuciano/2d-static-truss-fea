from setuptools import setup


def parse_requirements(filename):
    return [
        line.strip() for line in open(filename) if line and not line.startswith("#")
    ]


if __name__ == "__main__":
    setup(
        name="truss_fea",
        version="1.0.0",
        description="2D Static Truss Finite Element Analysis",
        url="https://github.com/FelixLuciano/2d-static-truss-fea",
        author="Luciano Felix",
        packages=["truss_fea"],
        package_dir={"truss_fea": "src"},
        license="MIT",
        install_requires=parse_requirements("requirements.txt"),
    )
