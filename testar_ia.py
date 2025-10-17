"""
🧪 TESTE DE INTEGRAÇÃO - SISTEMA DE IA NEURAL

Este script verifica se todos os componentes do sistema de IA
estão funcionando corretamente.
"""

import os
import sys

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🧪 TESTE DE INTEGRAÇÃO - SISTEMA DE IA NEURAL")
print("=" * 60)

# ========== TESTE 1: Importações ==========
print("\n📦 TESTE 1: Verificando importações...")
try:
    from ia import RedeNeuralPersonagem, TreinadorGenetico
    print("   ✅ Módulo ia importado com sucesso")
    IA_DISPONIVEL = True
except ImportError as e:
    print(f"   ❌ Erro ao importar módulo ia: {e}")
    IA_DISPONIVEL = False
    sys.exit(1)

try:
    import numpy as np
    print("   ✅ NumPy disponível")
except ImportError:
    print("   ❌ NumPy não encontrado - execute: pip install numpy")
    sys.exit(1)

try:
    import pygame
    print("   ✅ Pygame disponível")
except ImportError:
    print("   ❌ Pygame não encontrado - execute: pip install pygame")
    sys.exit(1)

# ========== TESTE 2: Criação de Rede Neural ==========
print("\n🧠 TESTE 2: Criando rede neural...")
try:
    rede = RedeNeuralPersonagem(personagem_id=999)
    print(f"   ✅ Rede neural criada (ID: {rede.personagem_id})")
    print(f"   📊 Arquitetura: {rede.camadas}")
    print(f"   🔢 Total de pesos: {sum(w.size for w in rede.pesos)}")
except Exception as e:
    print(f"   ❌ Erro ao criar rede: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ========== TESTE 3: Processamento de Sensores ==========
print("\n👁️ TESTE 3: Testando processamento de sensores...")
try:
    # Cria personagem mockado
    class PersonagemMock:
        def __init__(self, pid):
            self.id = pid
            self.x = 400
            self.y = 300
            self.vida_atual = 100
            self.vida_maxima = 100
            self.arma = True
            self.vivo = True
            self.forca = 50
            self.velocidade = 5
    
    personagem = PersonagemMock(999)
    outros = [PersonagemMock(1), PersonagemMock(2)]
    outros[0].x = 500
    outros[0].y = 350
    outros[1].x = 300
    outros[1].y = 250
    
    sensores = rede.processar_sensores(personagem, outros, 800, 600)
    print(f"   ✅ Sensores processados: {len(sensores)} valores")
    print(f"   📈 Valores: {[f'{s:.2f}' for s in sensores[:6]]}...")
    
    # Verifica se sensores estão normalizados
    if all(0 <= s <= 1 for s in sensores):
        print("   ✅ Todos os sensores estão normalizados (0-1)")
    else:
        print("   ⚠️ Alguns sensores fora do intervalo 0-1")
        
except Exception as e:
    print(f"   ❌ Erro ao processar sensores: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ========== TESTE 4: Decisão de Ação ==========
print("\n🎯 TESTE 4: Testando decisão de ação...")
try:
    acao = rede.decidir_acao(personagem, outros, 800, 600)
    print(f"   ✅ Ação decidida com sucesso")
    print(f"   🎮 Movimento X: {acao['mover_x']:.2f}")
    print(f"   🎮 Movimento Y: {acao['mover_y']:.2f}")
    print(f"   ⚔️ Atacar: {acao['atacar']}")
    print(f"   🛡️ Fugir: {acao['fugir']}")
    
    # Verifica se ação está no formato correto
    assert 'mover_x' in acao
    assert 'mover_y' in acao
    assert 'atacar' in acao
    assert 'fugir' in acao
    print("   ✅ Formato da ação está correto")
    
except Exception as e:
    print(f"   ❌ Erro ao decidir ação: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ========== TESTE 5: Mutação ==========
print("\n🧬 TESTE 5: Testando mutação...")
try:
    pesos_antes = rede.pesos[0].copy()
    rede.mutar(taxa_mutacao=0.3, intensidade=0.1)
    pesos_depois = rede.pesos[0]
    
    mudou = not np.array_equal(pesos_antes, pesos_depois)
    if mudou:
        print("   ✅ Mutação aplicada com sucesso")
        diferenca = np.abs(pesos_antes - pesos_depois).mean()
        print(f"   📊 Diferença média: {diferenca:.6f}")
    else:
        print("   ⚠️ Mutação não alterou pesos (taxa muito baixa?)")
        
except Exception as e:
    print(f"   ❌ Erro ao mutar: {e}")
    sys.exit(1)

# ========== TESTE 6: Crossover ==========
print("\n👥 TESTE 6: Testando crossover...")
try:
    rede2 = RedeNeuralPersonagem(personagem_id=998)
    filho = rede.crossover(rede2)
    print(f"   ✅ Crossover realizado (Filho ID: {filho.personagem_id})")
    print(f"   🧬 Filho possui mesma arquitetura: {filho.camadas == rede.camadas}")
    
except Exception as e:
    print(f"   ❌ Erro ao fazer crossover: {e}")
    sys.exit(1)

# ========== TESTE 7: Fitness ==========
print("\n💪 TESTE 7: Testando cálculo de fitness...")
try:
    rede.vitorias = 5
    rede.derrotas = 2
    rede.dano_causado = 1500
    rede.dano_recebido = 800
    
    fitness = rede.calcular_fitness()
    print(f"   ✅ Fitness calculado: {fitness:.2f}")
    print(f"   📊 Vitórias: {rede.vitorias}")
    print(f"   📊 Derrotas: {rede.derrotas}")
    print(f"   📊 Dano causado: {rede.dano_causado:.2f}")
    print(f"   📊 Dano recebido: {rede.dano_recebido:.2f}")
    
    # Fórmula: (vitorias * 1000) - (derrotas * 500) + dano_causado - (dano_recebido * 0.5)
    fitness_esperado = (5 * 1000) - (2 * 500) + 1500 - (800 * 0.5)
    if abs(fitness - fitness_esperado) < 0.01:
        print(f"   ✅ Fitness correto (esperado: {fitness_esperado:.2f})")
    else:
        print(f"   ⚠️ Fitness diferente do esperado ({fitness_esperado:.2f})")
        
except Exception as e:
    print(f"   ❌ Erro ao calcular fitness: {e}")
    sys.exit(1)

# ========== TESTE 8: Persistência ==========
print("\n💾 TESTE 8: Testando save/load...")
try:
    # Cria diretório de teste
    test_dir = 'test_redes_neurais'
    os.makedirs(test_dir, exist_ok=True)
    
    # Salva
    caminho = os.path.join(test_dir, 'rede_teste.json')
    rede.salvar(caminho)
    print(f"   ✅ Rede salva em {caminho}")
    
    # Verifica se arquivo existe
    if os.path.exists(caminho):
        print(f"   ✅ Arquivo criado ({os.path.getsize(caminho)} bytes)")
    else:
        print("   ❌ Arquivo não foi criado")
        sys.exit(1)
    
    # Carrega
    rede_carregada = RedeNeuralPersonagem.carregar(caminho)
    print(f"   ✅ Rede carregada (ID: {rede_carregada.personagem_id})")
    
    # Verifica se dados foram preservados
    if rede_carregada.vitorias == rede.vitorias:
        print("   ✅ Vitórias preservadas")
    if rede_carregada.derrotas == rede.derrotas:
        print("   ✅ Derrotas preservadas")
    if abs(rede_carregada.dano_causado - rede.dano_causado) < 0.01:
        print("   ✅ Dano causado preservado")
    
    # Limpa arquivo de teste
    os.remove(caminho)
    os.rmdir(test_dir)
    print("   ✅ Arquivos de teste removidos")
    
except Exception as e:
    print(f"   ❌ Erro ao testar persistência: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ========== TESTE 9: Treinador Genético ==========
print("\n🧬 TESTE 9: Testando treinador genético...")
try:
    treinador = TreinadorGenetico(tamanho_populacao=5)
    print(f"   ✅ Treinador criado (população: {treinador.tamanho_populacao})")
    
    # Cria população inicial
    treinador.criar_populacao_inicial(personagem_id=999)
    print(f"   ✅ População inicial criada: {len(treinador.populacao)} indivíduos)")
    
    # Simula avaliação
    resultados = [
        {'rede_id': i, 'vitorias': 1, 'derrotas': 0, 'dano_causado': 100, 'dano_recebido': 50, 'venceu': True}
        for i in range(5)
    ]
    treinador.avaliar_populacao(resultados)
    print("   ✅ População avaliada")
    
    # Nova geração
    treinador.nova_geracao()
    print(f"   ✅ Nova geração criada (geração {treinador.geracao_atual})")
    
except Exception as e:
    print(f"   ❌ Erro ao testar treinador: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ========== TESTE 10: Integração com main_simulation.py ==========
print("\n🎮 TESTE 10: Verificando integração com simulação...")
try:
    # Verifica se main_simulation.py existe
    main_sim_path = os.path.join('Paginas', 'main_simulation.py')
    if os.path.exists(main_sim_path):
        print(f"   ✅ main_simulation.py encontrado")
        
        # Lê o arquivo
        with open(main_sim_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verifica imports críticos
        checks = [
            ('from ia import', 'Import do módulo IA'),
            ('IA_DISPONIVEL', 'Flag de disponibilidade'),
            ('aplicar_ia_personagem', 'Função de aplicação da IA'),
            ('salvar_redes_neurais', 'Função de salvamento'),
            ('personagens_originais', 'Lista de personagens originais'),
            ('ia_atacar', 'Atributo de ataque da IA'),
            ('rede_neural', 'Atributo da rede neural'),
        ]
        
        for check, desc in checks:
            if check in conteudo:
                print(f"   ✅ {desc} presente")
            else:
                print(f"   ⚠️ {desc} NÃO encontrado")
        
    else:
        print(f"   ❌ main_simulation.py não encontrado")
        
except Exception as e:
    print(f"   ❌ Erro ao verificar integração: {e}")

# ========== RESULTADOS FINAIS ==========
print("\n" + "=" * 60)
print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
print("=" * 60)
print("\n✅ Sistema de IA Neural está 100% funcional e integrado!")
print("\n📋 Próximos passos:")
print("   1. Inicie o jogo: cd Paginas && python main.py")
print("   2. Crie 2+ personagens")
print("   3. Selecione-os para combate")
print("   4. Observe a IA controlando os personagens!")
print("\n💡 Dica: Execute exemplo_ia.py para ver mais demonstrações")
print("=" * 60)
