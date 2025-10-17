"""
Visualizador Compacto de Rede Neural
Renderiza em uma surface que pode ser exibida ao lado da arena principal
"""
import pygame
import numpy as np
import math

class VisualizadorRedeCompacto:
    """Visualizador compacto de rede neural para exibir ao lado da arena"""
    
    def __init__(self, largura=450, altura=600):
        self.largura = largura
        self.altura = altura
        self.surface = None
        
        # Cores
        self.COR_BG = (15, 15, 25)
        self.COR_P1 = (80, 120, 255)
        self.COR_P2 = (255, 80, 80)
        self.COR_TEXTO = (200, 200, 200)
        
        # Labels
        self.labels_entrada = ["PosX", "PosY", "Dir→X", "Dir→Y", "Dist", 
                              "HP", "HP_Ini", "Arma", "BordaX", "BordaY", "Nini", "Força"]
        self.labels_saida = ["MovX", "MovY", "Atk", "Fug", "Ângulo"]
        
    def inicializar(self):
        """Cria a surface"""
        self.surface = pygame.Surface((self.largura, self.altura))
        pygame.font.init()
        
    def desenhar_rede_compacta(self, personagem, y_offset, cor, titulo):
        """Desenha versão compacta da rede neural"""
        if not hasattr(personagem, 'rede_neural') or personagem.rede_neural is None:
            font = pygame.font.Font(None, 20)
            texto = font.render("Sem IA", True, (150, 150, 150))
            self.surface.blit(texto, (self.largura // 2 - 30, y_offset + 80))
            return
        
        rede = personagem.rede_neural
        
        # Título
        font_titulo = pygame.font.Font(None, 24)
        texto_titulo = font_titulo.render(titulo, True, cor)
        self.surface.blit(texto_titulo, (15, y_offset))
        
        # Info compacta
        font_pequena = pygame.font.Font(None, 15)
        info = font_pequena.render(
            f"Gen:{rede.geração} Fit:{int(rede.fitness)} V:{rede.vitorias} D:{rede.derrotas}",
            True, (150, 150, 150)
        )
        self.surface.blit(info, (15, y_offset + 22))
        
        # Obtém valores se houver
        if not hasattr(rede, '_ultima_entrada'):
            return
        
        entrada = rede._ultima_entrada
        
        # Propaga para obter saídas
        ativacoes = [entrada.reshape(1, -1)]
        for i in range(len(rede.pesos)):
            z = np.dot(ativacoes[-1], rede.pesos[i]) + rede.bias[i]
            if i < len(rede.pesos) - 1:
                ativacao = np.tanh(z)
            else:
                ativacao = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
            ativacoes.append(ativacao)
        
        entradas_vals = ativacoes[0][0]
        saidas_vals = ativacoes[-1][0]
        
        # Desenha entradas (12) - em coluna com mais espaço
        y_start = y_offset + 48
        font_val = pygame.font.Font(None, 17)
        
        # Título entradas
        font_titulo_secao = pygame.font.Font(None, 19)
        titulo_entradas = font_titulo_secao.render("📊 SENSORES:", True, (150, 200, 255))
        self.surface.blit(titulo_entradas, (15, y_start - 5))
        y_start += 20
        
        for i in range(12):
            val = entradas_vals[i]
            label = self.labels_entrada[i]
            
            # Barra de intensidade (mais larga)
            barra_w = int(abs(val) * 120)
            barra_cor = (int(cor[0] * abs(val)), int(cor[1] * abs(val)), int(cor[2] * abs(val)))
            pygame.draw.rect(self.surface, barra_cor, (15, y_start + i*15 + 2, barra_w, 10))
            pygame.draw.rect(self.surface, (50, 50, 50), (15, y_start + i*15 + 2, 120, 10), 1)
            
            # Texto com mais espaço
            texto = font_val.render(f"{label}: {val:.2f}", True, self.COR_TEXTO)
            self.surface.blit(texto, (145, y_start + i*15))
        
        # Desenha saídas (5) com mais espaço
        y_saidas = y_start + 12*15 + 15
        font_saida_titulo = pygame.font.Font(None, 19)
        texto_saida_titulo = font_saida_titulo.render("⚡ AÇÕES:", True, (255, 255, 100))
        self.surface.blit(texto_saida_titulo, (15, y_saidas))
        
        y_saidas += 25
        font_saida_val = pygame.font.Font(None, 18)
        for i in range(5):
            val = saidas_vals[i]
            label = self.labels_saida[i]
            
            # Barra maior
            barra_w = int(val * 180)
            barra_cor = (int(100 + val * 155), int(200 * val), int(100))
            pygame.draw.rect(self.surface, barra_cor, (15, y_saidas + i*20 + 2, barra_w, 14))
            pygame.draw.rect(self.surface, (50, 50, 50), (15, y_saidas + i*20 + 2, 180, 14), 1)
            
            # Texto com destaque se ativo
            cor_texto = (255, 255, 100) if val > 0.5 else self.COR_TEXTO
            texto = font_saida_val.render(f"{label}: {val:.2f}", True, cor_texto)
            self.surface.blit(texto, (205, y_saidas + i*20))
        
    def renderizar(self, personagem1, personagem2, rodada_info=None):
        """
        Renderiza a visualização e retorna a surface
        
        Returns:
            pygame.Surface com a visualização
        """
        if self.surface is None:
            self.inicializar()
        
        # Limpa
        self.surface.fill(self.COR_BG)
        
        # Borda
        pygame.draw.rect(self.surface, (80, 80, 100), (0, 0, self.largura, self.altura), 3)
        
        # Título
        font_titulo = pygame.font.Font(None, 26)
        titulo = font_titulo.render("🧠 REDES NEURAIS", True, (255, 255, 255))
        self.surface.blit(titulo, (self.largura // 2 - 100, 8))
        
        # Info da rodada
        if rodada_info:
            font_info = pygame.font.Font(None, 17)
            info_text = f"Rodada: {rodada_info.get('rodada','?')} | Tempo: {rodada_info.get('tempo','?')}s"
            texto_info = font_info.render(info_text, True, (180, 180, 180))
            self.surface.blit(texto_info, (15, 33))
            
            # HP dos jogadores
            hp_text = f"P1 HP: {rodada_info.get('p1_vida','?')} | P2 HP: {rodada_info.get('p2_vida','?')}"
            texto_hp = font_info.render(hp_text, True, (255, 200, 100))
            self.surface.blit(texto_hp, (15, 50))
        
        # Linha divisória horizontal mais grossa
        pygame.draw.line(self.surface, (100, 100, 120), (10, self.altura // 2 - 5), 
                        (self.largura - 10, self.altura // 2 - 5), 3)
        
        # Player 1 (cima) - ajusta y_offset para não sobrepor
        self.desenhar_rede_compacta(personagem1, 70, self.COR_P1, "🔵 PLAYER 1")
        
        # Player 2 (baixo) - ajusta y_offset
        self.desenhar_rede_compacta(personagem2, self.altura // 2 + 5, self.COR_P2, "🔴 PLAYER 2")
        
        return self.surface


def criar_visualizador():
    """Cria e retorna um visualizador compacto"""
    return VisualizadorRedeCompacto()
