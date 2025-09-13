
import pygame
import sys
# from Paginas.main_simulation import run_simulation
# from Paginas.agentesP import show_agents_carousel
# from Paginas.SelectionP import show_selection_carousel

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
		# Botões principais
		btn_social = pygame.Rect(100, 100, 200, 50)
		btn_agents = pygame.Rect(100, 200, 200, 50)
		btn_simulation = pygame.Rect(100, 300, 200, 50)
		draw_button('Redes Sociais', btn_social)
		draw_button('Agentes', btn_agents)
		draw_button('Simulação', btn_simulation)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_social.collidepoint(event.pos):
					# Abrir redes sociais (placeholder)
					pass
				elif btn_agents.collidepoint(event.pos):
					import agentesP
					agentesP.show_agents_carousel(screen)
					pygame.event.clear()
					screen.fill((30,30,30))
					draw_button('Redes Sociais', btn_social)
					draw_button('Agentes', btn_agents)
					draw_button('Simulação', btn_simulation)
					pygame.display.flip()
				elif btn_simulation.collidepoint(event.pos):
					import SelectionP
					SelectionP.show_selection_carousel(screen)
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
