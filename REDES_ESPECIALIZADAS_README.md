# 🧠⚔️ Sistema de Redes Neurais Especializadas por Arma

## 📋 Visão Geral

O sistema agora suporta **redes neurais especializadas** para cada combinação de **Personagem + Arma**. Isso significa que cada personagem desenvolve estratégias de combate únicas dependendo da arma que está usando.

## 🎯 Por Que Isso É Importante?

### Antes (Sistema Antigo):
```
Personagem 0 → 1 rede neural genérica
  ├─ Com Espada: usa mesma IA
  ├─ Com Arco: usa mesma IA
  ├─ Com Adaga: usa mesma IA
  └─ Com Martelo: usa mesma IA
```
❌ **Problema**: A IA não sabia adaptar estratégias para cada arma!

### Agora (Sistema Novo):
```
Personagem 0
  ├─ rede_personagem_0_arma_1.json → IA especializada em ESPADA
  ├─ rede_personagem_0_arma_2.json → IA especializada em ARCO
  ├─ rede_personagem_0_arma_3.json → IA especializada em ADAGA
  └─ rede_personagem_0_arma_4.json → IA especializada em MARTELO
```
✅ **Solução**: Cada arma tem sua própria IA treinada!

## 🔧 Como Funciona

### 1. Criação de Redes Neurais

```python
# Antes
rede = RedeNeuralPersonagem(personagem_id=0)

# Agora
rede_espada = RedeNeuralPersonagem(personagem_id=0, arma_id=1)
rede_arco = RedeNeuralPersonagem(personagem_id=0, arma_id=2)
```

### 2. Salvamento de Arquivos

As redes são salvas com nomenclatura específica:

```
redes_neurais/
├── rede_personagem_0_arma_1.json  # Personagem 0 com Espada
├── rede_personagem_0_arma_2.json  # Personagem 0 com Arco
├── rede_personagem_1_arma_1.json  # Personagem 1 com Espada
├── rede_personagem_1_arma_3.json  # Personagem 1 com Adaga
└── ...
```

### 3. Carregamento Automático

O sistema **automaticamente** carrega a rede correta baseado na arma equipada:

```python
# No modo treino ou simulação:
if personagem tem arma:
    carregar rede_personagem_{id}_arma_{arma_id}.json
else:
    carregar rede_personagem_{id}.json (genérica)
```

## 💡 Exemplos de Comportamentos Especializados

### ⚔️ Espada (Arma 1)
- **Alcance curto**
- **Dano médio**
- **IA aprende**: Aproximar-se do inimigo, circular, atacar quando próximo

### 🏹 Arco (Arma 2)
- **Alcance longo**
- **Dano baixo**
- **IA aprende**: Manter distância, fugir quando inimigo se aproxima, atirar de longe

### 🗡️ Adaga (Arma 3)
- **Alcance muito curto**
- **Dano alto**
- **Velocidade rápida**
- **IA aprende**: Ataques rápidos, hit-and-run, aproveitar cooldown inimigo

### 🔨 Martelo (Arma 4)
- **Alcance médio**
- **Dano muito alto**
- **Velocidade lenta**
- **IA aprende**: Timing preciso, golpes devastadores, tankar dano

## 🎮 Como Treinar IAs Especializadas

### Método 1: Modo Treino Loop

1. Execute `python Paginas/main.py`
2. Clique em **"🔄 Modo Treino Loop (30s)"**
3. Selecione:
   - Personagem 1 (ex: ID 0)
   - Personagem 2 (ex: ID 1)
   - **Arma específica para cada um**
   - Mapa
4. Deixe rodar várias rodadas (20-50+)
5. A IA aprenderá estratégias específicas para aquela arma

### Método 2: Treinar Todas as Combinações

Execute múltiplas sessões de treino:

```
Sessão 1: P0 com Espada vs P1 com Espada
Sessão 2: P0 com Arco vs P1 com Espada
Sessão 3: P0 com Adaga vs P1 com Arco
...
```

Após todas as sessões, você terá IAs especializadas para cada arma!

## 📊 Visualizando Diferenças

Execute o script de teste:

```bash
python testar_redes_especializadas.py
```

Isso irá:
- ✅ Criar redes de exemplo
- ✅ Salvar com nomes corretos
- ✅ Carregar e verificar
- ✅ Comparar estatísticas

## 🔍 Arquitetura Técnica

### Estrutura da Classe `RedeNeuralPersonagem`

```python
class RedeNeuralPersonagem:
    def __init__(self, personagem_id, arma_id=None, camadas=[12, 16, 8, 4]):
        self.personagem_id = personagem_id  # ID do personagem
        self.arma_id = arma_id              # ID da arma (NOVO!)
        self.camadas = camadas
        # ... pesos, bias, etc.
```

### Arquivo JSON

```json
{
  "personagem_id": 0,
  "arma_id": 1,
  "camadas": [12, 16, 8, 4],
  "pesos": [...],
  "bias": [...],
  "fitness": 500,
  "vitorias": 10,
  "derrotas": 5,
  "dano_causado": 2500,
  "dano_recebido": 1200
}
```

## 🧪 Experimentos Recomendados

### Experimento 1: Especialização Pura
- Treine P0 com Espada por 50 rodadas
- Treine P0 com Arco por 50 rodadas
- Compare: Quem vence em P0_Espada vs P0_Arco?

### Experimento 2: Meta-Aprendizado
- Treine múltiplas armas
- Identifique qual arma desenvolve melhor IA
- Use essa arma como "principal"

### Experimento 3: Counter-Strategies
- Treine P0_Arco vs P1_Espada (arqueiro vs guerreiro)
- Observe se P0 aprende a manter distância
- Observe se P1 aprende a fechar a distância

## 📈 Métricas de Sucesso

Após treinamento extensivo, você deve observar:

✅ **Especialização**:
- IA com arco mantém distância > IA com espada
- IA com adaga ataca mais frequentemente
- IA com martelo aguarda momento certo

✅ **Independência**:
- Treinar P0 com Espada não afeta P0 com Arco
- Cada rede evolui separadamente

✅ **Performance**:
- IAs especializadas vencem mais que genéricas
- Menos empates por timeout
- Estratégias visíveis no comportamento

## 🚀 Melhorias Futuras Possíveis

1. **Transfer Learning**: Usar rede de uma arma como base para outra similar
2. **Ensemble**: Combinar decisões de múltiplas redes
3. **Meta-IA**: IA que escolhe qual arma usar baseado no oponente
4. **Análise de Matchups**: Qual arma é counter de qual
5. **Torneios**: Cada personagem escolhe sua melhor arma

## 🎓 Conceitos de IA Envolvidos

- **Specialization**: Redes diferentes para tarefas diferentes
- **Domain Adaptation**: Adaptar comportamento ao contexto (arma)
- **Multi-Task Learning**: Aprender múltiplas habilidades independentemente
- **Genetic Algorithm**: Evolução através de combates repetidos
- **Fitness Function**: Vitórias, dano, sobrevivência

## 🐛 Troubleshooting

### Problema: Arquivo não encontrado
```
Solução: Execute o modo treino primeiro para criar as redes
```

### Problema: Todas as IAs agem igual
```
Solução: Treine mais rodadas (mínimo 20-30 por arma)
```

### Problema: IA não melhora
```
Solução: Verifique se fitness está sendo calculado corretamente
         Aumente taxa de mutação no algoritmo genético
```

## 📝 Notas Importantes

- 🔄 **Retrocompatibilidade**: Redes antigas sem `arma_id` ainda funcionam
- 💾 **Backup**: Faça backup antes de treinos longos
- 🧠 **Memória**: Cada rede ocupa ~2-5 KB
- ⚡ **Performance**: Não há impacto de performance (mesmo número de operações)

---

**Desenvolvido para Arena Effect Simulator 2.0**
**Sistema de IA com Especialização por Arma**
