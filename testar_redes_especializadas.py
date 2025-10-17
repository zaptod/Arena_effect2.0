"""
Script de teste para sistema de redes neurais especializadas por arma
Demonstra como cada personagem pode ter IAs diferentes para cada arma
"""
import os
import sys

# Adiciona diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ia import RedeNeuralPersonagem

def testar_redes_especializadas():
    """Testa criação e salvamento de redes neurais especializadas"""
    
    print("🧪 TESTE: Sistema de Redes Neurais Especializadas por Arma")
    print("=" * 60)
    
    # Cenário: Personagem 0 com diferentes armas
    personagem_id = 0
    armas_ids = [1, 2, 3, 4]  # Espada, Arco, Lança, Martelo
    
    print(f"\n📊 Criando redes especializadas para Personagem {personagem_id}:")
    print("-" * 60)
    
    for arma_id in armas_ids:
        print(f"\n⚔️ Arma {arma_id}:")
        
        # Cria rede especializada
        rede = RedeNeuralPersonagem(personagem_id, arma_id)
        print(f"  ✓ Rede neural criada: Personagem {rede.personagem_id} + Arma {rede.arma_id}")
        
        # Define estatísticas simuladas
        rede.vitorias = arma_id * 5
        rede.fitness = arma_id * 100
        rede.dano_causado = arma_id * 200
        
        # Salva
        rede.salvar()
        caminho_esperado = f"redes_neurais/rede_personagem_{personagem_id}_arma_{arma_id}.json"
        
        if os.path.exists(caminho_esperado):
            print(f"  ✓ Salva em: {caminho_esperado}")
        else:
            print(f"  ✗ ERRO: Arquivo não encontrado!")
        
        # Carrega de volta
        rede_carregada = RedeNeuralPersonagem.carregar(caminho_esperado)
        
        if rede_carregada.arma_id == arma_id:
            print(f"  ✓ Carregada com arma_id correto: {rede_carregada.arma_id}")
        else:
            print(f"  ✗ ERRO: arma_id incorreto!")
        
        if rede_carregada.vitorias == arma_id * 5:
            print(f"  ✓ Estatísticas preservadas: {rede_carregada.vitorias} vitórias")
        else:
            print(f"  ✗ ERRO: Estatísticas perdidas!")
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("\n📁 Arquivos criados:")
    
    redes_dir = "redes_neurais"
    if os.path.exists(redes_dir):
        arquivos = sorted([f for f in os.listdir(redes_dir) if f.startswith('rede_personagem_0')])
        for arquivo in arquivos:
            tamanho = os.path.getsize(os.path.join(redes_dir, arquivo))
            print(f"  - {arquivo} ({tamanho} bytes)")
    
    print("\n💡 INTERPRETAÇÃO:")
    print("  Cada arquivo representa uma IA especializada.")
    print("  Exemplo: rede_personagem_0_arma_1.json")
    print("    → Personagem 0 quando usa Arma 1 (Espada)")
    print("\n  Isso significa que:")
    print("    ⚔️ Com espada: IA aprende a combater corpo-a-corpo")
    print("    🏹 Com arco: IA aprende a manter distância")
    print("    🗡️ Com adaga: IA aprende ataques rápidos")
    print("    🔨 Com martelo: IA aprende golpes pesados")

def comparar_comportamentos():
    """Demonstra como verificar diferenças entre redes"""
    print("\n\n🔍 COMPARAÇÃO DE COMPORTAMENTOS:")
    print("=" * 60)
    
    personagem_id = 0
    
    # Carrega redes de armas diferentes
    try:
        rede_espada = RedeNeuralPersonagem.carregar("redes_neurais/rede_personagem_0_arma_1.json")
        rede_arco = RedeNeuralPersonagem.carregar("redes_neurais/rede_personagem_0_arma_2.json")
        
        print(f"\n📊 Personagem {personagem_id}:")
        print(f"\n  ⚔️ Com ESPADA (Arma 1):")
        print(f"    - Vitórias: {rede_espada.vitorias}")
        print(f"    - Fitness: {rede_espada.fitness}")
        print(f"    - Dano causado: {rede_espada.dano_causado}")
        
        print(f"\n  🏹 Com ARCO (Arma 2):")
        print(f"    - Vitórias: {rede_arco.vitorias}")
        print(f"    - Fitness: {rede_arco.fitness}")
        print(f"    - Dano causado: {rede_arco.dano_causado}")
        
        print("\n💡 Os pesos das redes são INDEPENDENTES!")
        print("   A IA com espada não interfere na IA com arco.")
        
    except FileNotFoundError:
        print("⚠️ Execute o teste acima primeiro para criar as redes.")

if __name__ == '__main__':
    testar_redes_especializadas()
    comparar_comportamentos()
    
    print("\n\n🎮 PRÓXIMOS PASSOS:")
    print("  1. Execute o modo treino loop com diferentes armas")
    print("  2. Deixe treinar várias rodadas")
    print("  3. Compare as estatísticas das redes especializadas")
    print("  4. Observe como cada IA desenvolve estratégias únicas!")
