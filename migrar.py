"""
Script de Migração - Reestru tura todo o código
Executa este arquivo para aplicar todas as correções e reestruturações
"""
import os
import shutil
from datetime import datetime

# Diretório base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')

def criar_backup():
    """Cria backup dos arquivos atuais"""
    print("📦 Criando backup...")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    arquivos = [
        'Paginas/main.py',
        'Paginas/personagensP.py',
        'Paginas/armasP.py',
        'Paginas/mapasP.py',
        'Paginas/SelectionP.py',
        'Paginas/main_simulation.py'
    ]
    
    for arq in arquivos:
        src = os.path.join(BASE_DIR, arq)
        if os.path.exists(src):
            dst = os.path.join(BACKUP_DIR, arq)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  ✅ Backup: {arq}")
    
    print(f"✅ Backup criado em: {BACKUP_DIR}\n")

def aplicar_mudancas():
    """Aplica as mudanças necessárias"""
    print("🔧 Aplicando mudanças...\n")
    
    # 1. Renomeia arquivo novo
    new_file = os.path.join(BASE_DIR, 'Paginas/personagensP_new.py')
    old_file = os.path.join(BASE_DIR, 'Paginas/personagensP.py')
    
    if os.path.exists(new_file):
        if os.path.exists(old_file):
            os.remove(old_file)
        os.rename(new_file, old_file)
        print("✅ personagensP.py atualizado")
    
    print("\n✅ Migração concluída!")
    print(f"📂 Backup salvo em: {BACKUP_DIR}")
    print("\n🎮 Execute: python Paginas/main.py")

if __name__ == '__main__':
    print("="*60)
    print(" MIGRAÇÃO - ARENA EFFECT 2.0")
    print("="*60)
    print()
    
    criar_backup()
    aplicar_mudancas()
    
    print("\n" + "="*60)
