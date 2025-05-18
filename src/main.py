from AFD import *
from Personagem import *
from Sprite import *
import pygame

def renderizar (tela, sprites, personagem, x = None, y = 400):
    if x is None: x = personagem.x

    tela.fill((30, 30, 30))
    tela.blit(sprites[personagem.frame], (x, y))
    pygame.display.flip()

def main():
    # Definindo as constantes
    FRAME_RATE = 60

    # Definindo os estados do personagem
    IDLE_RIGHT = "IDLE_RIGHT"
    IDLE_LEFT = "IDLE_LEFT"
    WALK_RIGHT = "WALK_RIGHT"
    WALK_LEFT = "WALK_LEFT"
    HAMMER_RIGHT = "HAMMER_RIGHT"
    HAMMER_LEFT = "HAMMER_LEFT"
    DASH_RIGHT = "DASH_RIGHT"
    DASH_LEFT = "DASH_LEFT"
    CROUCH_RIGHT = "CROUCH_RIGHT"
    CROUCH_LEFT = "CROUCH_LEFT"

    # Definindo as teclas aceitas pelo programa
    alfabeto_teclas = {
        'a': pygame.K_a,
        'd': pygame.K_d,
        'z': pygame.K_z,
        'f' : pygame.K_f,
        's': pygame.K_s,
        None: None
    }

    # Definindo as transições dos estados do personagem
    transicoes = {
        (IDLE_RIGHT, 'd'): WALK_RIGHT,
        (IDLE_RIGHT, 'a'): WALK_LEFT,
        (IDLE_RIGHT, None): IDLE_RIGHT,
        (IDLE_RIGHT, 'z'): HAMMER_RIGHT,
        (IDLE_RIGHT, 'f'): DASH_RIGHT,
        (IDLE_RIGHT, 's'): CROUCH_RIGHT,

        (IDLE_LEFT, 'd'): WALK_RIGHT,
        (IDLE_LEFT, 'a'): WALK_LEFT,
        (IDLE_LEFT, None): IDLE_LEFT,
        (IDLE_LEFT, 'z'): HAMMER_LEFT,
        (IDLE_LEFT, 'f'): DASH_LEFT,
        (IDLE_LEFT, 's'): CROUCH_LEFT,

        (WALK_RIGHT, 'd'): WALK_RIGHT,
        (WALK_RIGHT, 'a'): WALK_LEFT,
        (WALK_RIGHT, None): IDLE_RIGHT,
        (WALK_RIGHT, 'z'): HAMMER_RIGHT,
        (WALK_RIGHT, 'f'): DASH_RIGHT,
        (WALK_RIGHT, 's'): CROUCH_RIGHT,

        (WALK_LEFT, 'd'): WALK_RIGHT,
        (WALK_LEFT, 'a'): WALK_LEFT,
        (WALK_LEFT, None): IDLE_LEFT,
        (WALK_LEFT, 'z'): HAMMER_LEFT,
        (WALK_LEFT, 'f'): DASH_LEFT,
        (WALK_LEFT, 's'): CROUCH_LEFT,

        (HAMMER_LEFT, None): IDLE_LEFT,
        (HAMMER_RIGHT, None): IDLE_RIGHT,

        (DASH_LEFT, None): IDLE_LEFT,
        (DASH_RIGHT, None): IDLE_RIGHT,

        (CROUCH_RIGHT, None): IDLE_RIGHT,
        (CROUCH_LEFT, None): IDLE_LEFT,
    }

    # Criando o AFD para controlar o personagem
    afd = AFD(
        estados={estado for (estado, _) in transicoes.keys()},
        alfabeto={simbolo for simbolo in alfabeto_teclas.keys()},
        transicoes=transicoes,
        estado_inicial=IDLE_RIGHT,
        estados_finais=None
    )

    # Inicialização do PyGame
    pygame.init()
    info = pygame.display.Info()
    w, h = 960, 540
    tela = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Jogo com AFD")
    clock = pygame.time.Clock()

    # Controle dos frames do personagem
    ultimo_tick = pygame.time.get_ticks()
    DELAY = 95  # Demora 95ms para transicionar de um frame para o outro

    # Criando o personagem
    personagem = Personagem(x = w // 2)

    # Importando os sprites
    sprites_idle_right = Sprite.carregar_sprites("..\\sprites\\idle\\right")
    sprites_idle_left  = Sprite.carregar_sprites("..\\sprites\\idle\\left")
    sprites_walk_right = Sprite.carregar_sprites("..\\sprites\\walk\\right")
    sprites_walk_left  = Sprite.carregar_sprites("..\\sprites\\walk\\left")
    sprites_hammer_right = Sprite.carregar_sprites("..\\sprites\\hammer\\right")
    sprites_hammer_left= Sprite.carregar_sprites("..\\sprites\\hammer\\left")
    sprites_dash_right = Sprite.carregar_sprites("..\\sprites\\dash\\right")
    sprites_dash_left = Sprite.carregar_sprites("..\\sprites\\dash\\left")
    sprites_crouch_right = Sprite.carregar_sprites("..\\sprites\\crouch\\right")
    sprites_crouch_left = Sprite.carregar_sprites("..\\sprites\\crouch\\left")

    # Definindo as ações realizadas pelo personagem
    acoes = {
        IDLE_RIGHT:     (personagem.idle, sprites_idle_right),
        IDLE_LEFT:      (personagem.idle, sprites_idle_left),
        WALK_RIGHT:     (personagem.walk_right, sprites_walk_right),
        WALK_LEFT:      (personagem.walk_left, sprites_walk_left),
        HAMMER_RIGHT:   (personagem.hammer_right, sprites_hammer_right),
        HAMMER_LEFT:    (personagem.hammer_left, sprites_hammer_left),
        DASH_RIGHT:     (personagem.idle, sprites_dash_right),
        DASH_LEFT:      (personagem.idle, sprites_dash_left),
        CROUCH_RIGHT:   (personagem.crouch_right, sprites_crouch_right),
        CROUCH_LEFT:    (personagem.crouch_left, sprites_crouch_left)
    }

    # Flag para controlar execução completa do hammer e do dash
    hammering = False
    dashing = False
    crouching = False
    estado_atual = afd.estado_inicial
    direcao = "right" if "RIGHT" in estado_atual else "left"

    em_execucao = True
    while em_execucao:

        agora = pygame.time.get_ticks()

        # Devemos tratar os eventos que interrompam o loop de execução, como animações em que o personagem precisa
        # ficar parado, por exemplo, em ataques.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                em_execucao = False

            # Apertando a tecla Z e olhando para a esquerda, o personagem entra em modo de ataque com o martelo para
            # a esquerda.
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_z and "LEFT" in estado_atual:
                if not hammering:
                    hammering = True
                    personagem.frame = 0
                    estado_atual = HAMMER_LEFT

            # Apertando a tecla Z e olhando para a direita, o personagem entra em modo de ataque com o martelo para
            # a direita.
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_z and "RIGHT" in estado_atual:
                if not hammering:
                    hammering = True
                    personagem.frame = 0
                    estado_atual = HAMMER_RIGHT

            # Apertando a tecla F, o personagem entra em modo dash.
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_f:
                if not dashing:
                    dashing = True
                    personagem.frame = 0

                    personagem.start_dash(direcao)
                    estado_atual = DASH_RIGHT if direcao == "right" else DASH_LEFT

            # Apertando a tecla S, o personagem agacha, se apertar S novamente, ele se levanta.
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_s:
                crouching = not crouching
                personagem.frame = 0
                if crouching:
                    crouching = True
                    estado_atual = CROUCH_RIGHT if direcao == "right" else CROUCH_LEFT
                else:
                    estado_atual = IDLE_RIGHT if estado_atual == CROUCH_RIGHT else IDLE_LEFT

        # Nesta parte do código, colocaremos as animações que devem ser feitas separadamente (ataques e supers).
        # Ataque 1: Ataque de martelo
        if hammering:
            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame += 1

                # Se passou do último frame, encerra o ataque e volta a ficar parado (idle)
                if personagem.frame >= len(sprites_hammer_left):
                    hammering = False
                    personagem.frame = 0
                    estado_atual = IDLE_LEFT

            # Mostrando na tela o ataque
            acao, sprites = acoes[estado_atual]
            acao()
            renderizar(tela, sprites, personagem)
            clock.tick(FRAME_RATE)
            continue  # Pula a execução das teclas normais (andar, pular, agachar, etc.)

        # Dash: o personagem avança em um dash.
        if dashing:
            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame += 1
                personagem.update_dash()

                limite = len(sprites_dash_left) if estado_atual == DASH_LEFT else len(sprites_dash_right)
                if personagem.frame >= limite:
                    dashing = False
                    personagem.frame = 0

                    direcao = "left" if estado_atual == DASH_LEFT else "right"
                    estado_atual = IDLE_LEFT if direcao == "left" else IDLE_RIGHT

            # Mostrando na tela o ataque
            acao, sprites = acoes[estado_atual]
            acao()
            renderizar(tela, sprites, personagem)
            clock.tick(FRAME_RATE)
            continue

        # Crouch: personagem agacha e se levanta.
        if crouching:
            acao, sprites = acoes[estado_atual]
            acao()
            # Deixa iterando apenas sob os 4 frames finais para ficar agachado
            sprites = sprites[-4:]
            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame = (personagem.frame + 1) % len(sprites)
            renderizar(tela, sprites, personagem)
            clock.tick(FRAME_RATE)
            continue

        # Transições normais (sem ataques e supers)
        teclas = pygame.key.get_pressed()
        if teclas[alfabeto_teclas['d']]:
            simbolo = 'd'
            direcao = "right"
        elif teclas[alfabeto_teclas['a']]:
            simbolo = 'a'
            direcao = "left"
        else:
            simbolo = None

        # Executando a ação
        estado_atual = afd.processar(simbolo)
        acao, sprites = acoes[estado_atual]
        acao()

        # Atualização de frame normal
        if agora - ultimo_tick > DELAY:
            ultimo_tick = agora
            personagem.frame = (personagem.frame + 1) % len(sprites)

        # Renderização final
        renderizar(tela, sprites, personagem)
        clock.tick(FRAME_RATE)

    pygame.quit()

if __name__ == '__main__':
    main()
