class Personagem:
    def __init__(self, x = 100, y = 400):
        self.x = x
        self.y = y
        self.frame = 0
        self.velocidade_andando = 4.5
        self.velocidade_pulando = 6.5

    def idle (self):
        pass # O personagem não se move

    def walk_right (self):
        self.x += self.velocidade_andando

    def walk_left (self):
        self.x -= self.velocidade_andando

    def hammer_right(self):
        pass # O personagem não se move

    def hammer_left (self):
        pass # O personagem não se move

    def stay_in_bounds(self, screen_width, screen_height, sprite_width, sprite_height):
        if self.x < 0:
            self.x = 0
        elif self.x + sprite_width > screen_width:
            self.x = screen_width - sprite_width

        if self.y < 0:
            self.y = 0
        elif self.y + sprite_height > screen_height:
            self.y = screen_height - sprite_height