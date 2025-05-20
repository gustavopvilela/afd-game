class Personagem:
    def __init__(self, x = 100, y = 355):
        self.x = x
        self.y = y
        self.frame = 0
        self.velocidade_andando = 4.5
        self.velocidade_pulando = 6.5

        # Dash:
        self.dash_ocorrendo = False
        self.dash_restante = 0
        self.distancia_dash_total = 1800
        self.distancia_dash_frame = 80
        self.direcao_dash = "right"

    def idle (self):
        pass # O personagem não se move

    def walk_right (self):
        self.x += self.velocidade_andando
        self.direcao_dash = "right"

    def walk_left (self):
        self.x -= self.velocidade_andando
        self.direcao_dash = "left"

    def crouch_right (self):
        self.direcao_dash = "right"
        pass

    def crouch_left (self):
        self.direcao_dash = "left"
        pass

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

    def start_dash (self, direcao):
        if not self.dash_ocorrendo:
            self.dash_ocorrendo = True
            self.dash_restante = self.distancia_dash_total
            self.direcao_dash = direcao

    def update_dash (self):
        if self.dash_ocorrendo:
            if self.dash_restante > 0:
                deslocamento = min(self.distancia_dash_frame, self.dash_restante)
                if self.direcao_dash == "right":
                    self.x += deslocamento
                else:
                    self.x -= deslocamento
                self.dash_restante -= deslocamento
            else:
                self.dash_ocorrendo = False
