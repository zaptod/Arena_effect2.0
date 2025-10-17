# Sistema de Armas - Arena Effect 2.0

## 📋 Visão Geral

Este sistema implementa 4 armas diferentes com características únicas:

### 🗡️ Armas Disponíveis

1. **Espada Curta** (ID: 1)
   - Dano: 10
   - Alcance: 1.5
   - Velocidade de Ataque: 1.0
   - Descrição: Arma corpo a corpo básica com bom equilíbrio

2. **Arco Longo** (ID: 2)
   - Dano: 15
   - Alcance: 10.0
   - Velocidade de Ataque: 0.5
   - Descrição: Arma de longo alcance com alto dano

3. **Machado de Batalha** (ID: 3)
   - Dano: 20
   - Alcance: 2.0
   - Velocidade de Ataque: 0.7
   - Descrição: Arma pesada de alto dano mas lenta

4. **Adaga** (ID: 4)
   - Dano: 5
   - Alcance: 1.0
   - Velocidade de Ataque: 2.0
   - Descrição: Arma rápida de baixo dano

## 🎮 Funcionalidades

Cada arma possui os seguintes métodos:

### `update(dt)`
Atualiza o cooldown da arma baseado no tempo decorrido.

### `pode_atacar()`
Verifica se a arma está pronta para atacar (cooldown zerado).

### `atacar()`
Executa um ataque e inicia o cooldown. Retorna `True` se o ataque foi bem-sucedido.

### `draw(screen, personagem_x, personagem_y, target_x, target_y)`
Desenha a arma próxima ao personagem, apontando para o alvo.

### `draw_icon(screen, x, y, size=50)`
Desenha um ícone da arma para uso em interfaces (menus, inventário, etc.).
O ícone inclui o valor de dano sobreposto.

### `verificar_hit(personagem_x, personagem_y, alvo_x, alvo_y, alvo_tamanho)`
Verifica se um ataque atingiu o alvo baseado no alcance da arma.

## 🎨 Visualização

Cada arma é desenhada de forma única:
- **Espada**: Lâmina com cabo e guarda
- **Arco**: Arco curvo com corda e flecha
- **Machado**: Cabo longo com lâmina triangular
- **Adaga**: Lâmina curta e fina

## 🧪 Testando as Armas

Para visualizar as armas em ação, execute:

```bash
python armas/visualizador_armas.py
```

### Controles do Visualizador:
- **Setas ← →**: Trocar entre armas
- **ESPAÇO**: Executar ataque
- **Mouse**: Apontar arma

## 💻 Como Usar no Código

### Exemplo Básico:

```python
from armas.arma1 import criar_arma

# Criar uma espada
espada = criar_arma(1)

# Em seu loop de jogo
dt = clock.tick(60) / 1000.0
espada.update(dt)

# Desenhar a arma
mouse_x, mouse_y = pygame.mouse.get_pos()
espada.draw(screen, personagem_x, personagem_y, mouse_x, mouse_y)

# Atacar
if tecla_ataque_pressionada:
    if espada.atacar():
        print("Ataque executado!")
        # Verificar se acertou algum inimigo
        if espada.verificar_hit(personagem_x, personagem_y, inimigo_x, inimigo_y, inimigo_raio):
            inimigo_vida -= espada.dano
```

### Exemplo com Sprites Personalizados:

```python
from armas.arma1 import Arma

# Criar arma com sprite customizado
espada = Arma(
    nome='Espada Mágica',
    id=5,
    dano=25,
    alcance=2.0,
    velocidade_ataque=1.2,
    sprite_path='caminho/para/sprite.png'
)
```

## 🔧 Customização

Para criar novas armas, use a classe `Arma` como base:

```python
import pygame
import math
from armas.arma1 import Arma

class MinhaArmaCustomizada(Arma):
    def draw(self, screen, personagem_x, personagem_y, target_x=None, target_y=None):
        # Seu código de desenho personalizado
        pass
```

## 📊 Sistema de Cooldown

O sistema de cooldown garante que cada arma ataque na velocidade correta:
- **Cooldown** = 1.0 / velocidade_ataque
- Exemplo: Espada (vel. 1.0) = 1 ataque/segundo
- Exemplo: Adaga (vel. 2.0) = 2 ataques/segundo
- Exemplo: Arco (vel. 0.5) = 1 ataque a cada 2 segundos

## 🎯 Integração com Personagens

As armas foram projetadas para se integrar facilmente com o sistema de personagens:

```python
class Personagem:
    def __init__(self, ...):
        self.arma = criar_espada(1)  # Arma inicial
        
    def update(self, dt):
        # Atualiza a arma
        self.arma.update(dt)
        
    def draw(self, screen):
        # Desenha o personagem
        pygame.draw.circle(screen, self.cor, (self.x, self.y), self.tamanho)
        
        # Desenha a arma
        self.arma.draw(screen, self.x, self.y, alvo_x, alvo_y)
```

## 📝 Notas

- As armas desenham representações visuais mesmo sem sprites
- Todos os cálculos de alcance são feitos automaticamente
- O sistema de cooldown é baseado em tempo real (delta time)
- Compatível com a arquitetura modular do Arena Effect 2.0
