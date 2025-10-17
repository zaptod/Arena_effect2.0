# 💤 Sistema Anti-Inatividade - Modo Treino

## 📋 Visão Geral

O **Sistema Anti-Inatividade** detecta quando os personagens estão evitando o combate e encerra a rodada automaticamente, evitando partidas onde ninguém ataca.

## 🎯 Problema Resolvido

### Antes:
```
❌ Personagem 1 foge do Personagem 2
❌ Personagem 2 foge do Personagem 1
❌ Ninguém ataca por 20+ segundos
❌ Rodada continua até timeout (30s)
❌ IA aprende a FUGIR em vez de LUTAR
```

### Agora:
```
✅ Se ninguém causar dano por 10 segundos
✅ Rodada termina imediatamente em EMPATE
✅ Nenhum personagem ganha
✅ IA é penalizada por comportamento passivo
✅ Incentiva combate ativo
```

## ⚙️ Como Funciona

### 1. Detecção de Dano
```python
# Contador de tempo sem dano
tempo_sem_dano = 0.0

# A cada frame SEM dano:
tempo_sem_dano += dt_seconds

# Quando HÁ dano:
tempo_sem_dano = 0.0  # RESETA!
```

### 2. Timeout de Inatividade
```python
TIMEOUT_INATIVIDADE = 10.0 segundos

if tempo_sem_dano >= 10.0:
    vencedor = "EMPATE"
    # Rodada encerra imediatamente
```

### 3. Reset Automático
O contador é **resetado** sempre que:
- ✅ Qualquer personagem causa dano
- ✅ Um ataque de arma acerta o alvo
- ✅ Nova rodada começa

## 🎨 Interface Visual

### Indicador de Inatividade

Aparece no **canto superior direito** após 5 segundos sem dano:

```
┌─────────────────┐
│ 💤 SEM DANO!    │  ← Título
│    4.8s         │  ← Tempo restante
└─────────────────┘
```

**Cores do Indicador:**
- 🟨 **Amarelo** (10s → 5s): "Atenção, sem combate"
- 🟧 **Laranja** (5s → 2s): "Aviso, tome ação!"
- 🟥 **Vermelho** (2s → 0s): "CRÍTICO! Empate iminente!"

### Mensagem de Resultado

Quando empate por inatividade:
```
⚔️ EMPATE!
💤 10s sem dano! Ninguém quis lutar!
🔄 Próxima rodada em 2.5s
```

## 📊 Impacto na IA

### Comportamento Penalizado
```
❌ Fugir constantemente sem atacar
❌ Manter distância excessiva
❌ Evitar engajamento
❌ Estratégias puramente defensivas
```

### Comportamento Incentivado
```
✅ Perseguir o oponente
✅ Atacar quando possível
✅ Fechar distância (melee)
✅ Manter pressão (ranged)
✅ Engajar ativamente
```

### Evolução Esperada

Após várias rodadas com o sistema:

**Geração 1-10**: Muitos empates por inatividade
```
P1 e P2 aprendem que fugir = empate (0 pontos)
```

**Geração 11-30**: Redução de empates
```
IAs começam a testar ataques
Descobrem que atacar > fugir
```

**Geração 31+**: Comportamento agressivo
```
IAs perseguem ativamente
Ataques frequentes
Poucos empates por inatividade
```

## 🔧 Configuração

### Ajustar Timeout

Edite `modo_treino.py`:

```python
# Linha ~289
TIMEOUT_INATIVIDADE = 10.0  # segundos

# Valores sugeridos:
# 5.0  - Muito agressivo (força combate rápido)
# 10.0 - Balanceado (padrão)
# 15.0 - Mais permissivo
# 20.0 - Relaxado
```

### Ajustar Aviso Visual

```python
# Linha ~517
if tempo_sem_dano > 5.0:  # Mostra após X segundos

# Valores sugeridos:
# 3.0 - Aviso antecipado
# 5.0 - Balanceado (padrão)
# 7.0 - Aviso tardio
```

## 🧪 Testes Realizados

### Teste 1: Fuga Mútua
```
Configuração: P0 com Arco vs P1 com Arco
Comportamento: Ambos fogem constantemente
Resultado: ✅ Empate após 10s
Tempo total: ~10.2s
```

### Teste 2: Combate Normal
```
Configuração: P0 com Espada vs P1 com Espada
Comportamento: Ataques constantes
Resultado: ✅ Vencedor determinado normalmente
Contador: Resetado a cada hit
```

### Teste 3: Um Foge, Um Persegue
```
Configuração: P0 com Adaga vs P1 com Arco
Comportamento: P0 persegue, P1 foge mas ataca
Resultado: ✅ Contador resetado pelos ataques do P1
Tempo total: Variável (depende dos hits)
```

## 📈 Métricas de Sucesso

### Indicadores Positivos
- ✅ Redução de empates por inatividade ao longo das gerações
- ✅ Aumento de vitórias por morte (combate real)
- ✅ Tempo médio de rodada diminui
- ✅ Dano médio por rodada aumenta

### Indicadores Negativos (Problemas)
- ⚠️ Muitos empates por inatividade persistindo (>50%)
  - **Solução**: Reduzir TIMEOUT_INATIVIDADE para 7-8s
- ⚠️ IAs muito agressivas morrendo rápido
  - **Solução**: Aumentar TIMEOUT_INATIVIDADE para 12-15s

## 🎮 Estratégias de Treino

### Para IAs Agressivas
```
1. Mantenha TIMEOUT_INATIVIDADE = 10.0s
2. Treine com armas de corpo-a-corpo
3. Penalidade incentiva fechamento de distância
```

### Para IAs Táticas
```
1. Aumente TIMEOUT_INATIVIDADE = 15.0s
2. Permite mais posicionamento
3. Mantém pressão sem forçar suicídio
```

### Para IAs Kiting (Arco)
```
1. Mantenha padrão (10.0s)
2. IA aprende: "Fugir É BOM, mas preciso ATIRAR"
3. Desenvolve kiting ativo (foge + ataca)
```

## 🐛 Troubleshooting

### Problema: Muitos empates por inatividade
```
Causa: IAs não aprenderam a atacar ainda
Solução: Continue treinando (20-50+ gerações)
         IAs eventualmente descobrem que atacar é melhor
```

### Problema: IAs muito passivas
```
Causa: TIMEOUT muito alto
Solução: Reduza para 7-8 segundos
         Força decisões mais rápidas
```

### Problema: IAs se suicidam
```
Causa: TIMEOUT muito baixo
Solução: Aumente para 12-15 segundos
         Permite estratégia mais pensada
```

### Problema: Contador não reseta
```
Causa: Dano não está sendo detectado
Solução: Verifique logs, deve aparecer:
         "RESETA CONTADOR DE INATIVIDADE"
```

## 💡 Dicas Avançadas

### 1. Treino em Fases
```
Fase 1 (Gerações 1-20): TIMEOUT = 15s (permissivo)
→ IAs aprendem básico sem pressão

Fase 2 (Gerações 21-50): TIMEOUT = 10s (balanceado)
→ IAs refinam estratégias

Fase 3 (Gerações 51+): TIMEOUT = 7s (agressivo)
→ IAs desenvolvem combate intenso
```

### 2. Diferentes Timeouts por Arma
```python
# Exemplo de configuração avançada
if arma_alcance_longo:  # Arco
    TIMEOUT_INATIVIDADE = 12.0
else:  # Melee
    TIMEOUT_INATIVIDADE = 8.0
```

### 3. Análise de Logs
```
Busque no console:
"💤 INATIVIDADE DETECTADA!" - Conta quantos por sessão
"RESETA CONTADOR" - Frequência de ataques

Meta: <10% de empates por inatividade após 50 gerações
```

## 📊 Exemplo de Evolução

```
Gerações 1-10:
  Empates: 45% inatividade, 30% timeout, 25% morte
  → IAs fugindo muito

Gerações 11-30:
  Empates: 20% inatividade, 25% timeout, 55% morte
  → IAs testando ataques

Gerações 31-50:
  Empates: 5% inatividade, 15% timeout, 80% morte
  → IAs combatendo ativamente

Gerações 51+:
  Empates: 2% inatividade, 8% timeout, 90% morte
  → IAs mestres do combate
```

## 🎓 Conceitos de IA

- **Negative Reinforcement**: Empate = 0 fitness (penalidade)
- **Exploration vs Exploitation**: IAs descobrem que atacar > fugir
- **Behavioral Shaping**: Sistema guia IAs para comportamento desejado
- **Adaptive Strategies**: IAs desenvolvem táticas únicas por arma

---

**Desenvolvido para Arena Effect Simulator 2.0**
**Sistema Anti-Inatividade para Treino de IA**
