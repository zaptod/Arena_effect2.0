"""
Visualizador de Armas - Versão Reestruturada
Interface para visualizar armas disponíveis
"""
import pygame
import sys
import os

from utils import (
    WIDTH, HEIGHT, FPS, COLOR_BG_LIGHT, COLOR_TEXT, COLOR_BUTTON,
    draw_button, draw_back_button, draw_title, is_mouse_over, draw_info_box
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bases_de_dados.Banco_de_dados_armas import armas_db

def load_arma_visual(arma_id):
    """Carrega uma arma para visualização"""
    import importlib.util
    armas_dir = os.path.join(os.path.dirname(__file__), '..', 'armas')
    fname = f'arma{arma_id}.py'
    fpath = os.path.join(armas_dir, fname)
    
    if not os.path.exists(fpath):
        return None
    
    spec = importlib.util.spec_from_file_location(f'arma{arma_id}', fpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.criar_arma(arma_id)

def show_armas_carousel(screen, fonts):
    """Exibe carrossel de armas"""
    clock = pygame.time.Clock()
    arma_atual = 0
    running = True
    
    # Carrega primeira arma
    arma_obj = load_arma_visual(armas_db[arma_atual]['id'])
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLOR_BG_LIGHT)
        
        # Botão voltar
        back_rect = draw_back_button(screen, fonts['medium'])
        
        # Título
        draw_title(screen, 'Armas Disponíveis', fonts['large'], 50)
        
        # Informações da arma atual
        arma = armas_db[arma_atual]
        y_info = 120
        
        # Nome
        nome_txt = fonts['large'].render(arma['nome'], True, COLOR_TEXT)
        nome_rect = nome_txt.get_rect(center=(WIDTH//2, y_info))
        screen.blit(nome_txt, nome_rect)
        
        # Stats
        stats = [
            f"Dano: {arma['dano']}",
            f"Alcance: {arma['alcance']}",
            f"Velocidade Ataque: {arma['velocidade_ataque']}",
            f"Descrição: {arma['descricao']}"
        ]
        
        for i, stat in enumerate(stats):
            stat_txt = fonts['medium'].render(stat, True, COLOR_TEXT)
            stat_rect = stat_txt.get_rect(center=(WIDTH//2, y_info + 50 + i*35))
            screen.blit(stat_txt, stat_rect)
        
        # Visualização da arma
        if arma_obj:
            # Desenha círculo representando personagem
            personagem_x, personagem_y = WIDTH//2, 350
            pygame.draw.circle(screen, (0, 255, 0), (personagem_x, personagem_y), 30)
            pygame.draw.circle(screen, COLOR_TEXT, (personagem_x, personagem_y), 30, 2)
            
            # Desenha arma
            target_x, target_y = pygame.mouse.get_pos()
            arma_obj.draw(screen, personagem_x, personagem_y, target_x, target_y)
            
            # Ícone
            arma_obj.draw_icon(screen, WIDTH//2, 450, size=60)
        
        # Botões de navegação
        btn_prev = pygame.Rect(100, HEIGHT//2 - 25, 100, 50)
        btn_next = pygame.Rect(WIDTH - 200, HEIGHT//2 - 25, 100, 50)
        
        draw_button(screen, '◀ Anterior', btn_prev, fonts['medium'],
                   hover=is_mouse_over(btn_prev, mouse_pos))
        draw_button(screen, 'Próxima ▶', btn_next, fonts['medium'],
                   hover=is_mouse_over(btn_next, mouse_pos))
        
        # Indicador de página
        page_txt = fonts['small'].render(f"{arma_atual + 1} / {len(armas_db)}", True, COLOR_TEXT)
        page_rect = page_txt.get_rect(center=(WIDTH//2, HEIGHT - 80))
        screen.blit(page_txt, page_rect)
        
        # Informações
        info_lines = [
            "Use o mouse para apontar a arma",
            "← → para navegar | ESC para voltar"
        ]
        draw_info_box(screen, info_lines, fonts['small'], y=HEIGHT-60)
        
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
                    arma_atual = (arma_atual + 1) % len(armas_db)
                    arma_obj = load_arma_visual(armas_db[arma_atual]['id'])
                elif event.key == pygame.K_LEFT:
                    arma_atual = (arma_atual - 1) % len(armas_db)
                    arma_obj = load_arma_visual(armas_db[arma_atual]['id'])
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False
                elif btn_prev.collidepoint(event.pos):
                    arma_atual = (arma_atual - 1) % len(armas_db)
                    arma_obj = load_arma_visual(armas_db[arma_atual]['id'])
                elif btn_next.collidepoint(event.pos):
                    arma_atual = (arma_atual + 1) % len(armas_db)
                    arma_obj = load_arma_visual(armas_db[arma_atual]['id'])
        
        pygame.display.flip()
        clock.tick(FPS)
