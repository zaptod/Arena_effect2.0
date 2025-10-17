"""
Exemplo de Uso do Sistema de IA Neural
Demonstra criação, treinamento e uso das redes neurais
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from ia import RedeNeuralPersonagem, TreinadorGenetico
import numpy as np

def exemplo_basico():
    """Exemplo básico de criação e uso de rede neural"""
    print("=" * 60)
    print("EXEMPLO 1: Criação e Uso Básico")
    print("=" * 60)
    
    # Criar rede neural
    rede = RedeNeuralPersonagem(personagem_id=1)
    print(f"✅ Rede neural criada para personagem {rede.personagem_id}")
    print(f"   Arquitetura: {rede.camadas}")
    
    # Criar personagem simulado
    class PersonagemSimulado:
        def __init__(self):
            self.id = 1
            self.x = 400
            self.y = 300
            self.velocidade = 5
            self.massa = 10
            self.forca = 50
            self.vida_maxima = 100
            self.vida_atual = 100
            self.arma = None
    
    personagem = PersonagemSimulado()
    
    # Criar inimigo simulado
    class InimigoSimulado:
        def __init__(self):
            self.id = 2
            self.x = 600
            self.y = 400
            self.forca = 40
            self.vida_maxima = 100
            self.vida_atual = 80
    
    inimigo = InimigoSimulado()
    
    # Decidir ação
    acao = rede.decidir_acao(personagem, [inimigo], largura=800, altura=600)
    
    print(f"\n📊 Ação decidida pela rede:")
    print(f"   Mover X: {acao['mover_x']:.2f}")
    print(f"   Mover Y: {acao['mover_y']:.2f}")
    print(f"   Atacar: {acao['atacar']}")
    print(f"   Fugir: {acao['fugir']}")
    
    # Salvar rede
    rede.salvar("redes_neurais/teste_exemplo1.json")
    print(f"\n💾 Rede salva em: redes_neurais/teste_exemplo1.json")
    
    # Carregar rede
    rede_carregada = RedeNeuralPersonagem.carregar("redes_neurais/teste_exemplo1.json")
    print(f"📂 Rede carregada com sucesso!")
    
    print()

def exemplo_treinamento():
    """Exemplo de treinamento com algoritmo genético"""
    print("=" * 60)
    print("EXEMPLO 2: Treinamento com Algoritmo Genético")
    print("=" * 60)
    
    # Criar treinador
    treinador = TreinadorGenetico(
        tamanho_populacao=10,  # População pequena para exemplo
        taxa_mutacao=0.15,
        taxa_elite=0.2
    )
    
    # População inicial
    treinador.criar_populacao_inicial(personagem_id=1)
    
    # Simular 5 gerações
    print(f"\n🧬 Iniciando treinamento (5 gerações)...\n")
    
    for geracao in range(5):
        # Simular combates e resultados
        resultados = []
        for i, rede in enumerate(treinador.populacao):
            # Resultado simulado (aleatório)
            venceu = np.random.random() > 0.5
            dano_causado = np.random.randint(50, 150)
            dano_recebido = np.random.randint(30, 100)
            
            resultados.append({
                'rede_id': i,
                'venceu': venceu,
                'dano_causado': dano_causado,
                'dano_recebido': dano_recebido,
                'vida_restante': 100 - dano_recebido
            })
        
        # Avaliar
        treinador.avaliar_populacao(resultados)
        
        # Nova geração (exceto na última)
        if geracao < 4:
            treinador.nova_geracao()
    
    # Melhor rede
    melhor = treinador.get_melhor_rede()
    print(f"\n🏆 Melhor rede da geração {treinador.geracao_atual}:")
    print(f"   Fitness: {melhor.fitness:.2f}")
    print(f"   Vitórias: {melhor.vitorias}")
    print(f"   Derrotas: {melhor.derrotas}")
    
    # Salvar melhor
    caminho = treinador.salvar_melhor(personagem_id=1)
    print(f"   Salva em: {caminho}")
    
    print()

def exemplo_mutacao():
    """Exemplo de mutação e crossover"""
    print("=" * 60)
    print("EXEMPLO 3: Mutação e Crossover")
    print("=" * 60)
    
    # Criar duas redes
    rede1 = RedeNeuralPersonagem(personagem_id=1)
    rede2 = RedeNeuralPersonagem(personagem_id=1)
    
    print("✅ Duas redes criadas")
    
    # Crossover
    filho = rede1.crossover(rede2)
    print(f"🧬 Filho criado através de crossover")
    print(f"   Geração: {filho.geração}")
    
    # Clonar para comparar
    filho_original = filho.clonar()
    
    # Mutar
    filho.mutar(taxa_mutacao=0.2, intensidade=0.5)
    print(f"⚡ Mutação aplicada (taxa=0.2, intensidade=0.5)")
    
    # Comparar pesos antes e depois
    diferenca = np.abs(filho.pesos[0] - filho_original.pesos[0]).mean()
    print(f"   Diferença média nos pesos: {diferenca:.4f}")
    
    print()

def exemplo_sensores():
    """Exemplo de processamento de sensores"""
    print("=" * 60)
    print("EXEMPLO 4: Sistema de Sensores")
    print("=" * 60)
    
    rede = RedeNeuralPersonagem(personagem_id=1)
    
    # Criar cenário
    class Personagem:
        def __init__(self, id, x, y, vida):
            self.id = id
            self.x = x
            self.y = y
            self.velocidade = 5
            self.massa = 10
            self.forca = 50
            self.vida_maxima = 100
            self.vida_atual = vida
            self.arma = True
    
    protagonista = Personagem(1, 200, 300, 80)  # Vida 80%
    inimigo1 = Personagem(2, 600, 300, 50)      # Perto, vida 50%
    inimigo2 = Personagem(3, 700, 500, 90)      # Longe, vida 90%
    
    # Processar sensores
    sensores = rede.processar_sensores(
        protagonista,
        [inimigo1, inimigo2],
        largura=800,
        altura=600
    )
    
    print("📡 Sensores capturados:\n")
    print(f"   [0] Posição X normalizada: {sensores[0]:.3f}")
    print(f"   [1] Posição Y normalizada: {sensores[1]:.3f}")
    print(f"   [2] Direção X para inimigo: {sensores[2]:.3f}")
    print(f"   [3] Direção Y para inimigo: {sensores[3]:.3f}")
    print(f"   [4] Distância para inimigo: {sensores[4]:.3f}")
    print(f"   [5] Vida própria: {sensores[5]:.3f}")
    print(f"   [6] Vida inimigo próximo: {sensores[6]:.3f}")
    print(f"   [7] Tem arma: {sensores[7]:.3f}")
    print(f"   [8] Distância borda X: {sensores[8]:.3f}")
    print(f"   [9] Distância borda Y: {sensores[9]:.3f}")
    print(f"   [10] Número de inimigos: {sensores[10]:.3f}")
    print(f"   [11] Força relativa: {sensores[11]:.3f}")
    
    # Decidir ação baseado nesses sensores
    acao = rede.decidir_acao(protagonista, [inimigo1, inimigo2])
    
    print(f"\n🎯 Ação decidida:")
    print(f"   Mover em direção a X={acao['mover_x']:.2f}, Y={acao['mover_y']:.2f}")
    
    if acao['fugir']:
        print(f"   🏃 Modo FUGA ativado!")
    elif acao['atacar']:
        print(f"   ⚔️ Modo ATAQUE ativado!")
    else:
        print(f"   🤔 Modo CAUTELOSO (observando)")
    
    print()

def exemplo_fitness():
    """Exemplo de cálculo de fitness"""
    print("=" * 60)
    print("EXEMPLO 5: Cálculo de Fitness")
    print("=" * 60)
    
    # Criar 3 redes com diferentes desempenhos
    rede_agressiva = RedeNeuralPersonagem(personagem_id=1)
    rede_agressiva.vitorias = 5
    rede_agressiva.derrotas = 2
    rede_agressiva.dano_causado = 800
    rede_agressiva.dano_recebido = 600
    
    rede_defensiva = RedeNeuralPersonagem(personagem_id=2)
    rede_defensiva.vitorias = 3
    rede_defensiva.derrotas = 1
    rede_defensiva.dano_causado = 400
    rede_defensiva.dano_recebido = 200
    
    rede_fraca = RedeNeuralPersonagem(personagem_id=3)
    rede_fraca.vitorias = 1
    rede_fraca.derrotas = 5
    rede_fraca.dano_causado = 200
    rede_fraca.dano_recebido = 900
    
    # Calcular fitness
    fitness_agressiva = rede_agressiva.calcular_fitness()
    fitness_defensiva = rede_defensiva.calcular_fitness()
    fitness_fraca = rede_fraca.calcular_fitness()
    
    print("📊 Comparação de Fitness:\n")
    
    print("🗡️ Rede Agressiva:")
    print(f"   Vitórias: {rede_agressiva.vitorias}, Derrotas: {rede_agressiva.derrotas}")
    print(f"   Dano causado: {rede_agressiva.dano_causado}, Dano recebido: {rede_agressiva.dano_recebido}")
    print(f"   FITNESS: {fitness_agressiva:.2f}")
    
    print("\n🛡️ Rede Defensiva:")
    print(f"   Vitórias: {rede_defensiva.vitorias}, Derrotas: {rede_defensiva.derrotas}")
    print(f"   Dano causado: {rede_defensiva.dano_causado}, Dano recebido: {rede_defensiva.dano_recebido}")
    print(f"   FITNESS: {fitness_defensiva:.2f}")
    
    print("\n😵 Rede Fraca:")
    print(f"   Vitórias: {rede_fraca.vitorias}, Derrotas: {rede_fraca.derrotas}")
    print(f"   Dano causado: {rede_fraca.dano_causado}, Dano recebido: {rede_fraca.dano_recebido}")
    print(f"   FITNESS: {fitness_fraca:.2f}")
    
    print(f"\n🏆 Vencedor: ", end="")
    if fitness_agressiva > fitness_defensiva and fitness_agressiva > fitness_fraca:
        print("Rede Agressiva!")
    elif fitness_defensiva > fitness_fraca:
        print("Rede Defensiva!")
    else:
        print("Rede Fraca!")
    
    print()

def main():
    """Executa todos os exemplos"""
    print("\n" + "=" * 60)
    print("  SISTEMA DE IA NEURAL - EXEMPLOS DE USO")
    print("=" * 60 + "\n")
    
    try:
        exemplo_basico()
        exemplo_sensores()
        exemplo_fitness()
        exemplo_mutacao()
        exemplo_treinamento()
        
        print("=" * 60)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
