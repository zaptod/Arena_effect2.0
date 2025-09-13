
import pygame

class Agente:
	def __init__(self, nome, id, tamanho, velocidade, massa, cor, comportamentos, x, y):
		self.nome = nome
		self.id = id
		self.tamanho = tamanho
		self.velocidade = velocidade
		self.massa = massa
		self.cor = cor
		self.forca = velocidade * massa
		self.comportamentos = comportamentos
		self.x = x
		self.y = y
		self.vx = velocidade
		self.vy = velocidade


def criar_agente(agent_id, x, y):
	# Nome é passado diretamente na chamada abaixo
	return Agente(
		nome='agent',  # <-- Este valor será alterado pelo patch de edição
		id=agent_id,
		tamanho=20,
		velocidade=3,
		massa=5,
		cor=(0,255,0),
		comportamentos=[],
		x=x,
		y=y
	)