
import pygame

def desenhar_mapa(screen):
	"""Mapa Labirinto - Corredores e passagens"""
	
	# Fundo (chão de pedra)
	screen.fill((50, 50, 70))
	
	# Paredes externas
	parede_cor = (30, 30, 50)
	pygame.draw.rect(screen, parede_cor, (0, 0, 800, 20))      # Topo
	pygame.draw.rect(screen, parede_cor, (0, 580, 800, 20))    # Base
	pygame.draw.rect(screen, parede_cor, (0, 0, 20, 600))      # Esquerda
	pygame.draw.rect(screen, parede_cor, (780, 0, 20, 600))    # Direita
	
	# Paredes internas (labirinto)
	parede_interna = (80, 80, 100)
	
	# Paredes horizontais
	pygame.draw.rect(screen, parede_interna, (100, 150, 250, 20))
	pygame.draw.rect(screen, parede_interna, (450, 150, 250, 20))
	pygame.draw.rect(screen, parede_interna, (100, 430, 250, 20))
	pygame.draw.rect(screen, parede_interna, (450, 430, 250, 20))
	
	# Paredes verticais
	pygame.draw.rect(screen, parede_interna, (250, 20, 20, 250))
	pygame.draw.rect(screen, parede_interna, (530, 20, 20, 250))
	pygame.draw.rect(screen, parede_interna, (250, 330, 20, 250))
	pygame.draw.rect(screen, parede_interna, (530, 330, 20, 250))
	
	# Blocos centrais (obstáculos)
	pygame.draw.rect(screen, parede_interna, (350, 250, 100, 20))
	pygame.draw.rect(screen, parede_interna, (350, 330, 100, 20))
	pygame.draw.rect(screen, parede_interna, (380, 250, 20, 100))
	
	# Salas (áreas especiais)
	pygame.draw.circle(screen, (100, 50, 150), (150, 100), 30)    # Sala roxa
	pygame.draw.circle(screen, (150, 100, 50), (650, 100), 30)    # Sala laranja
	pygame.draw.circle(screen, (50, 150, 100), (150, 500), 30)    # Sala ciano
	pygame.draw.circle(screen, (150, 50, 50), (650, 500), 30)     # Sala vermelha
	
	# Centro (objetivo)
	pygame.draw.circle(screen, (255, 215, 0), (400, 300), 25)
	pygame.draw.circle(screen, (255, 255, 150), (400, 300), 15)
