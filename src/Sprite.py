import os
import pygame

class Sprite:
    """
        Carrega os sprites numa pasta. Esses sprites são colocados em
        uma lista para que se possa fazer um loop entre eles, gerando uma
        animação.
    """
    @staticmethod
    def carregar_sprites (pasta):
        sprites = []
        for arquivo in os.listdir(pasta):
            # Carrega a imagem e deixa o fundo transparente, se for possível
            imagem = pygame.image.load(os.path.join(pasta, arquivo)).convert_alpha()
            sprites.append(imagem)

        return sprites