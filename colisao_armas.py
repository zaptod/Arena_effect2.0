"""
Sistema de Colisão entre Armas
Funções para detectar e processar colisões/ricochetes entre armas
"""
import math

def segmentos_se_cruzam(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    Verifica se dois segmentos de linha se cruzam
    Segmento 1: (x1,y1) -> (x2,y2)
    Segmento 2: (x3,y3) -> (x4,y4)
    
    Returns:
        tuple: (se_cruzam: bool, ponto_x: float, ponto_y: float) ou (False, None, None)
    """
    # Calcula os determinantes
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    if abs(denom) < 1e-10:  # Linhas paralelas
        return False, None, None
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    
    # Verifica se a interseção está dentro de ambos os segmentos
    if 0 <= t <= 1 and 0 <= u <= 1:
        # Calcula ponto de interseção
        intersecao_x = x1 + t * (x2 - x1)
        intersecao_y = y1 + t * (y2 - y1)
        return True, intersecao_x, intersecao_y
    
    return False, None, None


def verificar_colisao_armas(arma1, personagem1_x, personagem1_y,
                            arma2, personagem2_x, personagem2_y):
    """
    Verifica se duas armas colidem
    
    Args:
        arma1: Primeira arma
        personagem1_x, personagem1_y: Posição do personagem 1
        arma2: Segunda arma
        personagem2_x, personagem2_y: Posição do personagem 2
    
    Returns:
        dict: {
            'colidiu': bool,
            'ponto_x': float,
            'ponto_y': float,
            'angulo_colisao': float
        }
    """
    # Obtém linhas das armas
    x1_i, y1_i, x1_f, y1_f = arma1.get_linha_arma(personagem1_x, personagem1_y)
    x2_i, y2_i, x2_f, y2_f = arma2.get_linha_arma(personagem2_x, personagem2_y)
    
    # Verifica se os segmentos se cruzam
    cruzam, ponto_x, ponto_y = segmentos_se_cruzam(
        x1_i, y1_i, x1_f, y1_f,
        x2_i, y2_i, x2_f, y2_f
    )
    
    if not cruzam:
        return {
            'colidiu': False,
            'ponto_x': None,
            'ponto_y': None,
            'angulo_colisao': None
        }
    
    # Calcula ângulo de colisão (perpendicular à linha entre as pontas)
    dx = x1_f - x2_f
    dy = y1_f - y2_f
    angulo_colisao = math.atan2(dy, dx) + math.pi / 2
    
    return {
        'colidiu': True,
        'ponto_x': ponto_x,
        'ponto_y': ponto_y,
        'angulo_colisao': angulo_colisao
    }


def aplicar_ricochete_armas(arma1, arma2, resultado_colisao):
    """
    Aplica efeito de ricochete em ambas as armas após colisão
    
    Args:
        arma1: Primeira arma
        arma2: Segunda arma
        resultado_colisao: Resultado da função verificar_colisao_armas
    """
    if not resultado_colisao['colidiu']:
        return
    
    angulo = resultado_colisao['angulo_colisao']
    
    # Aplica ricochete em ambas as armas
    arma1.aplicar_ricochete(angulo)
    arma2.aplicar_ricochete(angulo + math.pi)  # Ângulo oposto


def processar_colisoes_armas(personagens):
    """
    Verifica e processa colisões entre todas as armas dos personagens
    
    Args:
        personagens: Lista de personagens com armas
    
    Returns:
        int: Número de colisões detectadas
    """
    colisoes = 0
    
    for i, p1 in enumerate(personagens):
        # Verifica se personagem tem arma
        if not hasattr(p1, 'arma') or p1.arma is None:
            continue
        
        for p2 in personagens[i+1:]:
            # Verifica se segundo personagem tem arma
            if not hasattr(p2, 'arma') or p2.arma is None:
                continue
            
            # Verifica colisão
            resultado = verificar_colisao_armas(
                p1.arma, p1.x, p1.y,
                p2.arma, p2.x, p2.y
            )
            
            if resultado['colidiu']:
                # Aplica ricochete
                aplicar_ricochete_armas(p1.arma, p2.arma, resultado)
                colisoes += 1
    
    return colisoes
