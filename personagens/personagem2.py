import pygame
class Personagem:
    def __init__(self, nome, id, tamanho, velocidade, massa, cor, comportamentos, x, y):
        self.nome = 'dadadada'
        self.id = id
        self.tamanho = 20
        self.velocidade = 3
        self.massa = 5
        self.cor = (0, 255, 0)
        self.forca = velocidade * massa
        self.comportamentos = comportamentos
        self.x = x
        self.y = y
        self.vx = velocidade
        self.vy = velocidade
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > 800:
            self.vx *= -1
        if self.y < 0 or self.y > 600:
            self.vy *= -1
    def draw(self, screen):
        pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.tamanho)
    def check_collision(self, other):
        dist = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        return dist < self.tamanho + other.tamanho
    def handle_collision(self, other):
        self.vx *= -1
        self.vy *= -1
        other.vx *= -1
        other.vy *= -1
    def check_wall_collision(self):
        if self.x - self.tamanho < 0 or self.x + self.tamanho > 800:
            self.vx *= -1
        if self.y - self.tamanho < 0 or self.y + self.tamanho > 600:
            self.vy *= -1

def criar_personagem(personagem_id, x, y):
    return Personagem(
        nome='',
        id=2,
        tamanho=20,
        velocidade=3,
        massa=5,
        cor=(0, 255, 0),
        comportamentos=[],
        x=x,
        y=y
    )
