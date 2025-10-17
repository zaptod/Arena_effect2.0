"""
Gerenciador de Personagens - Versão Reestruturada
Interface completa para criar, editar e excluir personagens
"""
import pygame
import sys
import os
import importlib

from utils import (
    WIDTH, HEIGHT, FPS, COLOR_BG_LIGHT, COLOR_TEXT, COLOR_BUTTON,
    COLOR_DANGER, COLOR_SELECTED, COLOR_SUCCESS, draw_button, draw_back_button,
    draw_title, is_mouse_over, draw_info_box
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_personagens import personagens_db as _personagens_db
from bases_de_dados.Banco_de_dados_comportamentais import comportamentos_db

# Variável global para o banco de personagens
personagens_db = _personagens_db

def recarregar_personagens():
    """Recarrega o banco de dados de personagens"""
    global personagens_db
    banco_mod = importlib.import_module('bases_de_dados.Banco_de_dados_personagens')
    importlib.reload(banco_mod)
    personagens_db = banco_mod.personagens_db
    return personagens_db

def show_personagens_carousel(screen, fonts):
    """Exibe carrossel de personagens com funcionalidades completas"""
    clock = pygame.time.Clock()
    carousel_start = 0
    visible_count = 4
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLOR_BG_LIGHT)
        
        # Botão voltar
        back_rect = draw_back_button(screen, fonts['medium'])
        
        # Título
        draw_title(screen, 'Gerenciar Personagens', fonts['large'], 50)
        
        # Botão criar novo
        btn_novo = pygame.Rect(WIDTH//2 - 150, 100, 300, 50)
        draw_button(screen, '➕ Criar Novo Personagem', btn_novo, fonts['medium'],
                   color=COLOR_SUCCESS, hover=is_mouse_over(btn_novo, mouse_pos))
        
        # Setas de navegação
        btn_left = pygame.Rect(50, 300, 50, 50)
        btn_right = pygame.Rect(WIDTH - 100, 300, 50, 50)
        
        if carousel_start > 0:
            pygame.draw.polygon(screen, COLOR_TEXT, [
                (btn_left.x+40, btn_left.y+25),
                (btn_left.x+10, btn_left.y+10),
                (btn_left.x+10, btn_left.y+40)
            ])
        
        if carousel_start + visible_count < len(personagens_db):
            pygame.draw.polygon(screen, COLOR_TEXT, [
                (btn_right.x+10, btn_right.y+25),
                (btn_right.x+40, btn_right.y+10),
                (btn_right.x+40, btn_right.y+40)
            ])
        
        # Lista de personagens
        end = min(len(personagens_db), carousel_start + visible_count)
        for idx, personagem in enumerate(personagens_db[carousel_start:end]):
            y = 170 + idx*100
            rect = pygame.Rect(120, y, 560, 85)
            
            # Cor baseada no status
            color = COLOR_SELECTED if personagem.get('ativo', True) else COLOR_DANGER
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, COLOR_TEXT, rect, 2, border_radius=10)
            
            # Informações do personagem
            nome_txt = fonts['medium'].render(f"{personagem['nome']}", True, COLOR_TEXT)
            screen.blit(nome_txt, (rect.x+15, rect.y+10))
            
            id_txt = fonts['small'].render(f"ID: {personagem['id']}", True, COLOR_TEXT)
            screen.blit(id_txt, (rect.x+15, rect.y+40))
            
            # Botões de ação
            btn_edit = pygame.Rect(rect.x+380, rect.y+15, 80, 30)
            btn_del = pygame.Rect(rect.x+470, rect.y+15, 80, 30)
            
            draw_button(screen, 'Editar', btn_edit, fonts['small'], 
                       hover=is_mouse_over(btn_edit, mouse_pos))
            draw_button(screen, 'Excluir', btn_del, fonts['small'],
                       color=COLOR_DANGER, hover=is_mouse_over(btn_del, mouse_pos))
            
            # Highlight no hover
            if is_mouse_over(rect, mouse_pos):
                pygame.draw.rect(screen, (255, 255, 0), rect, 3, border_radius=10)
        
        # Informações
        info_lines = [
            f"Total: {len(personagens_db)} personagens",
            f"Página: {carousel_start//visible_count + 1}/{(len(personagens_db)-1)//visible_count + 1}",
            "Clique para editar | ESC para voltar"
        ]
        draw_info_box(screen, info_lines, fonts['small'])
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT and carousel_start + visible_count < len(personagens_db):
                    carousel_start += 1
                elif event.key == pygame.K_LEFT and carousel_start > 0:
                    carousel_start -= 1
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Botão voltar
                if back_rect.collidepoint(event.pos):
                    running = False
                
                # Botão criar novo
                elif btn_novo.collidepoint(event.pos):
                    criar_personagem_interface(screen, fonts)
                    recarregar_personagens()
                
                # Navegação
                elif btn_left.collidepoint(event.pos) and carousel_start > 0:
                    carousel_start -= 1
                elif btn_right.collidepoint(event.pos) and carousel_start + visible_count < len(personagens_db):
                    carousel_start += 1
                
                # Ações nos personagens
                else:
                    for idx, personagem in enumerate(personagens_db[carousel_start:end]):
                        y = 170 + idx*100
                        rect = pygame.Rect(120, y, 560, 85)
                        btn_edit = pygame.Rect(rect.x+380, rect.y+15, 80, 30)
                        btn_del = pygame.Rect(rect.x+470, rect.y+15, 80, 30)
                        
                        if btn_edit.collidepoint(event.pos):
                            editar_personagem_interface(screen, fonts, personagem)
                            recarregar_personagens()
                            break
                        
                        elif btn_del.collidepoint(event.pos):
                            excluir_personagem(personagem['id'])
                            recarregar_personagens()
                            if carousel_start > 0 and carousel_start >= len(personagens_db):
                                carousel_start -= 1
                            break
                        
                        elif rect.collidepoint(event.pos):
                            editar_personagem_interface(screen, fonts, personagem)
                            recarregar_personagens()
                            break
        
        pygame.display.flip()
        clock.tick(FPS)

def criar_personagem_interface(screen, fonts):
    """Interface para criar novo personagem"""
    # Importa o criador
    from Paginas.PersonagemCreate import criar_personagem_popup
    criar_personagem_popup(screen, fonts)

def editar_personagem_interface(screen, fonts, personagem):
    """Interface para editar personagem existente"""
    # Importa o editor
    from Paginas.PersonagemEdit import edit_personagem
    edit_personagem(personagem, screen, fonts)

def excluir_personagem(personagem_id):
    """Exclui um personagem pelo ID"""
    nome_arquivo = f"personagem{personagem_id}.py"
    caminho = os.path.join(os.path.dirname(__file__), '..', 'personagens', nome_arquivo)
    
    if os.path.exists(caminho):
        try:
            # Remove o arquivo
            os.remove(caminho)
            
            # Remove do banco de dados em memória
            global personagens_db
            personagens_db = [p for p in personagens_db if p['id'] != personagem_id]
            
            print(f"✅ Personagem ID {personagem_id} excluído (ID disponível para reutilização)")
            return True
        except Exception as e:
            print(f"❌ Erro ao excluir personagem: {e}")
            return False
    return False
