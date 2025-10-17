# 🖥️ Visualizador de Redes Neurais - Modo Treino

## 📺 Nova Funcionalidade

Ao iniciar o **Modo Treino Loop**, uma **segunda janela** será aberta automaticamente mostrando as redes neurais de ambos os jogadores em tempo real!

## 🎨 O Que é Exibido

### Janela Principal (Jogo)
- ✅ Arena de combate
- ✅ Personagens lutando
- ✅ Timer de 30 segundos
- ✅ Estatísticas de vitórias

### Janela Secundária (Visualizador Neural) ⭐ NOVO!
- 🧠 **Redes Neurais Lado a Lado**
  - Player 1 (Azul) - Esquerda
  - Player 2 (Vermelho) - Direita

- 📊 **Cada Rede Mostra**:
  - **Camada de Entrada** (12 neurônios)
    - Pos X, Pos Y
    - Direção → Inimigo (X, Y)
    - Distância do Inimigo
    - Vida Própria, Vida Inimigo
    - Tem Arma
    - Distância das Bordas (X, Y)
    - Número de Inimigos
    - Força Relativa
  
  - **Camadas Ocultas** (16 e 8 neurônios)
    - Neurônios processando informações
    - Conexões entre camadas (pesos)
  
  - **Camada de Saída** (5 neurônios)
    - Movimento X
    - Movimento Y
    - Atacar
    - Fugir
    - **Ângulo da Arma** ⭐

## 🎨 Visualização em Tempo Real

### Cores dos Neurônios
- **Mais escuro**: Neurônio inativo (valor próximo de 0)
- **Mais brilhante**: Neurônio ativo (valor próximo de 1)
- **Player 1**: Tom azul 🔵
- **Player 2**: Tom vermelho 🔴

### Conexões Entre Neurônios
- **Verde**: Peso positivo (conexão excitatória)
- **Vermelho**: Peso negativo (conexão inibitória)
- **Espessura**: Magnitude do peso
- ⚠️ Apenas as 20 conexões mais fortes são mostradas (para evitar poluição visual)

### Informações Exibidas
```
Legenda ao lado de cada neurônio:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENTRADAS (12):
  Pos X: 0.45
  Pos Y: 0.62
  Dir→Inimigo X: -0.23
  Dir→Inimigo Y: 0.87
  ... etc

SAÍDAS (5):
  Mov X: 0.32
  Mov Y: -0.12
  Atacar: 0.88  ← Alta probabilidade!
  Fugir: 0.05
  Ângulo Arma: 0.74  ← ~4.66 radianos
```

### Informações da Rodada
```
┌─────────────────────────────┐
│ Rodada: 15                  │
│ Tempo: 12s                  │
│ P1 HP: 87                   │
│ P2 HP: 65                   │
└─────────────────────────────┘
```

### Estatísticas da IA
```
Gen: 5 | Fitness: 2340 | V:8 D:2
     ↑         ↑         ↑   ↑
  Geração   Pontos   Vitórias Derrotas
```

## 🚀 Como Usar

1. **Inicie o Modo Treino**:
   ```
   Menu Principal → 🔄 Modo Treino Loop (30s)
   ```

2. **Selecione Personagens e Armas**:
   - Player 1 e Player 2
   - Armas respectivas
   - Mapa

3. **Clique em "Iniciar Treino"**:
   - Janela principal abre (arena)
   - **Janela secundária abre automaticamente** (visualizador) 🎉

4. **Observe as IAs Aprendendo**:
   - Veja os neurônios piscando
   - Observe quais sensores são mais usados
   - Acompanhe as decisões em tempo real

## 🎯 O Que Observar

### Comportamentos Interessantes

#### 🔍 Neurônios de Entrada
- **Pos X/Y altamente ativados**: IA está ciente da posição
- **Dir→Inimigo piscando**: IA rastreando o oponente
- **Dist Inimigo oscilando**: IA medindo distância constantemente
- **Vida Própria baixa → Fugir ativa**: Comportamento de sobrevivência!

#### 🧠 Camadas Ocultas
- **Muitos neurônios ativos**: IA processando muita informação
- **Poucos neurônios ativos**: IA simplificou a estratégia
- **Padrões cíclicos**: IA pode estar em loop de decisão

#### ⚡ Neurônios de Saída
- **Atacar sempre alto**: IA agressiva
- **Fugir frequentemente ativo**: IA defensiva
- **Mov X/Y coordenados**: Movimento estratégico
- **Ângulo Arma variando**: IA controlando mira independentemente! ⭐

### Evolução ao Longo das Rodadas
- **Primeiras Rodadas**: Comportamento aleatório, neurônios erráticos
- **Rodadas Intermediárias**: Padrões começam a surgir
- **Rodadas Avançadas**: Estratégias claras, decisões coordenadas

## 🛠️ Controles

### Janela Principal
- `ESPAÇO`: Pausar/Continuar
- `ESC`: Sair do treino
- Mouse: Clicar nos botões

### Janela do Visualizador
- ❌ **Fechar janela**: Encerra o treino completo
- 👁️ **Somente visualização**: Não há controles interativos

## ⚙️ Requisitos

- ✅ Python 3.13.2
- ✅ Pygame 2.6.1
- ✅ NumPy
- ✅ Sistema de IA ativo

## ⚠️ Notas Importantes

### Performance
- O visualizador pode **reduzir levemente o FPS** do treino
- Recomendado para observação e aprendizado, não para treinos longos (milhares de rodadas)

### Erros
Se o visualizador não abrir:
```
⚠️ Visualizador de rede neural não disponível
```
**Motivo**: Erro na importação do módulo
**Solução**: Verifique se `visualizador_rede.py` está no diretório raiz

### Fechamento
- **Fechar qualquer janela**: Encerra ambas
- **ESC na janela principal**: Encerra gracefully
- As redes neurais são **salvas automaticamente** ao sair

## 🎓 Dicas de Aprendizado

### Para Entender a IA
1. **Observe uma rodada completa** sem pausar
2. **Compare Player 1 vs Player 2**: Quem usa mais quais sensores?
3. **Pause em momentos chave**: Quando atacam, quando fogem
4. **Monitore a evolução**: Como o Fitness muda?

### Para Treinar Melhor
1. **Deixe rodar várias rodadas** (30+)
2. **Observe quando empates ocorrem**: IAs muito defensivas?
3. **Note comportamentos emergentes**: Estratégias não programadas!
4. **Compare gerações**: Gen 1 vs Gen 10 - diferença visível

## 📈 Exemplos de Padrões

### IA Agressiva
```
Entrada: Dist Inimigo = 0.3 (próximo)
Saída:   Atacar = 0.95 ✓
         Fugir = 0.05
         Ângulo Arma = aponta para inimigo
```

### IA Defensiva
```
Entrada: Vida Própria = 0.2 (baixa)
Saída:   Fugir = 0.90 ✓
         Mov X/Y = afastando
         Atacar = 0.10
```

### IA Tática (Emergente!)
```
Entrada: Dist Inimigo = 0.7 (longe)
         Vida Própria = 0.8 (alta)
Saída:   Mov X/Y = aproximando
         Ângulo Arma = antecipando posição!
         Atacar = 0.50 (aguardando momento)
```

## 🎉 Aproveite!

Use o visualizador para:
- 🎓 **Aprender** como redes neurais funcionam
- 🔬 **Investigar** comportamentos emergentes
- 🎮 **Divertir-se** vendo IAs evoluírem
- 🏆 **Competir** - qual IA aprende mais rápido?

**Dica Final**: Deixe rodar por 50+ rodadas e veja a magia acontecer! 🧙‍♂️✨
