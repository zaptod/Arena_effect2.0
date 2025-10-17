"""
Simulação Principal - Versão Reestruturada com IA Neural
Motor de simulação com personagens, armas, mapas e controles completos
Sistema de IA: Redes neurais controlam movimentos e ataques
"""
import pygame
import random
import sys
import os

from utils import (
    WIDTH, HEIGHT, FPS, COLOR_BG, COLOR_TEXT, COLOR_BUTTON,
    COLOR_SUCCESS, COLOR_DANGER, draw_button, is_mouse_over,
    draw_info_box, format_time, load_module_function
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa sistema de IA
try:
    from ia import RedeNeuralPersonagem
    IA_DISPONIVEL = True
except ImportError:
    print("⚠️ Módulo IA não disponível. Instale numpy: pip install numpy")
    IA_DISPONIVEL = False

# Importa sistema de colisão de armas
try:
    from colisao_armas import processar_colisoes_armas
    COLISAO_ARMAS_DISPONIVEL = True
except ImportError:
    print("⚠️ Sistema de colisão de armas não disponível")
    COLISAO_ARMAS_DISPONIVEL = False

def load_personagem(personagem_id):
    """Carrega um personagem pelo ID"""
    personagens_dir = os.path.join(os.path.dirname(__file__), '..', 'personagens')
    fname = f'personagem{personagem_id}.py'
    fpath = os.path.join(personagens_dir, fname)
    criar_personagem = load_module_function(fpath, 'criar_personagem')
    return criar_personagem

def load_arma(arma_id):
    """Carrega uma arma pelo ID"""
    armas_dir = os.path.join(os.path.dirname(__file__), '..', 'armas')
    fname = f'arma{arma_id}.py'
    fpath = os.path.join(armas_dir, fname)
    
    if not os.path.exists(fpath):
        return None
    
    criar_arma = load_module_function(fpath, 'criar_arma')
    return criar_arma(arma_id)

def load_mapa(mapa_id):
    """Carrega função de desenho do mapa"""
    mapas_dir = os.path.join(os.path.dirname(__file__), '..', 'mapas')
    fname = f'mapa{mapa_id}.py'
    fpath = os.path.join(mapas_dir, fname)
    desenhar_mapa = load_module_function(fpath, 'desenhar_mapa')
    return desenhar_mapa

# ========== FUNÇÕES DE FÍSICA ==========

def update_personagem(personagem, dt, width=WIDTH, height=HEIGHT):
    """Atualiza posição do personagem com controle de IA"""
    # Aplica movimento baseado em velocidade
    personagem.x += personagem.vx * dt
    personagem.y += personagem.vy * dt
    
    # Mantém dentro dos limites
    if personagem.x < personagem.tamanho:
        personagem.x = personagem.tamanho
        personagem.vx = 0
    elif personagem.x > width - personagem.tamanho:
        personagem.x = width - personagem.tamanho
        personagem.vx = 0
    
    if personagem.y < personagem.tamanho:
        personagem.y = personagem.tamanho
        personagem.vy = 0
    elif personagem.y > height - personagem.tamanho:
        personagem.y = height - personagem.tamanho
        personagem.vy = 0

def check_collision(p1, p2):
    """Verifica colisão entre dois personagens"""
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = (dx*dx + dy*dy)**0.5
    return dist < (p1.tamanho + p2.tamanho)

def handle_collision(p1, p2):
    """Trata colisão entre personagens - Empurrão sem dano"""
    # Colisão corpo a corpo apenas empurra, NÃO causa dano
    # Dano é causado apenas pelas ARMAS
    
    # Calcula vetor de separação
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dist = (dx*dx + dy*dy)**0.5
    
    if dist > 0:
        # Normaliza
        dx /= dist
        dy /= dist
        
        # Separa os personagens
        overlap = (p1.tamanho + p2.tamanho) - dist
        p1.x -= dx * overlap * 0.5
        p1.y -= dy * overlap * 0.5
        p2.x += dx * overlap * 0.5
        p2.y += dy * overlap * 0.5

def salvar_redes_neurais(personagens, vencedores):
    """Salva as redes neurais com fitness atualizado após combate"""
    try:
        for personagem in personagens:
            if hasattr(personagem, 'rede_neural') and personagem.rede_neural is not None:
                # Atualiza vitórias/derrotas
                if personagem in vencedores:
                    personagem.rede_neural.vitorias += 1
                else:
                    personagem.rede_neural.derrotas += 1
                
                # Salva a rede neural
                caminho_rede = os.path.join('redes_neurais', f'rede_personagem_{personagem.id}.json')
                personagem.rede_neural.salvar(caminho_rede)
                print(f"✅ Rede neural do personagem {personagem.nome} salva com fitness: {personagem.rede_neural.calcular_fitness():.2f}")
    except Exception as e:
        print(f"⚠️ Erro ao salvar redes neurais: {e}")

def aplicar_ia_personagem(personagem, outros_personagens, width=WIDTH, height=HEIGHT):
    """Aplica decisões da rede neural ao personagem"""
    if not hasattr(personagem, 'rede_neural') or personagem.rede_neural is None:
        return
    
    # IA decide ação
    acao = personagem.rede_neural.decidir_acao(personagem, outros_personagens, width, height)
    
    # Aplica movimento
    personagem.vx = acao['mover_x'] * personagem.velocidade
    personagem.vy = acao['mover_y'] * personagem.velocidade
    
    # Armazena decisão de ataque
    personagem.ia_atacar = acao['atacar']
    personagem.ia_fugir = acao['fugir']
    
    # Armazena ângulo da arma decidido pela IA
    personagem.ia_angulo_arma = acao.get('angulo_arma', 0)

# ========== SIMULAÇÃO PRINCIPAL ==========

def run_simulation(selected_map_id, selected_personagem_ids, selected_arma_ids, screen, fonts):
    """Executa a simulação principal"""
    clock = pygame.time.Clock()
    
    # Carrega mapa
    desenhar_mapa = load_mapa(selected_map_id)
    
    # Cria personagens
    personagens = []
    personagens_originais = []  # Guarda referência para salvar no final
    armas_list = list(selected_arma_ids) if selected_arma_ids else []
    
    for idx, personagem_id in enumerate(selected_personagem_ids):
        x = random.randint(60, WIDTH - 60)
        y = random.randint(60, HEIGHT - 60)
        
        criar_personagem = load_personagem(personagem_id)
        personagem = criar_personagem(personagem_id, x, y)
        
        # Equipa arma
        if armas_list:
            arma_id = armas_list[idx % len(armas_list)]
            personagem.arma = load_arma(arma_id)
        else:
            personagem.arma = None
        
        # Carrega rede neural (IA) - específica por arma
        if IA_DISPONIVEL:
            try:
                # Tenta carregar rede específica para esta arma
                if idx < len(selected_arma_ids):
                    arma_atual = selected_arma_ids[idx]
                    caminho_rede_arma = os.path.join(
                        os.path.dirname(__file__), '..', 'redes_neurais',
                        f'rede_personagem_{personagem_id}_arma_{arma_atual}.json'
                    )
                    
                    if os.path.exists(caminho_rede_arma):
                        personagem.rede_neural = RedeNeuralPersonagem.carregar(caminho_rede_arma)
                        print(f"🧠⚔️ IA especializada carregada: Personagem {personagem_id} + Arma {arma_atual}")
                    else:
                        # Cria nova rede neural específica para esta arma
                        personagem.rede_neural = RedeNeuralPersonagem(personagem_id, arma_atual)
                        print(f"🧠⚔️ Nova IA especializada criada: Personagem {personagem_id} + Arma {arma_atual}")
                else:
                    # Sem arma - usa rede genérica
                    caminho_rede = os.path.join(
                        os.path.dirname(__file__), '..', 'redes_neurais',
                        f'rede_personagem_{personagem_id}.json'
                    )
                    if os.path.exists(caminho_rede):
                        personagem.rede_neural = RedeNeuralPersonagem.carregar(caminho_rede)
                        print(f"🧠 IA genérica carregada: Personagem {personagem_id}")
                    else:
                        personagem.rede_neural = RedeNeuralPersonagem(personagem_id)
                        print(f"🧠 Nova IA genérica criada: Personagem {personagem_id}")
            except Exception as e:
                print(f"⚠️ Erro ao carregar IA do personagem {personagem_id}: {e}")
                personagem.rede_neural = None
        else:
            personagem.rede_neural = None
        
        # Inicializa atributos de IA
        personagem.ia_atacar = False
        personagem.ia_fugir = False
        
        personagens.append(personagem)
        personagens_originais.append(personagem)  # Mantém referência original
    
    # Estado da simulação
    running = True
    paused = False
    tempo_total = 0
    show_stats = True
    
    while running:
        dt = clock.tick(FPS) / 16.67  # Normalizado para 60 FPS
        dt_seconds = dt / 60.0
        
        if not paused:
            tempo_total += dt_seconds
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Desenha fundo e mapa
        screen.fill(COLOR_BG)
        desenhar_mapa(screen)
        
        # Atualiza e desenha personagens
        if not paused:
            for personagem in personagens:
                # Aplica IA se disponível
                if IA_DISPONIVEL:
                    aplicar_ia_personagem(personagem, personagens, WIDTH, HEIGHT)
                
                update_personagem(personagem, dt, WIDTH, HEIGHT)
                
                # Verifica se IA quer atacar
                if IA_DISPONIVEL and hasattr(personagem, 'ia_atacar') and personagem.ia_atacar:
                    if hasattr(personagem, 'arma') and personagem.arma and personagem.arma.pode_atacar():
                        personagem.arma.atacar()
                
                # Atualiza arma
                if hasattr(personagem, 'arma') and personagem.arma:
                    personagem.arma.update(dt_seconds)
            
            # Verifica ataques com arma (depois de atualizar todos)
            for atacante in personagens:
                if not hasattr(atacante, 'arma') or not atacante.arma:
                    continue
                
                # Verifica se está atacando (cooldown ativo = acabou de atacar)
                if atacante.arma.cooldown > 0 and atacante.arma.cooldown > (1.0 / atacante.arma.velocidade_ataque - 0.1):
                    # Verifica cada possível alvo
                    for alvo in personagens:
                        if alvo.id == atacante.id:  # Não ataca a si mesmo
                            continue
                        
                        # Verifica se a arma acertou o alvo
                        if atacante.arma.verificar_hit(atacante.x, atacante.y, alvo.x, alvo.y, alvo.tamanho):
                            # Aplica dano da arma
                            dano = atacante.arma.dano
                            alvo.receber_dano(dano)
                            
                            # Registra dano para fitness da IA
                            if hasattr(atacante, 'rede_neural') and atacante.rede_neural:
                                atacante.rede_neural.dano_causado += dano
                            
                            if hasattr(alvo, 'rede_neural') and alvo.rede_neural:
                                alvo.rede_neural.dano_recebido += dano
                            
                            # Feedback visual (opcional - pode adicionar depois)
                            print(f"⚔️ {atacante.nome} acertou {alvo.nome} com {atacante.arma.nome}! (-{dano} HP)")
        
        # Remove personagens mortos
        if not paused:
            personagens = [p for p in personagens if getattr(p, 'vivo', True)]
        
        # Desenha personagens e armas
        for personagem in personagens:
            if not getattr(personagem, 'vivo', True):
                continue
                
            # Desenha personagem
            pygame.draw.circle(screen, personagem.cor, 
                             (int(personagem.x), int(personagem.y)), personagem.tamanho)
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(personagem.x), int(personagem.y)), personagem.tamanho, 2)
            
            # Desenha barra de vida
            if hasattr(personagem, 'vida_atual') and hasattr(personagem, 'vida_maxima'):
                barra_width = 50
                barra_height = 5
                barra_x = personagem.x - barra_width // 2
                barra_y = personagem.y - personagem.tamanho - 15
                
                # Fundo da barra (vermelho)
                pygame.draw.rect(screen, (200, 0, 0), 
                               (int(barra_x), int(barra_y), barra_width, barra_height))
                
                # Barra de vida (verde)
                vida_percent = personagem.vida_atual / personagem.vida_maxima
                barra_vida_width = int(barra_width * vida_percent)
                cor_vida = (0, 255, 0) if vida_percent > 0.5 else (255, 255, 0) if vida_percent > 0.2 else (255, 0, 0)
                pygame.draw.rect(screen, cor_vida,
                               (int(barra_x), int(barra_y), barra_vida_width, barra_height))
                
                # Borda da barra
                pygame.draw.rect(screen, (255, 255, 255),
                               (int(barra_x), int(barra_y), barra_width, barra_height), 1)
                
                # Texto de vida
                vida_text = fonts['small'].render(f"{int(personagem.vida_atual)}", True, (255, 255, 255))
                vida_rect = vida_text.get_rect(center=(int(personagem.x), int(barra_y - 10)))
                screen.blit(vida_text, vida_rect)
            
            # Desenha arma
            if hasattr(personagem, 'arma') and personagem.arma:
                # Se a IA definiu um ângulo, usa ele; senão mira no alvo
                if hasattr(personagem, 'ia_angulo_arma'):
                    # IA controla o ângulo da arma
                    personagem.arma.draw(screen, personagem.x, personagem.y, angulo_direto=personagem.ia_angulo_arma)
                else:
                    # Sem IA: mira no alvo mais próximo (modo manual/padrão)
                    target_x, target_y = None, None
                    min_dist = float('inf')
                    
                    for outro in personagens:
                        if outro is not personagem and getattr(outro, 'vivo', True):
                            dx = outro.x - personagem.x
                            dy = outro.y - personagem.y
                            dist = (dx*dx + dy*dy)**0.5
                            if dist < min_dist:
                                min_dist = dist
                                target_x, target_y = outro.x, outro.y
                    
                    personagem.arma.draw(screen, personagem.x, personagem.y, target_x, target_y)
        
        # Colisões
        if not paused:
            for i, p1 in enumerate(personagens):
                for p2 in personagens[i+1:]:
                    if check_collision(p1, p2):
                        handle_collision(p1, p2)
            
            # Colisão entre armas (ricochete)
            if COLISAO_ARMAS_DISPONIVEL:
                colisoes_armas = processar_colisoes_armas(personagens)
                # Opcional: exibir contador de ricochetes (comentado por padrão)
                # if colisoes_armas > 0:
                #     print(f"⚔️ {colisoes_armas} ricochete(s) detectado(s)!")
        
        # ========== UI ==========
        
        # Botões de controle
        btn_pause = pygame.Rect(10, 10, 100, 40)
        btn_reset = pygame.Rect(120, 10, 100, 40)
        btn_exit = pygame.Rect(WIDTH - 110, 10, 100, 40)
        
        pause_text = 'Continuar' if paused else 'Pausar'
        draw_button(screen, pause_text, btn_pause, fonts['small'],
                   color=COLOR_SUCCESS if paused else COLOR_BUTTON,
                   hover=is_mouse_over(btn_pause, mouse_pos))
        
        draw_button(screen, 'Reiniciar', btn_reset, fonts['small'],
                   color=COLOR_WARNING, hover=is_mouse_over(btn_reset, mouse_pos))
        
        draw_button(screen, 'Sair', btn_exit, fonts['small'],
                   color=COLOR_DANGER, hover=is_mouse_over(btn_exit, mouse_pos))
        
        # Estatísticas
        if show_stats:
            vivos = len([p for p in personagens if getattr(p, 'vivo', True)])
            total = len(personagens)
            
            stats_lines = [
                f"⏱️ Tempo: {format_time(tempo_total)}",
                f"� Vivos: {vivos} / {total}",
                f"⚔️ Armas: {len([p for p in personagens if hasattr(p, 'arma') and p.arma])}",
                f"🎮 FPS: {int(clock.get_fps())}"
            ]
            draw_info_box(screen, stats_lines, fonts['small'], x=10, y=HEIGHT-120)
        
        # Verifica vitória (apenas 1 vivo)
        vivos_final = [p for p in personagens if getattr(p, 'vivo', True)]
        if len(vivos_final) <= 1 and len(personagens) > 1:
            # Overlay de vitória
            victory_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            victory_overlay.fill((0, 0, 0, 150))
            screen.blit(victory_overlay, (0, 0))
            
            if len(vivos_final) == 1:
                vencedor = vivos_final[0]
                victory_txt = fonts['title'].render(f'🏆 {vencedor.nome} VENCEU!', True, (255, 215, 0))
            else:
                victory_txt = fonts['title'].render('⚔️ EMPATE!', True, (200, 200, 200))
            
            victory_rect = victory_txt.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(victory_txt, victory_rect)
            
            # Instruções
            inst_txt = fonts['medium'].render('Pressione R para reiniciar ou ESC para sair', True, COLOR_TEXT)
            inst_rect = inst_txt.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
            screen.blit(inst_txt, inst_rect)
        
        # Indicador de pausa
        if paused:
            pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 100))
            screen.blit(pause_overlay, (0, 0))
            
            pause_txt = fonts['title'].render('|| PAUSADO', True, (255, 255, 0))
            pause_rect = pause_txt.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(pause_txt, pause_rect)
        
        # Instruções
        if paused:
            instructions = [
                "ESPAÇO: Continuar",
                "R: Reiniciar",
                "ESC: Sair"
            ]
            for i, txt in enumerate(instructions):
                inst_surface = fonts['small'].render(txt, True, COLOR_TEXT)
                inst_rect = inst_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 60 + i*25))
                screen.blit(inst_surface, inst_rect)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # Reinicia simulação
                    return run_simulation(selected_map_id, selected_personagem_ids,
                                        selected_arma_ids, screen, fonts)
                elif event.key == pygame.K_s:
                    show_stats = not show_stats
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause.collidepoint(event.pos):
                    paused = not paused
                elif btn_reset.collidepoint(event.pos):
                    return run_simulation(selected_map_id, selected_personagem_ids,
                                        selected_arma_ids, screen, fonts)
                elif btn_exit.collidepoint(event.pos):
                    running = False
        
        pygame.display.flip()
    
    # Salva as redes neurais ao final da simulação
    if IA_DISPONIVEL:
        salvar_redes_neurais(personagens_originais, vivos_final)

COLOR_WARNING = (200, 150, 0)  # Adiciona cor que faltava
