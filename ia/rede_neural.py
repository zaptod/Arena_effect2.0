"""
Rede Neural para Controle de Personagens
Sistema de IA usando redes neurais para decidir movimentos e ataques
"""
import numpy as np
import json
import os

class RedeNeuralPersonagem:
    """
    Rede Neural Feedforward para controlar um personagem
    
    Arquitetura:
    - Camada de entrada: Sensores do ambiente
    - Camadas ocultas: Processamento
    - Camada de saída: Ações (movimento + ataque)
    """
    
    def __init__(self, personagem_id, arma_id=None, camadas=[12, 16, 8, 5]):
        """
        Inicializa a rede neural
        
        Args:
            personagem_id: ID do personagem
            arma_id: ID da arma equipada (None = sem arma específica)
            camadas: Lista com número de neurônios em cada camada
                    [entrada, oculta1, oculta2, saída]
        """
        self.personagem_id = personagem_id
        self.arma_id = arma_id  # Nova propriedade para arma específica
        self.camadas = camadas
        
        # Inicializa pesos e bias aleatoriamente
        self.pesos = []
        self.bias = []
        
        for i in range(len(camadas) - 1):
            # Xavier initialization
            limite = np.sqrt(6 / (camadas[i] + camadas[i+1]))
            peso = np.random.uniform(-limite, limite, (camadas[i], camadas[i+1]))
            b = np.zeros((1, camadas[i+1]))
            
            self.pesos.append(peso)
            self.bias.append(b)
        
        # Estatísticas de treinamento
        self.fitness = 0
        self.geração = 0
        self.vitorias = 0
        self.derrotas = 0
        self.dano_causado = 0
        self.dano_recebido = 0
    
    def sigmoid(self, x):
        """Função de ativação sigmoid"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def tanh(self, x):
        """Função de ativação tanh"""
        return np.tanh(x)
    
    def relu(self, x):
        """Função de ativação ReLU"""
        return np.maximum(0, x)
    
    def forward(self, entrada):
        """
        Propagação para frente
        
        Args:
            entrada: Array numpy com valores dos sensores
        
        Returns:
            saida: Array com as ações a serem tomadas
        """
        ativacao = entrada.reshape(1, -1)
        
        # Armazena última entrada para visualização
        self._ultima_entrada = entrada
        
        # Passa por cada camada
        for i in range(len(self.pesos)):
            z = np.dot(ativacao, self.pesos[i]) + self.bias[i]
            
            # Usa tanh nas camadas ocultas e sigmoid na saída
            if i < len(self.pesos) - 1:
                ativacao = self.tanh(z)
            else:
                ativacao = self.sigmoid(z)
        
        return ativacao.flatten()
    
    def processar_sensores(self, personagem, outros_personagens, largura, altura):
        """
        Coleta informações do ambiente e converte em entrada para a rede
        
        Sensores (12 entradas):
        0-1: Posição normalizada (x, y)
        2-3: Direção para o inimigo mais próximo
        4: Distância para o inimigo mais próximo
        5: Vida própria normalizada
        6: Vida do inimigo mais próximo normalizada
        7: Tem arma equipada (0 ou 1)
        8-9: Distância para as bordas (x, y)
        10: Número de inimigos vivos
        11: Força relativa (própria / média dos outros)
        
        Args:
            personagem: Objeto do personagem
            outros_personagens: Lista de outros personagens
            largura: Largura do mapa
            altura: Altura do mapa
        
        Returns:
            Array numpy com 12 valores normalizados
        """
        sensores = np.zeros(12)
        
        # 0-1: Posição normalizada
        sensores[0] = personagem.x / largura
        sensores[1] = personagem.y / altura
        
        # Encontra inimigo mais próximo vivo
        inimigos_vivos = [p for p in outros_personagens 
                         if p.id != personagem.id and getattr(p, 'vivo', True)]
        
        if inimigos_vivos:
            distancias = []
            for inimigo in inimigos_vivos:
                dx = inimigo.x - personagem.x
                dy = inimigo.y - personagem.y
                dist = np.sqrt(dx**2 + dy**2)
                distancias.append((dist, inimigo, dx, dy))
            
            distancias.sort(key=lambda x: x[0])
            dist_min, inimigo_prox, dx, dy = distancias[0]
            
            # 2-3: Direção normalizada para o inimigo
            if dist_min > 0:
                sensores[2] = dx / dist_min  # Normalizado entre -1 e 1
                sensores[3] = dy / dist_min
            
            # 4: Distância normalizada
            dist_max = np.sqrt(largura**2 + altura**2)
            sensores[4] = dist_min / dist_max
            
            # 5: Vida própria normalizada
            if hasattr(personagem, 'vida_atual'):
                sensores[5] = personagem.vida_atual / personagem.vida_maxima
            else:
                sensores[5] = 1.0
            
            # 6: Vida do inimigo mais próximo
            if hasattr(inimigo_prox, 'vida_atual'):
                sensores[6] = inimigo_prox.vida_atual / inimigo_prox.vida_maxima
            else:
                sensores[6] = 1.0
            
            # 7: Tem arma
            sensores[7] = 1.0 if hasattr(personagem, 'arma') and personagem.arma else 0.0
            
            # 8-9: Distância para as bordas normalizadas
            sensores[8] = min(personagem.x, largura - personagem.x) / largura
            sensores[9] = min(personagem.y, altura - personagem.y) / altura
            
            # 10: Número de inimigos vivos normalizado
            sensores[10] = len(inimigos_vivos) / max(len(outros_personagens), 1)
            
            # 11: Força relativa
            forca_media = np.mean([p.forca for p in inimigos_vivos])
            sensores[11] = personagem.forca / max(forca_media, 1)
        else:
            # Sem inimigos, valores padrão
            sensores[5] = getattr(personagem, 'vida_atual', 100) / getattr(personagem, 'vida_maxima', 100)
            sensores[7] = 1.0 if hasattr(personagem, 'arma') and personagem.arma else 0.0
            sensores[8] = min(personagem.x, largura - personagem.x) / largura
            sensores[9] = min(personagem.y, altura - personagem.y) / altura
        
        return sensores
    
    def decidir_acao(self, personagem, outros_personagens, largura=800, altura=600):
        """
        Decide a ação do personagem baseado nos sensores
        
        Saídas (5 neurônios):
        0: Movimento X (-1 a 1)
        1: Movimento Y (-1 a 1)
        2: Atacar (>0.5 = sim)
        3: Fugir (>0.5 = sim, inverte movimento)
        4: Ângulo da arma (0 a 2π radianos)
        
        Args:
            personagem: Objeto do personagem
            outros_personagens: Lista de outros personagens
            largura: Largura do mapa
            altura: Altura do mapa
        
        Returns:
            dict com 'mover_x', 'mover_y', 'atacar', 'fugir', 'angulo_arma'
        """
        # Coleta sensores
        sensores = self.processar_sensores(personagem, outros_personagens, largura, altura)
        
        # Processa na rede neural
        saida = self.forward(sensores)
        
        # Converte saída (0-1) para ações
        # Movimento: converte de (0-1) para (-1 a 1)
        mover_x = (saida[0] - 0.5) * 2
        mover_y = (saida[1] - 0.5) * 2
        
        # Se fugir está ativo, inverte movimento
        fugir = saida[3] > 0.5
        if fugir:
            mover_x = -mover_x
            mover_y = -mover_y
        
        # Ângulo da arma: converte de (0-1) para (0 a 2π)
        angulo_arma = saida[4] * 2 * np.pi
        
        return {
            'mover_x': mover_x,
            'mover_y': mover_y,
            'atacar': saida[2] > 0.5,
            'fugir': fugir,
            'angulo_arma': angulo_arma
        }
    
    def calcular_fitness(self):
        """
        Calcula fitness da rede neural baseado no desempenho
        
        Fitness = pontos positivos - pontos negativos
        
        Pontos positivos:
        - Vitórias: +1000
        - Dano causado: +1 por ponto
        - Sobrevivência: +(vida_restante * 2)
        
        Pontos negativos:
        - Derrotas: -500
        - Dano recebido: -0.5 por ponto
        """
        fitness = 0
        
        # Vitórias e derrotas
        fitness += self.vitorias * 1000
        fitness -= self.derrotas * 500
        
        # Dano
        fitness += self.dano_causado
        fitness -= self.dano_recebido * 0.5
        
        self.fitness = fitness
        return fitness
    
    def mutar(self, taxa_mutacao=0.1, intensidade=0.3):
        """
        Aplica mutação nos pesos e bias
        
        Args:
            taxa_mutacao: Probabilidade de cada peso sofrer mutação
            intensidade: Quanto o peso pode mudar (-intensidade a +intensidade)
        """
        for i in range(len(self.pesos)):
            # Mutação nos pesos
            mascara = np.random.random(self.pesos[i].shape) < taxa_mutacao
            mutacao = np.random.uniform(-intensidade, intensidade, self.pesos[i].shape)
            self.pesos[i] += mascara * mutacao
            
            # Mutação no bias
            mascara_bias = np.random.random(self.bias[i].shape) < taxa_mutacao
            mutacao_bias = np.random.uniform(-intensidade, intensidade, self.bias[i].shape)
            self.bias[i] += mascara_bias * mutacao_bias
    
    def crossover(self, outra_rede):
        """
        Cria uma nova rede combinando com outra (reprodução)
        
        Args:
            outra_rede: Outra RedeNeuralPersonagem
        
        Returns:
            Nova RedeNeuralPersonagem com genes combinados
        """
        nova_rede = RedeNeuralPersonagem(self.personagem_id, self.arma_id, self.camadas)
        
        for i in range(len(self.pesos)):
            # Crossover de ponto único para cada camada
            ponto_corte = np.random.randint(0, self.pesos[i].size)
            
            pesos_flat1 = self.pesos[i].flatten()
            pesos_flat2 = outra_rede.pesos[i].flatten()
            
            novo_peso_flat = np.concatenate([
                pesos_flat1[:ponto_corte],
                pesos_flat2[ponto_corte:]
            ])
            
            nova_rede.pesos[i] = novo_peso_flat.reshape(self.pesos[i].shape)
            
            # Mesmo para bias
            bias_flat1 = self.bias[i].flatten()
            bias_flat2 = outra_rede.bias[i].flatten()
            ponto_corte_bias = np.random.randint(0, len(bias_flat1))
            
            novo_bias_flat = np.concatenate([
                bias_flat1[:ponto_corte_bias],
                bias_flat2[ponto_corte_bias:]
            ])
            
            nova_rede.bias[i] = novo_bias_flat.reshape(self.bias[i].shape)
        
        return nova_rede
    
    def salvar(self, caminho=None):
        """Salva a rede neural em arquivo JSON"""
        if caminho is None:
            # Nome do arquivo inclui arma se especificada
            if self.arma_id is not None:
                caminho = f"redes_neurais/rede_personagem_{self.personagem_id}_arma_{self.arma_id}.json"
            else:
                caminho = f"redes_neurais/rede_personagem_{self.personagem_id}.json"
        
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        
        dados = {
            'personagem_id': self.personagem_id,
            'arma_id': self.arma_id,  # Salva ID da arma
            'camadas': self.camadas,
            'pesos': [p.tolist() for p in self.pesos],
            'bias': [b.tolist() for b in self.bias],
            'fitness': self.fitness,
            'geração': self.geração,
            'vitorias': self.vitorias,
            'derrotas': self.derrotas,
            'dano_causado': self.dano_causado,
            'dano_recebido': self.dano_recebido
        }
        
        with open(caminho, 'w') as f:
            json.dump(dados, f, indent=2)
    
    @staticmethod
    def carregar(caminho):
        """Carrega uma rede neural de arquivo JSON"""
        with open(caminho, 'r') as f:
            dados = json.load(f)
        
        # Carrega com arma_id se disponível
        arma_id = dados.get('arma_id', None)
        rede = RedeNeuralPersonagem(dados['personagem_id'], arma_id, dados['camadas'])
        rede.pesos = [np.array(p) for p in dados['pesos']]
        rede.bias = [np.array(b) for b in dados['bias']]
        rede.fitness = dados.get('fitness', 0)
        rede.geração = dados.get('geração', 0)
        rede.vitorias = dados.get('vitorias', 0)
        rede.derrotas = dados.get('derrotas', 0)
        rede.dano_causado = dados.get('dano_causado', 0)
        rede.dano_recebido = dados.get('dano_recebido', 0)
        
        return rede
    
    def clonar(self):
        """Cria uma cópia exata da rede"""
        nova_rede = RedeNeuralPersonagem(self.personagem_id, self.arma_id, self.camadas)
        nova_rede.pesos = [p.copy() for p in self.pesos]
        nova_rede.bias = [b.copy() for b in self.bias]
        nova_rede.fitness = self.fitness
        nova_rede.geração = self.geração
        nova_rede.arma_id = self.arma_id
        return nova_rede
