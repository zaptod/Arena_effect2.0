import pygame

class Personagem:
    def __init__(self, nome, id, tamanho, velocidade, massa, cor, comportamentos, x, y):
        self.nome = 'gerald'
        self.id = id
        self.tamanho = 30
        self.velocidade = 2
        self.massa = 30
        self.cor = (0, 255, 0)
        self.forca = velocidade * massa
        self.comportamentos = comportamentos
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.vida_maxima = 100
        self.vida_atual = 100
        self.vivo = True
    
    def receber_dano(self, dano):
        if self.vivo:
            self.vida_atual -= dano
            if self.vida_atual <= 0:
                self.vida_atual = 0
                self.vivo = False
        return self.vivo
    
    def curar(self, quantidade):
        if self.vivo:
            self.vida_atual = min(self.vida_atual + quantidade, self.vida_maxima)
    
    def update(self):
        pass
    
    def draw(self, screen):
        if self.vivo:
            pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.tamanho)
    
    def check_collision(self, other):
        dist = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        return dist < self.tamanho + other.tamanho
    
    def handle_collision(self, other):
        pass
    
    def check_wall_collision(self):
        pass

def criar_personagem(personagem_id, x, y):
    return Personagem(
        nome='gerald',
        id=1,
        tamanho=20,
        velocidade=3,
        massa=5,
        cor=(0, 255, 0),
        comportamentos=[1, 2, 3],
        x=x,
        y=y
    )
