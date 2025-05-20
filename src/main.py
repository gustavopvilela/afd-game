from AFD import *
from Personagem import *
from Sprite import *
import pygame

def renderizar (tela, sprites, personagem, x = None, y = None):
    if x is None: x = personagem.x
    if y is None: y = personagem.y

    # Alinhar as bases dos sprites do personagem à altura em que ele está
    img = sprites[personagem.frame]
    rect = img.get_rect()
    rect.x = x
    rect.bottom = y
    tela.blit(img, rect)

    pygame.display.flip()

def main():
    # Definindo as constantes
    FRAME_RATE = 70

    # Definindo os estados do personagem
    IDLE_RIGHT = "IDLE_RIGHT"
    IDLE_LEFT = "IDLE_LEFT"
    WALK_RIGHT = "WALK_RIGHT"
    WALK_LEFT = "WALK_LEFT"
    HAMMER_RIGHT = "HAMMER_RIGHT"
    HAMMER_LEFT = "HAMMER_LEFT"
    JUMP = "JUMP"

    # Definindo as teclas aceitas pelo programa
    alfabeto_teclas = {
        'a': pygame.K_a,
        'd': pygame.K_d,
        'z': pygame.K_z,
        'w': pygame.K_w,
        None: None
    }

    # Definindo as transições dos estados do personagem
    transicoes = {
        (IDLE_RIGHT, 'd'): WALK_RIGHT,
        (IDLE_RIGHT, 'a'): WALK_LEFT,
        (IDLE_RIGHT, None): IDLE_RIGHT,
        (IDLE_RIGHT, 'z'): HAMMER_RIGHT,

        (IDLE_LEFT, 'd'): WALK_RIGHT,
        (IDLE_LEFT, 'a'): WALK_LEFT,
        (IDLE_LEFT, None): IDLE_LEFT,
        (IDLE_LEFT, 'z'): HAMMER_LEFT,

        (WALK_RIGHT, 'd'): WALK_RIGHT,
        (WALK_RIGHT, 'a'): WALK_LEFT,
        (WALK_RIGHT, None): IDLE_RIGHT,
        (WALK_RIGHT, 'z'): HAMMER_RIGHT,

        (WALK_LEFT, 'd'): WALK_RIGHT,
        (WALK_LEFT, 'a'): WALK_LEFT,
        (WALK_LEFT, None): IDLE_LEFT,
        (WALK_LEFT, 'z'): HAMMER_LEFT,

        (HAMMER_LEFT, None): IDLE_LEFT,
        (HAMMER_RIGHT, None): IDLE_RIGHT,
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
    w, h = 960, 540
    tela = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Jogo com AFD")
    icon = pygame.image.load("..\\sprites\\icon\\icon.jpg")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    background = pygame.image.load('../sprites/background/background2.jpg').convert()
    background = pygame.transform.scale(background, (w, h))

    # Controle dos frames do personagem
    ultimo_tick = pygame.time.get_ticks()
    DELAY = 80  # Demora 95ms para transicionar de um frame para o outro

    # Criando o personagem
    personagem = Personagem(x = w // 2)

    # Importando os sprites
    sprites_idle_right = Sprite.carregar_sprites("..\\sprites\\idle\\right")
    sprites_idle_left  = Sprite.carregar_sprites("..\\sprites\\idle\\left")
    sprites_walk_right = Sprite.carregar_sprites("..\\sprites\\walk\\right")
    sprites_walk_left  = Sprite.carregar_sprites("..\\sprites\\walk\\left")
    sprites_hammer_right = Sprite.carregar_sprites("..\\sprites\\hammer\\right")
    sprites_hammer_left= Sprite.carregar_sprites("..\\sprites\\hammer\\left")
    sprites_jump_right = Sprite.carregar_sprites("..\\sprites\\jump\\right")
    sprites_jump_left = Sprite.carregar_sprites("..\\sprites\\jump\\left")

    # Definindo as ações realizadas pelo personagem
    acoes = {
        IDLE_RIGHT:     (personagem.idle, sprites_idle_right),
        IDLE_LEFT:      (personagem.idle, sprites_idle_left),
        WALK_RIGHT:     (personagem.walk_right, sprites_walk_right),
        WALK_LEFT:      (personagem.walk_left, sprites_walk_left),
        HAMMER_RIGHT:   (personagem.hammer_right, sprites_hammer_right),
        HAMMER_LEFT:    (personagem.hammer_left, sprites_hammer_left),
        # A ação de pular é tratada separadamente
    }

    # Flag para controlar execução completa do hammer
    hammering = False
    estado_atual = afd.estado_inicial

    # Variáveis para controlar o pulo do personagem
    jumping = False
    velocidade_vertical = 0  # < 0: move para cima; > 0 move para baixo
    gravidade = 1  # Diminui a velocidade vertical na subida e aumenta na descida
    forca_pulo = -25  # Velocidade inicial do pulo
    y_chao = personagem.y

    em_execucao = True
    while em_execucao:
        # Atualizando a direção do pulo a cada rodada para ser coerente
        direcao_pulo = +1 if "RIGHT" in estado_atual else -1

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

            # Tratando o evento de pulo
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_w:
                if not jumping and not hammering:
                    jumping = True
                    velocidade_vertical = forca_pulo
                    personagem.frame = 0

        # Renderizando o pulo
        if jumping:
            # Física vertical
            personagem.y += velocidade_vertical
            velocidade_vertical += gravidade

            # Controle horizontal no ar
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a]:
                personagem.x -= personagem.velocidade_pulando
                direcao_pulo = -1
            elif teclas[pygame.K_d]:
                personagem.x += personagem.velocidade_pulando
                direcao_pulo = +1

            # Aterrissagem
            if personagem.y >= y_chao:
                personagem.y = y_chao
                jumping = False
                personagem.frame = 0

            sprites = sprites_jump_right if direcao_pulo > 0 else sprites_jump_left

            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame = (personagem.frame + 1) % len(sprites)

            # Renderizando
            personagem.stay_in_bounds(w, h, sprites[personagem.frame % len(sprites)].get_width(), sprites[personagem.frame % len(sprites)].get_height())
            tela.blit(background, (0, 0))
            renderizar(tela, sprites, personagem)
            clock.tick(FRAME_RATE)
            continue

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
            personagem.stay_in_bounds(w, h, sprites[personagem.frame % len(sprites)].get_width(), sprites[personagem.frame % len(sprites)].get_height())
            tela.blit(background, (0, 0))
            renderizar(tela, sprites, personagem)
            clock.tick(FRAME_RATE)
            continue  # Pula a execução das teclas normais (andar, pular, agachar, etc.)

        # Transições normais (sem ataques e supers)
        teclas = pygame.key.get_pressed()
        if teclas[alfabeto_teclas['d']]: simbolo = 'd'
        elif teclas[alfabeto_teclas['a']]: simbolo = 'a'
        else: simbolo = None

        # Executando a ação
        estado_atual = afd.processar(simbolo)
        acao, sprites = acoes[estado_atual]
        acao()
        personagem.stay_in_bounds(w, h, sprites[personagem.frame % len(sprites)].get_width(), sprites[personagem.frame % len(sprites)].get_height())

        # Atualização de frame normal
        if agora - ultimo_tick > DELAY:
            ultimo_tick = agora
            personagem.frame = (personagem.frame + 1) % len(sprites)

        # Renderização final
        tela.blit(background, (0, 0))
        renderizar(tela, sprites, personagem)
        clock.tick(FRAME_RATE)

    pygame.quit()

if __name__ == '__main__':
    main()