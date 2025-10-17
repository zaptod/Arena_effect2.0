"""
Modo Treino - Timer de 30 segundos em LOOP
Sistema automático para treinar redes neurais com rodadas contínuas
"""
import pygame
import sys
import os
import random

# Importa utilitários
from utils import (
    WIDTH, HEIGHT, FPS, COLOR_BG, COLOR_SUCCESS, COLOR_TEXT, COLOR_BUTTON,
    COLOR_DANGER, COLOR_WARNING, init_fonts, draw_button, draw_title, 
    is_mouse_over, load_personagem, load_arma, load_mapa
)

# Tenta importar IA
try:
    from ia import RedeNeuralPersonagem, TreinadorGenetico
    IA_DISPONIVEL = True
except ImportError:
    IA_DISPONIVEL = False
    RedeNeuralPersonagem = None
    TreinadorGenetico = None

def show_treino_selection(screen, fonts):
    """Tela de seleção para modo treino"""
    # Carrega personagens disponíveis
    personagens_dir = os.path.join(os.path.dirname(__file__), '..', 'personagens')
    personagem_files = [f for f in os.listdir(personagens_dir) if f.startswith('personagem') and f.endswith('.py')]
    personagens_ids = sorted([int(f.replace('personagem', '').replace('.py', '')) for f in personagem_files])
    
    # Carrega armas disponíveis
    armas_dir = os.path.join(os.path.dirname(__file__), '..', 'armas')
    arma_files = [f for f in os.listdir(armas_dir) if f.startswith('arma') and f.endswith('.py') and 'backup' not in f]
    armas_ids = sorted([int(f.replace('arma', '').replace('.py', '')) for f in arma_files])
    
    # Carrega mapas disponíveis
    mapas_dir = os.path.join(os.path.dirname(__file__), '..', 'mapas')
    mapa_files = [f for f in os.listdir(mapas_dir) if f.startswith('mapa') and f.endswith('.py')]
    mapas_ids = sorted([int(f.replace('mapa', '').replace('.py', '')) for f in mapa_files])
    
    # Estado da seleção
    personagem1_id = personagens_ids[0] if personagens_ids else None
    personagem2_id = personagens_ids[1] if len(personagens_ids) > 1 else personagens_ids[0]
    arma1_id = armas_ids[0] if armas_ids else None
    arma2_id = armas_ids[1] if len(armas_ids) > 1 else armas_ids[0]
    mapa_id = mapas_ids[0] if mapas_ids else None
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLOR_BG)
        
        # Título
        draw_title(screen, '⏱️ MODO TREINO', fonts['title'], 50)
        
        # Instruções
        instrucoes = [
            "⏱️ Timer: 30 segundos por rodada",
            "🔄 MODO LOOP: Rodadas contínuas automáticas",
            "🧠 Objetivo: Treinar redes neurais através de combates repetidos",
            "⚠️ Punição: -50 HP se o tempo acabar",
            "🏆 Ao final de cada rodada, as redes são salvas e reinicia automaticamente"
        ]
        
        y_offset = 100
        for i, texto in enumerate(instrucoes):
            cor = (255, 215, 0) if i == 0 else (200, 200, 200)
            surface = fonts['small'].render(texto, True, cor)
            rect = surface.get_rect(center=(WIDTH//2, y_offset + i*25))
            screen.blit(surface, rect)
        
        # Seleção de personagens
        y_start = 230
        
        # Personagem 1
        p1_text = fonts['medium'].render(f"Personagem 1: {personagem1_id}", True, COLOR_TEXT)
        screen.blit(p1_text, (50, y_start))
        
        btn_p1_prev = pygame.Rect(50, y_start + 35, 40, 40)
        btn_p1_next = pygame.Rect(100, y_start + 35, 40, 40)
        draw_button(screen, '<', btn_p1_prev, fonts['medium'], hover=is_mouse_over(btn_p1_prev, mouse_pos))
        draw_button(screen, '>', btn_p1_next, fonts['medium'], hover=is_mouse_over(btn_p1_next, mouse_pos))
        
        # Arma 1
        a1_text = fonts['small'].render(f"Arma: {arma1_id}", True, COLOR_TEXT)
        screen.blit(a1_text, (160, y_start + 45))
        
        btn_a1_prev = pygame.Rect(220, y_start + 35, 30, 40)
        btn_a1_next = pygame.Rect(260, y_start + 35, 30, 40)
        draw_button(screen, '<', btn_a1_prev, fonts['small'], hover=is_mouse_over(btn_a1_prev, mouse_pos))
        draw_button(screen, '>', btn_a1_next, fonts['small'], hover=is_mouse_over(btn_a1_next, mouse_pos))
        
        # Personagem 2
        p2_text = fonts['medium'].render(f"Personagem 2: {personagem2_id}", True, COLOR_TEXT)
        screen.blit(p2_text, (WIDTH - 350, y_start))
        
        btn_p2_prev = pygame.Rect(WIDTH - 350, y_start + 35, 40, 40)
        btn_p2_next = pygame.Rect(WIDTH - 300, y_start + 35, 40, 40)
        draw_button(screen, '<', btn_p2_prev, fonts['medium'], hover=is_mouse_over(btn_p2_prev, mouse_pos))
        draw_button(screen, '>', btn_p2_next, fonts['medium'], hover=is_mouse_over(btn_p2_next, mouse_pos))
        
        # Arma 2
        a2_text = fonts['small'].render(f"Arma: {arma2_id}", True, COLOR_TEXT)
        screen.blit(a2_text, (WIDTH - 240, y_start + 45))
        
        btn_a2_prev = pygame.Rect(WIDTH - 180, y_start + 35, 30, 40)
        btn_a2_next = pygame.Rect(WIDTH - 140, y_start + 35, 30, 40)
        draw_button(screen, '<', btn_a2_prev, fonts['small'], hover=is_mouse_over(btn_a2_prev, mouse_pos))
        draw_button(screen, '>', btn_a2_next, fonts['small'], hover=is_mouse_over(btn_a2_next, mouse_pos))
        
        # Seleção de mapa
        mapa_text = fonts['medium'].render(f"Mapa: {mapa_id}", True, COLOR_TEXT)
        screen.blit(mapa_text, (WIDTH//2 - 100, y_start + 100))
        
        btn_m_prev = pygame.Rect(WIDTH//2 + 40, y_start + 95, 40, 40)
        btn_m_next = pygame.Rect(WIDTH//2 + 90, y_start + 95, 40, 40)
        draw_button(screen, '<', btn_m_prev, fonts['medium'], hover=is_mouse_over(btn_m_prev, mouse_pos))
        draw_button(screen, '>', btn_m_next, fonts['medium'], hover=is_mouse_over(btn_m_next, mouse_pos))
        
        # Botões principais
        btn_start = pygame.Rect(WIDTH//2 - 150, HEIGHT - 150, 300, 60)
        btn_back = pygame.Rect(WIDTH//2 - 100, HEIGHT - 70, 200, 40)
        
        draw_button(screen, '🔄 INICIAR TREINO LOOP', btn_start, fonts['medium'], 
                   color=COLOR_SUCCESS, hover=is_mouse_over(btn_start, mouse_pos))
        draw_button(screen, 'Voltar', btn_back, fonts['small'], 
                   color=COLOR_DANGER, hover=is_mouse_over(btn_back, mouse_pos))
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Personagem 1
                if btn_p1_prev.collidepoint(event.pos):
                    idx = personagens_ids.index(personagem1_id)
                    personagem1_id = personagens_ids[(idx - 1) % len(personagens_ids)]
                elif btn_p1_next.collidepoint(event.pos):
                    idx = personagens_ids.index(personagem1_id)
                    personagem1_id = personagens_ids[(idx + 1) % len(personagens_ids)]
                
                # Arma 1
                elif btn_a1_prev.collidepoint(event.pos):
                    idx = armas_ids.index(arma1_id)
                    arma1_id = armas_ids[(idx - 1) % len(armas_ids)]
                elif btn_a1_next.collidepoint(event.pos):
                    idx = armas_ids.index(arma1_id)
                    arma1_id = armas_ids[(idx + 1) % len(armas_ids)]
                
                # Personagem 2
                elif btn_p2_prev.collidepoint(event.pos):
                    idx = personagens_ids.index(personagem2_id)
                    personagem2_id = personagens_ids[(idx - 1) % len(personagens_ids)]
                elif btn_p2_next.collidepoint(event.pos):
                    idx = personagens_ids.index(personagem2_id)
                    personagem2_id = personagens_ids[(idx + 1) % len(personagens_ids)]
                
                # Arma 2
                elif btn_a2_prev.collidepoint(event.pos):
                    idx = armas_ids.index(arma2_id)
                    arma2_id = armas_ids[(idx - 1) % len(armas_ids)]
                elif btn_a2_next.collidepoint(event.pos):
                    idx = armas_ids.index(arma2_id)
                    arma2_id = armas_ids[(idx + 1) % len(armas_ids)]
                
                # Mapa
                elif btn_m_prev.collidepoint(event.pos):
                    idx = mapas_ids.index(mapa_id)
                    mapa_id = mapas_ids[(idx - 1) % len(mapas_ids)]
                elif btn_m_next.collidepoint(event.pos):
                    idx = mapas_ids.index(mapa_id)
                    mapa_id = mapas_ids[(idx + 1) % len(mapas_ids)]
                
                # Iniciar
                elif btn_start.collidepoint(event.pos):
                    run_treino(mapa_id, [personagem1_id, personagem2_id], 
                              [arma1_id, arma2_id], screen, fonts)
                    
                # Voltar
                elif btn_back.collidepoint(event.pos):
                    return
        
        pygame.display.flip()
        clock.tick(FPS)

def run_treino(selected_map_id, selected_personagem_ids, selected_arma_ids, screen, fonts):
    """Executa o modo treino em LOOP com timer de 30 segundos"""
    # Importa funções da simulação principal
    from main_simulation import (
        update_personagem, check_collision, handle_collision,
        aplicar_ia_personagem, salvar_redes_neurais
    )
    
    # Importa sistema de colisão de armas
    try:
        from colisao_armas import processar_colisoes_armas
        COLISAO_ARMAS_DISPONIVEL = True
    except ImportError:
        COLISAO_ARMAS_DISPONIVEL = False
    
    # Importa visualizador de rede neural
    try:
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from visualizador_rede_compacto import criar_visualizador
        VISUALIZADOR_DISPONIVEL = True
    except ImportError:
        VISUALIZADOR_DISPONIVEL = False
        print("⚠️ Visualizador de rede neural não disponível")
    
    clock = pygame.time.Clock()
    
    # Cria visualizador de rede neural (painel lateral)
    visualizador = None
    largura_visualizador = 0
    if VISUALIZADOR_DISPONIVEL and IA_DISPONIVEL:
        try:
            visualizador = criar_visualizador()
            visualizador.inicializar()
            largura_visualizador = visualizador.largura
            print("✅ Visualizador de rede neural iniciado!")
        except Exception as e:
            print(f"⚠️ Erro ao criar visualizador: {e}")
            visualizador = None
            largura_visualizador = 0
    
    # Expande a janela se visualizador estiver ativo
    # IMPORTANTE: A simulação continua usando WIDTH (800px), o visualizador é renderado ao lado
    largura_total = WIDTH + largura_visualizador
    screen = pygame.display.set_mode((largura_total, HEIGHT))
    pygame.display.set_caption('Modo Treino - Arena + Visualizador Neural')
    
    print(f"🖥️  Janela: {largura_total}x{HEIGHT} (Arena: {WIDTH}px + Visualizador: {largura_visualizador}px)")
    
    # Carrega mapa
    desenhar_mapa = load_mapa(selected_map_id)
    
    # Estado do loop de treino
    running = True
    paused = False
    rodada_atual = 1
    total_vitorias = {pid: 0 for pid in selected_personagem_ids}
    total_empates = 0
    
    print(f"🎮 TREINO INICIADO!")
    print(f"   Personagem 1 ID: {selected_personagem_ids[0]}")
    print(f"   Personagem 2 ID: {selected_personagem_ids[1]}")
    print(f"   Arma 1 ID: {selected_arma_ids[0] if selected_arma_ids else 'Nenhuma'}")
    print(f"   Arma 2 ID: {selected_arma_ids[1] if len(selected_arma_ids) > 1 else 'Nenhuma'}")
    print(f"   Mapa ID: {selected_map_id}")
    
    # Função para criar/resetar personagens
    def criar_personagens_treino():
        personagens = []
        personagens_originais = []
        
        for idx, personagem_id in enumerate(selected_personagem_ids):
            x = 200 if idx == 0 else WIDTH - 200
            y = HEIGHT // 2
            
            criar_personagem = load_personagem(personagem_id)
            personagem = criar_personagem(personagem_id, x, y)
            
            # Equipa arma
            if idx < len(selected_arma_ids):
                arma_id = selected_arma_ids[idx]
                personagem.arma = load_arma(arma_id)
            else:
                personagem.arma = None
                arma_id = None
            
            # Carrega rede neural (IA) - específica por arma
            if IA_DISPONIVEL:
                try:
                    if arma_id is not None:
                        # Tenta carregar rede específica para esta arma
                        caminho_rede_arma = os.path.join(
                            os.path.dirname(__file__), '..', 'redes_neurais',
                            f'rede_personagem_{personagem_id}_arma_{arma_id}.json'
                        )
                        
                        if os.path.exists(caminho_rede_arma):
                            personagem.rede_neural = RedeNeuralPersonagem.carregar(caminho_rede_arma)
                        else:
                            # Cria nova rede neural específica para esta arma
                            personagem.rede_neural = RedeNeuralPersonagem(personagem_id, arma_id)
                    else:
                        # Sem arma - usa rede genérica
                        caminho_rede = os.path.join(
                            os.path.dirname(__file__), '..', 'redes_neurais',
                            f'rede_personagem_{personagem_id}.json'
                        )
                        if os.path.exists(caminho_rede):
                            personagem.rede_neural = RedeNeuralPersonagem.carregar(caminho_rede)
                        else:
                            personagem.rede_neural = RedeNeuralPersonagem(personagem_id)
                except Exception as e:
                    print(f"⚠️ Erro ao carregar IA: {e}")
                    personagem.rede_neural = None
            else:
                personagem.rede_neural = None
            
            personagem.ia_atacar = False
            personagem.ia_fugir = False
            
            personagens.append(personagem)
            personagens_originais.append(personagem)
        
        return personagens, personagens_originais
    
    # Cria primeira rodada
    personagens, personagens_originais = criar_personagens_treino()
    
    # Estado da rodada
    tempo_treino = 30.0  # 30 segundos por rodada
    tempo_restante = tempo_treino
    punido = False
    vencedor = None
    tempo_entre_rodadas = 0  # Contador para delay entre rodadas
    
    # Sistema de detecção de inatividade
    tempo_sem_dano = 0.0  # Contador de tempo sem dano
    TIMEOUT_INATIVIDADE = 10.0  # 10 segundos sem dano = empate
    ultimo_dano_causado = False  # Flag para resetar contador
    
    while running:
        dt = clock.tick(FPS) / 16.67
        dt_seconds = dt / 60.0
        
        # Se há vencedor, aguarda antes de iniciar próxima rodada
        if vencedor and not paused:
            tempo_entre_rodadas += dt_seconds
            
            # Após 3 segundos, inicia nova rodada automaticamente
            if tempo_entre_rodadas >= 3.0:
                # Salva resultados
                if vencedor != "EMPATE":
                    print(f"📊 Salvando vitória para {vencedor.nome} (ID: {vencedor.id})")
                    total_vitorias[vencedor.id] += 1
                else:
                    print(f"📊 Salvando EMPATE. Total atual: {total_empates}")
                    total_empates += 1
                
                # Log das estatísticas
                print(f"📈 Estatísticas atuais:")
                print(f"   P1 (ID {selected_personagem_ids[0]}): {total_vitorias[selected_personagem_ids[0]]} vitórias")
                print(f"   P2 (ID {selected_personagem_ids[1]}): {total_vitorias[selected_personagem_ids[1]]} vitórias")
                print(f"   Empates: {total_empates}")
                
                # Salva redes neurais
                if IA_DISPONIVEL:
                    vivos_final = [vencedor] if vencedor != "EMPATE" else []
                    salvar_redes_neurais(personagens_originais, vivos_final)
                
                # Reinicia rodada
                rodada_atual += 1
                personagens, personagens_originais = criar_personagens_treino()
                tempo_restante = tempo_treino
                punido = False
                vencedor = None
                tempo_entre_rodadas = 0
                tempo_sem_dano = 0.0  # Reseta contador de inatividade
                ultimo_dano_causado = False
                print(f"\n🔄 RODADA {rodada_atual} INICIADA!")
        
        if not paused and not vencedor:
            tempo_restante -= dt_seconds
            tempo_sem_dano += dt_seconds  # Incrementa tempo sem dano
            
            # Verifica inatividade (10 segundos sem dano)
            if tempo_sem_dano >= TIMEOUT_INATIVIDADE:
                vencedor = "EMPATE"
                print(f"💤 INATIVIDADE DETECTADA! {tempo_sem_dano:.1f}s sem dano - Rodada encerrada!")
                print("⚔️ EMPATE POR INATIVIDADE!")
            
            # Tempo acabou!
            if tempo_restante <= 0:
                tempo_restante = 0
                if not punido:
                    punido = True
                    # Aplica punição: 50 HP de dano em ambos os personagens vivos
                    for p in personagens:
                        if getattr(p, 'vivo', True):
                            p.receber_dano(50)
                            print(f"⏱️💥 TEMPO ESGOTADO! {p.nome} perdeu 50 HP como punição!")
                    
                    # Verifica vencedor após punição
                    vivos = [p for p in personagens if getattr(p, 'vivo', True)]
                    if len(vivos) == 0:
                        vencedor = "EMPATE"
                        print("⚔️ EMPATE! Ambos foram derrotados.")
                    elif len(vivos) == 1:
                        vencedor = vivos[0]
                        print(f"🏆 {vencedor.nome} VENCEU! (Único sobrevivente)")
                    else:
                        # Ambos vivos, vence quem tem mais HP
                        hp_list = [(p, p.vida_atual) for p in vivos]
                        max_hp = max(hp_list, key=lambda x: x[1])[1]
                        vencedores_potenciais = [p for p, hp in hp_list if hp == max_hp]
                        
                        if len(vencedores_potenciais) > 1:
                            # Empate de HP
                            vencedor = "EMPATE"
                            print(f"⚔️ EMPATE! Ambos têm {max_hp} HP.")
                        else:
                            vencedor = vencedores_potenciais[0]
                            print(f"🏆 {vencedor.nome} VENCEU! ({vencedor.vida_atual} HP vs {[p.vida_atual for p in vivos if p != vencedor][0]} HP)")
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Desenha fundo e mapa
        screen.fill(COLOR_BG)
        desenhar_mapa(screen)
        
        # Atualiza e desenha personagens
        if not paused and not vencedor:
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
            
            # Verifica ataques com arma
            for atacante in personagens:
                if not hasattr(atacante, 'arma') or not atacante.arma:
                    continue
                
                if atacante.arma.cooldown > 0 and atacante.arma.cooldown > (1.0 / atacante.arma.velocidade_ataque - 0.1):
                    for alvo in personagens:
                        if alvo.id == atacante.id:
                            continue
                        
                        if atacante.arma.verificar_hit(atacante.x, atacante.y, alvo.x, alvo.y, alvo.tamanho):
                            dano = atacante.arma.dano
                            alvo.receber_dano(dano)
                            
                            # RESETA CONTADOR DE INATIVIDADE
                            tempo_sem_dano = 0.0
                            ultimo_dano_causado = True
                            
                            if hasattr(atacante, 'rede_neural') and atacante.rede_neural:
                                atacante.rede_neural.dano_causado += dano
                            
                            if hasattr(alvo, 'rede_neural') and alvo.rede_neural:
                                alvo.rede_neural.dano_recebido += dano
        
        # Remove personagens mortos
        if not paused:
            personagens = [p for p in personagens if getattr(p, 'vivo', True)]
        
        # Verifica vencedor (morte)
        vivos_atuais = [p for p in personagens if getattr(p, 'vivo', True)]
        if len(vivos_atuais) <= 1 and not vencedor:
            if len(vivos_atuais) == 1:
                vencedor = vivos_atuais[0]
                print(f"🏆 {vencedor.nome} VENCEU por morte do oponente!")
            else:
                vencedor = "EMPATE"
                print("⚔️ EMPATE! Ambos foram derrotados simultaneamente.")
        
        # Desenha personagens
        for personagem in personagens:
            if not getattr(personagem, 'vivo', True):
                continue
            
            pygame.draw.circle(screen, personagem.cor, 
                             (int(personagem.x), int(personagem.y)), personagem.tamanho)
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(personagem.x), int(personagem.y)), personagem.tamanho, 2)
            
            # Barra de vida
            if hasattr(personagem, 'vida_atual') and hasattr(personagem, 'vida_maxima'):
                barra_width = 50
                barra_height = 5
                barra_x = personagem.x - barra_width // 2
                barra_y = personagem.y - personagem.tamanho - 15
                
                pygame.draw.rect(screen, (200, 0, 0), 
                               (int(barra_x), int(barra_y), barra_width, barra_height))
                
                vida_percent = personagem.vida_atual / personagem.vida_maxima
                barra_vida_width = int(barra_width * vida_percent)
                cor_vida = (0, 255, 0) if vida_percent > 0.5 else (255, 255, 0) if vida_percent > 0.2 else (255, 0, 0)
                pygame.draw.rect(screen, cor_vida,
                               (int(barra_x), int(barra_y), barra_vida_width, barra_height))
                
                pygame.draw.rect(screen, (255, 255, 255),
                               (int(barra_x), int(barra_y), barra_width, barra_height), 1)
                
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
                        if outro.id != personagem.id:
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
                processar_colisoes_armas(personagens)
        
        # ========== UI - TIMER E ESTATÍSTICAS =========
        # Timer no topo (destaque)
        timer_bg = pygame.Rect(WIDTH//2 - 120, 10, 240, 60)
        pygame.draw.rect(screen, (0, 0, 0, 180), timer_bg)
        pygame.draw.rect(screen, (255, 215, 0) if tempo_restante > 10 else (255, 0, 0), timer_bg, 3)
        
        segundos = int(tempo_restante)
        milissegundos = int((tempo_restante % 1) * 100)
        
        timer_text = fonts['title'].render(f"{segundos:02d}.{milissegundos:02d}", True, 
                                          (255, 215, 0) if tempo_restante > 10 else (255, 0, 0))
        timer_rect = timer_text.get_rect(center=(WIDTH//2, 40))
        screen.blit(timer_text, timer_rect)
        
        # Painel de estatísticas (canto superior esquerdo)
        stats_bg = pygame.Rect(10, 80, 200, 100)
        pygame.draw.rect(screen, (0, 0, 0, 150), stats_bg, border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100), stats_bg, 2, border_radius=5)
        
        stats_lines = [
            f"🔄 Rodada: {rodada_atual}",
            f"🏆 P1: {total_vitorias.get(selected_personagem_ids[0], 0)} vitórias",
            f"🏆 P2: {total_vitorias.get(selected_personagem_ids[1], 0)} vitórias",
            f"🤝 Empates: {total_empates}"
        ]
        
        for i, line in enumerate(stats_lines):
            stat_text = fonts['small'].render(line, True, (255, 255, 255))
            screen.blit(stat_text, (20, 90 + i*22))
        
        # Indicador de inatividade (canto superior direito)
        if not vencedor and tempo_sem_dano > 5.0:  # Mostra aviso após 5 segundos
            inatividade_bg = pygame.Rect(WIDTH - 210, 80, 200, 60)
            
            # Cor muda conforme proximidade do timeout
            tempo_restante_inatividade = TIMEOUT_INATIVIDADE - tempo_sem_dano
            if tempo_restante_inatividade <= 2.0:
                cor_borda = (255, 0, 0)  # Vermelho crítico
            elif tempo_restante_inatividade <= 5.0:
                cor_borda = (255, 150, 0)  # Laranja aviso
            else:
                cor_borda = (255, 255, 0)  # Amarelo atenção
            
            pygame.draw.rect(screen, (0, 0, 0, 150), inatividade_bg, border_radius=5)
            pygame.draw.rect(screen, cor_borda, inatividade_bg, 3, border_radius=5)
            
            aviso_text = fonts['small'].render('💤 SEM DANO!', True, (255, 255, 255))
            screen.blit(aviso_text, (WIDTH - 200, 85))
            
            tempo_inativ_text = fonts['medium'].render(f'{tempo_restante_inatividade:.1f}s', True, cor_borda)
            screen.blit(tempo_inativ_text, (WIDTH - 200, 108))
        
        # Botões de controle
        btn_pause = pygame.Rect(10, 10, 100, 40)
        btn_exit = pygame.Rect(WIDTH - 110, 10, 100, 40)
        
        pause_text = 'Continuar' if paused else 'Pausar'
        draw_button(screen, pause_text, btn_pause, fonts['small'],
                   color=COLOR_SUCCESS if paused else COLOR_BUTTON,
                   hover=is_mouse_over(btn_pause, mouse_pos))
        
        draw_button(screen, 'Sair', btn_exit, fonts['small'],
                   color=COLOR_DANGER, hover=is_mouse_over(btn_exit, mouse_pos))
        
        # Overlay de resultado (transitório - 3 segundos)
        if vencedor:
            victory_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            victory_overlay.fill((0, 0, 0, 120))
            screen.blit(victory_overlay, (0, 0))
            
            if vencedor == "EMPATE":
                victory_txt = fonts['title'].render('⚔️ EMPATE!', True, (200, 200, 200))
            else:
                victory_txt = fonts['title'].render(f'🏆 {vencedor.nome} VENCEU!', True, (255, 215, 0))
            
            victory_rect = victory_txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
            screen.blit(victory_txt, victory_rect)
            
            if punido:
                punido_txt = fonts['medium'].render('⏱️ Tempo esgotado! Ambos foram punidos com -50 HP', 
                                                     True, (255, 100, 100))
                punido_rect = punido_txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
                screen.blit(punido_txt, punido_rect)
            elif tempo_sem_dano >= TIMEOUT_INATIVIDADE:
                # Empate por inatividade
                inatividade_txt = fonts['medium'].render('💤 10s sem dano! Ninguém quis lutar!', 
                                                         True, (255, 200, 100))
                inatividade_rect = inatividade_txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
                screen.blit(inatividade_txt, inatividade_rect)
            
            # Contador de próxima rodada
            tempo_restante_rodada = 3.0 - tempo_entre_rodadas
            next_txt = fonts['large'].render(f'🔄 Próxima rodada em {tempo_restante_rodada:.1f}s', 
                                             True, (100, 255, 100))
            next_rect = next_txt.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
            screen.blit(next_txt, next_rect)
            
            inst_txt = fonts['small'].render('Pressione ESC para sair do treino', True, (180, 180, 180))
            inst_rect = inst_txt.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
            screen.blit(inst_txt, inst_rect)
        
        # Indicador de pausa
        if paused:
            pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 100))
            screen.blit(pause_overlay, (0, 0))
            
            pause_txt = fonts['title'].render('|| PAUSADO', True, (255, 255, 0))
            pause_rect = pause_txt.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(pause_txt, pause_rect)
        
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
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause.collidepoint(event.pos):
                    paused = not paused
                elif btn_exit.collidepoint(event.pos):
                    running = False
        
        # Atualiza visualizador de rede neural (painel lateral)
        if visualizador:
            try:
                # Renderiza visualização
                rodada_info = {
                    'rodada': rodada_atual,
                    'tempo': f'{int(tempo_restante)}',
                    'p1_vida': int(personagens[0].vida_atual) if hasattr(personagens[0], 'vida_atual') else '?',
                    'p2_vida': int(personagens[1].vida_atual) if hasattr(personagens[1], 'vida_atual') else '?'
                }
                surface_viz = visualizador.renderizar(personagens[0], personagens[1], rodada_info)
                
                # Blita a surface do visualizador ao lado da arena
                screen.blit(surface_viz, (WIDTH, 0))
            except Exception as e:
                print(f"⚠️ Erro no visualizador: {e}")
                visualizador = None
        
        pygame.display.flip()
    
    # Salva redes neurais ao sair do treino
    # Fecha visualizador
    if visualizador:
        try:
            visualizador.fechar()
            print("✅ Visualizador fechado")
        except:
            pass
    
    if IA_DISPONIVEL:
        print(f"\n🧠 TREINO FINALIZADO!")
        print(f"📊 Total de rodadas: {rodada_atual}")
        print(f"🏆 Vitórias P1 ({selected_personagem_ids[0]}): {total_vitorias[selected_personagem_ids[0]]}")
        print(f"🏆 Vitórias P2 ({selected_personagem_ids[1]}): {total_vitorias[selected_personagem_ids[1]]}")
        print(f"🤝 Empates: {total_empates}")
        
        # Salva última rodada
        if vencedor and vencedor != "EMPATE":
            vivos_final = [vencedor]
            salvar_redes_neurais(personagens_originais, vivos_final)
