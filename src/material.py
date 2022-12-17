import numpy as np


class Material:
    elasticity:float
    area:float

    def __init__(self, elasticity:float, area:float):
        self.elasticity = elasticity
        self.area = area
