# 🔄 Modo Treino Loop - Sistema de Treinamento de IA

## 📋 Visão Geral

O **Modo Treino Loop** é um sistema automatizado para treinar as redes neurais dos personagens através de combates contínuos e repetidos.

## ⏱️ Características Principais

### 🕐 Timer de 30 Segundos
- Cada rodada dura **30 segundos**
- Timer otimizado para combates rápidos e intensos
- Incentiva comportamento agressivo da IA

### 🔄 Sistema de Loop Automático
- **Rodadas contínuas**: Ao final de cada combate, uma nova rodada começa automaticamente
- **Intervalo de 3 segundos** entre rodadas
- Sistema roda indefinidamente até que você pressione ESC

### 🧠 Treinamento de Rede Neural
- Redes neurais são **salvas automaticamente** ao final de cada rodada
- Vitórias e derrotas afetam o fitness das redes
- Sistema de evolução através de combates repetidos

### ⚠️ Sistema de Punição
- Se o timer chegar a **0 segundos**: Ambos os personagens perdem **50 HP**
- Incentiva IAs agressivas que finalizam lutas rapidamente
- Após punição, vencedor é determinado por HP restante

### 💤 Sistema Anti-Inatividade (NOVO!)
- Se **ninguém causar dano por 10 segundos**: Rodada termina em **EMPATE**
- Evita situações onde personagens ficam fugindo sem lutar
- Incentiva comportamento agressivo e engajamento
- Indicador visual aparece após 5 segundos sem dano
- Contador regressivo mostra tempo restante antes do empate

## 📊 Estatísticas em Tempo Real

Durante o treino, você vê:
- 🔄 **Número da rodada atual**
- 🏆 **Vitórias do Personagem 1**
- 🏆 **Vitórias do Personagem 2**
- 🤝 **Total de empates**

## 🎮 Como Usar

1. **Acesse o Menu Principal**
   ```
   python Paginas/main.py
   ```

2. **Clique em "🔄 Modo Treino Loop (30s)"**

3. **Configure o Treino:**
   - Selecione 2 personagens
   - Escolha 1 arma para cada personagem
   - Selecione 1 mapa

4. **Clique em "🔄 INICIAR TREINO LOOP"**

5. **O Sistema Irá:**
   - Iniciar a primeira rodada (30s)
   - Determinar o vencedor
   - Salvar as redes neurais
   - Aguardar 3 segundos
   - Iniciar a próxima rodada automaticamente
   - Repetir indefinidamente

6. **Para Parar o Treino:**
   - Pressione **ESC** a qualquer momento
   - Ou pressione **ESPAÇO** para pausar/continuar

## 🎯 Objetivo

O objetivo do Modo Treino Loop é:
- 🧠 **Evoluir as redes neurais** através de experiência de combate
- 📈 **Melhorar estratégias** de ataque e defesa
- 🏆 **Desenvolver comportamentos vencedores**
- ⚡ **Criar IAs mais agressivas** que finalizam lutas rapidamente

## 💾 Salvamento de Progresso

- Redes neurais são salvas em `redes_neurais/rede_personagem_X.json`
- Cada rodada atualiza o fitness da IA vencedora
- Vencedores acumulam experiência positiva
- Perdedores acumulam experiência negativa (incentivando evolução)

## 📈 Resultados Esperados

Após várias rodadas de treino, você deve observar:
- ✅ IAs mais agressivas
- ✅ Melhores estratégias de combate
- ✅ Uso mais eficiente das armas
- ✅ Menor número de empates por timeout
- ✅ Lutas mais rápidas e decisivas

## 🔧 Parâmetros Configuráveis

Para ajustar o treino, edite `modo_treino.py`:
- `tempo_treino = 30.0` - Duração de cada rodada (segundos)
- `tempo_entre_rodadas >= 3.0` - Intervalo entre rodadas (segundos)
- Punição de HP no timeout (linha do `receber_dano(50)`)

## 🎨 Interface

### Durante o Combate:
- Timer grande no centro superior
- Painel de estatísticas no canto superior esquerdo
- **Indicador de inatividade** no canto superior direito (após 5s sem dano)
  - Amarelo: Aviso inicial
  - Laranja: Atenção (≤5s restantes)
  - Vermelho: Crítico (≤2s restantes)
- Barras de vida dos personagens
- Botões de Pausar e Sair

### Ao Final de Cada Rodada:
- Overlay semi-transparente
- Nome do vencedor (ou "EMPATE")
- Razão do resultado:
  - Vitória por morte
  - Empate por timeout com punição
  - **Empate por inatividade (10s sem dano)**
- Contador regressivo para próxima rodada
- Instruções de saída (ESC)

## 🚀 Dicas de Uso

1. **Treino Noturno**: Deixe rodando durante a noite para treinar extensivamente
2. **Comparação**: Treine diferentes combinações de personagens/armas
3. **Evolução**: Observe como as estatísticas mudam ao longo das rodadas
4. **Backup**: Faça backup das redes neurais antes de treinos longos

## ⚙️ Requisitos Técnicos

- Python 3.13+
- Pygame 2.6.1+
- NumPy (para redes neurais)
- Módulo `ia/` completo e funcional

---

**Desenvolvido para Arena Effect Simulator 2.0**
**Sistema de IA com Redes Neurais e Algoritmo Genético**
