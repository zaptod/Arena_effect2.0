# 🎯 Atualização: IA Controla Ângulo da Arma

## 📋 Resumo das Mudanças

A rede neural agora tem **controle total sobre o ângulo da arma**, ao invés de sempre mirar automaticamente no oponente.

## 🧠 Mudanças na Rede Neural

### Arquitetura Atualizada
- **Antes**: 12 → 16 → 8 → **4** (sem controle de ângulo)
- **Depois**: 12 → 16 → 8 → **5** (com controle de ângulo)

### Nova Saída (#5)
```python
# Saídas da rede neural:
0: Movimento X (-1 a 1)
1: Movimento Y (-1 a 1)  
2: Atacar (>0.5 = sim)
3: Fugir (>0.5 = sim, inverte movimento)
4: Ângulo da arma (0 a 2π radianos) ⬅️ NOVO!
```

### Código Atualizado
```python
# Em ia/rede_neural.py - decidir_acao()
angulo_arma = saida[4] * 2 * np.pi  # Converte (0-1) para (0 a 2π)

return {
    'mover_x': mover_x,
    'mover_y': mover_y,
    'atacar': saida[2] > 0.5,
    'fugir': fugir,
    'angulo_arma': angulo_arma  # ⬅️ NOVO!
}
```

## ⚔️ Mudanças nas Armas

### Método draw() Atualizado
```python
def draw(self, screen, personagem_x, personagem_y, target_x=None, target_y=None, angulo_direto=None):
    """
    Args:
        angulo_direto: Se fornecido, usa este ângulo ao invés de calcular pelo alvo
    """
    # Se angulo_direto foi fornecido, usa ele; senão calcula pelo alvo
    if angulo_direto is not None:
        self.angulo = angulo_direto  # ⬅️ IA define o ângulo
    elif target_x is not None and target_y is not None:
        dx = target_x - personagem_x
        dy = target_y - personagem_y
        self.angulo = math.atan2(dy, dx)  # ⬅️ Mira automática (modo manual)
```

### Arquivos Atualizados
- ✅ `armas/arma1.py`
- ✅ `armas/arma2.py`
- ✅ `armas/arma3.py`
- ✅ `armas/arma4.py`

## 🎮 Mudanças nas Simulações

### Aplicação da IA
```python
# Em main_simulation.py - aplicar_ia_personagem()
def aplicar_ia_personagem(personagem, outros_personagens, width=WIDTH, height=HEIGHT):
    acao = personagem.rede_neural.decidir_acao(personagem, outros_personagens, width, height)
    
    personagem.vx = acao['mover_x'] * personagem.velocidade
    personagem.vy = acao['mover_y'] * personagem.velocidade
    personagem.ia_atacar = acao['atacar']
    personagem.ia_fugir = acao['fugir']
    personagem.ia_angulo_arma = acao.get('angulo_arma', 0)  # ⬅️ NOVO!
```

### Desenho das Armas
```python
# Em main_simulation.py e modo_treino.py
if hasattr(personagem, 'ia_angulo_arma'):
    # IA controla o ângulo da arma
    personagem.arma.draw(screen, personagem.x, personagem.y, 
                        angulo_direto=personagem.ia_angulo_arma)
else:
    # Sem IA: mira no alvo mais próximo (modo manual/padrão)
    personagem.arma.draw(screen, personagem.x, personagem.y, target_x, target_y)
```

## 🔄 Compatibilidade

### Redes Neurais Antigas
⚠️ **Redes neurais salvas com a arquitetura antiga (12→16→8→4) não funcionarão!**

**Solução**: O sistema criará novas redes automaticamente com a arquitetura atualizada (12→16→8→5).

### Modo Manual
✅ Personagens sem IA ainda funcionam normalmente (mira automática no alvo mais próximo).

## 🎯 Vantagens da Mudança

### Para a IA
1. **Maior controle tático**: Pode escolher mirar em diferentes direções
2. **Estratégias complexas**: Pode fingir mirar em uma direção e atacar em outra
3. **Antecipação**: Pode mirar onde o inimigo estará, não onde está
4. **Defesa**: Pode manter a arma em posição defensiva

### Para o Treinamento
1. **Espaço de ações maior**: Mais possibilidades para aprender
2. **Comportamentos emergentes**: Estratégias não previstas podem surgir
3. **Diferenciação**: IAs podem desenvolver estilos de luta únicos

## 📁 Arquivos Modificados

### Core
- ✅ `ia/rede_neural.py` - Arquitetura 5 saídas + lógica de ângulo
- ✅ `armas/arma1.py, arma2.py, arma3.py, arma4.py` - Suporte a angulo_direto

### Simulações
- ✅ `Paginas/main_simulation.py` - Aplicação de ângulo da IA
- ✅ `Paginas/modo_treino.py` - Aplicação de ângulo da IA (via import)

### Scripts Auxiliares
- ✅ `atualizar_armas_angulo.py` - Script de propagação automática

## 🚀 Próximos Passos

1. **Testar no modo treino** - Ver como as IAs aprendem a controlar o ângulo
2. **Monitorar comportamentos** - Observar se surgem estratégias interessantes
3. **Ajustar fitness** - Talvez premiar precisão de mira (se necessário)
4. **Treinar várias gerações** - Deixar evoluir e ver o que acontece!

## 💡 Dica de Uso

Execute o modo treino loop por várias rodadas para ver as IAs aprendendo a:
- Antecipar movimento do oponente
- Manter distância otimizando ângulo de ataque
- Desenvolver padrões de movimentação + mira coordenados

**O aprendizado pode levar mais tempo**, pois agora há uma dimensão extra para otimizar! 🎓
