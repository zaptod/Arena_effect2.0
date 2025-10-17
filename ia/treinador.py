"""
Sistema de Treinamento por Algoritmo Genético
Evolui as redes neurais através de gerações
"""
import numpy as np
import os
import json
from .rede_neural import RedeNeuralPersonagem

class TreinadorGenetico:
    """
    Treina redes neurais usando algoritmo genético
    
    Processo:
    1. Cria população inicial
    2. Avalia fitness (através de combates)
    3. Seleciona os melhores
    4. Crossover e mutação
    5. Nova geração
    """
    
    def __init__(self, tamanho_populacao=20, taxa_mutacao=0.15, taxa_elite=0.2):
        """
        Args:
            tamanho_populacao: Número de redes na população
            taxa_mutacao: Probabilidade de mutação
            taxa_elite: Porcentagem dos melhores que passam direto
        """
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_elite = taxa_elite
        self.populacao = []
        self.geracao_atual = 0
        self.historico = []
        
    def criar_populacao_inicial(self, personagem_id, camadas=[12, 16, 8, 4]):
        """Cria população inicial com redes aleatórias"""
        self.populacao = []
        for i in range(self.tamanho_populacao):
            rede = RedeNeuralPersonagem(personagem_id, camadas)
            rede.geração = 0
            self.populacao.append(rede)
        print(f"✅ População inicial criada: {self.tamanho_populacao} redes")
    
    def avaliar_populacao(self, resultados_combates):
        """
        Avalia o fitness de cada rede baseado nos resultados
        
        Args:
            resultados_combates: Lista de dicionários com resultados
                [{'rede_id': int, 'venceu': bool, 'dano_causado': float, 
                  'dano_recebido': float, 'vida_restante': float}, ...]
        """
        for resultado in resultados_combates:
            rede_id = resultado['rede_id']
            if rede_id < len(self.populacao):
                rede = self.populacao[rede_id]
                
                if resultado['venceu']:
                    rede.vitorias += 1
                else:
                    rede.derrotas += 1
                
                rede.dano_causado += resultado.get('dano_causado', 0)
                rede.dano_recebido += resultado.get('dano_recebido', 0)
                
                rede.calcular_fitness()
        
        # Ordena por fitness
        self.populacao.sort(key=lambda r: r.fitness, reverse=True)
        
        # Salva estatísticas
        melhor_fitness = self.populacao[0].fitness
        fitness_medio = np.mean([r.fitness for r in self.populacao])
        
        self.historico.append({
            'geracao': self.geracao_atual,
            'melhor_fitness': melhor_fitness,
            'fitness_medio': fitness_medio,
            'pior_fitness': self.populacao[-1].fitness
        })
        
        print(f"📊 Geração {self.geracao_atual}:")
        print(f"   Melhor: {melhor_fitness:.2f}")
        print(f"   Média: {fitness_medio:.2f}")
        print(f"   Pior: {self.populacao[-1].fitness:.2f}")
    
    def selecionar_pais(self):
        """
        Seleciona pais para reprodução usando seleção por torneio
        
        Returns:
            Tupla com duas redes parentais
        """
        # Torneio: escolhe 3 aleatórios e pega o melhor
        torneio_size = 3
        candidatos1 = np.random.choice(self.populacao, torneio_size, replace=False)
        pai1 = max(candidatos1, key=lambda r: r.fitness)
        
        candidatos2 = np.random.choice(self.populacao, torneio_size, replace=False)
        pai2 = max(candidatos2, key=lambda r: r.fitness)
        
        return pai1, pai2
    
    def nova_geracao(self):
        """Cria nova geração através de seleção, crossover e mutação"""
        nova_populacao = []
        
        # Elitismo: mantém os melhores
        num_elite = int(self.tamanho_populacao * self.taxa_elite)
        for i in range(num_elite):
            elite = self.populacao[i].clonar()
            elite.geração = self.geracao_atual + 1
            nova_populacao.append(elite)
        
        # Preenche o resto com filhos
        while len(nova_populacao) < self.tamanho_populacao:
            pai1, pai2 = self.selecionar_pais()
            
            # Crossover
            filho = pai1.crossover(pai2)
            filho.geração = self.geracao_atual + 1
            
            # Mutação
            if np.random.random() < self.taxa_mutacao:
                filho.mutar(taxa_mutacao=0.1, intensidade=0.3)
            
            # Reset estatísticas do filho
            filho.fitness = 0
            filho.vitorias = 0
            filho.derrotas = 0
            filho.dano_causado = 0
            filho.dano_recebido = 0
            
            nova_populacao.append(filho)
        
        self.populacao = nova_populacao
        self.geracao_atual += 1
        
        print(f"🧬 Nova geração {self.geracao_atual} criada!")
    
    def get_melhor_rede(self):
        """Retorna a melhor rede da população atual"""
        return max(self.populacao, key=lambda r: r.fitness)
    
    def salvar_populacao(self, diretorio="redes_neurais/populacao"):
        """Salva toda a população"""
        os.makedirs(diretorio, exist_ok=True)
        
        for i, rede in enumerate(self.populacao):
            caminho = os.path.join(diretorio, f"rede_{i}_gen_{self.geracao_atual}.json")
            rede.salvar(caminho)
        
        # Salva metadados
        meta = {
            'geracao': self.geracao_atual,
            'tamanho_populacao': self.tamanho_populacao,
            'historico': self.historico
        }
        
        with open(os.path.join(diretorio, 'meta.json'), 'w') as f:
            json.dump(meta, f, indent=2)
        
        print(f"💾 População salva em {diretorio}")
    
    def carregar_populacao(self, diretorio="redes_neurais/populacao"):
        """Carrega população salva"""
        # Carrega metadados
        with open(os.path.join(diretorio, 'meta.json'), 'r') as f:
            meta = json.load(f)
        
        self.geracao_atual = meta['geracao']
        self.historico = meta['historico']
        
        # Carrega redes
        arquivos = [f for f in os.listdir(diretorio) if f.endswith('.json') and f != 'meta.json']
        self.populacao = []
        
        for arquivo in sorted(arquivos):
            caminho = os.path.join(diretorio, arquivo)
            rede = RedeNeuralPersonagem.carregar(caminho)
            self.populacao.append(rede)
        
        print(f"📂 População carregada: {len(self.populacao)} redes, geração {self.geracao_atual}")
    
    def salvar_melhor(self, personagem_id):
        """Salva apenas a melhor rede"""
        melhor = self.get_melhor_rede()
        caminho = f"redes_neurais/melhor_rede_personagem_{personagem_id}.json"
        melhor.salvar(caminho)
        print(f"🏆 Melhor rede salva: Fitness {melhor.fitness:.2f}")
        return caminho
    
    def plotar_progresso(self):
        """Retorna dados para plotar gráfico de progresso"""
        geracoes = [h['geracao'] for h in self.historico]
        melhor = [h['melhor_fitness'] for h in self.historico]
        media = [h['fitness_medio'] for h in self.historico]
        pior = [h['pior_fitness'] for h in self.historico]
        
        return {
            'geracoes': geracoes,
            'melhor_fitness': melhor,
            'fitness_medio': media,
            'pior_fitness': pior
        }
