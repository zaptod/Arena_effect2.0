"""
Visualizador de Rede Neural em Tempo Real
Mostra as entradas, camadas ocultas e saídas das redes neurais durante o treino
RENDERIZA EM UMA SURFACE QUE PODE SER BLITADA NA JANELA PRINCIPAL
"""
import pygame
import math
import numpy as np

class VisualizadorRede:
    """Visualiza a rede neural em tempo real"""
    
    def __init__(self, largura=400, altura=600):
        """Inicializa o visualizador"""
        self.largura = largura
        self.altura = altura
        self.surface = None  # Surface ao invés de screen
        self.font_titulo = None
        self.font_normal = None
        self.font_pequena = None
        
        # Cores
        self.COR_BG = (20, 20, 30)
        self.COR_NEURONIO_INATIVO = (60, 60, 80)
        self.COR_NEURONIO_ATIVO = (100, 200, 255)
        self.COR_CONEXAO = (50, 50, 70)
        self.COR_TEXTO = (200, 200, 200)
        self.COR_P1 = (100, 150, 255)  # Azul
        self.COR_P2 = (255, 100, 100)  # Vermelho
        
        # Labels das entradas (12 sensores)
        self.labels_entrada = [
            "Pos X",
            "Pos Y", 
            "Dir→Inimigo X",
            "Dir→Inimigo Y",
            "Dist Inimigo",
            "Vida Própria",
            "Vida Inimigo",
            "Tem Arma",
            "Dist Borda X",
            "Dist Borda Y",
            "Num Inimigos",
            "Força Relativa"
        ]
        
        # Labels das saídas (5 ações)
        self.labels_saida = [
            "Mov X",
            "Mov Y",
            "Atacar",
            "Fugir",
            "Ângulo Arma"
        ]
        
    def inicializar(self):
        """Cria a surface do visualizador"""
        # Cria surface ao invés de janela separada
        self.surface = pygame.Surface((self.largura, self.altura))
        
        # Fontes
        self.font_titulo = pygame.font.Font(None, 24)
        self.font_normal = pygame.font.Font(None, 18)
        self.font_pequena = pygame.font.Font(None, 14)
        
    def fechar(self):
        """Fecha o visualizador"""
        self.surface = None
    
    def desenhar_neuronio(self, x, y, raio, ativacao, cor_base):
        """Desenha um neurônio com intensidade baseada na ativação"""
        # Calcula cor baseada na ativação (0-1)
        intensidade = abs(ativacao)
        r = int(cor_base[0] + (255 - cor_base[0]) * intensidade)
        g = int(cor_base[1] + (255 - cor_base[1]) * intensidade)
        b = int(cor_base[2] + (255 - cor_base[2]) * intensidade)
        cor = (min(255, r), min(255, g), min(255, b))
        
        # Desenha círculo na surface
        pygame.draw.circle(self.surface, cor, (int(x), int(y)), raio)
        pygame.draw.circle(self.surface, (200, 200, 200), (int(x), int(y)), raio, 1)
    
    def desenhar_conexao(self, x1, y1, x2, y2, peso):
        """Desenha uma conexão entre neurônios"""
        # Espessura baseada no peso
        espessura = max(1, min(2, int(abs(peso) * 2)))
        
        # Cor baseada no sinal do peso
        if peso > 0:
            cor = (100, 200, 100)  # Verde para positivo
        else:
            cor = (200, 100, 100)  # Vermelho para negativo
        
        pygame.draw.line(self.surface, cor, (int(x1), int(y1)), (int(x2), int(y2)), espessura)
    
    def desenhar_rede(self, personagem, x_offset, y_offset, cor, titulo):
        """
        Desenha a rede neural de um personagem
        
        Args:
            personagem: Objeto do personagem com rede_neural
            x_offset: Offset horizontal
            y_offset: Offset vertical  
            cor: Cor do personagem
            titulo: Título da rede
        """
        if not hasattr(personagem, 'rede_neural') or personagem.rede_neural is None:
            # Sem rede neural
            texto = self.font_normal.render("Sem IA", True, (150, 150, 150))
            self.screen.blit(texto, (x_offset + 150, y_offset + 100))
            return
        
        rede = personagem.rede_neural
        
        # Título
        texto_titulo = self.font_titulo.render(titulo, True, cor)
        self.screen.blit(texto_titulo, (x_offset + 150, y_offset - 30))
        
        # Informações da rede
        info_text = self.font_pequena.render(
            f"Gen: {rede.geração} | Fitness: {int(rede.fitness)} | V:{rede.vitorias} D:{rede.derrotas}",
            True, (150, 150, 150)
        )
        self.screen.blit(info_text, (x_offset + 100, y_offset - 10))
        
        # Obtém valores das camadas (se houver estado recente)
        if not hasattr(rede, '_ultima_entrada'):
            return
        
        entrada = rede._ultima_entrada
        
        # Propaga para obter valores intermediários
        ativacoes = [entrada.reshape(1, -1)]
        
        for i in range(len(rede.pesos)):
            z = np.dot(ativacoes[-1], rede.pesos[i]) + rede.bias[i]
            if i < len(rede.pesos) - 1:
                ativacao = np.tanh(z)
            else:
                ativacao = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
            ativacoes.append(ativacao)
        
        # Layout da rede
        camadas = [12, 16, 8, 5]  # Entradas, oculta1, oculta2, saídas
        largura_camada = 100
        altura_neuronio = 25
        
        # Desenha cada camada
        posicoes_neuronios = []
        
        for idx_camada, num_neuronios in enumerate(camadas):
            x = x_offset + idx_camada * largura_camada
            posicoes_camada = []
            
            # Calcula espaçamento vertical
            altura_total = num_neuronios * altura_neuronio
            y_start = y_offset + (250 - altura_total) / 2
            
            for idx_neuronio in range(num_neuronios):
                y = y_start + idx_neuronio * altura_neuronio
                posicoes_camada.append((x, y))
                
                # Pega ativação do neurônio
                if idx_camada < len(ativacoes):
                    ativacao = ativacoes[idx_camada][0, idx_neuronio]
                else:
                    ativacao = 0
                
                # Desenha neurônio
                raio = 6 if idx_camada == 0 or idx_camada == len(camadas) - 1 else 5
                self.desenhar_neuronio(x, y, raio, ativacao, cor)
                
                # Labels para entrada e saída
                if idx_camada == 0:  # Entradas
                    label = self.font_pequena.render(
                        f"{self.labels_entrada[idx_neuronio]}: {ativacao:.2f}",
                        True, self.COR_TEXTO
                    )
                    self.screen.blit(label, (x - 100, y - 6))
                
                elif idx_camada == len(camadas) - 1:  # Saídas
                    label = self.font_pequena.render(
                        f"{self.labels_saida[idx_neuronio]}: {ativacao:.2f}",
                        True, self.COR_TEXTO
                    )
                    self.screen.blit(label, (x + 15, y - 6))
            
            posicoes_neuronios.append(posicoes_camada)
        
        # Desenha conexões (apenas algumas para não poluir)
        # Mostra apenas conexões mais fortes
        for idx_camada in range(len(camadas) - 1):
            pesos_camada = rede.pesos[idx_camada]
            
            # Limita número de conexões desenhadas
            max_conexoes = 20
            conexoes_desenhadas = 0
            
            for i, pos1 in enumerate(posicoes_neuronios[idx_camada]):
                for j, pos2 in enumerate(posicoes_neuronios[idx_camada + 1]):
                    if conexoes_desenhadas >= max_conexoes:
                        break
                    
                    peso = pesos_camada[i, j]
                    if abs(peso) > 0.5:  # Apenas pesos significativos
                        self.desenhar_conexao(pos1[0], pos1[1], pos2[0], pos2[1], peso)
                        conexoes_desenhadas += 1
                
                if conexoes_desenhadas >= max_conexoes:
                    break
    
    def atualizar(self, personagem1, personagem2, rodada_info=None):
        """
        Atualiza a visualização com os estados atuais das redes
        
        Args:
            personagem1: Primeiro personagem
            personagem2: Segundo personagem
            rodada_info: Dict com informações da rodada (opcional)
        """
        if not self.screen:
            self.inicializar()
        
        # Limpa tela
        self.screen.fill(self.COR_BG)
        
        # Título principal
        titulo = self.font_titulo.render("Visualização das Redes Neurais", True, (255, 255, 255))
        self.screen.blit(titulo, (self.largura // 2 - 150, 10))
        
        # Informações da rodada
        if rodada_info:
            info_lines = [
                f"Rodada: {rodada_info.get('rodada', '?')}",
                f"Tempo: {rodada_info.get('tempo', '?')}s",
                f"P1 HP: {rodada_info.get('p1_vida', '?')}",
                f"P2 HP: {rodada_info.get('p2_vida', '?')}"
            ]
            
            for i, line in enumerate(info_lines):
                texto = self.font_pequena.render(line, True, (200, 200, 200))
                self.screen.blit(texto, (10, 10 + i * 20))
        
        # Desenha legenda das cores
        legenda_y = self.altura - 60
        pygame.draw.circle(self.screen, self.COR_P1, (20, legenda_y), 8)
        texto = self.font_pequena.render("Player 1", True, self.COR_P1)
        self.screen.blit(texto, (35, legenda_y - 8))
        
        pygame.draw.circle(self.screen, self.COR_P2, (20, legenda_y + 25), 8)
        texto = self.font_pequena.render("Player 2", True, self.COR_P2)
        self.screen.blit(texto, (35, legenda_y + 17))
        
        # Linha divisória
        pygame.draw.line(self.screen, (80, 80, 80), 
                        (self.largura // 2, 50), 
                        (self.largura // 2, self.altura - 80), 2)
        
        # Desenha redes
        self.desenhar_rede(personagem1, 50, 100, self.COR_P1, "Player 1 - IA")
        self.desenhar_rede(personagem2, self.largura // 2 + 50, 100, self.COR_P2, "Player 2 - IA")
        
        # Atualiza display
        pygame.display.flip()
    
    def processar_eventos(self):
        """Processa eventos da janela do visualizador"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True


# Função auxiliar para usar no modo treino
def criar_visualizador():
    """Cria e retorna um visualizador de rede neural"""
    return VisualizadorRede()
