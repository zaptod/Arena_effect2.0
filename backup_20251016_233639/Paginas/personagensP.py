"""
Gerenciador de Personagens
Interface para criar, editar e excluir personagens
"""
import pygame
import sys
import os
import importlib

# Importa utilitários
from utils import (
    WIDTH, HEIGHT, FPS, COLOR_BG_LIGHT, COLOR_TEXT, COLOR_BUTTON,
    COLOR_DANGER, COLOR_SELECTED, draw_button, draw_back_button,
    draw_title, is_mouse_over, draw_info_box
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_personagens import personagens_db
from bases_de_dados.Banco_de_dados_comportamentais import comportamentos_db

def recarregar_personagens():
	"""Recarrega o banco de dados de personagens"""
	global personagens_db
	banco_mod = importlib.import_module('bases_de_dados.Banco_de_dados_personagens')
	importlib.reload(banco_mod)
	personagens_db = banco_mod.personagens_db

def show_personagens_carousel(screen, fonts):
	"""Exibe carrossel de personagens"""
	clock = pygame.time.Clock()
	carousel_start = 0
	running = True
	visible_count = 5
	
	while running:
		screen.fill((40,40,60))
		btn_novo = pygame.Rect(150, 30, 500, 50)
		pygame.draw.rect(screen, (70,130,180), btn_novo)
		txt = font.render('Criar Novo Personagem', True, (255,255,255))
		screen.blit(txt, (btn_novo.x+10, btn_novo.y+10))
		
		btn_voltar = pygame.Rect(20, 20, 100, 40)
		pygame.draw.rect(screen, (130,70,70), btn_voltar)
		screen.blit(font.render('Voltar', True, (255,255,255)), (btn_voltar.x+10, btn_voltar.y+5))
		
		btn_left = pygame.Rect(80, 180, 50, 50)
		btn_right = pygame.Rect(670, 180, 50, 50)
		pygame.draw.polygon(screen, (200,200,200), [(btn_left.x+40, btn_left.y+25), (btn_left.x+10, btn_left.y+10), (btn_left.x+10, btn_left.y+40)])
		pygame.draw.polygon(screen, (200,200,200), [(btn_right.x+10, btn_right.y+25), (btn_right.x+40, btn_right.y+10), (btn_right.x+40, btn_right.y+40)])
		
		end = min(len(personagens_db), carousel_start + visible_count)
		for idx, personagem in enumerate(personagens_db[carousel_start:end]):
			y = 100 + idx*90
			rect = pygame.Rect(150, y, 500, 80)
			color = (0,200,0) if personagem.get('ativo', True) else (200,0,0)
			pygame.draw.rect(screen, color, rect)
			txt = font.render(f"{personagem['nome']} (ID: {personagem['id']})", True, (255,255,255))
			screen.blit(txt, (rect.x+10, rect.y+10))
			
			btn_del = pygame.Rect(rect.x+420, rect.y+20, 60, 40)
			pygame.draw.rect(screen, (200,50,50), btn_del)
			screen.blit(font.render('Apagar', True, (255,255,255)), (btn_del.x+5, btn_del.y+5))
			
			if rect.collidepoint(pygame.mouse.get_pos()):
				pygame.draw.rect(screen, (255,255,0), rect, 3)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT and carousel_start + visible_count < len(personagens_db):
					carousel_start += 1
				elif event.key == pygame.K_LEFT and carousel_start > 0:
					carousel_start -= 1
				elif event.key == pygame.K_ESCAPE:
					running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_voltar.collidepoint(event.pos):
					running = False
				if btn_novo.collidepoint(event.pos):
					popup_criar_personagem(screen)
					recarregar_personagens()
				if btn_left.collidepoint(event.pos) and carousel_start > 0:
					carousel_start -= 1
				if btn_right.collidepoint(event.pos) and carousel_start + visible_count < len(personagens_db):
					carousel_start += 1
				
				for idx, personagem in enumerate(personagens_db[carousel_start:end]):
					y = 100 + idx*90
					rect = pygame.Rect(150, y, 500, 80)
					btn_del = pygame.Rect(rect.x+420, rect.y+20, 60, 40)
					
					if btn_del.collidepoint(event.pos):
						nome_arquivo = f"personagem{personagem['id']}.py"
						caminho = os.path.join(os.path.dirname(__file__), '..', 'personagens', nome_arquivo)
						
						if os.path.exists(caminho):
							try:
								os.remove(caminho)
								recarregar_personagens()
								if carousel_start > 0 and carousel_start + visible_count > len(personagens_db):
									carousel_start -= 1
							except Exception as e:
								txt = font.render(f"Erro ao apagar: {e}", True, (255,50,50))
								screen.blit(txt, (150, 80))
								pygame.display.flip()
								pygame.time.wait(1200)
						else:
							txt = font.render(f"Arquivo não encontrado!\n{caminho}", True, (255,50,50))
							screen.blit(txt, (150, 80))
							pygame.display.flip()
							pygame.time.wait(1800)
						break
					
					if rect.collidepoint(event.pos):
						from Paginas.PersonagemEdit import edit_personagem
						edit_personagem(personagem, screen)
						recarregar_personagens()
		
		pygame.display.flip()
		clock.tick(60)

def popup_criar_personagem(screen):
	font = pygame.font.SysFont(None, 28)
	popup = pygame.Surface((500, 500))
	attr_names = ['nome', 'tamanho', 'velocidade', 'massa', 'cor']
	attr_values = {'nome': '', 'tamanho': 20, 'velocidade': 3, 'massa': 5, 'cor': (0,255,0)}
	selected_attr = 0
	selected_comps = set()
	running_popup = True
	popup_x, popup_y = 150, 50
	
	while running_popup:
		popup.fill((60,60,80))
		popup.blit(font.render('Criar Novo Personagem', True, (255,255,255)), (140, 20))
		
		for i, attr in enumerate(attr_names):
			value = attr_values[attr]
			txt = font.render(f"{attr}: {value}", True, (255,255,255))
			y = 70 + i*40
			color = (255,255,0) if i == selected_attr else (255,255,255)
			popup.blit(txt, (50, y))
		
		popup.blit(font.render('Comportamentos:', True, (255,255,255)), (50, 300))
		for j, comp in enumerate(comportamentos_db):
			y = 340 + j*30
			sel = comp['id'] in selected_comps
			color = (0,200,0) if sel else (200,200,200)
			txt = font.render(f"{comp['nome']}", True, color)
			popup.blit(txt, (70, y))
		
		btn_confirm = pygame.Rect(popup_x+180, popup_y+450, 140, 30)
		pygame.draw.rect(screen, (70,130,180), btn_confirm)
		screen.blit(font.render('Salvar', True, (255,255,255)), (btn_confirm.x+20, btn_confirm.y+5))
		screen.blit(popup, (popup_x, popup_y))
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running_popup = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN and selected_attr < len(attr_names)-1:
					selected_attr += 1
				elif event.key == pygame.K_UP and selected_attr > 0:
					selected_attr -= 1
				elif event.key == pygame.K_RIGHT:
					attr = attr_names[selected_attr]
					if isinstance(attr_values[attr], int):
						attr_values[attr] += 1
				elif event.key == pygame.K_LEFT:
					attr = attr_names[selected_attr]
					if isinstance(attr_values[attr], int):
						attr_values[attr] -= 1
				elif event.key == pygame.K_ESCAPE:
					running_popup = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_confirm.collidepoint(event.pos):
					novo_id = max([p['id'] for p in personagens_db]+[0]) + 1
					nome_arquivo = f"personagem{novo_id}.py"
					caminho = os.path.join(os.path.dirname(__file__), '..', 'personagens', nome_arquivo)
					cor_valor = attr_values['cor']
					
					# Garante que cor seja sempre uma tupla de inteiros
					if isinstance(cor_valor, str):
						try:
							cor_valor = tuple(map(int, cor_valor.strip('()').split(',')))
						except Exception:
							cor_valor = (0, 255, 0)
					
					personagem_code = (
						"import pygame\n"
						"class Personagem:\n"
						"    def __init__(self, nome, id, tamanho, velocidade, massa, cor, comportamentos, x, y):\n"
						"        self.nome = nome\n"
						"        self.id = id\n"
						"        self.tamanho = tamanho\n"
						"        self.velocidade = velocidade\n"
						"        self.massa = massa\n"
						"        self.cor = cor\n"
						"        self.forca = velocidade * massa\n"
						"        self.comportamentos = comportamentos\n"
						"        self.x = x\n"
						"        self.y = y\n"
						"        self.vx = velocidade\n"
						"        self.vy = velocidade\n"
						"    def update(self):\n"
						"        self.x += self.vx\n"
						"        self.y += self.vy\n"
						"        if self.x < 0 or self.x > 800:\n"
						"            self.vx *= -1\n"
						"        if self.y < 0 or self.y > 600:\n"
						"            self.vy *= -1\n"
						"    def draw(self, screen):\n"
						"        pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.tamanho)\n"
						"    def check_collision(self, other):\n"
						"        dist = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5\n"
						"        return dist < self.tamanho + other.tamanho\n"
						"    def handle_collision(self, other):\n"
						"        self.vx *= -1\n"
						"        self.vy *= -1\n"
						"        other.vx *= -1\n"
						"        other.vy *= -1\n"
						"    def check_wall_collision(self):\n"
						"        if self.x - self.tamanho < 0 or self.x + self.tamanho > 800:\n"
						"            self.vx *= -1\n"
						"        if self.y - self.tamanho < 0 or self.y + self.tamanho > 600:\n"
						"            self.vy *= -1\n"
						"\ndef criar_personagem(personagem_id, x, y):\n"
						f"    return Personagem(\n        nome='{attr_values['nome']}',\n        id={novo_id},\n        tamanho={attr_values['tamanho']},\n        velocidade={attr_values['velocidade']},\n        massa={attr_values['massa']},\n        cor={cor_valor},\n        comportamentos={list(selected_comps)},\n        x=x,\n        y=y\n    )\n"
					)
					
					with open(caminho, 'w', encoding='utf-8') as f:
						f.write(personagem_code)
					
					running_popup = False
					importlib.invalidate_caches()
