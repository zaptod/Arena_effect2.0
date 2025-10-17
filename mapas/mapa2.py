
import pygame

def desenhar_mapa(screen):
	"""Mapa Arena - Estilo coliseu"""
	
	# Fundo (areia)
	screen.fill((194, 178, 128))
	
	# Paredes externas (pedra escura)
	pygame.draw.rect(screen, (60, 50, 40), (0, 0, 800, 25))      # Topo
	pygame.draw.rect(screen, (60, 50, 40), (0, 575, 800, 25))    # Base
	pygame.draw.rect(screen, (60, 50, 40), (0, 0, 25, 600))      # Esquerda
	pygame.draw.rect(screen, (60, 50, 40), (775, 0, 25, 600))    # Direita
	
	# Arena circular central (marcação)
	pygame.draw.circle(screen, (150, 120, 80), (400, 300), 200, 3)
	pygame.draw.circle(screen, (150, 120, 80), (400, 300), 150, 2)
	pygame.draw.circle(screen, (150, 120, 80), (400, 300), 100, 2)
	
	# Pilares nos cantos (obstáculos)
	pilar_cor = (100, 80, 60)
	pygame.draw.rect(screen, pilar_cor, (100, 100, 40, 40))      # Superior esquerdo
	pygame.draw.rect(screen, pilar_cor, (660, 100, 40, 40))      # Superior direito
	pygame.draw.rect(screen, pilar_cor, (100, 460, 40, 40))      # Inferior esquerdo
	pygame.draw.rect(screen, pilar_cor, (660, 460, 40, 40))      # Inferior direito
	
	# Pilares intermediários
	pygame.draw.rect(screen, pilar_cor, (250, 200, 30, 30))
	pygame.draw.rect(screen, pilar_cor, (520, 200, 30, 30))
	pygame.draw.rect(screen, pilar_cor, (250, 370, 30, 30))
	pygame.draw.rect(screen, pilar_cor, (520, 370, 30, 30))
	
	# Centro da arena (círculo dourado)
	pygame.draw.circle(screen, (255, 215, 0), (400, 300), 30)
	pygame.draw.circle(screen, (255, 235, 100), (400, 300), 20)
