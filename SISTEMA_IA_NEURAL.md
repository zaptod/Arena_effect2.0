# 🧠 Sistema de Inteligência Artificial Neural

## Visão Geral

Cada personagem possui sua própria **Rede Neural** que controla:
- **Movimentos** (para onde ir)
- **Ataques** (quando atacar)
- **Estratégias** (fugir ou atacar)

As redes neurais **evoluem** através de **Algoritmo Genético**:
1. Combates avaliam o desempenho
2. Melhores redes sobrevivem
3. Reprodução cria novas redes
4. Mutações trazem variedade
5. Nova geração é testada

---

## 🏗️ Arquitetura da Rede Neural

### Camadas
```
Entrada (12 neurônios) → Sensores do ambiente
    ↓
Oculta 1 (16 neurônios) → Processamento
    ↓
Oculta 2 (8 neurônios) → Decisão
    ↓
Saída (4 neurônios) → Ações
```

### Entrada - 12 Sensores

| # | Sensor | Descrição | Normalização |
|---|--------|-----------|--------------|
| 0 | pos_x | Posição X | 0-1 (x/largura) |
| 1 | pos_y | Posição Y | 0-1 (y/altura) |
| 2 | dir_inimigo_x | Direção X para inimigo | -1 a 1 |
| 3 | dir_inimigo_y | Direção Y para inimigo | -1 a 1 |
| 4 | dist_inimigo | Distância normalizada | 0-1 |
| 5 | vida_propria | HP próprio | 0-1 |
| 6 | vida_inimigo | HP do inimigo mais próximo | 0-1 |
| 7 | tem_arma | Arma equipada | 0 ou 1 |
| 8 | dist_borda_x | Distância para borda X | 0-1 |
| 9 | dist_borda_y | Distância para borda Y | 0-1 |
| 10 | num_inimigos | Número de inimigos vivos | 0-1 |
| 11 | forca_relativa | Força própria / média inimigos | 0-2+ |

### Saída - 4 Ações

| # | Ação | Descrição | Interpretação |
|---|------|-----------|---------------|
| 0 | mover_x | Movimento horizontal | 0-1 → -1 a 1 |
| 1 | mover_y | Movimento vertical | 0-1 → -1 a 1 |
| 2 | atacar | Deve atacar | >0.5 = SIM |
| 3 | fugir | Deve fugir | >0.5 = inverte movimento |

---

## 🧬 Algoritmo Genético

### Fluxo de Evolução

```
Geração N
    ↓
Combates (avaliação)
    ↓
Cálculo de Fitness
    ↓
Seleção (torneio)
    ↓
Elitismo (melhores passam)
    ↓
Crossover (reprodução)
    ↓
Mutação (variação)
    ↓
Geração N+1
```

### Fitness (Pontuação)

```python
Fitness = Pontos Positivos - Pontos Negativos

Pontos Positivos:
+ Vitória: +1000
+ Dano causado: +1 por HP
+ Vida restante: +2 por HP

Pontos Negativos:
- Derrota: -500
- Dano recebido: -0.5 por HP
```

### Exemplo de Fitness

```
Personagem A:
- 3 vitórias, 1 derrota
- Causou 450 de dano
- Recebeu 300 de dano
- Vida média restante: 40 HP

Fitness = (3×1000) - (1×500) + 450 - (300×0.5) + (40×2)
        = 3000 - 500 + 450 - 150 + 80
        = 2880 pontos
```

### Parâmetros de Evolução

| Parâmetro | Valor Padrão | Descrição |
|-----------|--------------|-----------|
| População | 20 | Redes por geração |
| Taxa Elite | 20% | Melhores que passam direto |
| Taxa Mutação | 15% | Chance de sofrer mutação |
| Intensidade Mutação | 0.3 | Quanto os pesos mudam |
| Tamanho Torneio | 3 | Candidatos na seleção |

---

## 💻 Uso do Sistema

### 1. Criar Rede Neural

```python
from ia import RedeNeuralPersonagem

# Cria rede para personagem ID 1
rede = RedeNeuralPersonagem(
    personagem_id=1,
    camadas=[12, 16, 8, 4]  # entrada, oculta1, oculta2, saída
)
```

### 2. Decidir Ação

```python
# Durante o jogo
acao = rede.decidir_acao(
    personagem=meu_personagem,
    outros_personagens=lista_inimigos,
    largura=800,
    altura=600
)

# acao contém:
# {'mover_x': -0.5, 'mover_y': 0.8, 'atacar': True, 'fugir': False}

# Aplicar movimento
meu_personagem.vx = acao['mover_x'] * meu_personagem.velocidade
meu_personagem.vy = acao['mover_y'] * meu_personagem.velocidade

# Atacar se necessário
if acao['atacar'] and meu_personagem.arma:
    meu_personagem.arma.disparar()
```

### 3. Treinar com Algoritmo Genético

```python
from ia import TreinadorGenetico

# Criar treinador
treinador = TreinadorGenetico(
    tamanho_populacao=20,
    taxa_mutacao=0.15,
    taxa_elite=0.2
)

# População inicial
treinador.criar_populacao_inicial(personagem_id=1)

# Loop de treinamento
for geracao in range(100):
    # 1. Executar combates com cada rede
    resultados = executar_combates(treinador.populacao)
    
    # 2. Avaliar fitness
    treinador.avaliar_populacao(resultados)
    
    # 3. Salvar melhor
    if geracao % 10 == 0:
        treinador.salvar_melhor(personagem_id=1)
    
    # 4. Nova geração
    treinador.nova_geracao()

# Salvar população final
treinador.salvar_populacao()
```

### 4. Salvar e Carregar

```python
# Salvar rede
rede.salvar("redes_neurais/minha_rede.json")

# Carregar rede
rede_carregada = RedeNeuralPersonagem.carregar(
    "redes_neurais/minha_rede.json"
)

# Usar rede carregada
acao = rede_carregada.decidir_acao(personagem, inimigos)
```

---

## 📊 Exemplos de Comportamento

### Comportamento Agressivo

```
Sensores:
- Inimigo próximo
- Vida alta (>70%)
- Tem arma

Ação da Rede:
- mover_x, mover_y → Em direção ao inimigo
- atacar → True
- fugir → False

Resultado: Persegue e ataca
```

### Comportamento Defensivo

```
Sensores:
- Inimigo próximo
- Vida baixa (<30%)
- Muitos inimigos

Ação da Rede:
- mover_x, mover_y → Direção aleatória
- atacar → False
- fugir → True

Resultado: Foge para se recuperar
```

### Comportamento Estratégico

```
Sensores:
- Inimigo longe
- Vida média (50%)
- Perto da borda

Ação da Rede:
- mover_x, mover_y → Para o centro
- atacar → False (economiza energia)
- fugir → False

Resultado: Posicionamento tático
```

---

## 🎮 Integração com o Jogo

### Modificar main_simulation.py

```python
# Carregar rede neural do personagem
if hasattr(personagem, 'rede_neural'):
    # IA controla
    acao = personagem.rede_neural.decidir_acao(
        personagem, personagens, WIDTH, HEIGHT
    )
    
    # Aplicar movimento
    personagem.vx = acao['mover_x'] * personagem.velocidade
    personagem.vy = acao['mover_y'] * personagem.velocidade
    
    # Atacar
    if acao['atacar'] and personagem.arma:
        # Lógica de ataque
        pass
else:
    # Controle manual ou padrão
    pass
```

### Modificar PersonagemCreate.py

```python
# Ao criar personagem, cria também sua rede neural
from ia import RedeNeuralPersonagem

rede = RedeNeuralPersonagem(novo_id)
rede.salvar(f"redes_neurais/rede_personagem_{novo_id}.json")
```

---

## 📈 Progresso de Treinamento

### Gerações Típicas

| Geração | Fitness Médio | Comportamento |
|---------|---------------|---------------|
| 0-10 | 0-500 | Movimento aleatório |
| 10-30 | 500-1500 | Aprende a evitar bordas |
| 30-60 | 1500-3000 | Persegue inimigos |
| 60-100 | 3000-5000 | Estratégias complexas |
| 100+ | 5000+ | Comportamento otimizado |

### Convergência

```
Fitness
  ^
  |     /-----------  (convergiu)
  |    /
  |   /
  |  /
  | /
  |/___________________>
  0  20  40  60  80  100  Gerações
```

---

## 🔧 Ajustes Finos

### Aumentar Exploração

```python
# Mais mutação, mais variedade
treinador.taxa_mutacao = 0.25

# Menor elite, mais renovação
treinador.taxa_elite = 0.1
```

### Aumentar Estabilidade

```python
# Menos mutação, mais conservador
treinador.taxa_mutacao = 0.05

# Maior elite, preserva bons genes
treinador.taxa_elite = 0.3
```

### Mudar Arquitetura

```python
# Rede mais profunda
rede = RedeNeuralPersonagem(
    personagem_id=1,
    camadas=[12, 32, 16, 8, 4]  # +1 camada oculta
)

# Rede mais larga
rede = RedeNeuralPersonagem(
    personagem_id=1,
    camadas=[12, 24, 24, 4]  # neurônios extras
)
```

---

## 🎯 Estratégias Avançadas

### Co-Evolução

Treinar múltiplos personagens simultaneamente:
```python
# Cada personagem tem sua rede
redes = {
    1: RedeNeuralPersonagem(1),
    2: RedeNeuralPersonagem(2),
    3: RedeNeuralPersonagem(3)
}

# Combates entre todos
for p1 in redes:
    for p2 in redes:
        if p1 != p2:
            resultado = combate(redes[p1], redes[p2])
            # Atualizar fitness
```

### Transfer Learning

Usar rede treinada como base:
```python
# Carregar rede experiente
rede_base = RedeNeuralPersonagem.carregar("melhor_rede.json")

# Criar nova com mesma base
nova_rede = rede_base.clonar()
nova_rede.personagem_id = 2

# Pequena mutação para especializar
nova_rede.mutar(taxa_mutacao=0.05, intensidade=0.1)
```

### Ensembles

Combinar várias redes:
```python
# 3 redes votam
redes = [rede1, rede2, rede3]
acoes = [r.decidir_acao(p, inimigos) for r in redes]

# Média das decisões
acao_final = {
    'mover_x': np.mean([a['mover_x'] for a in acoes]),
    'mover_y': np.mean([a['mover_y'] for a in acoes]),
    'atacar': sum([a['atacar'] for a in acoes]) >= 2,
    'fugir': sum([a['fugir'] for a in acoes]) >= 2
}
```

---

## 📚 Referências Técnicas

### Funções de Ativação

- **Sigmoid**: Saída 0-1, suave
- **Tanh**: Saída -1 a 1, centrada
- **ReLU**: Linear positiva, rápida

### Inicialização Xavier

```python
limite = sqrt(6 / (neurônios_entrada + neurônios_saída))
pesos = random_uniform(-limite, limite)
```

### Seleção por Torneio

1. Escolhe K candidatos aleatórios
2. Retorna o melhor do grupo
3. Mais justo que seleção pura

---

## 🚀 Próximos Passos

1. ✅ Sistema de rede neural implementado
2. ✅ Algoritmo genético pronto
3. ⏳ Integrar com simulação
4. ⏳ Interface de treinamento
5. ⏳ Visualização de comportamento
6. ⏳ Sistema de aprendizado contínuo

---

**Versão:** 1.0  
**Data:** 17 de outubro de 2025  
**Status:** Pronto para integração
