
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_personagens import personagens_db
from bases_de_dados.Banco_de_dados_mapas import mapas_db
from bases_de_dados.Banco_de_dados_armas import armas_db

def show_selection_carousel(screen):
	font = pygame.font.SysFont(None, 28)
	clock = pygame.time.Clock()
	selected_personagens = set()
	selected_armas = set()
	selected_map = None
	running = True
	from Paginas.main_simulation import run_simulation
	
	while running:
		screen.fill((60,60,80))
		
		# Seção de personagens
		screen.blit(font.render('Selecione personagens:', True, (255,255,255)), (50, 30))
		y_personagens = 70
		for idx, personagem in enumerate([p for p in personagens_db if p['ativo']]):
			rect = pygame.Rect(50, y_personagens+idx*40, 200, 35)
			color = (0,200,0) if personagem['id'] in selected_personagens else (200,200,200)
			pygame.draw.rect(screen, color, rect)
			txt = font.render(personagem['nome'], True, (0,0,0))
			screen.blit(txt, (rect.x+10, rect.y+5))
		
		# Seção de armas
		screen.blit(font.render('Selecione armas:', True, (255,255,255)), (280, 30))
		y_armas = 70
		for idx, arma in enumerate(armas_db):
			rect = pygame.Rect(280, y_armas+idx*40, 200, 35)
			color = (200,100,0) if arma['id'] in selected_armas else (200,200,200)
			pygame.draw.rect(screen, color, rect)
			txt = font.render(arma['nome'], True, (0,0,0))
			screen.blit(txt, (rect.x+10, rect.y+5))
		
		# Seção de mapas
		screen.blit(font.render('Selecione mapa:', True, (255,255,255)), (510, 30))
		y_maps = 70
		for idx, mapa in enumerate(mapas_db):
			rect = pygame.Rect(510, y_maps+idx*40, 200, 35)
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
				# Seleção de personagens
				for idx, personagem in enumerate([p for p in personagens_db if p['ativo']]):
					rect = pygame.Rect(50, y_personagens+idx*40, 200, 35)
					if rect.collidepoint(event.pos):
						if personagem['id'] in selected_personagens:
							selected_personagens.remove(personagem['id'])
						else:
							selected_personagens.add(personagem['id'])
				
				# Seleção de armas
				for idx, arma in enumerate(armas_db):
					rect = pygame.Rect(280, y_armas+idx*40, 200, 35)
					if rect.collidepoint(event.pos):
						if arma['id'] in selected_armas:
							selected_armas.remove(arma['id'])
						else:
							selected_armas.add(arma['id'])
				
				# Seleção de mapas
				for idx, mapa in enumerate(mapas_db):
					rect = pygame.Rect(510, y_maps+idx*40, 200, 35)
					if rect.collidepoint(event.pos):
						selected_map = mapa['id']
				
				# Iniciar simulação
				if btn_sim.collidepoint(event.pos):
					if selected_map and selected_personagens:
						running = False
						run_simulation(selected_map, list(selected_personagens), list(selected_armas))
		
		pygame.display.flip()
		clock.tick(60)
