import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_mapas import mapas_db

def show_mapas_carousel(screen):
	font = pygame.font.SysFont(None, 28)
	clock = pygame.time.Clock()
	carousel_start = 0
	running = True
	visible_count = 5
	
	while running:
		screen.fill((40,40,60))
		
		# Botão voltar
		btn_voltar = pygame.Rect(20, 20, 100, 40)
		pygame.draw.rect(screen, (130,70,70), btn_voltar)
		screen.blit(font.render('Voltar', True, (255,255,255)), (btn_voltar.x+10, btn_voltar.y+5))
		
		# Título
		screen.blit(font.render('Mapas Disponíveis', True, (255,255,255)), (250, 30))
		
		# Botões de navegação
		btn_left = pygame.Rect(80, 180, 50, 50)
		btn_right = pygame.Rect(670, 180, 50, 50)
		pygame.draw.polygon(screen, (200,200,200), [(btn_left.x+40, btn_left.y+25), (btn_left.x+10, btn_left.y+10), (btn_left.x+10, btn_left.y+40)])
		pygame.draw.polygon(screen, (200,200,200), [(btn_right.x+10, btn_right.y+25), (btn_right.x+40, btn_right.y+10), (btn_right.x+40, btn_right.y+40)])
		
		# Lista de mapas
		end = min(len(mapas_db), carousel_start + visible_count)
		for idx, mapa in enumerate(mapas_db[carousel_start:end]):
			y = 100 + idx*90
			rect = pygame.Rect(150, y, 500, 80)
			pygame.draw.rect(screen, (0,130,130), rect)
			
			txt = font.render(f"{mapa['nome']} (ID: {mapa['id']})", True, (255,255,255))
			screen.blit(txt, (rect.x+10, rect.y+10))
			
			txt_arquivo = font.render(f"Arquivo: {mapa['arquivo']}", True, (200,200,200))
			screen.blit(txt_arquivo, (rect.x+10, rect.y+40))
			
			if rect.collidepoint(pygame.mouse.get_pos()):
				pygame.draw.rect(screen, (255,255,0), rect, 3)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT and carousel_start + visible_count < len(mapas_db):
					carousel_start += 1
				elif event.key == pygame.K_LEFT and carousel_start > 0:
					carousel_start -= 1
				elif event.key == pygame.K_ESCAPE:
					running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_voltar.collidepoint(event.pos):
					running = False
				if btn_left.collidepoint(event.pos) and carousel_start > 0:
					carousel_start -= 1
				if btn_right.collidepoint(event.pos) and carousel_start + visible_count < len(mapas_db):
					carousel_start += 1
					
		pygame.display.flip()
		clock.tick(60)
