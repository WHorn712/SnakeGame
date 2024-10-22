import pygame
import sys


# Inicializar o Pygame
pygame.init()

# Definir cores (nova paleta)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
FUNDO = (240, 240, 245)  # Cinza bem claro com um toque de azul
COR_BOTAO1 = (100, 180, 255)  # Azul claro
COR_BOTAO2 = (255, 180, 100)  # Laranja claro
COR_HOVER = (70, 70, 70)  # Cinza escuro para o efeito hover

# Configurar a tela
largura = 400
altura = 300
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("SNAKE GAME")

# Definir os botões
botao1 = pygame.Rect(50, 100, 120, 50)
botao2 = pygame.Rect(230, 100, 120, 50)


# Função para desenhar os botões
def desenhar_botoes(mouse_pos):
    # Verificar se o mouse está sobre os botões
    hover1 = botao1.collidepoint(mouse_pos)
    hover2 = botao2.collidepoint(mouse_pos)

    # Desenhar botão 1 com efeito hover
    cor1 = COR_HOVER if hover1 else COR_BOTAO1
    pygame.draw.rect(tela, cor1, botao1)
    if hover1:
        pygame.draw.rect(tela, COR_BOTAO1, botao1.inflate(-4, -4))

    # Desenhar botão 2 com efeito hover
    cor2 = COR_HOVER if hover2 else COR_BOTAO2
    pygame.draw.rect(tela, cor2, botao2)
    if hover2:
        pygame.draw.rect(tela, COR_BOTAO2, botao2.inflate(-4, -4))

    fonte = pygame.font.Font(None, 30)
    texto1 = fonte.render("Jogar", True, PRETO)
    texto2 = fonte.render("IA", True, PRETO)

    tela.blit(texto1, (botao1.x + 20, botao1.y + 15))
    tela.blit(texto2, (botao2.x + 20, botao2.y + 15))


# Loop principal
executando = True
clock = pygame.time.Clock()
while executando:
    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao1.collidepoint(evento.pos):
                import main_game_manual
            elif botao2.collidepoint(evento.pos):
                import main_game_IA

    # Preencher a tela com a cor de fundo
    tela.fill(FUNDO)

    # Desenhar os botões
    desenhar_botoes(mouse_pos)

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de quadros
    clock.tick(60)

# Encerrar o Pygame
pygame.quit()
sys.exit()