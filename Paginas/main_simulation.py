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

from agentes.agente0 import criar_agente # Supondo função para criar agente

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

def run_simulation(selected_map_id, selected_agent_ids):
	pygame.init()
	WIDTH, HEIGHT = 800, 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	font = pygame.font.SysFont(None, 28)
	clock = pygame.time.Clock()
	# Inicializa mapa
	desenhar_mapa(screen)
	# Inicializa agentes
	agentes = []
	for agent_id in selected_agent_ids:
		x = random.randint(50, WIDTH-50)
		y = random.randint(50, HEIGHT-50)
		agente = criar_agente(agent_id, x, y)
		agentes.append(agente)
	running = True
	while running:
		delta_time = clock.tick(120) / 16.67  # Normaliza para 60 FPS base
		screen.fill((20,20,20))
		desenhar_mapa(screen)
		# Atualiza e desenha agentes
		for agente in agentes:
			update_agent(agente, delta_time, WIDTH, HEIGHT)
			draw_agent(agente, screen)
		# Interações agente-agente
		pares_processados = set()
		for i, a1 in enumerate(agentes):
			for j, a2 in enumerate(agentes[i+1:], start=i+1):
				par = tuple(sorted([id(a1), id(a2)]))
				if par in pares_processados:
					continue
				if check_collision(a1, a2):
					handle_collision(a1, a2)
					pares_processados.add(par)
		# Interações agente-ambiente (exemplo: colisão com parede)
		for agente in agentes:
			check_wall_collision(agente, WIDTH, HEIGHT)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		pygame.display.flip()
