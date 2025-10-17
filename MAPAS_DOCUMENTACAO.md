# 🗺️ Mapas Disponíveis - Arena Effect 2.0

## Mapas Criados

### 1. Mapa Simples (mapa0.py)
**ID:** 1  
**Estilo:** Básico  
**Descrição:** Arena básica com paredes e centro dourado

**Elementos:**
- ✅ Paredes externas cinzas
- ✅ Centro dourado (ponto de referência)
- ✅ Design minimalista
- ✅ Ideal para testes e combates diretos

---

### 2. Mapa Avançado (mapa1.py)
**ID:** 2  
**Estilo:** Tático  
**Descrição:** Mapa com obstáculos em cruz e zonas coloridas

**Elementos:**
- ✅ Paredes externas grossas
- ✅ Obstáculos centrais em forma de cruz
- ✅ 4 obstáculos nos cantos
- ✅ 4 zonas coloridas (vermelho, verde, azul, amarelo)
- ✅ Centro dourado brilhante
- ✅ Fundo azul escuro

**Estratégia:** Use os obstáculos para emboscadas e proteção

---

### 3. Arena Coliseu (mapa2.py)
**ID:** 3  
**Estilo:** Gladiador  
**Descrição:** Estilo coliseu romano com pilares e círculos

**Elementos:**
- ✅ Fundo de areia (cor bege)
- ✅ Paredes de pedra escura
- ✅ 3 círculos concêntricos marcando a arena
- ✅ 8 pilares de pedra (4 cantos + 4 intermediários)
- ✅ Centro dourado brilhante
- ✅ Atmosfera de combate gladiador

**Estratégia:** Use os pilares como cobertura, mantenha distância do centro

---

### 4. Labirinto (mapa3.py)
**ID:** 4  
**Estilo:** Tático Complexo  
**Descrição:** Corredores e passagens estratégicas

**Elementos:**
- ✅ Fundo de pedra escura
- ✅ Sistema complexo de paredes
- ✅ Paredes horizontais e verticais criando corredores
- ✅ 4 salas coloridas (roxa, laranja, ciano, vermelha)
- ✅ Obstáculos centrais
- ✅ Centro dourado (objetivo)

**Estratégia:** Navegue pelos corredores, use as salas como pontos estratégicos

---

## 🎨 Paleta de Cores

### Mapa Simples
- Fundo: Padrão
- Paredes: Cinza (100, 100, 100)
- Centro: Dourado (255, 215, 0)

### Mapa Avançado
- Fundo: Azul escuro (40, 40, 60)
- Paredes: Cinza azulado (80-120, 80-120, 100-140)
- Zonas: RGB variadas
- Centro: Dourado brilhante

### Arena Coliseu
- Fundo: Areia (194, 178, 128)
- Paredes: Pedra escura (60, 50, 40)
- Pilares: Pedra média (100, 80, 60)
- Centro: Dourado intenso

### Labirinto
- Fundo: Pedra escura (50, 50, 70)
- Paredes: Muito escuro (30, 30, 50)
- Paredes internas: Cinza (80, 80, 100)
- Salas: Cores variadas
- Centro: Dourado brilhante

---

## 📐 Dimensões

**Tamanho padrão:** 800x600 pixels

**Paredes externas:** 20-30 pixels de espessura

**Obstáculos:** Variável por mapa
- Simples: Nenhum
- Avançado: Cruz central + 4 cantos
- Coliseu: 8 pilares
- Labirinto: Sistema complexo de paredes

---

## 🎮 Como Adicionar Novos Mapas

1. Crie arquivo `mapaN.py` na pasta `mapas/`
2. Implemente função `desenhar_mapa(screen)`
3. Adicione entrada no `Banco_de_dados_mapas.py`:

```python
{
    'id': N,
    'nome': 'Nome do Mapa',
    'arquivo': 'mapas/mapaN.py',
    'descricao': 'Descrição breve'
}
```

4. O sistema carregará automaticamente!

---

## 🛠️ Estrutura de Função

```python
import pygame

def desenhar_mapa(screen):
    """Descrição do mapa"""
    
    # Fundo
    screen.fill((R, G, B))
    
    # Paredes externas
    pygame.draw.rect(screen, cor, (x, y, w, h))
    
    # Obstáculos
    pygame.draw.rect(screen, cor, (x, y, w, h))
    
    # Elementos decorativos
    pygame.draw.circle(screen, cor, (x, y), raio)
```

---

## 📊 Estatísticas

- **Total de mapas:** 4
- **Complexidade:**
  - Simples: 1 mapa
  - Média: 2 mapas
  - Alta: 1 mapa
- **Todos os mapas testados:** ✅

---

## ✨ Próximas Adições Sugeridas

1. **Mapa Floresta** - Árvores como obstáculos
2. **Mapa Gelo** - Superfície escorregadia (visual)
3. **Mapa Deserto** - Dunas de areia
4. **Mapa Cyberpunk** - Neon e geometria moderna
5. **Mapa Vulcão** - Lava e pedras

---

**Criado em:** 16 de outubro de 2025  
**Versão:** Arena Effect 2.0
