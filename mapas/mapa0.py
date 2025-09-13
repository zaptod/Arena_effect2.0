
import pygame

def desenhar_mapa(screen):
	# Desenha paredes (retângulos nas bordas)
	pygame.draw.rect(screen, (100,100,100), (0,0,800,20)) # Topo
	pygame.draw.rect(screen, (100,100,100), (0,580,800,20)) # Base
	pygame.draw.rect(screen, (100,100,100), (0,0,20,600)) # Esquerda
	pygame.draw.rect(screen, (100,100,100), (780,0,20,600)) # Direita
	# Elemento interativo: círculo central
	pygame.draw.circle(screen, (255,215,0), (400,300), 40)