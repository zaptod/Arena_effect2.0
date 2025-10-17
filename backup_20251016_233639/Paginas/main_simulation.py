# Funções globais de movimentação, desenho e colisão com parede
def update_agent(agente, delta_time, width=800, height=600):
	# Usa delta time para manter velocidade consistente
	agente.x += agente.vx * delta_time
	agente.y += agente.vy * delta_time
	# Limites da tela
	if agente.x < 0 or agente.x > width:
		agente.vx *= -1
	if agente.y < 0 or agente.y > height:
		agente.vy *= -1

def draw_agent(agente, screen):
	pygame.draw.circle(screen, agente.cor, (int(agente.x), int(agente.y)), agente.tamanho)

def check_wall_collision(agente, width=800, height=600):
	if agente.x - agente.tamanho < 0 or agente.x + agente.tamanho > width:
		agente.vx *= -1
	if agente.y - agente.tamanho < 0 or agente.y + agente.tamanho > height:
		agente.vy *= -1

import pygame
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mapas.mapa0 import desenhar_mapa # Supondo função para desenhar paredes


def load_personagem_params(personagem_id):
	import importlib.util, os
	personagens_dir = os.path.join(os.path.dirname(__file__), '..', 'personagens')
	fname = f'personagem{personagem_id}.py'
	fpath = os.path.join(personagens_dir, fname)
	if not os.path.exists(fpath):
		raise FileNotFoundError(f'Arquivo do personagem não encontrado: {fpath}')
	spec = importlib.util.spec_from_file_location(f'personagem{personagem_id}', fpath)
	mod = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(mod)
	# Espera que o arquivo tenha a classe Personagem e a função criar_personagem
	return mod.criar_personagem

def load_arma(arma_id):
	"""Carrega uma arma pelo ID"""
	import importlib.util
	armas_dir = os.path.join(os.path.dirname(__file__), '..', 'armas')
	fname = f'arma{arma_id}.py'
	fpath = os.path.join(armas_dir, fname)
	if not os.path.exists(fpath):
		return None
	spec = importlib.util.spec_from_file_location(f'arma{arma_id}', fpath)
	mod = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(mod)
	return mod.criar_arma(arma_id)

# Funções globais de colisão e resposta
def check_collision(a1, a2):
	dist = ((a1.x - a2.x)**2 + (a1.y - a2.y)**2)**0.5
	return dist < a1.tamanho + a2.tamanho

def handle_collision(a1, a2):
	dx = a1.x - a2.x
	dy = a1.y - a2.y
	if abs(dx) > abs(dy):
		a1.vx *= -1
		a2.vx *= -1
	else:
		a1.vy *= -1
		a2.vy *= -1
	# Reposiciona para evitar sobreposição
	dist = (dx**2 + dy**2)**0.5
	min_dist = a1.tamanho + a2.tamanho
	if dist == 0:
		dx, dy = 1, 0
		dist = 1
	overlap = min_dist - dist
	if overlap > 0:
		# Move cada agente metade do overlap na direção oposta
		move_x = (dx / dist) * (overlap / 2)
		move_y = (dy / dist) * (overlap / 2)
		a1.x += move_x
		a1.y += move_y
		a2.x -= move_x
		a2.y -= move_y
		# Reforça separação se ainda estiverem sobrepostos
		if check_collision(a1, a2):
			extra = 1.0
			a1.x += move_x * extra
			a1.y += move_y * extra
			a2.x -= move_x * extra
			a2.y -= move_y * extra

def run_simulation(selected_map_id, selected_personagem_ids, selected_arma_ids=[]):
	pygame.init()
	WIDTH, HEIGHT = 800, 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	font = pygame.font.SysFont(None, 28)
	clock = pygame.time.Clock()
	# Inicializa mapa
	desenhar_mapa(screen)
	# Inicializa personagens
	personagens = []
	for idx, personagem_id in enumerate(selected_personagem_ids):
		x = random.randint(50, WIDTH-50)
		y = random.randint(50, HEIGHT-50)
		criar_personagem = load_personagem_params(personagem_id)
		personagem = criar_personagem(personagem_id, x, y)
		
		# Equipa arma se houver armas selecionadas
		if selected_arma_ids and idx < len(selected_arma_ids):
			arma_id = list(selected_arma_ids)[idx % len(selected_arma_ids)]
			personagem.arma = load_arma(arma_id)
		else:
			personagem.arma = None
		
		personagens.append(personagem)
	running = True
	while running:
		delta_time = clock.tick(120) / 16.67  # Normaliza para 60 FPS base
		dt_seconds = delta_time / 60.0  # Converte para segundos
		screen.fill((20,20,20))
		desenhar_mapa(screen)
		# Atualiza e desenha personagens
		for personagem in personagens:
			update_agent(personagem, delta_time, WIDTH, HEIGHT)
			
			# Atualiza arma se tiver
			if hasattr(personagem, 'arma') and personagem.arma:
				personagem.arma.update(dt_seconds)
			
			draw_agent(personagem, screen)
			
			# Desenha arma se tiver
			if hasattr(personagem, 'arma') and personagem.arma:
				# Encontra o personagem mais próximo como alvo
				target_x, target_y = None, None
				min_dist = float('inf')
				for outro in personagens:
					if outro is not personagem:
						dx = outro.x - personagem.x
						dy = outro.y - personagem.y
						dist = (dx*dx + dy*dy)**0.5
						if dist < min_dist:
							min_dist = dist
							target_x, target_y = outro.x, outro.y
				
				# Desenha arma apontando para o alvo mais próximo
				personagem.arma.draw(screen, personagem.x, personagem.y, target_x, target_y)
		# Interações personagem-personagem
		pares_processados = set()
		for i, p1 in enumerate(personagens):
			for j, p2 in enumerate(personagens[i+1:], start=i+1):
				par = tuple(sorted([id(p1), id(p2)]))
				if par in pares_processados:
					continue
				if check_collision(p1, p2):
					handle_collision(p1, p2)
					pares_processados.add(par)
		# Interações personagem-ambiente (exemplo: colisão com parede)
		for personagem in personagens:
			check_wall_collision(personagem, WIDTH, HEIGHT)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		pygame.display.flip()
