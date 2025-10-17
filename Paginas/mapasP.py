"""
Visualizador de Mapas - Versão Reestruturada
Interface para visualizar mapas disponíveis
"""
import pygame
import sys
import os

from utils import (
    WIDTH, HEIGHT, FPS, COLOR_BG_LIGHT, COLOR_TEXT, COLOR_BUTTON,
    draw_button, draw_back_button, draw_title, is_mouse_over, draw_info_box
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_mapas import mapas_db

def load_mapa_visual(mapa_id):
    """Carrega função de desenho do mapa"""
    import importlib.util
    mapas_dir = os.path.join(os.path.dirname(__file__), '..', 'mapas')
    fname = f'mapa{mapa_id}.py'
    fpath = os.path.join(mapas_dir, fname)
    
    if not os.path.exists(fpath):
        return None
    
    spec = importlib.util.spec_from_file_location(f'mapa{mapa_id}', fpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.desenhar_mapa

def show_mapas_carousel(screen, fonts):
    """Exibe carrossel de mapas"""
    clock = pygame.time.Clock()
    mapa_atual = 0
    running = True
    
    # Cria surface para preview do mapa
    mapa_surface = pygame.Surface((600, 400))
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLOR_BG_LIGHT)
        
        # Botão voltar
        back_rect = draw_back_button(screen, fonts['medium'])
        
        # Título
        draw_title(screen, 'Mapas Disponíveis', fonts['large'], 50)
        
        # Informações do mapa atual
        mapa = mapas_db[mapa_atual]
        
        # Nome do mapa
        nome_txt = fonts['large'].render(mapa['nome'], True, COLOR_TEXT)
        nome_rect = nome_txt.get_rect(center=(WIDTH//2, 100))
        screen.blit(nome_txt, nome_rect)
        
        # Descrição
        if 'descricao' in mapa:
            desc_txt = fonts['small'].render(mapa['descricao'], True, (200, 200, 200))
            desc_rect = desc_txt.get_rect(center=(WIDTH//2, 130))
            screen.blit(desc_txt, desc_rect)
        
        # Preview do mapa
        preview_rect = pygame.Rect(100, 160, 600, 300)
        pygame.draw.rect(screen, (20, 20, 20), preview_rect)
        pygame.draw.rect(screen, COLOR_TEXT, preview_rect, 2)
        
        # Desenha o mapa no preview
        mapa_surface.fill((20, 20, 20))
        desenhar_mapa = load_mapa_visual(mapa['id'])
        if desenhar_mapa:
            try:
                desenhar_mapa(mapa_surface)
            except:
                error_txt = fonts['small'].render("Erro ao carregar mapa", True, (255, 0, 0))
                mapa_surface.blit(error_txt, (200, 180))
        
        # Redimensiona e desenha
        scaled_surface = pygame.transform.scale(mapa_surface, (preview_rect.width - 4, preview_rect.height - 4))
        screen.blit(scaled_surface, (preview_rect.x + 2, preview_rect.y + 2))
        
        # Botões de navegação
        btn_prev = pygame.Rect(100, HEIGHT - 80, 100, 50)
        btn_next = pygame.Rect(WIDTH - 200, HEIGHT - 80, 100, 50)
        
        draw_button(screen, '◀ Anterior', btn_prev, fonts['medium'],
                   hover=is_mouse_over(btn_prev, mouse_pos))
        draw_button(screen, 'Próximo ▶', btn_next, fonts['medium'],
                   hover=is_mouse_over(btn_next, mouse_pos))
        
        # Indicador de página
        page_txt = fonts['small'].render(f"{mapa_atual + 1} / {len(mapas_db)}", True, COLOR_TEXT)
        page_rect = page_txt.get_rect(center=(WIDTH//2, HEIGHT - 55))
        screen.blit(page_txt, page_rect)
        
        # Informações
        info_lines = [
            f"ID: {mapa['id']} | Obstáculos: {mapa.get('obstaculos', 'Padrão')}",
            "← → para navegar | ESC para voltar"
        ]
        draw_info_box(screen, info_lines, fonts['small'], y=470)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT:
                    mapa_atual = (mapa_atual + 1) % len(mapas_db)
                elif event.key == pygame.K_LEFT:
                    mapa_atual = (mapa_atual - 1) % len(mapas_db)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False
                elif btn_prev.collidepoint(event.pos):
                    mapa_atual = (mapa_atual - 1) % len(mapas_db)
                elif btn_next.collidepoint(event.pos):
                    mapa_atual = (mapa_atual + 1) % len(mapas_db)
        
        pygame.display.flip()
        clock.tick(FPS)
