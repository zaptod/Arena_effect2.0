# 💚 Sistema de Vida e Combate - Arena Effect 2.0

## ⚔️ Mudanças Implementadas

### 1. Sistema de Vida
Todos os personagens agora possuem:
- **Vida Máxima:** 100 HP
- **Vida Atual:** Inicia em 100 HP
- **Status:** Vivo ou Morto

### 2. Movimento Removido
- ❌ **Sem movimento aleatório**
- ✅ **Personagens ficam estáticos**
- ✅ **Aguardando implementação de estímulos de movimento**

### 3. Sistema de Dano
- **Dano por colisão:** 50% da força do atacante
- **Força:** Calculada como `velocidade × massa`
- **Dano mútuo:** Ambos personagens recebem dano ao colidir

---

## 📊 Atributos do Personagem

```python
class Personagem:
    # Atributos básicos
    nome: str
    id: int
    tamanho: int
    velocidade: int
    massa: int
    cor: tuple
    forca: int  # velocidade × massa
    
    # Sistema de movimento (desativado)
    x, y: float  # Posição
    vx, vy: float = 0, 0  # Velocidade (sempre 0)
    
    # Sistema de vida
    vida_maxima: int = 100
    vida_atual: int = 100
    vivo: bool = True
```

---

## 🎮 Métodos de Combate

### `receber_dano(dano)`
```python
def receber_dano(self, dano):
    """Aplica dano ao personagem"""
    if self.vivo:
        self.vida_atual -= dano
        if self.vida_atual <= 0:
            self.vida_atual = 0
            self.vivo = False
    return self.vivo
```

**Exemplo:**
```python
personagem.receber_dano(25)  # Perde 25 HP
# vida_atual: 100 → 75
```

### `curar(quantidade)`
```python
def curar(self, quantidade):
    """Cura o personagem"""
    if self.vivo:
        self.vida_atual = min(self.vida_atual + quantidade, self.vida_maxima)
```

**Exemplo:**
```python
personagem.curar(30)  # Recupera 30 HP
# vida_atual: 70 → 100 (máximo)
```

---

## 💥 Sistema de Colisões

### Cálculo de Dano
```python
# Personagem 1
velocidade = 5
massa = 10
forca = velocidade × massa = 50
dano = forca × 0.5 = 25 HP

# Personagem 2
velocidade = 3
massa = 8
forca = velocidade × massa = 24
dano = forca × 0.5 = 12 HP
```

### Colisão
```python
# Ao colidir:
p1.receber_dano(12)  # Recebe dano do P2
p2.receber_dano(25)  # Recebe dano do P1

# Resultado:
# P1: 100 → 88 HP
# P2: 100 → 75 HP
```

---

## 📺 Interface Visual

### Barra de Vida
- **Posição:** Acima do personagem
- **Largura:** 50 pixels
- **Altura:** 5 pixels
- **Cores:**
  - 🟢 Verde: > 50% HP
  - 🟡 Amarelo: 20-50% HP
  - 🔴 Vermelho: < 20% HP

### Texto de Vida
- **Exibe:** Vida atual (inteiro)
- **Posição:** Acima da barra de vida
- **Cor:** Branco

### Exemplo Visual
```
      [75]
    [=========>  ]
        🟢
```

---

## 🏆 Sistema de Vitória

### Condições de Vitória
1. **Vencedor Único:** Apenas 1 personagem vivo
2. **Empate:** Todos os personagens mortos

### Tela de Vitória
```
╔════════════════════════════╗
║   🏆 JOGADOR 1 VENCEU!    ║
║                            ║
║  Pressione R para          ║
║  reiniciar ou ESC          ║
║  para sair                 ║
╚════════════════════════════╝
```

---

## 📊 Estatísticas em Tempo Real

### Painel de Informações
```
⏱️ Tempo: 01:23
💚 Vivos: 3 / 5
⚔️ Armas: 5
🎮 FPS: 60
```

**Legenda:**
- **Tempo:** Tempo decorrido na simulação
- **Vivos:** Personagens vivos / Total
- **Armas:** Personagens equipados com armas
- **FPS:** Frames por segundo

---

## 🎯 Exemplos de Combate

### Combate 1v1
```python
# Início
P1: 100 HP (Força: 50)
P2: 100 HP (Força: 30)

# Colisão 1
P1: 100 → 85 HP
P2: 100 → 75 HP

# Colisão 2
P1: 85 → 70 HP
P2: 75 → 50 HP

# Colisão 3
P1: 70 → 55 HP
P2: 50 → 25 HP

# Colisão 4
P1: 55 → 40 HP
P2: 25 → 0 HP (MORTO)

# Resultado: P1 VENCEU!
```

### Combate 3 Players
```python
# Início
P1: 100 HP (Força: 40)
P2: 100 HP (Força: 50)
P3: 100 HP (Força: 30)

# Rodada 1
P1 vs P2 → P1: 75 HP, P2: 80 HP
P1 vs P3 → P1: 60 HP, P3: 80 HP

# Rodada 2
P2 vs P3 → P2: 65 HP, P3: 55 HP
P1 vs P2 → P1: 35 HP, P2: 45 HP

# Rodada 3
P3 vs P1 → P3: 35 HP, P1: 20 HP
P2 vs P3 → P2: 30 HP, P3: 10 HP

# Rodada 4
P1 vs P3 → P1: 15 HP, P3: 0 HP (MORTO)
P2 vs P1 → P2: 10 HP, P1: 0 HP (MORTO)

# Resultado: P2 VENCEU!
```

---

## ⚙️ Configurações Futuras

### Movimento (Desativado)
```python
# Atualmente:
vx = 0  # Sem movimento horizontal
vy = 0  # Sem movimento vertical

# Futuro (com estímulos):
# - Movimento baseado em comportamentos
# - Busca de alvos
# - Fuga de ameaças
# - Patrulhamento de área
```

### Dano de Armas (Planejado)
```python
# Sistema atual: Apenas dano por colisão
# Sistema futuro:
# - Dano à distância com armas
# - Diferentes tipos de projéteis
# - Taxa de disparo
# - Alcance efetivo
```

---

## 🔧 Criando Personagens com Vida

### Template Automático
Ao criar um personagem pelo sistema, o código já inclui:
```python
# Sistema de vida (automático)
self.vida_maxima = 100
self.vida_atual = 100
self.vivo = True

# Métodos de combate
def receber_dano(self, dano):
    # Código de dano

def curar(self, quantidade):
    # Código de cura
```

### Personagens Existentes
Personagens criados antes da atualização podem não ter o sistema de vida. Para atualizá-los:

1. Abra o arquivo do personagem
2. Adicione no `__init__`:
```python
self.vida_maxima = 100
self.vida_atual = 100
self.vivo = True
```

3. Adicione os métodos:
```python
def receber_dano(self, dano):
    if self.vivo:
        self.vida_atual -= dano
        if self.vida_atual <= 0:
            self.vida_atual = 0
            self.vivo = False
    return self.vivo

def curar(self, quantidade):
    if self.vivo:
        self.vida_atual = min(self.vida_atual + quantidade, self.vida_maxima)
```

---

## 📝 Notas Importantes

1. **Sem Movimento:** Personagens são estáticos até implementação de estímulos
2. **Dano Fixo:** Dano baseado em força (50% do valor)
3. **Vida Regeneração:** Não implementada (apenas método curar manual)
4. **Morte Permanente:** Personagens mortos são removidos da simulação
5. **Colisões Contínuas:** Personagens colidindo aplicam dano continuamente

---

## 🚀 Próximos Passos

1. ✅ Sistema de vida implementado
2. ✅ Movimento removido
3. ⏳ Implementar estímulos de movimento
4. ⏳ Dano de armas à distância
5. ⏳ Sistema de comportamentos ativos
6. ⏳ Habilidades especiais
7. ⏳ Sistema de equipes

---

**Versão:** 2.0  
**Data:** 17 de outubro de 2025  
**Status:** Sistema de vida ativo, movimento desativado
