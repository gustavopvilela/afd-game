from AFD import *
from Personagem import *
from Sprite import *

# Criando o personagem
personagem = Personagem()

# Definindo os estados do personagem
IDLE_RIGHT = "IDLE_RIGHT"
IDLE_LEFT = "IDLE_LEFT"
WALK_RIGHT = "WALK_RIGHT"
WALK_LEFT = "WALK_LEFT"

# Definindo as teclas aceitas pelo programa
alfabeto = ['a', 'd', None]

# Definindo as transições dos estados do personagem
transicoes = {
    (IDLE_RIGHT, 'd'): WALK_RIGHT,
    (IDLE_RIGHT, 'a'): WALK_LEFT,
    (IDLE_RIGHT, None): IDLE_RIGHT,
    (IDLE_LEFT, 'd'): WALK_RIGHT,
    (IDLE_LEFT, 'a'): WALK_LEFT,
    (IDLE_LEFT, None): IDLE_LEFT,
    (WALK_RIGHT, 'd'): WALK_RIGHT,
    (WALK_RIGHT, 'a'): WALK_LEFT,
    (WALK_RIGHT, None): IDLE_RIGHT,
    (WALK_LEFT, 'd'): WALK_RIGHT,
    (WALK_LEFT, 'a'): WALK_LEFT,
    (WALK_LEFT, None): IDLE_LEFT,
}

# Criando o AFD para controlar o personagem
afd = AFD(
    estados = [IDLE_RIGHT, IDLE_LEFT, WALK_RIGHT, WALK_LEFT],
    alfabeto = alfabeto,
    transicoes = transicoes,
    estado_inicial = IDLE_RIGHT,
    estados_finais = None
)

# Inicialização do PyGame
pygame.init()
w, h = 960, 540
tela = pygame.display.set_mode((w, h))
pygame.display.set_caption("Jogo com AFD")
clock = pygame.time.Clock()

# Controle dos frames do personagem
ultimo_tick = pygame.time.get_ticks()
DELAY = 95 # Demora 95ms para transicionar de um frame para o outro

# Importando os sprites
sprites_idle_right = Sprite.carregar_sprites("..\\sprites\\idle\\right")
sprites_idle_left = Sprite.carregar_sprites("..\\sprites\\idle\\left")
sprites_walk_right = Sprite.carregar_sprites("..\\sprites\\walk\\right")
sprites_walk_left = Sprite.carregar_sprites("..\\sprites\\walk\\left")

# Definindo as ações realizadas pelo personagem
acoes = {
    IDLE_RIGHT: (personagem.idle, sprites_idle_right),
    IDLE_LEFT: (personagem.idle, sprites_idle_left),
    WALK_RIGHT: (personagem.walk_right, sprites_walk_right),
    WALK_LEFT: (personagem.walk_left, sprites_walk_left),
}

em_execucao = True
while em_execucao:
    agora = pygame.time.get_ticks()

    # Capturando as teclas pressionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_d]: simbolo = 'd'
    elif teclas[pygame.K_a]: simbolo = 'a'
    else: simbolo = None

    # Encontramos o novo estado do personagem
    estado_atual = afd.processar(simbolo)

    # Do dicionário de ações, chamamos a ação correspondente com o estado atual
    acao, sprites = acoes[estado_atual]
    acao()

    # Tratando o evento de saída do PyGame para encerrar o programa
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            em_execucao = False

    # A cada 95ms, atualizamos o frame do personagem
    if agora - ultimo_tick > DELAY:
        ultimo_tick = agora
        personagem.frame = (personagem.frame + 1) % len(sprites)

    # Por fim, basta renderizar tudo na tela
    tela.fill((30, 30, 30)) # Fundo cinza
    tela.blit(sprites[personagem.frame], (personagem.x, 400))
    pygame.display.flip()
    clock.tick(60)

pygame.quit() # Encerra o PyGame