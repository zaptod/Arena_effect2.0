"""
Script para atualizar todas as armas com sistema de ricochete
"""
import re

# Lê o arma1.py atualizado
with open('armas/arma1.py', 'r', encoding='utf-8') as f:
    arma1_content = f.read()

# Extrai a classe Arma completa
class_match = re.search(r'(class Arma:.*?)(?=\ndef criar_arma)', arma1_content, re.DOTALL)
if not class_match:
    print("Erro: Não foi possível extrair a classe Arma")
    exit(1)

arma_class = class_match.group(1).strip()

# Atualiza arma2.py (Arco)
print("Atualizando arma2.py...")
with open('armas/arma2.py', 'r', encoding='utf-8') as f:
    arma2_content = f.read()

# Substitui a classe Arma mantendo a função criar_arma
arma2_updated = re.sub(
    r'class Arma:.*?(?=\ndef criar_arma)',
    arma_class + '\n\n',
    arma2_content,
    flags=re.DOTALL
)

with open('armas/arma2.py', 'w', encoding='utf-8') as f:
    f.write(arma2_updated)
print("✅ arma2.py atualizado")

# Atualiza arma3.py (Lança)
print("Atualizando arma3.py...")
with open('armas/arma3.py', 'r', encoding='utf-8') as f:
    arma3_content = f.read()

arma3_updated = re.sub(
    r'class Arma:.*?(?=\ndef criar_arma)',
    arma_class + '\n\n',
    arma3_content,
    flags=re.DOTALL
)

with open('armas/arma3.py', 'w', encoding='utf-8') as f:
    f.write(arma3_updated)
print("✅ arma3.py atualizado")

# Atualiza arma4.py (Martelo)
print("Atualizando arma4.py...")
with open('armas/arma4.py', 'r', encoding='utf-8') as f:
    arma4_content = f.read()

arma4_updated = re.sub(
    r'class Arma:.*?(?=\ndef criar_arma)',
    arma_class + '\n\n',
    arma4_content,
    flags=re.DOTALL
)

with open('armas/arma4.py', 'w', encoding='utf-8') as f:
    f.write(arma4_updated)
print("✅ arma4.py atualizado")

print("\n🎉 Todas as armas atualizadas com sistema de ricochete!")
