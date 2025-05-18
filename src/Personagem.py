class Personagem:
    def __init__(self, x = 100):
        self.x = x
        self.frame = 0
        self.distancia_movimento = 3.5

        # Dash:
        self.dash_ocorrendo = False
        self.dash_restante = 0
        self.distancia_dash_total = 1800
        self.distancia_dash_frame = 80
        self.direcao_dash = "right"

    def idle (self):
        pass # O personagem não se move

    def walk_right (self):
        self.direcao_dash = "right"
        self.x += self.distancia_movimento

    def walk_left (self):
        self.direcao_dash = "left"
        self.x -= self.distancia_movimento

    def crouch_right (self):
        pass

    def crouch_left (self):
        pass

    def hammer_right(self):
        pass # O personagem não se move

    def hammer_left (self):
        pass # O personagem não se move

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
