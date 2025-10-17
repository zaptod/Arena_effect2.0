"""
Módulo de Utilitários Comuns
Funções e constantes compartilhadas entre todas as páginas
"""
import pygame
import sys
import os

# Adiciona o diretório raiz ao path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60

# Cores
COLOR_BG = (30, 30, 30)
COLOR_BG_LIGHT = (60, 60, 80)
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON = (70, 130, 180)
COLOR_BUTTON_HOVER = (90, 150, 200)
COLOR_SUCCESS = (0, 150, 0)
COLOR_WARNING = (200, 150, 0)
COLOR_DANGER = (200, 0, 0)
COLOR_SELECTED = (0, 200, 0)

# Fontes
def init_fonts():
    """Inicializa fontes do pygame"""
    return {
        'title': pygame.font.SysFont(None, 48),
        'large': pygame.font.SysFont(None, 36),
        'medium': pygame.font.SysFont(None, 28),
        'small': pygame.font.SysFont(None, 20)
    }

def draw_button(screen, text, rect, font, color=COLOR_BUTTON, hover=False):
    """Desenha um botão com hover effect"""
    button_color = COLOR_BUTTON_HOVER if hover else color
    pygame.draw.rect(screen, button_color, rect, border_radius=5)
    pygame.draw.rect(screen, COLOR_TEXT, rect, 2, border_radius=5)
    
    txt = font.render(text, True, COLOR_TEXT)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)
    
    return rect

def draw_title(screen, text, font, y=30):
    """Desenha um título centralizado"""
    txt = font.render(text, True, COLOR_TEXT)
    txt_rect = txt.get_rect(center=(WIDTH // 2, y))
    screen.blit(txt, txt_rect)

def draw_back_button(screen, font):
    """Desenha botão de voltar no canto superior esquerdo"""
    back_rect = pygame.Rect(10, 10, 100, 40)
    pygame.draw.rect(screen, (100, 100, 100), back_rect, border_radius=5)
    pygame.draw.rect(screen, COLOR_TEXT, back_rect, 2, border_radius=5)
    
    txt = font.render("← Voltar", True, COLOR_TEXT)
    txt_rect = txt.get_rect(center=back_rect.center)
    screen.blit(txt, txt_rect)
    
    return back_rect

def is_mouse_over(rect, mouse_pos):
    """Verifica se o mouse está sobre um retângulo"""
    return rect.collidepoint(mouse_pos)

def draw_info_box(screen, lines, font, x=10, y=500, bg_color=(40, 40, 40)):
    """Desenha uma caixa de informações"""
    max_width = max([font.size(line)[0] for line in lines]) + 20
    height = len(lines) * 25 + 10
    
    info_rect = pygame.Rect(x, y, max_width, height)
    pygame.draw.rect(screen, bg_color, info_rect, border_radius=5)
    pygame.draw.rect(screen, COLOR_TEXT, info_rect, 1, border_radius=5)
    
    for i, line in enumerate(lines):
        txt = font.render(line, True, COLOR_TEXT)
        screen.blit(txt, (x + 10, y + 5 + i * 25))

def load_module_function(module_path, function_name):
    """Carrega uma função de um módulo dinamicamente"""
    import importlib.util
    
    if not os.path.exists(module_path):
        raise FileNotFoundError(f'Módulo não encontrado: {module_path}')
    
    spec = importlib.util.spec_from_file_location("dynamic_module", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    return getattr(mod, function_name)

def format_time(seconds):
    """Formata segundos em MM:SS"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def load_personagem(personagem_id):
    """Carrega um personagem pelo ID"""
    personagens_dir = os.path.join(ROOT_DIR, 'personagens')
    fname = f'personagem{personagem_id}.py'
    fpath = os.path.join(personagens_dir, fname)
    criar_personagem = load_module_function(fpath, 'criar_personagem')
    return criar_personagem

def load_arma(arma_id):
    """Carrega uma arma pelo ID"""
    armas_dir = os.path.join(ROOT_DIR, 'armas')
    fname = f'arma{arma_id}.py'
    fpath = os.path.join(armas_dir, fname)
    
    if not os.path.exists(fpath):
        return None
    
    criar_arma = load_module_function(fpath, 'criar_arma')
    return criar_arma(arma_id)

def load_mapa(mapa_id):
    """Carrega função de desenho do mapa"""
    mapas_dir = os.path.join(ROOT_DIR, 'mapas')
    fname = f'mapa{mapa_id}.py'
    fpath = os.path.join(mapas_dir, fname)
    desenhar_mapa = load_module_function(fpath, 'desenhar_mapa')
    return desenhar_mapa
