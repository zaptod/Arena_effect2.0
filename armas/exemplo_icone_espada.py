import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from armas.arma1 import criar_arma

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Espada - Exemplo como na imagem")
clock = pygame.time.Clock()

# Cria a espada
espada = criar_arma(1)

# Posição central
center_x = 200
center_y = 200

font_large = pygame.font.SysFont(None, 72)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))
    
    # Desenha o círculo verde (como na imagem)
    pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), 60)
    pygame.draw.circle(screen, (0, 200, 0), (center_x, center_y), 60, 3)
    
    # Desenha o número no centro (similar à imagem - pode ser o dano da arma)
    numero = font_large.render(str(int(espada.dano)), True, (0, 0, 0))
    numero_rect = numero.get_rect(center=(center_x, center_y))
    screen.blit(numero, numero_rect)
    
    # Desenha a espada em cima do círculo (apontando para cima)
    espada_x = center_x
    espada_y = center_y - 60  # Acima do círculo
    
    # Desenha espada vertical simples
    # Lâmina
    pygame.draw.line(screen, (192, 192, 192), 
                    (espada_x, espada_y - 40), 
                    (espada_x, espada_y + 10), 5)
    
    # Cabo
    pygame.draw.line(screen, (139, 69, 19), 
                    (espada_x, espada_y + 10), 
                    (espada_x, espada_y + 25), 6)
    
    # Guarda
    pygame.draw.line(screen, (192, 192, 192), 
                    (espada_x - 12, espada_y + 10), 
                    (espada_x + 12, espada_y + 10), 4)
    
    # Informações
    font_small = pygame.font.SysFont(None, 20)
    info = font_small.render(f"{espada.nome} - Dano: {espada.dano}", True, (0, 0, 0))
    screen.blit(info, (center_x - 80, center_y + 100))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
