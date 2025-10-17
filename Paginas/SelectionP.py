"""
Página de Seleção - Versão Reestruturada
Interface para selecionar personagens, armas e mapas para simulação
"""
import pygame
import sys
import os

from utils import (
    WIDTH, HEIGHT, FPS, COLOR_BG_LIGHT, COLOR_TEXT, COLOR_BUTTON,
    COLOR_SELECTED, COLOR_SUCCESS, draw_button, draw_back_button,
    draw_title, is_mouse_over, draw_info_box
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_personagens import personagens_db
from bases_de_dados.Banco_de_dados_armas import armas_db
from bases_de_dados.Banco_de_dados_mapas import mapas_db

def show_selection_carousel(screen, fonts):
    """Interface de seleção completa"""
    clock = pygame.time.Clock()
    
    # Estado da seleção
    selected_personagens = set()
    selected_armas = set()
    selected_map = None
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLOR_BG_LIGHT)
        
        # Botão voltar
        back_rect = draw_back_button(screen, fonts['medium'])
        
        # Título
        draw_title(screen, 'Configurar Simulação', fonts['large'], 30)
        
        # COLUNA 1: PERSONAGENS
        x1, y1 = 30, 80
        label1 = fonts['medium'].render('🎮 Personagens', True, COLOR_TEXT)
        screen.blit(label1, (x1, y1))
        
        # Lista de personagens ativos
        personagens_ativos = [p for p in personagens_db if p.get('ativo', True)]
        for idx, personagem in enumerate(personagens_ativos[:6]):  # Máximo 6
            rect = pygame.Rect(x1, y1 + 40 + idx*50, 220, 45)
            
            is_selected = personagem['id'] in selected_personagens
            color = COLOR_SELECTED if is_selected else (100, 100, 100)
            
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, COLOR_TEXT, rect, 2, border_radius=5)
            
            txt = fonts['small'].render(personagem['nome'][:18], True, COLOR_TEXT)
            screen.blit(txt, (rect.x + 10, rect.y + 12))
            
            # Ícone de seleção
            if is_selected:
                check_txt = fonts['medium'].render('✓', True, (0, 255, 0))
                screen.blit(check_txt, (rect.x + 190, rect.y + 8))
        
        # COLUNA 2: ARMAS
        x2, y2 = 280, 80
        label2 = fonts['medium'].render('⚔️ Armas', True, COLOR_TEXT)
        screen.blit(label2, (x2, y2))
        
        hint2 = fonts['small'].render('(1 por personagem)', True, (150, 150, 150))
        screen.blit(hint2, (x2, y2 + 25))
        
        for idx, arma in enumerate(armas_db):
            rect = pygame.Rect(x2, y2 + 55 + idx*50, 220, 45)
            
            is_selected = arma['id'] in selected_armas
            color = (200, 100, 0) if is_selected else (100, 100, 100)
            
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, COLOR_TEXT, rect, 2, border_radius=5)
            
            txt = fonts['small'].render(arma['nome'], True, COLOR_TEXT)
            screen.blit(txt, (rect.x + 10, rect.y + 5))
            
            stats = fonts['small'].render(f"D:{arma['dano']} A:{arma['alcance']}", True, (200, 200, 200))
            screen.blit(stats, (rect.x + 10, rect.y + 25))
            
            if is_selected:
                check_txt = fonts['medium'].render('✓', True, (255, 200, 0))
                screen.blit(check_txt, (rect.x + 190, rect.y + 8))
        
        # COLUNA 3: MAPAS
        x3, y3 = 530, 80
        label3 = fonts['medium'].render('🗺️ Mapas', True, COLOR_TEXT)
        screen.blit(label3, (x3, y3))
        
        for idx, mapa in enumerate(mapas_db[:6]):  # Máximo 6
            rect = pygame.Rect(x3, y3 + 40 + idx*50, 220, 45)
            
            is_selected = mapa['id'] == selected_map
            color = (0, 100, 200) if is_selected else (100, 100, 100)
            
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, COLOR_TEXT, rect, 2, border_radius=5)
            
            txt = fonts['small'].render(mapa['nome'][:18], True, COLOR_TEXT)
            screen.blit(txt, (rect.x + 10, rect.y + 12))
            
            if is_selected:
                check_txt = fonts['medium'].render('✓', True, (0, 150, 255))
                screen.blit(check_txt, (rect.x + 190, rect.y + 8))
        
        # RESUMO DA SELEÇÃO
        resumo_y = 420
        resumo_bg = pygame.Rect(30, resumo_y, WIDTH - 60, 80)
        pygame.draw.rect(screen, (50, 50, 70), resumo_bg, border_radius=10)
        pygame.draw.rect(screen, COLOR_TEXT, resumo_bg, 2, border_radius=10)
        
        resumo_lines = [
            f"✓ {len(selected_personagens)} personagens selecionados",
            f"⚔️ {len(selected_armas)} armas selecionadas",
            f"🗺️ {1 if selected_map else 0} mapa selecionado"
        ]
        
        for i, line in enumerate(resumo_lines):
            txt = fonts['small'].render(line, True, COLOR_TEXT)
            screen.blit(txt, (50, resumo_y + 15 + i*22))
        
        # BOTÃO INICIAR
        can_start = len(selected_personagens) >= 2 and selected_map is not None
        btn_start = pygame.Rect(WIDTH//2 - 150, 520, 300, 60)
        
        if can_start:
            draw_button(screen, '▶️ INICIAR SIMULAÇÃO', btn_start, fonts['large'],
                       color=COLOR_SUCCESS, hover=is_mouse_over(btn_start, mouse_pos))
        else:
            pygame.draw.rect(screen, (80, 80, 80), btn_start, border_radius=5)
            pygame.draw.rect(screen, (120, 120, 120), btn_start, 2, border_radius=5)
            txt = fonts['medium'].render('Selecione 2+ personagens e 1 mapa', True, (150, 150, 150))
            txt_rect = txt.get_rect(center=btn_start.center)
            screen.blit(txt, txt_rect)
        
        # INFORMAÇÕES
        info_lines = [
            "Clique para selecionar/desselecionar",
            "Mínimo: 2 personagens + 1 mapa | ESC para voltar"
        ]
        draw_info_box(screen, info_lines, fonts['small'], y=HEIGHT-50)
        
        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Botão voltar
                if back_rect.collidepoint(event.pos):
                    running = False
                
                # Botão iniciar
                elif can_start and btn_start.collidepoint(event.pos):
                    from Paginas.main_simulation import run_simulation
                    run_simulation(selected_map, list(selected_personagens), 
                                 list(selected_armas), screen, fonts)
                    # Limpa seleções após simulação
                    selected_personagens.clear()
                    selected_armas.clear()
                    selected_map = None
                
                # Seleção de personagens
                else:
                    for idx, personagem in enumerate(personagens_ativos[:6]):
                        rect = pygame.Rect(x1, y1 + 40 + idx*50, 220, 45)
                        if rect.collidepoint(event.pos):
                            if personagem['id'] in selected_personagens:
                                selected_personagens.remove(personagem['id'])
                            else:
                                selected_personagens.add(personagem['id'])
                            break
                    
                    # Seleção de armas
                    for idx, arma in enumerate(armas_db):
                        rect = pygame.Rect(x2, y2 + 55 + idx*50, 220, 45)
                        if rect.collidepoint(event.pos):
                            if arma['id'] in selected_armas:
                                selected_armas.remove(arma['id'])
                            else:
                                selected_armas.add(arma['id'])
                            break
                    
                    # Seleção de mapas (apenas 1)
                    for idx, mapa in enumerate(mapas_db[:6]):
                        rect = pygame.Rect(x3, y3 + 40 + idx*50, 220, 45)
                        if rect.collidepoint(event.pos):
                            selected_map = mapa['id']
                            break
        
        pygame.display.flip()
        clock.tick(FPS)
