class Displacement:
    x:bool
    y:bool

    def __init__(self):
        self.x = False
        self.y = False
    
    def set_x(self):
        self.x = True

        return self
    
    def clear_x(self):
        self.x = False

        return self
    
    def set_y(self):
        self.y = True

        return self
    
    def clear_y(self):
        self.y = False

        return self

    def get_axis(self):
        return self.x, self.y
