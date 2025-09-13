
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_agentes import agentes_db
from bases_de_dados.Banco_de_dados_mapas import mapas_db
# from Paginas.main_simulation import run_simulation

def show_selection_carousel(screen):
	font = pygame.font.SysFont(None, 28)
	clock = pygame.time.Clock()
	selected_agents = set()
	selected_map = None
	running = True
	from Paginas.main_simulation import run_simulation
	while running:
		screen.fill((60,60,80))
		# Carrossel de agentes ativos
		screen.blit(font.render('Selecione agentes:', True, (255,255,255)), (50, 30))
		y_agents = 70
		for idx, agent in enumerate([a for a in agentes_db if a['ativo']]):
			rect = pygame.Rect(50, y_agents+idx*40, 200, 35)
			color = (0,200,0) if agent['id'] in selected_agents else (200,200,200)
			pygame.draw.rect(screen, color, rect)
			txt = font.render(agent['nome'], True, (0,0,0))
			screen.blit(txt, (rect.x+10, rect.y+5))
		# Carrossel de mapas
		screen.blit(font.render('Selecione mapa:', True, (255,255,255)), (350, 30))
		y_maps = 70
		for idx, mapa in enumerate(mapas_db):
			rect = pygame.Rect(350, y_maps+idx*40, 200, 35)
			color = (0,0,200) if mapa['id'] == selected_map else (200,200,200)
			pygame.draw.rect(screen, color, rect)
			txt = font.render(mapa['nome'], True, (0,0,0))
			screen.blit(txt, (rect.x+10, rect.y+5))
		# Botão iniciar simulação
		btn_sim = pygame.Rect(250, 400, 200, 50)
		pygame.draw.rect(screen, (70,130,180), btn_sim)
		txt = font.render('Iniciar Simulação', True, (255,255,255))
		screen.blit(txt, (btn_sim.x+10, btn_sim.y+10))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Seleção de agentes
				for idx, agent in enumerate([a for a in agentes_db if a['ativo']]):
					rect = pygame.Rect(50, y_agents+idx*40, 200, 35)
					if rect.collidepoint(event.pos):
						if agent['id'] in selected_agents:
							selected_agents.remove(agent['id'])
						else:
							selected_agents.add(agent['id'])
				# Seleção de mapas
				for idx, mapa in enumerate(mapas_db):
					rect = pygame.Rect(350, y_maps+idx*40, 200, 35)
					if rect.collidepoint(event.pos):
						selected_map = mapa['id']
				# Iniciar simulação
				if btn_sim.collidepoint(event.pos):
					if selected_map and selected_agents:
						running = False
						run_simulation(selected_map, list(selected_agents))
		pygame.display.flip()
		clock.tick(60)
