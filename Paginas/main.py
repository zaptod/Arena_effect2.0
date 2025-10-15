
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arena Effect Simulator')

font = pygame.font.SysFont(None, 36)

def draw_button(text, rect, color=(70,130,180)):
	pygame.draw.rect(screen, color, rect)
	txt = font.render(text, True, (255,255,255))
	screen.blit(txt, (rect.x + 10, rect.y + 10))

def main():
	clock = pygame.time.Clock()
	running = True
	while running:
		screen.fill((30,30,30))
		# Título
		titulo = font.render('Arena Effect Simulator', True, (255,255,255))
		screen.blit(titulo, (WIDTH//2 - 150, 30))
		
		# Botões principais
		btn_personagens = pygame.Rect(100, 120, 250, 50)
		btn_armas = pygame.Rect(100, 190, 250, 50)
		btn_mapas = pygame.Rect(100, 260, 250, 50)
		btn_simulation = pygame.Rect(100, 330, 250, 50)
		
		draw_button('Personagens', btn_personagens)
		draw_button('Armas', btn_armas)
		draw_button('Mapas', btn_mapas)
		draw_button('Iniciar Simulação', btn_simulation, color=(0,150,0))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_personagens.collidepoint(event.pos):
					import personagensP
					personagensP.show_personagens_carousel(screen)
					pygame.event.clear()
					screen.fill((30,30,30))
				elif btn_armas.collidepoint(event.pos):
					import armasP
					armasP.show_armas_carousel(screen)
					pygame.event.clear()
					screen.fill((30,30,30))
				elif btn_mapas.collidepoint(event.pos):
					import mapasP
					mapasP.show_mapas_carousel(screen)
					pygame.event.clear()
					screen.fill((30,30,30))
				elif btn_simulation.collidepoint(event.pos):
					import SelectionP
					SelectionP.show_selection_carousel(screen)
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
