"""
Script para atualizar o método draw() das armas com suporte a angulo_direto
"""
import re

# Lê a arma1 atualizada
with open('armas/arma1.py', 'r', encoding='utf-8') as f:
    arma1_content = f.read()

# Extrai o método draw completo da arma1
pattern = r'(    def draw\(self, screen, personagem_x, personagem_y.*?\n(?:        .*\n)*?)(?=    def |\Z)'
match = re.search(pattern, arma1_content, re.DOTALL)

if match:
    novo_draw = match.group(1)
    print("✅ Método draw() extraído da arma1.py")
    print(f"Tamanho: {len(novo_draw)} caracteres")
    
    # Atualiza armas 2, 3 e 4
    for num in [2, 3, 4]:
        arquivo = f'armas/arma{num}.py'
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Substitui o método draw antigo pelo novo
            conteudo_novo = re.sub(pattern, novo_draw, conteudo, flags=re.DOTALL)
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo_novo)
            
            print(f"✅ arma{num}.py atualizado")
        except Exception as e:
            print(f"❌ Erro ao atualizar arma{num}.py: {e}")
    
    print("\n🎉 Todas as armas atualizadas com suporte a angulo_direto!")
else:
    print("❌ Não foi possível extrair o método draw()")
