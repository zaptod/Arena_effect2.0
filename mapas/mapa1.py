
import pygame

def desenhar_mapa(screen):
	"""Mapa Avançado com obstáculos e zonas"""
	
	# Fundo
	screen.fill((40, 40, 60))
	
	# Paredes externas (mais grossas)
	pygame.draw.rect(screen, (80, 80, 100), (0, 0, 800, 30))      # Topo
	pygame.draw.rect(screen, (80, 80, 100), (0, 570, 800, 30))    # Base
	pygame.draw.rect(screen, (80, 80, 100), (0, 0, 30, 600))      # Esquerda
	pygame.draw.rect(screen, (80, 80, 100), (770, 0, 30, 600))    # Direita
	
	# Obstáculos centrais (cruz)
	pygame.draw.rect(screen, (100, 100, 120), (350, 250, 100, 100))  # Centro
	pygame.draw.rect(screen, (100, 100, 120), (300, 280, 50, 40))    # Esquerda
	pygame.draw.rect(screen, (100, 100, 120), (450, 280, 50, 40))    # Direita
	pygame.draw.rect(screen, (100, 100, 120), (380, 200, 40, 50))    # Topo
	pygame.draw.rect(screen, (100, 100, 120), (380, 350, 40, 50))    # Base
	
	# Cantos estratégicos
	pygame.draw.rect(screen, (120, 120, 140), (50, 50, 80, 80))      # Superior esquerdo
	pygame.draw.rect(screen, (120, 120, 140), (670, 50, 80, 80))     # Superior direito
	pygame.draw.rect(screen, (120, 120, 140), (50, 470, 80, 80))     # Inferior esquerdo
	pygame.draw.rect(screen, (120, 120, 140), (670, 470, 80, 80))    # Inferior direito
	
	# Zonas especiais (círculos decorativos)
	pygame.draw.circle(screen, (200, 50, 50), (200, 150), 25)        # Zona vermelha
	pygame.draw.circle(screen, (50, 200, 50), (600, 150), 25)        # Zona verde
	pygame.draw.circle(screen, (50, 50, 200), (200, 450), 25)        # Zona azul
	pygame.draw.circle(screen, (200, 200, 50), (600, 450), 25)       # Zona amarela
	
	# Elemento central especial (ponto dourado)
	pygame.draw.circle(screen, (255, 215, 0), (400, 300), 20)
	pygame.draw.circle(screen, (255, 255, 100), (400, 300), 12)
