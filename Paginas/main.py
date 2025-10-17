
"""
Arena Effect Simulator - Página Principal
Menu principal com navegação para todas as funcionalidades
"""
import pygame
import sys
import os

# Importa utilitários
from utils import (
    WIDTH, HEIGHT, FPS, COLOR_BG, COLOR_SUCCESS, COLOR_TEXT,
    init_fonts, draw_button, draw_title, is_mouse_over, draw_info_box
)

def main():
    """Função principal do menu"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Arena Effect Simulator 2.0')
    clock = pygame.time.Clock()
    fonts = init_fonts()
    
    # Estado do menu
    running = True
    
    # Botões principais
    buttons = {
        'personagens': pygame.Rect(WIDTH//2 - 150, 140, 300, 50),
        'armas': pygame.Rect(WIDTH//2 - 150, 200, 300, 50),
        'mapas': pygame.Rect(WIDTH//2 - 150, 260, 300, 50),
        'simulation': pygame.Rect(WIDTH//2 - 150, 340, 300, 60),
        'treino': pygame.Rect(WIDTH//2 - 150, 410, 300, 60)
    }
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLOR_BG)
        
        # Título
        draw_title(screen, 'Arena Effect Simulator', fonts['title'], 50)
        
        # Subtítulo
        subtitle = fonts['small'].render('Versão 2.0 - Sistema Completo', True, (150, 150, 150))
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 90))
        screen.blit(subtitle, subtitle_rect)
        
        # Desenha botões com hover effect
        for key, rect in buttons.items():
            hover = is_mouse_over(rect, mouse_pos)
            
            if key == 'personagens':
                draw_button(screen, '👤 Gerenciar Personagens', rect, fonts['medium'], hover=hover)
            elif key == 'armas':
                draw_button(screen, '⚔️ Visualizar Armas', rect, fonts['medium'], hover=hover)
            elif key == 'mapas':
                draw_button(screen, '🗺️ Visualizar Mapas', rect, fonts['medium'], hover=hover)
            elif key == 'simulation':
                draw_button(screen, '▶️ Iniciar Simulação', rect, fonts['medium'], 
                          color=COLOR_SUCCESS, hover=hover)
            elif key == 'treino':
                draw_button(screen, '🔄 Modo Treino Loop (30s)', rect, fonts['medium'], 
                          color=(255, 150, 0), hover=hover)
        
        # Informações na parte inferior
        info_lines = [
            "Personagens: Criar, editar e excluir",
            "Armas: 4 tipos disponíveis",
            "Mapas: Diversos ambientes",
            "Simulação: Combate livre",
            "🔄 Treino Loop: 30s por rodada - Rodadas contínuas para treinar IA"
        ]
        draw_info_box(screen, info_lines, fonts['small'])
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons['personagens'].collidepoint(event.pos):
                    import personagensP
                    personagensP.show_personagens_carousel(screen, fonts)
                    pygame.event.clear()
                    
                elif buttons['armas'].collidepoint(event.pos):
                    import armasP
                    armasP.show_armas_carousel(screen, fonts)
                    pygame.event.clear()
                    
                elif buttons['mapas'].collidepoint(event.pos):
                    import mapasP
                    mapasP.show_mapas_carousel(screen, fonts)
                    pygame.event.clear()
                    
                elif buttons['simulation'].collidepoint(event.pos):
                    import SelectionP
                    SelectionP.show_selection_carousel(screen, fonts)
                    pygame.event.clear()
                
                elif buttons['treino'].collidepoint(event.pos):
                    import modo_treino
                    modo_treino.show_treino_selection(screen, fonts)
                    pygame.event.clear()
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
