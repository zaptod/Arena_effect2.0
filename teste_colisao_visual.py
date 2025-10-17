"""
🎯 TESTE VISUAL - Sistema de Colisão de Armas

Este script demonstra visualmente a diferença entre:
- ANTES: Colisão no centro do personagem (incorreto)
- DEPOIS: Colisão na ponta da arma (correto)
"""

import pygame
import math
import sys

# Inicializa pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Teste de Colisão - Armas')
clock = pygame.time.Clock()

# Cores
COLOR_BG = (20, 20, 30)
COLOR_PLAYER = (100, 200, 255)
COLOR_TARGET = (255, 100, 100)
COLOR_WEAPON = (200, 200, 200)
COLOR_HIT_OLD = (255, 0, 0)
COLOR_HIT_NEW = (0, 255, 0)
COLOR_TEXT = (255, 255, 255)

# Fonte
font_title = pygame.font.SysFont(None, 36)
font_text = pygame.font.SysFont(None, 24)
font_small = pygame.font.SysFont(None, 18)

# Personagens
player_x, player_y = 200, HEIGHT // 2
target_x, target_y = 500, HEIGHT // 2
player_size = 20
target_size = 20

# Arma
weapon_offset = 25
weapon_length = 100  # Alcance da espada
weapon_angle = 0

# Estado
running = True
modo_comparacao = True

print("=" * 60)
print("🎯 TESTE VISUAL - COLISÃO DE ARMAS")
print("=" * 60)
print("\n📋 Controles:")
print("   SETAS: Mover personagem")
print("   ESPAÇO: Alternar modo (Antigo/Novo)")
print("   R: Resetar posições")
print("   ESC: Sair")
print("\n🎮 Observe:")
print("   CÍRCULO VERMELHO: Sistema antigo (centro do personagem)")
print("   CÍRCULO VERDE: Sistema novo (ponta da arma)")
print("=" * 60)

while running:
    dt = clock.tick(60) / 1000.0
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                modo_comparacao = not modo_comparacao
            elif event.key == pygame.K_r:
                player_x, player_y = 200, HEIGHT // 2
                target_x, target_y = 500, HEIGHT // 2
    
    # Movimento do personagem
    keys = pygame.key.get_pressed()
    speed = 200 * dt
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_UP]:
        player_y -= speed
    if keys[pygame.K_DOWN]:
        player_y += speed
    
    # Calcula ângulo da arma apontando para o alvo
    dx = target_x - player_x
    dy = target_y - player_y
    weapon_angle = math.atan2(dy, dx)
    
    # ========== SISTEMA ANTIGO (INCORRETO) ==========
    # Distância do CENTRO do personagem até o alvo
    dist_center = math.sqrt(dx*dx + dy*dy)
    alcance_total_old = weapon_length + target_size
    hit_old = dist_center <= alcance_total_old
    
    # ========== SISTEMA NOVO (CORRETO) ==========
    # Posição da PONTA da arma
    weapon_tip_x = player_x + math.cos(weapon_angle) * (weapon_offset + weapon_length)
    weapon_tip_y = player_y + math.sin(weapon_angle) * (weapon_offset + weapon_length)
    
    # Distância da PONTA da arma até o alvo
    tip_dx = target_x - weapon_tip_x
    tip_dy = target_y - weapon_tip_y
    dist_tip = math.sqrt(tip_dx*tip_dx + tip_dy*tip_dy)
    hit_new = dist_tip <= target_size
    
    # ========== DESENHO ==========
    screen.fill(COLOR_BG)
    
    # Título
    title = font_title.render("TESTE DE COLISÃO - ARMAS", True, COLOR_TEXT)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Modo atual
    modo_text = "Modo: " + ("COMPARAÇÃO" if modo_comparacao else "SISTEMA NOVO")
    modo_surface = font_text.render(modo_text, True, (255, 255, 0))
    screen.blit(modo_surface, (20, 70))
    
    # ========== SISTEMA ANTIGO (VERMELHO) ==========
    if modo_comparacao:
        # Círculo de alcance antigo (centro do personagem)
        pygame.draw.circle(screen, COLOR_HIT_OLD, 
                          (int(player_x), int(player_y)), 
                          int(alcance_total_old), 2)
        
        # Indicador de colisão antiga
        if hit_old:
            pygame.draw.line(screen, COLOR_HIT_OLD,
                           (int(player_x), int(player_y)),
                           (int(target_x), int(target_y)), 2)
            status_old = font_text.render("ANTIGO: HIT!", True, COLOR_HIT_OLD)
        else:
            status_old = font_text.render("ANTIGO: MISS", True, (100, 100, 100))
        screen.blit(status_old, (20, 100))
    
    # ========== SISTEMA NOVO (VERDE) ==========
    # Círculo de alcance novo (ponta da arma)
    pygame.draw.circle(screen, COLOR_HIT_NEW, 
                      (int(weapon_tip_x), int(weapon_tip_y)), 
                      int(target_size), 2)
    
    # Indicador de colisão nova
    if hit_new:
        pygame.draw.line(screen, COLOR_HIT_NEW,
                       (int(weapon_tip_x), int(weapon_tip_y)),
                       (int(target_x), int(target_y)), 2)
        status_new = font_text.render("NOVO: HIT!", True, COLOR_HIT_NEW)
    else:
        status_new = font_text.render("NOVO: MISS", True, (100, 100, 100))
    
    y_offset = 130 if modo_comparacao else 100
    screen.blit(status_new, (20, y_offset))
    
    # ========== ARMA ==========
    # Base da arma (próximo ao personagem)
    weapon_base_x = player_x + math.cos(weapon_angle) * weapon_offset
    weapon_base_y = player_y + math.sin(weapon_angle) * weapon_offset
    
    # Desenha arma (linha da base até a ponta)
    pygame.draw.line(screen, COLOR_WEAPON,
                    (int(weapon_base_x), int(weapon_base_y)),
                    (int(weapon_tip_x), int(weapon_tip_y)), 4)
    
    # Desenha ponta da arma (destaque)
    pygame.draw.circle(screen, (255, 255, 0), 
                      (int(weapon_tip_x), int(weapon_tip_y)), 5)
    
    # ========== PERSONAGEM ==========
    pygame.draw.circle(screen, COLOR_PLAYER, 
                      (int(player_x), int(player_y)), player_size)
    pygame.draw.circle(screen, (255, 255, 255), 
                      (int(player_x), int(player_y)), player_size, 2)
    
    # ========== ALVO ==========
    pygame.draw.circle(screen, COLOR_TARGET, 
                      (int(target_x), int(target_y)), target_size)
    pygame.draw.circle(screen, (255, 255, 255), 
                      (int(target_x), int(target_y)), target_size, 2)
    
    # ========== INFORMAÇÕES ==========
    info_y = HEIGHT - 120
    
    # Distâncias
    info_texts = [
        f"Distância Centro → Alvo: {dist_center:.1f} px",
        f"Distância Ponta → Alvo: {dist_tip:.1f} px",
        f"",
        f"Alcance Antigo: {alcance_total_old:.1f} px (centro + arma + alvo)",
        f"Alcance Novo: {target_size:.1f} px (apenas tamanho do alvo)",
    ]
    
    for i, text in enumerate(info_texts):
        surface = font_small.render(text, True, COLOR_TEXT)
        screen.blit(surface, (20, info_y + i * 20))
    
    # Controles
    controls = [
        "SETAS: Mover | ESPAÇO: Modo | R: Reset | ESC: Sair"
    ]
    for i, text in enumerate(controls):
        surface = font_small.render(text, True, (150, 150, 150))
        screen.blit(surface, (20, HEIGHT - 30 + i * 20))
    
    # Legenda
    legend_x = WIDTH - 250
    legend_y = 70
    legend_texts = [
        ("Círculo Azul:", COLOR_PLAYER, "Personagem"),
        ("Círculo Vermelho:", COLOR_TARGET, "Alvo"),
        ("Linha Branca:", COLOR_WEAPON, "Arma"),
        ("Círculo Amarelo:", (255, 255, 0), "Ponta da Arma"),
        ("", None, ""),
        ("Círculo Vermelho:", COLOR_HIT_OLD, "Alcance Antigo"),
        ("Círculo Verde:", COLOR_HIT_NEW, "Alcance Novo"),
    ]
    
    for i, (text, color, desc) in enumerate(legend_texts):
        if color:
            pygame.draw.circle(screen, color, (legend_x, legend_y + i * 25), 8)
        surface = font_small.render(f"{text} {desc}", True, COLOR_TEXT)
        screen.blit(surface, (legend_x + 20, legend_y + i * 25 - 8))
    
    # ========== RESULTADO DA COMPARAÇÃO ==========
    if modo_comparacao and hit_old != hit_new:
        if hit_old and not hit_new:
            # Antigo detecta mas novo não (FALSO POSITIVO)
            warning = font_text.render("⚠️ FALSO POSITIVO - Antigo sistema detecta incorretamente!", 
                                      True, (255, 150, 0))
            screen.blit(warning, (WIDTH//2 - warning.get_width()//2, HEIGHT//2 - 50))
        elif not hit_old and hit_new:
            # Novo detecta mas antigo não (raro, mas possível com armas curtas)
            info = font_text.render("✅ Novo sistema mais preciso!", 
                                   True, COLOR_HIT_NEW)
            screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2 - 50))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
