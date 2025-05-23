import time

from AFD import *
from Personagem import *
from Sprite import *
import pygame

def renderizar (tela, sprites, personagem, fade, alpha, kuro, alpha_kuro, x = None, y = None):
    if x is None: x = personagem.x
    if y is None: y = personagem.y

    # Alinhar as bases dos sprites do personagem à altura em que ele está
    img = sprites[personagem.frame]
    rect = img.get_rect()
    rect.x = x
    rect.bottom = y
    tela.blit(img, rect)

    # Aplicando o fade
    fade.set_alpha(alpha)
    tela.blit(fade, (0, 0))

    # Colocando Kuro
    kuro.set_alpha(alpha_kuro)
    kuro_rect = kuro.get_rect()
    kuro_rect.center = (960 // 2, 540 // 2)
    tela.blit(kuro, kuro_rect)

    pygame.display.flip()

def desenhar_frame (personagem, h, sprites, tela, background, fade, alpha, kuro, alpha_kuro):
    personagem.stay_in_bounds(170, 790, h, sprites[personagem.frame % len(sprites)].get_width(), sprites[personagem.frame % len(sprites)].get_height())
    tela.blit(background, (0, 0))
    renderizar(tela, sprites, personagem, fade, alpha, kuro, alpha_kuro)

# Função de fazer fade-out na música para o super
def music_fade_out (duracao=1.0, volume_max=1.0):
    passos = 20
    delay = duracao / passos
    for i in range (passos):
        vol = volume_max * (1.0 - (i + 1) / passos)
        pygame.mixer.music.set_volume(vol)
        time.sleep(delay)
    pygame.mixer.music.pause()

def music_fade_in (duracao=1.0, volume_max=1.0):
    passos = 20
    delay = duracao / passos
    pygame.mixer.music.unpause()
    for i in range (passos):
        vol = volume_max * (i + 1) / passos
        pygame.mixer.music.set_volume(vol)
        time.sleep(delay)

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
    DASH_RIGHT = "DASH_RIGHT"
    DASH_LEFT = "DASH_LEFT"
    CROUCH_RIGHT = "CROUCH_RIGHT"
    CROUCH_LEFT = "CROUCH_LEFT"
    ENERGYEXPLOSION_RIGHT = "ENERGYEXPLOSION_RIGHT"
    ENERGYEXPLOSION_LEFT = "ENERGYEXPLOSION_LEFT"
    SUPER_LEFT = "SUPER_LEFT"
    SUPER_RIGHT = "SUPER_RIGHT"

    # Definindo as teclas aceitas pelo programa
    alfabeto_teclas = {
        'a': pygame.K_a,
        'd': pygame.K_d,
        'z': pygame.K_z,
        'w': pygame.K_w,
        'f' : pygame.K_f,
        's': pygame.K_s,
        'o': pygame.K_o,
        'r': pygame.K_r,
        'i': pygame.K_i,
        'e': pygame.K_e,
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
        (IDLE_RIGHT, 'e'): ENERGYEXPLOSION_RIGHT,

        (IDLE_LEFT, 'd'): WALK_RIGHT,
        (IDLE_LEFT, 'a'): WALK_LEFT,
        (IDLE_LEFT, None): IDLE_LEFT,
        (IDLE_LEFT, 'z'): HAMMER_LEFT,
        (IDLE_LEFT, 'f'): DASH_LEFT,
        (IDLE_LEFT, 's'): CROUCH_LEFT,
        (IDLE_LEFT, 'e'): ENERGYEXPLOSION_LEFT,

        (WALK_RIGHT, 'd'): WALK_RIGHT,
        (WALK_RIGHT, 'a'): WALK_LEFT,
        (WALK_RIGHT, None): IDLE_RIGHT,
        (WALK_RIGHT, 'z'): HAMMER_RIGHT,
        (WALK_RIGHT, 'f'): DASH_RIGHT,
        (WALK_RIGHT, 's'): CROUCH_RIGHT,
        (WALK_RIGHT, 'e'): ENERGYEXPLOSION_RIGHT,

        (WALK_LEFT, 'd'): WALK_RIGHT,
        (WALK_LEFT, 'a'): WALK_LEFT,
        (WALK_LEFT, None): IDLE_LEFT,
        (WALK_LEFT, 'z'): HAMMER_LEFT,
        (WALK_LEFT, 'f'): DASH_LEFT,
        (WALK_LEFT, 's'): CROUCH_LEFT,
        (WALK_LEFT, 'e'): ENERGYEXPLOSION_LEFT,

        (HAMMER_LEFT, None): IDLE_LEFT,
        (HAMMER_RIGHT, None): IDLE_RIGHT,

        (DASH_LEFT, None): IDLE_LEFT,
        (DASH_RIGHT, None): IDLE_RIGHT,

        (CROUCH_RIGHT, None): IDLE_RIGHT,
        (CROUCH_LEFT, None): IDLE_LEFT,

        (ENERGYEXPLOSION_LEFT, None): IDLE_LEFT,
        (ENERGYEXPLOSION_RIGHT, None): IDLE_RIGHT,
    }

    # Criando o AFD para controlar o personagem
    afd = AFD(
        estados={estado for (estado, _) in transicoes.keys()},
        alfabeto={simbolo for simbolo in alfabeto_teclas.keys()},
        transicoes=transicoes,
        estado_inicial=IDLE_RIGHT,
        estados_finais=set()
    )

    # Inicialização do PyGame
    pygame.init()
    pygame.mixer.init()
    w, h = 960, 540
    tela = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Jogo com AFD")
    icon = pygame.image.load("../sprites/icon/icon.jpg")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    # Definição da imagem de fundo
    background = pygame.image.load('../sprites/background/background2.jpg').convert()
    background = pygame.transform.scale(background, (w, h))

    # Definição dos sons
    jump_sound = pygame.mixer.Sound('../sounds/jump_sound.wav')
    jump_sound.set_volume(1.0)
    jump_sound_playing = False

    dash_sound = pygame.mixer.Sound('../sounds/dash_sound.wav')
    dash_sound.set_volume(1.0)
    dash_sound_playing = False

    super_sound = pygame.mixer.Sound('../sounds/super_sound.wav')
    super_sound.set_volume(1.0)
    super_sound_playing = False

    super_explosion_sound = pygame.mixer.Sound('../sounds/super_explosion_sound.wav')
    super_explosion_sound.set_volume(1.0)
    super_explosion_sound_playing = False

    super_launch_sound = pygame.mixer.Sound('../sounds/super_launch_sound.wav')
    super_launch_sound.set_volume(1.0)
    super_launch_sound_playing = False

    hammer_sound = pygame.mixer.Sound('../sounds/hammer_sound.wav')
    hammer_sound.set_volume(1.0)
    hammer_sound_playing = False

    energy_explosion_sound = pygame.mixer.Sound('../sounds/energy_explosion_sound.wav')
    energy_explosion_sound.set_volume(1.0)
    energy_explosion_sound_playing = False

    # Soundtrack
    pygame.mixer.music.load('../sounds/luma_pools.mp3')
    pygame.mixer.music.play(loops=-1, fade_ms=2000)
    pygame.mixer.music.set_volume(1.0)

    # Definição para o fade do super
    fade = pygame.Surface((w, h))
    fade.fill((0, 0, 0))

    alpha = 0
    fade_start = pygame.time.get_ticks()
    fading_out = False # A tela fica escura
    fading_in = False # A tela volta às cores
    FADE_DURATION = 3000 # milissegundos

    # Definição da imagem do super
    alpha_kuro = 0
    kuro = pygame.image.load('../sprites/super/kuro/kuro.png')
    w_kuro, h_kuro = kuro.get_size()
    novo_tamanho = (w_kuro // 2, h_kuro // 2)
    kuro = pygame.transform.smoothscale(kuro, novo_tamanho)
    kuro_in = False
    kuro_out = False

    # Controle dos frames do personagem
    ultimo_tick = pygame.time.get_ticks()
    DELAY = 80  # Demora 95ms para transicionar de um frame para o outro

    # Criando o personagem
    personagem = Personagem(x = w // 2)

    # Importando os sprites
    sprites_idle_right = Sprite.carregar_sprites("../sprites/idle/right")
    sprites_idle_left  = Sprite.carregar_sprites("../sprites/idle/left")
    sprites_walk_right = Sprite.carregar_sprites("../sprites/walk/right")
    sprites_walk_left  = Sprite.carregar_sprites("../sprites/walk/left")
    sprites_hammer_right = Sprite.carregar_sprites("../sprites/hammer/right")
    sprites_hammer_left= Sprite.carregar_sprites("../sprites/hammer/left")
    sprites_jump_right = Sprite.carregar_sprites("../sprites/jump/right")
    sprites_jump_left = Sprite.carregar_sprites("../sprites/jump/left")
    sprites_dash_right = Sprite.carregar_sprites("../sprites/dash/right")
    sprites_dash_left = Sprite.carregar_sprites("../sprites/dash/left")
    sprites_crouch_right = Sprite.carregar_sprites("../sprites/crouch/right")
    sprites_crouch_left = Sprite.carregar_sprites("../sprites/crouch/left")
    sprites_super_right = Sprite.carregar_sprites("../sprites/super/right")
    sprites_super_left = Sprite.carregar_sprites("../sprites/super/left")
    sprites_energyexplosion_right = Sprite.carregar_sprites("../sprites/energyexplosion/right")
    sprites_energyexplosion_left = Sprite.carregar_sprites("../sprites/energyexplosion/left")

    # Definindo as ações realizadas pelo personagem
    acoes = {
        IDLE_RIGHT:            (personagem.idle, sprites_idle_right),
        IDLE_LEFT:             (personagem.idle, sprites_idle_left),
        WALK_RIGHT:            (personagem.walk_right, sprites_walk_right),
        WALK_LEFT:             (personagem.walk_left, sprites_walk_left),
        HAMMER_RIGHT:          (personagem.hammer_right, sprites_hammer_right),
        HAMMER_LEFT:           (personagem.hammer_left, sprites_hammer_left),
        ENERGYEXPLOSION_RIGHT: (personagem.energyexplosion_right, sprites_energyexplosion_right),
        ENERGYEXPLOSION_LEFT:  (personagem.energyexplosion_left, sprites_energyexplosion_left),

        # A ação de pular é tratada separadamente

        DASH_RIGHT:     (personagem.idle, sprites_dash_right),
        DASH_LEFT:      (personagem.idle, sprites_dash_left),
        CROUCH_RIGHT:   (personagem.crouch_right, sprites_crouch_right),
        CROUCH_LEFT:    (personagem.crouch_left, sprites_crouch_left),

        # As ações COMBO_I e COMBO_N não são definidas aqui, pois elas não fazem nada.
        # São uma preparação para o super.

        SUPER_LEFT:     (personagem.super_left, sprites_super_left),
        SUPER_RIGHT:    (personagem.super_right, sprites_super_right)
    }

    # Flag para controlar execução completa do hammer e do dash
    supering = False
    hammering = False
    dashing = False
    crouching = False
    exploding = False
    estado_atual = afd.estado_inicial
    direcao = "right" if "RIGHT" in estado_atual else "left"

    # Variáveis para controlar o pulo do personagem
    jumping = False
    velocidade_vertical = 0  # < 0: move para cima; > 0 move para baixo
    gravidade = 1  # Diminui a velocidade vertical na subida e aumenta na descida
    forca_pulo = -25  # Velocidade inicial do pulo
    y_chao = personagem.y

    em_execucao = True
    while em_execucao:
        # Apertando a sequência de teclas, ele ativa o super
        if "SUPER" in estado_atual:
            if not supering:
                supering = True
                personagem.frame = 0

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

            # Apertando a tecla E e olhando para a direita, o personagem entra em modo de ataque com a explosão de energia para a direita.
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_e and "RIGHT" in estado_atual:
                if not exploding:
                    exploding = True
                    personagem.frame = 0
                    estado_atual = ENERGYEXPLOSION_RIGHT

            # Apertando a tecla E e olhando para a esquerda, o personagem entra em modo de ataque com a explosão de energia para a esquerda.
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_e and "LEFT" in estado_atual:
                if not exploding:
                    exploding = True
                    personagem.frame = 0
                    estado_atual = ENERGYEXPLOSION_LEFT

            # Tratando o evento de pulo
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_w:
                if not jumping and not hammering:
                    jumping = True
                    velocidade_vertical = forca_pulo
                    personagem.frame = 0

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

        # Renderizando o super
        if supering:
            if not super_explosion_sound_playing:
                super_explosion_sound.play()
                super_explosion_sound_playing = True

            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame += 1

                if personagem.frame == 14 and not super_launch_sound_playing:
                    super_launch_sound.play()
                    super_launch_sound_playing = True

                if personagem.frame > 16:
                    desloc_y = 30 * (3986 / 1000)
                    personagem.y -= desloc_y

                # Se passou do último frame, encerra o super e volta a ficar parado (idle)
                limite = len(sprites_super_right) if estado_atual == SUPER_RIGHT else len(sprites_super_left)
                if personagem.frame >= limite:
                    music_fade_out()

                    # supering = False
                    personagem.frame = 0
                    estado_atual = IDLE_RIGHT if estado_atual == SUPER_RIGHT else IDLE_LEFT

                    fade_start = pygame.time.get_ticks()
                    fading_out = True
                    fading_in = False

                # Renderizando o fade
                if fading_out:
                    if not super_sound_playing:
                        super_sound.play()
                        super_sound_playing = True

                    elapsed = pygame.time.get_ticks() - fade_start
                    personagem.frame = 0

                    if elapsed < FADE_DURATION:
                        alpha = int((elapsed / FADE_DURATION) * 255)  # Vai escurecendo a tela
                    else:
                        # Terminado o fade-out, fazemos o fade-in
                        fade_start = pygame.time.get_ticks()
                        fading_in = False
                        fading_out = False
                        kuro_in = True
                        kuro_out = False
                        alpha = 255

                elif kuro_in:
                    elapsed = pygame.time.get_ticks() - fade_start
                    personagem.frame = 0

                    if elapsed < FADE_DURATION:
                        alpha_kuro = int((elapsed / FADE_DURATION) * 255)
                    else:
                        # Terminado o fade-out, fazemos o fade-in
                        fade_start = pygame.time.get_ticks()
                        fading_in = False
                        fading_out = False
                        kuro_in = False
                        kuro_out = True
                        alpha_kuro = 255

                elif kuro_out:
                    elapsed = pygame.time.get_ticks() - fade_start
                    personagem.frame = 0

                    if elapsed < FADE_DURATION:
                        alpha_kuro = 255 - int((elapsed / FADE_DURATION) * 255)
                    else:
                        # Terminado o fade-out, fazemos o fade-in
                        fade_start = pygame.time.get_ticks()
                        fading_in = True
                        fading_out = False
                        kuro_in = False
                        kuro_out = False
                        alpha_kuro = 0

                        personagem.x = w // 2
                        personagem.y = y_chao

                elif fading_in:
                    elapsed = pygame.time.get_ticks() - fade_start

                    personagem.frame = 0

                    if elapsed < FADE_DURATION:
                        alpha = 255 - int((elapsed / FADE_DURATION) * 255)
                    else:
                        # Terminou o fade-in, a tela voltou ao normal
                        fading_in = False
                        fading_out = False
                        kuro_in = False
                        kuro_out = False
                        alpha = 0

                        # Definimos como o fim do super quando a tela terminar de fazer seu
                        # fade-in completamente
                        supering = False

                        # Voltamos a definir a variável do som como False para que
                        # ela possa voltar a tocar no próximo super
                        super_sound_playing = False
                        super_explosion_sound_playing = False
                        super_explosion_sound_playing = False

                        # Depois do super, a música volta a tocar normalmente
                        music_fade_in()

            acao, sprites = acoes[estado_atual]
            acao()
            desenhar_frame(personagem, h, sprites, tela, background, fade, alpha, kuro, alpha_kuro)
            clock.tick(FRAME_RATE)
            continue

        # Renderizando o pulo
        if jumping:
            if not jump_sound_playing:
                jump_sound.play()
                jump_sound_playing = True

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
                estado_atual = IDLE_RIGHT if direcao_pulo > 0 else IDLE_LEFT
                crouching = False
                jump_sound_playing = False

            sprites = sprites_jump_right if direcao_pulo > 0 else sprites_jump_left

            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame = (personagem.frame + 1) % len(sprites)

            # Renderizando
            desenhar_frame(personagem, h, sprites, tela, background, fade, alpha, kuro, alpha_kuro)
            clock.tick(FRAME_RATE)
            continue

        # Nesta parte do código, colocaremos as animações que devem ser feitas separadamente (ataques e supers).
        # Ataque 1: Ataque de martelo
        if hammering:
            if not hammer_sound_playing:
                hammer_sound.play()
                hammer_sound_playing = True

            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame += 1

                # Se passou do último frame, encerra o ataque e volta a ficar parado (idle)
                limite = len(sprites_hammer_left) if estado_atual == HAMMER_LEFT else len(sprites_hammer_right)
                if personagem.frame >= limite:
                    hammering = False
                    personagem.frame = 0
                    estado_atual = IDLE_LEFT

                    # Volta o som para tocar no próximo ataque
                    hammer_sound_playing = False

            # Mostrando na tela o ataque
            acao, sprites = acoes[estado_atual]
            acao()
            desenhar_frame(personagem, h, sprites, tela, background, fade, alpha, kuro, alpha_kuro)
            clock.tick(FRAME_RATE)
            continue  # Pula a execução das teclas normais (andar, pular, agachar, etc.)

        # Ataque 2: Ataque de explosão de energia
        if exploding:
            if not energy_explosion_sound_playing:
                energy_explosion_sound.play()
                energy_explosion_sound_playing = True

            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame += 1

                # Se passou do último frame, encerra o ataque e volta a ficar parado (idle)
                limite = len(sprites_energyexplosion_left) if estado_atual == ENERGYEXPLOSION_LEFT else len(sprites_energyexplosion_right)
                if personagem.frame >= limite:
                    exploding = False
                    personagem.frame = 0
                    estado_atual = IDLE_LEFT

                    energy_explosion_sound_playing = False

            # Mostrando na tela o ataque
            acao, sprites = acoes[estado_atual]
            acao()
            desenhar_frame(personagem, h, sprites, tela, background, fade, alpha, kuro, alpha_kuro)
            clock.tick(FRAME_RATE)
            continue  # Pula a execução das teclas normais (andar, pular, agachar, etc.)


        # Dash: o personagem avança em um dash.
        if dashing:
            if not dash_sound_playing:
                dash_sound.play()
                dash_sound_playing = True

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

                    dash_sound_playing = False

            # Mostrando na tela o ataque
            acao, sprites = acoes[estado_atual]
            acao()
            desenhar_frame(personagem, h, sprites, tela, background, fade, alpha, kuro, alpha_kuro)
            clock.tick(FRAME_RATE)
            continue

        # Crouch: personagem agacha e se levanta.
        if crouching:
            acao, sprites = acoes[estado_atual]
            acao()
            # Deixa iterando apenas sob os 4 frames finais para ficar agachado
            sprites = sprites[-4:]

            # Verifica se 'd' ou 'a' foi pressionado, se sim, desloca o personagem para a esquerda ou direita.
            teclas = pygame.key.get_pressed()
            if teclas[alfabeto_teclas['d']]:
                personagem.x += personagem.velocidade_andando - 2
                direcao = "right"
                estado_atual = CROUCH_RIGHT
            elif teclas[alfabeto_teclas['a']]:
                personagem.x -= personagem.velocidade_andando - 2
                direcao = "left"
                estado_atual = CROUCH_LEFT
            else:
                estado_atual = CROUCH_RIGHT if direcao=="right" else CROUCH_LEFT

            if agora - ultimo_tick > DELAY:
                ultimo_tick = agora
                personagem.frame = (personagem.frame + 1) % len(sprites)

            desenhar_frame(personagem, h, sprites, tela, background, fade, alpha, kuro, alpha_kuro)
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
        elif teclas[alfabeto_teclas['o']] and teclas[alfabeto_teclas['r']] and teclas[alfabeto_teclas['i']]:
            estado_atual = SUPER_RIGHT if "RIGHT" in estado_atual else SUPER_LEFT
            continue
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
        desenhar_frame(personagem, h, sprites, tela, background, fade, alpha, kuro, alpha_kuro)
        clock.tick(FRAME_RATE)

    pygame.quit()

if __name__ == '__main__':
    main()