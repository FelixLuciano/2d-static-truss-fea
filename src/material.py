class Material:
    elasticity:float
    area:float

    def __init__(self, elasticity:float, area:float):
        self.elasticity = elasticity
        self.area = area

    def set_elasticity(self, elasticity:float):
        self.elasticity = elasticity

    def set_area(self, area:float):
        self.area = area
