class Personagem:
    def __init__(self, x = 100):
        self.x = x
        self.frame = 0
        self.distancia_movimento = 3.5

    def idle (self):
        pass

    def walk_right (self):
        self.x += self.distancia_movimento

    def walk_left (self):
        self.x -= self.distancia_movimento