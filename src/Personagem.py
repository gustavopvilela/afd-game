class Personagem:
    def __init__(self, x = 100):
        self.x = x
        self.frame = 0
        self.distancia_movimento = 3.5

    def idle (self):
        pass # O personagem não se move

    def walk_right (self):
        self.x += self.distancia_movimento

    def walk_left (self):
        self.x -= self.distancia_movimento

    def hammer_right(self):
        pass # O personagem não se move

    def hammer_left (self):
        pass # O personagem não se move