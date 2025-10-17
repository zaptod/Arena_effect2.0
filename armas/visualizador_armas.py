import pygame
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from armas.arma1 import criar_arma as criar_espada
from armas.arma2 import criar_arma as criar_arco
from armas.arma3 import criar_arma as criar_machado
from armas.arma4 import criar_arma as criar_adaga

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Visualizador de Armas")
clock = pygame.time.Clock()

# Cria todas as armas
armas = [
    criar_espada(1),
    criar_arco(2),
    criar_machado(3),
    criar_adaga(4)
]

# Posição do "personagem" (centro da tela)
personagem_x = 400
personagem_y = 300
personagem_raio = 20

# Variáveis de controle
arma_selecionada = 0
tempo = 0

font = pygame.font.SysFont(None, 24)
font_small = pygame.font.SysFont(None, 18)

running = True
while running:
    dt = clock.tick(60) / 1000.0
    tempo += dt
    
    # Atualiza arma
    armas[arma_selecionada].update(dt)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                arma_selecionada = (arma_selecionada + 1) % len(armas)
            elif event.key == pygame.K_LEFT:
                arma_selecionada = (arma_selecionada - 1) % len(armas)
            elif event.key == pygame.K_SPACE:
                if armas[arma_selecionada].atacar():
                    print(f"{armas[arma_selecionada].nome} atacou!")
    
    # Pega posição do mouse para apontar arma
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Desenha
    screen.fill((40, 40, 60))
    
    # Desenha o personagem (círculo verde)
    pygame.draw.circle(screen, (0, 255, 0), (personagem_x, personagem_y), personagem_raio)
    
    # Desenha a arma selecionada
    armas[arma_selecionada].draw(screen, personagem_x, personagem_y, mouse_x, mouse_y)
    
    # Desenha informações da arma
    arma = armas[arma_selecionada]
    y_offset = 20
    
    info_texts = [
        f"Arma: {arma.nome}",
        f"Dano: {arma.dano}",
        f"Alcance: {arma.alcance}",
        f"Velocidade Ataque: {arma.velocidade_ataque}",
        f"Cooldown: {max(0, arma.cooldown):.2f}s"
    ]
    
    for i, text in enumerate(info_texts):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, y_offset + i * 25))
    
    # Instruções
    instrucoes = [
        "Setas <- -> : Trocar arma",
        "ESPAÇO: Atacar",
        "Mouse: Apontar arma"
    ]
    
    for i, text in enumerate(instrucoes):
        text_surface = font_small.render(text, True, (200, 200, 200))
        screen.blit(text_surface, (10, screen.get_height() - 70 + i * 20))
    
    # Desenha ícones de todas as armas na parte superior
    icon_y = 50
    for i, arma in enumerate(armas):
        icon_x = 600 + i * 70
        arma.draw_icon(screen, icon_x, icon_y, size=50)
        
        # Marca a arma selecionada
        if i == arma_selecionada:
            pygame.draw.circle(screen, (255, 255, 0), (icon_x, icon_y), 28, 3)
        
        # Nome da arma
        nome_surface = font_small.render(arma.nome.split()[0], True, (255, 255, 255))
        nome_rect = nome_surface.get_rect(center=(icon_x, icon_y + 40))
        screen.blit(nome_surface, nome_rect)
    
    pygame.display.flip()

pygame.quit()
