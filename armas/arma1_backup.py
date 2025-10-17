import pygame
import math

class Arma:
    def __init__(self, nome, id, dano, alcance, velocidade_ataque, sprite_path=None):
        self.nome = nome
        self.id = id
        self.dano = dano
        self.alcance = alcance
        self.velocidade_ataque = velocidade_ataque
        self.cooldown = 0
        self.angulo = 0
        self.sprite_path = sprite_path
        self.sprite = None
        
        # Atributos para ricochete
        self.ricochete_ativo = False
        self.tempo_ricochete = 0.0
        self.duracao_ricochete = 0.3  # 300ms de ricochete
        self.angulo_ricochete = 0.0
        
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                # Ajusta tamanho do sprite baseado no alcance
                tamanho = int(alcance * 20)
                self.sprite = pygame.transform.scale(self.sprite, (tamanho, tamanho))
            except:
                pass
    
    def update(self, dt):
        """Atualiza o cooldown da arma e efeito de ricochete"""
        if self.cooldown > 0:
            self.cooldown -= dt
        
        # Atualiza ricochete
        if self.ricochete_ativo:
            self.tempo_ricochete += dt
            if self.tempo_ricochete >= self.duracao_ricochete:
                self.ricochete_ativo = False
                self.tempo_ricochete = 0.0
    
    def pode_atacar(self):
        """Verifica se a arma pode atacar (cooldown zerado)"""
        return self.cooldown <= 0
    
    def atacar(self):
        """Realiza um ataque e inicia o cooldown"""
        if self.pode_atacar():
            self.cooldown = 1.0 / self.velocidade_ataque
            return True
        return False
    
    def draw(self, screen, personagem_x, personagem_y, target_x=None, target_y=None):
        """Desenha a arma próxima ao personagem"""
        # Calcula ângulo baseado no alvo ou na direção do movimento
        if target_x is not None and target_y is not None:
            dx = target_x - personagem_x
            dy = target_y - personagem_y
            self.angulo = math.atan2(dy, dx)
        
        # Aplica offset de ricochete se ativo
        angulo_final = self.angulo
        if self.ricochete_ativo:
            # Oscilação decrescente durante ricochete
            progresso = self.tempo_ricochete / self.duracao_ricochete
            intensidade = (1.0 - progresso) * 0.4  # Ângulo máximo de ricochete
            angulo_final += math.sin(progresso * math.pi * 4) * intensidade
        
        # Posição da arma ao lado do personagem
        offset_x = math.cos(angulo_final) * 25
        offset_y = math.sin(angulo_final) * 25
        arma_x = personagem_x + offset_x
        arma_y = personagem_y + offset_y
        
        if self.sprite:
            # Rotaciona o sprite
            rotated_sprite = pygame.transform.rotate(self.sprite, -math.degrees(angulo_final))
            rect = rotated_sprite.get_rect(center=(int(arma_x), int(arma_y)))
            screen.blit(rotated_sprite, rect)
        else:
            # Desenha uma representação simples se não houver sprite
            # Espada: linha com cabo
            end_x = arma_x + math.cos(angulo_final) * self.alcance * 20
            end_y = arma_y + math.sin(angulo_final) * self.alcance * 20
            
            # Cor da lâmina muda durante ricochete
            cor_lamina = (255, 200, 100) if self.ricochete_ativo else (200, 200, 200)
            
            # Lâmina
            pygame.draw.line(screen, cor_lamina, (int(arma_x), int(arma_y)), 
                           (int(end_x), int(end_y)), 3)
            
            # Cabo
            cabo_x = arma_x - math.cos(angulo_final) * 10
            cabo_y = arma_y - math.sin(angulo_final) * 10
            pygame.draw.line(screen, (139, 69, 19), (int(arma_x), int(arma_y)), 
                           (int(cabo_x), int(cabo_y)), 5)
            
            # Guarda
            guard_dx = math.cos(angulo_final + math.pi/2) * 8
            guard_dy = math.sin(angulo_final + math.pi/2) * 8
            pygame.draw.line(screen, (192, 192, 192), 
                           (int(arma_x - guard_dx), int(arma_y - guard_dy)),
                           (int(arma_x + guard_dx), int(arma_y + guard_dy)), 3)
        
        # Efeito visual de ricochete (faíscas)
        if self.ricochete_ativo and self.tempo_ricochete < 0.15:
            # Faíscas na ponta da arma
            ponta_x = arma_x + math.cos(angulo_final) * self.alcance * 20
            ponta_y = arma_y + math.sin(angulo_final) * self.alcance * 20
            for i in range(3):
                angulo_faisca = angulo_final + (i - 1) * 0.5
                comprimento = 10 - (self.tempo_ricochete / 0.15) * 10
                fx = ponta_x + math.cos(angulo_faisca) * comprimento
                fy = ponta_y + math.sin(angulo_faisca) * comprimento
                pygame.draw.line(screen, (255, 255, 100), 
                               (int(ponta_x), int(ponta_y)), (int(fx), int(fy)), 2)
    
    def draw_icon(self, screen, x, y, size=50):
        """Desenha um ícone da arma para interface"""
        if self.sprite:
            icon = pygame.transform.scale(self.sprite, (size, size))
            screen.blit(icon, (x - size//2, y - size//2))
        else:
            # Desenha ícone simplificado
            # Círculo de fundo
            pygame.draw.circle(screen, (100, 100, 100), (x, y), size//2)
            pygame.draw.circle(screen, (200, 200, 200), (x, y), size//2, 2)
            
            # Desenha espada simplificada
            blade_length = size * 0.3
            pygame.draw.line(screen, (200, 200, 200), 
                           (x, y - blade_length), (x, y + blade_length//2), 3)
            pygame.draw.line(screen, (139, 69, 19), 
                           (x, y + blade_length//2), (x, y + size//3), 4)
            pygame.draw.line(screen, (192, 192, 192), 
                           (x - 8, y + blade_length//2 - 5), 
                           (x + 8, y + blade_length//2 - 5), 3)
        
        # Desenha stats
        font = pygame.font.SysFont(None, 16)
        dano_text = font.render(f"{int(self.dano)}", True, (255, 255, 255))
        screen.blit(dano_text, (x - 8, y - 5))
    
    def verificar_hit(self, personagem_x, personagem_y, alvo_x, alvo_y, alvo_tamanho):
        """Verifica se o ataque acertou o alvo - colisão na PONTA da arma"""
        # Calcula a posição da PONTA da arma
        ponta_x = personagem_x + math.cos(self.angulo) * (25 + self.alcance * 20)
        ponta_y = personagem_y + math.sin(self.angulo) * (25 + self.alcance * 20)
        
        # Calcula distância da PONTA da arma até o alvo
        dx = alvo_x - ponta_x
        dy = alvo_y - ponta_y
        distancia = math.sqrt(dx*dx + dy*dy)
        
        # Verifica se a ponta da arma está tocando o alvo
        return distancia <= alvo_tamanho
    
    def get_linha_arma(self, personagem_x, personagem_y):
        """Retorna início e fim da linha da arma para colisão"""
        # Posição inicial (perto do personagem)
        inicio_x = personagem_x + math.cos(self.angulo) * 25
        inicio_y = personagem_y + math.sin(self.angulo) * 25
        
        # Posição final (ponta da arma)
        fim_x = personagem_x + math.cos(self.angulo) * (25 + self.alcance * 20)
        fim_y = personagem_y + math.sin(self.angulo) * (25 + self.alcance * 20)
        
        return (inicio_x, inicio_y, fim_x, fim_y)
    
    def aplicar_ricochete(self, angulo_colisao):
        """Aplica efeito de ricochete à arma"""
        self.ricochete_ativo = True
        self.tempo_ricochete = 0.0
        self.angulo_ricochete = angulo_colisao
        # O ângulo da arma será temporariamente afetado pelo ricochete

def criar_arma(arma_id):
    """Cria uma instância da Espada Curta"""
    return Arma(
        nome='Espada Curta',
        id=1,
        dano=10,
        alcance=1.5,
        velocidade_ataque=1.0
    )
