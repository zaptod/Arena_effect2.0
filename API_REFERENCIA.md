# 📋 REFERÊNCIA RÁPIDA - API do Sistema

## 🎮 Métodos das Armas

```python
# Classe Arma (base)
arma.pode_atacar()      # Verifica se pode atacar (cooldown)
arma.atacar()           # Realiza o ataque
arma.update(dt)         # Atualiza estado (cooldown, etc)
```

## 🤖 Métodos da Rede Neural

```python
# Classe RedeNeuralPersonagem
rede = RedeNeuralPersonagem(personagem_id)
rede = RedeNeuralPersonagem(personagem_id, camadas=[12, 16, 8, 4])

# Sensores e decisão
sensores = rede.processar_sensores(personagem, outros_personagens, width, height)
acao = rede.decidir_acao(personagem, outros_personagens, width, height)
# Retorna: {'mover_x': float, 'mover_y': float, 'atacar': bool, 'fugir': bool}

# Evolução
rede.mutar(taxa_mutacao=0.1, intensidade=0.3)
filho = rede.crossover(outra_rede)

# Fitness
fitness = rede.calcular_fitness()
# Baseia-se em: rede.vitorias, rede.derrotas, rede.dano_causado, rede.dano_recebido

# Persistência
rede.salvar('caminho/para/rede.json')
rede_carregada = RedeNeuralPersonagem.carregar('caminho/para/rede.json')

# Atributos principais
rede.personagem_id    # ID do personagem
rede.camadas          # [12, 16, 8, 4] - arquitetura
rede.pesos            # Lista de matrizes NumPy
rede.biases           # Lista de vetores NumPy
rede.vitorias         # Contador de vitórias
rede.derrotas         # Contador de derrotas
rede.dano_causado     # Total de dano causado
rede.dano_recebido    # Total de dano recebido
```

## 🧬 Métodos do Treinador Genético

```python
# Classe TreinadorGenetico
treinador = TreinadorGenetico(tamanho_populacao=20)

# População
treinador.criar_populacao_inicial(personagem_id)

# Avaliação
resultados = [
    {
        'rede_id': 0,
        'vitorias': 1,
        'derrotas': 0,
        'dano_causado': 100,
        'dano_recebido': 50,
        'venceu': True
    },
    # ... mais resultados
]
treinador.avaliar_populacao(resultados)

# Evolução
treinador.nova_geracao()

# Persistência
treinador.salvar_populacao('diretorio')
treinador.carregar_populacao('diretorio')

# Atributos
treinador.populacao          # Lista de RedeNeuralPersonagem
treinador.geracao_atual      # Número da geração atual
treinador.tamanho_populacao  # Tamanho da população
treinador.taxa_elitismo      # 0.2 (20% melhores passam)
treinador.historico_fitness  # Lista de fitness por geração
```

## 👤 Atributos do Personagem (com IA)

```python
# Atributos básicos (já existentes)
personagem.id
personagem.nome
personagem.x, personagem.y
personagem.vx, personagem.vy
personagem.velocidade
personagem.forca
personagem.tamanho
personagem.cor
personagem.vida_atual
personagem.vida_maxima
personagem.vivo
personagem.arma

# Novos atributos para IA
personagem.rede_neural       # RedeNeuralPersonagem ou None
personagem.ia_atacar         # bool - IA quer atacar?
personagem.ia_fugir          # bool - IA quer fugir?

# Métodos
personagem.receber_dano(valor)
personagem.curar(valor)
```

## 🎯 Funções da Simulação

```python
# main_simulation.py

# Aplicar IA ao personagem
aplicar_ia_personagem(personagem, outros_personagens, width, height)

# Salvar redes neurais após combate
salvar_redes_neurais(personagens_originais, vencedores)

# Verificar colisão
colidiu = check_collision(personagem1, personagem2)

# Tratar colisão (aplica dano e registra para fitness)
handle_collision(personagem1, personagem2)

# Atualizar posição
update_personagem(personagem, dt, width, height)
```

## 🔧 Flags e Constantes

```python
# Verificar disponibilidade da IA
from ia import RedeNeuralPersonagem, TreinadorGenetico
IA_DISPONIVEL = True  # ou False se import falhar

# Diretório de redes neurais
'redes_neurais/'  # Criado automaticamente
'redes_neurais/rede_personagem_{id}.json'
```

## 📊 Estrutura de Sensores (12 inputs)

```python
sensores = [
    personagem.x / width,              # 0: Posição X normalizada
    personagem.y / height,             # 1: Posição Y normalizada
    inimigo_x / width,                 # 2: Inimigo mais próximo X
    inimigo_y / height,                # 3: Inimigo mais próximo Y
    distancia / diagonal,              # 4: Distância do inimigo
    direcao_x,                         # 5: Direção X do inimigo (-1 a 1)
    direcao_y,                         # 6: Direção Y do inimigo (-1 a 1)
    personagem.vida_atual / vida_max,  # 7: Vida própria (0-1)
    inimigo.vida_atual / vida_max,     # 8: Vida do inimigo (0-1)
    1.0 if tem_arma else 0.0,          # 9: Possui arma?
    distancia_borda_x,                 # 10: Distância da borda X (0-1)
    distancia_borda_y                  # 11: Distância da borda Y (0-1)
]
```

## 🎮 Estrutura de Ação (4 outputs)

```python
acao = {
    'mover_x': -1.0 a 1.0,    # Movimento horizontal
    'mover_y': -1.0 a 1.0,    # Movimento vertical
    'atacar': True/False,      # Atacar agora?
    'fugir': True/False        # Modo defensivo?
}
```

## 💪 Fórmula de Fitness

```python
fitness = (vitorias * 1000) - (derrotas * 500) + dano_causado - (dano_recebido * 0.5)
```

**Interpretação:**
- `>= 1000`: IA excelente (vencendo batalhas)
- `0-1000`: IA mediana
- `< 0`: IA fraca (perdendo muito)

## 🚀 Fluxo Típico de Uso

### Combate Simples (automático):
```python
# 1. Inicie o jogo normalmente
python main.py

# 2. Selecione personagens e inicie simulação
# - Redes neurais carregam automaticamente
# - Se não existir, cria nova
# - IA controla personagens durante combate
# - Salva automaticamente ao final
```

### Treinamento Manual:
```python
from ia import RedeNeuralPersonagem, TreinadorGenetico

# Criar treinador
treinador = TreinadorGenetico(tamanho_populacao=20)
treinador.criar_populacao_inicial(personagem_id=1)

# Simular gerações
for geracao in range(50):
    # Executar combates (sua lógica aqui)
    resultados = executar_combates(treinador.populacao)
    
    # Avaliar
    treinador.avaliar_populacao(resultados)
    
    # Nova geração
    treinador.nova_geracao()
    
    # Salvar progresso
    if geracao % 10 == 0:
        treinador.salvar_populacao(f'treinamento_gen_{geracao}')
```

## 🐛 Troubleshooting Comum

### Problema: AttributeError 'pode_atirar'
**Solução:** Use `pode_atacar()` e `atacar()`

### Problema: KeyError 'tamanhos'
**Solução:** Use `rede.camadas` em vez de `rede.tamanhos`

### Problema: KeyError 'geracao'
**Solução:** Use `treinador.geracao_atual` em vez de `treinador.geracao`

### Problema: Import rede_neural falha
**Solução:** Use `from .rede_neural` (import relativo) em arquivos dentro de `ia/`

### Problema: Personagens não se movem
**Verificar:**
```python
print(IA_DISPONIVEL)  # Deve ser True
print(hasattr(personagem, 'rede_neural'))  # Deve ser True
print(personagem.vx, personagem.vy)  # Devem ser != 0
```

## 📁 Estrutura de Arquivos

```
Arena_effect2.0/
├── ia/
│   ├── __init__.py           # Exporta RedeNeuralPersonagem, TreinadorGenetico
│   ├── rede_neural.py        # Classe RedeNeuralPersonagem (658 linhas)
│   └── treinador.py          # Classe TreinadorGenetico (207 linhas)
│
├── redes_neurais/            # Criado automaticamente
│   ├── rede_personagem_1.json
│   ├── rede_personagem_2.json
│   └── ...
│
├── Paginas/
│   ├── main.py               # Menu principal
│   ├── main_simulation.py    # Simulação com IA integrada
│   ├── personagensP.py       # Gerenciamento de personagens
│   └── SelectionP.py         # Seleção para combate
│
├── exemplo_ia.py             # 5 exemplos de uso
├── testar_ia.py              # Testes de integração
├── SISTEMA_IA_NEURAL.md      # Documentação técnica completa
├── RESUMO_IA.md              # Resumo executivo
└── IA_INTEGRADA.md           # Guia de integração
```

## ✅ Checklist de Integração

- [x] Módulo `ia/` criado
- [x] Imports relativos corretos
- [x] `IA_DISPONIVEL` flag funcionando
- [x] Sensores normalizados (0-1)
- [x] Decisões aplicadas no game loop
- [x] Ataques controlados pela IA
- [x] Dano registrado para fitness
- [x] Salvamento automático após combate
- [x] Carregamento automático ao iniciar
- [x] Testes de integração passando
- [x] Métodos corretos (pode_atacar, atacar)

---

**Última atualização:** Sistema 100% integrado e funcional
