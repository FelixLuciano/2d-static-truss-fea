class Material:
    elasticity: float
    area: float

    def __init__(self, youngs_modulus: float, area: float):
        self.elasticity = youngs_modulus
        self.area = area

    def set_elasticity(self, youngs_modulus: float):
        self.elasticity = youngs_modulus

    def set_area(self, area: float):
        self.area = area
