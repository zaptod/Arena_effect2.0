"""
Teste de integração: Personagens com Armas
Este arquivo testa se os personagens aparecem com armas na simulação
"""
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from personagens.personagem1 import criar_personagem as criar_p1
from personagens.personagem2 import criar_personagem as criar_p2
from armas.arma1 import criar_arma as criar_espada
from armas.arma2 import criar_arma as criar_arco

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste: Personagens + Armas")
clock = pygame.time.Clock()

# Cria personagens
personagem1 = criar_p1(1, 200, 300)
personagem1.arma = criar_espada(1)

personagem2 = criar_p2(2, 600, 300)
personagem2.arma = criar_arco(2)

personagens = [personagem1, personagem2]

font = pygame.font.SysFont(None, 24)

running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Testa ataque
                for p in personagens:
                    if p.arma and p.arma.atacar():
                        print(f"{p.nome} atacou com {p.arma.nome}!")
    
    screen.fill((40, 40, 60))
    
    # Atualiza e desenha personagens
    for personagem in personagens:
        # Atualiza
        personagem.x += personagem.vx
        personagem.y += personagem.vy
        
        # Limites da tela
        if personagem.x < personagem.tamanho or personagem.x > 800 - personagem.tamanho:
            personagem.vx *= -1
        if personagem.y < personagem.tamanho or personagem.y > 600 - personagem.tamanho:
            personagem.vy *= -1
        
        # Atualiza arma
        if personagem.arma:
            personagem.arma.update(dt)
        
        # Desenha personagem
        pygame.draw.circle(screen, personagem.cor, (int(personagem.x), int(personagem.y)), personagem.tamanho)
        
        # Desenha arma apontando para o outro personagem
        if personagem.arma:
            outros = [p for p in personagens if p is not personagem]
            if outros:
                alvo = outros[0]
                personagem.arma.draw(screen, personagem.x, personagem.y, alvo.x, alvo.y)
    
    # Informações
    info_texts = [
        f"{personagens[0].nome} com {personagens[0].arma.nome if personagens[0].arma else 'Sem arma'}",
        f"{personagens[1].nome} com {personagens[1].arma.nome if personagens[1].arma else 'Sem arma'}",
        "",
        "ESPAÇO: Atacar"
    ]
    
    for i, text in enumerate(info_texts):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + i * 25))
    
    pygame.display.flip()

pygame.quit()
