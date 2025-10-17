"""
APLICAR REESTRUTURAÇÃO COMPLETA
Script que aplica todas as mudanças e testa o sistema
"""
import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def criar_backup():
    """Cria backup completo"""
    backup_dir = os.path.join(BASE_DIR, f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    print(f"\n📦 Criando backup em: {backup_dir}")
    
    os.makedirs(backup_dir, exist_ok=True)
    
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
            dst = os.path.join(backup_dir, arq)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  ✅ {arq}")
    
    return backup_dir

def aplicar_arquivos_novos():
    """Substitui arquivos antigos pelos novos"""
    print("\n🔧 Aplicando novos arquivos...")
    
    substituicoes = [
        ('personagensP_new.py', 'personagensP.py'),
        ('armasP_new.py', 'armasP.py'),
        ('mapasP_new.py', 'mapasP.py'),
        ('SelectionP_new.py', 'SelectionP.py'),
        ('main_simulation_new.py', 'main_simulation.py')
    ]
    
    for novo, antigo in substituicoes:
        novo_path = os.path.join(BASE_DIR, 'Paginas', novo)
        antigo_path = os.path.join(BASE_DIR, 'Paginas', antigo)
        
        if os.path.exists(novo_path):
            if os.path.exists(antigo_path):
                os.remove(antigo_path)
            shutil.move(novo_path, antigo_path)
            print(f"  ✅ {antigo} atualizado")
        else:
            print(f"  ⚠️  {novo} não encontrado, mantendo {antigo}")

def verificar_estrutura():
    """Verifica se todos os arquivos necessários existem"""
    print("\n🔍 Verificando estrutura...")
    
    arquivos_necessarios = [
        'Paginas/utils.py',
        'Paginas/main.py',
        'Paginas/personagensP.py',
        'Paginas/armasP.py',
        'Paginas/mapasP.py',
        'Paginas/SelectionP.py',
        'Paginas/main_simulation.py',
        'bases_de_dados/Banco_de_dados_personagens.py',
        'bases_de_dados/Banco_de_dados_armas.py',
        'bases_de_dados/Banco_de_dados_mapas.py',
        'armas/arma1.py',
        'armas/arma2.py',
        'armas/arma3.py',
        'armas/arma4.py'
    ]
    
    todos_ok = True
    for arq in arquivos_necessarios:
        path = os.path.join(BASE_DIR, arq)
        if os.path.exists(path):
            print(f"  ✅ {arq}")
        else:
            print(f"  ❌ {arq} - FALTANDO!")
            todos_ok = False
    
    return todos_ok

def limpar_arquivos_temporarios():
    """Remove arquivos temporários"""
    print("\n🧹 Limpando arquivos temporários...")
    
    temp_files = [
        'Paginas/personagensP_new.py',
        'Paginas/armasP_new.py',
        'Paginas/mapasP_new.py',
        'Paginas/SelectionP_new.py',
        'Paginas/main_simulation_new.py'
    ]
    
    for tf in temp_files:
        path = os.path.join(BASE_DIR, tf)
        if os.path.exists(path):
            os.remove(path)
            print(f"  🗑️  Removido: {tf}")

def main():
    print("="*70)
    print(" REESTRUTURAÇÃO COMPLETA - ARENA EFFECT 2.0")
    print("="*70)
    
    # 1. Criar backup
    backup_dir = criar_backup()
    
    # 2. Aplicar novos arquivos
    aplicar_arquivos_novos()
    
    # 3. Verificar estrutura
    estrutura_ok = verificar_estrutura()
    
    # 4. Limpar temporários
    limpar_arquivos_temporarios()
    
    print("\n" + "="*70)
    
    if estrutura_ok:
        print("✅ REESTRUTURAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"\n📂 Backup salvo em: {backup_dir}")
        print("\n🎮 Para testar, execute:")
        print(f"   cd {BASE_DIR}")
        print("   python Paginas/main.py")
        print("\n📋 Funcionalidades:")
        print("   • Menu principal reestruturado")
        print("   • Navegação completa entre páginas")
        print("   • Sistema de armas integrado")
        print("   • Controles de simulação (pausar, reiniciar)")
        print("   • Interface modernizada")
        print("\n⌨️  Atalhos na simulação:")
        print("   ESPAÇO: Pausar/Continuar")
        print("   R: Reiniciar")
        print("   S: Mostrar/Ocultar estatísticas")
        print("   ESC: Sair")
    else:
        print("⚠️  AVISO: Alguns arquivos estão faltando!")
        print("   Verifique a estrutura antes de executar.")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    main()
