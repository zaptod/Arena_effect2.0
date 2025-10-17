# 🎮 Arena Effect Simulator 2.0

**Simulador de combate com Inteligência Artificial baseada em Redes Neurais e Algoritmos Genéticos**

![Python](https://img.shields.io/badge/Python-3.13.2-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green)
![NumPy](https://img.shields.io/badge/NumPy-Required-orange)
![Status](https://img.shields.io/badge/Status-100%25%20Funcional-success)

---

## 🚀 Destaques

- 🧠 **IA Neural Individual**: Cada personagem possui sua própria rede neural
- 🧬 **Evolução Genética**: IAs aprendem e evoluem através de combates
- 💾 **Persistência**: Progresso salvo automaticamente em JSON
- 🎯 **12 Sensores**: Percepção completa do ambiente
- ⚔️ **Combate Inteligente**: Decisões de movimento e ataque autônomas
- 📊 **Sistema de Fitness**: Avaliação baseada em vitórias, dano e sobrevivência

---

## 📋 Índice

- [Início Rápido](#-início-rápido)
- [Características](#-características)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Arquitetura da IA](#-arquitetura-da-ia)
- [Documentação](#-documentação)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)

---

## ⚡ Início Rápido

```bash
# 1. Instalar dependências
pip install pygame numpy

# 2. Iniciar o jogo
cd Paginas
python main.py

# 3. Criar personagens e começar um combate!
```

**[Ver Guia Completo de Início Rápido →](INICIO_RAPIDO.md)**

---

## ✨ Características

### 🎮 Gameplay
- ✅ Sistema de combate em tempo real
- ✅ 4 tipos de armas com características únicas
- ✅ Múltiplos mapas com obstáculos
- ✅ Sistema de vida (100 HP)
- ✅ Dano baseado em força e colisão
- ✅ Pausar, reiniciar e controles intuitivos

### 🤖 Inteligência Artificial
- ✅ Rede Neural Feedforward (12→16→8→4)
- ✅ 12 sensores normalizados
- ✅ 4 ações de saída
- ✅ Algoritmo genético para evolução
- ✅ Seleção por torneio
- ✅ Elitismo (20%)
- ✅ Mutação gaussiana
- ✅ Crossover de ponto único
- ✅ Função de fitness multi-objetivo

### 💾 Persistência
- ✅ Salvamento automático de IAs
- ✅ Carregamento automático ao iniciar
- ✅ Formato JSON legível
- ✅ Histórico de combates
- ✅ Sistema de IDs reutilizável

---

## 🔧 Instalação

### Requisitos:
- Python 3.13.2 (ou superior)
- Pygame 2.6.1
- NumPy

### Passo a Passo:

```bash
# Clone o repositório
git clone https://github.com/zaptod/Arena_effect2.0.git
cd Arena_effect2.0

# Instale as dependências
pip install pygame numpy

# Execute o jogo
cd Paginas
python main.py
```

### Verificar Instalação:

```bash
# Testar todos os componentes
python testar_ia.py

# Ver exemplos práticos
python exemplo_ia.py
```

---

## 🎮 Como Usar

### 1. Menu Principal

Ao iniciar, você verá 4 opções:

- **👤 Gerenciar Personagens**: Criar, editar e excluir personagens
- **⚔️ Visualizar Armas**: Ver as 4 armas disponíveis
- **🗺️ Visualizar Mapas**: Explorar os mapas disponíveis
- **▶️ Iniciar Simulação**: Começar um combate

### 2. Criar Personagens

1. Clique em "👤 Gerenciar Personagens"
2. Clique em "➕ Criar Novo"
3. Configure:
   - Nome
   - Cor (RGB)
   - Tamanho (10-50)
   - Velocidade (1-10)
   - Força (10-100)
4. Clique em "Salvar"

### 3. Iniciar Combate

1. Clique em "▶️ Iniciar Simulação"
2. Selecione:
   - ✅ 2 ou mais personagens
   - ✅ 1 ou mais armas
   - ✅ 1 mapa
3. Clique em "Iniciar Simulação"
4. **Observe a IA em ação!**

### 4. Durante o Combate

| Tecla | Ação |
|-------|------|
| `ESPAÇO` | Pausar/Continuar |
| `R` | Reiniciar |
| `S` | Estatísticas |
| `ESC` | Sair |

---

## 🧠 Arquitetura da IA

### Rede Neural

```
12 INPUTS → 16 HIDDEN → 8 HIDDEN → 4 OUTPUTS
```

#### Sensores (12 inputs):
1. **Posição própria** (X, Y)
2. **Inimigo mais próximo** (X, Y, distância)
3. **Direção do inimigo** (X, Y)
4. **Vida** (própria, inimigo)
5. **Arma** (possui?)
6. **Bordas** (distância X, Y)

#### Ações (4 outputs):
1. **Mover X** (-1 a 1)
2. **Mover Y** (-1 a 1)
3. **Atacar** (sim/não)
4. **Fugir** (sim/não)

### Fitness

```python
Fitness = (vitórias × 1000) 
        - (derrotas × 500)
        + dano_causado
        - (dano_recebido × 0.5)
```

### Evolução

```
População Inicial (aleatória)
    ↓
Avaliar Fitness (combates)
    ↓
Seleção por Torneio (3 candidatos)
    ↓
Elitismo (20% melhores)
    ↓
Crossover + Mutação
    ↓
Nova Geração
    ↓
[Repetir]
```

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | Guia rápido de 3 passos |
| **[STATUS_FINAL.md](STATUS_FINAL.md)** | Status completo do projeto |
| **[SISTEMA_IA_NEURAL.md](SISTEMA_IA_NEURAL.md)** | Documentação técnica detalhada (500+ linhas) |
| **[API_REFERENCIA.md](API_REFERENCIA.md)** | Referência rápida de métodos |
| **[IA_INTEGRADA.md](IA_INTEGRADA.md)** | Guia de integração |
| **[RESUMO_IA.md](RESUMO_IA.md)** | Visão geral executiva |

---

## 📸 Screenshots

### Menu Principal
```
┌─────────────────────────────────────┐
│     Arena Effect Simulator 2.0      │
│                                     │
│  [👤 Gerenciar Personagens]         │
│  [⚔️ Visualizar Armas]              │
│  [🗺️ Visualizar Mapas]              │
│  [▶️ Iniciar Simulação]             │
└─────────────────────────────────────┘
```

### Combate em Ação
```
Personagem 1: ████████████░░░░░░░░ 60/100 HP
Personagem 2: █████████████████░░░ 85/100 HP

🎯 IA controlando movimento
⚔️ IA decidindo ataques
📊 Fitness sendo calculado
```

### Console
```
🧠 IA carregada para personagem 1
🧠 Nova IA criada para personagem 2
✅ Rede neural salva com fitness: 1234.56
```

---

## 🗺️ Roadmap

### ✅ Versão 2.0 (Atual)
- [x] Sistema de IA Neural completo
- [x] Algoritmo genético
- [x] Persistência automática
- [x] Integração total com gameplay
- [x] Documentação completa

### 🔮 Versão 2.1 (Planejada)
- [ ] Interface de treinamento
- [ ] Gráficos de evolução
- [ ] Visualização de decisões da IA
- [ ] Modo espectador

### 🌟 Versão 3.0 (Futuro)
- [ ] Redes LSTM (memória)
- [ ] Aprendizado por reforço
- [ ] Torneios automáticos
- [ ] Rankings globais
- [ ] Compartilhamento de IAs

---

## 🧪 Testes

### Teste de Integração:
```bash
python testar_ia.py
```

Verifica:
- ✅ Importações
- ✅ Criação de redes
- ✅ Sensores
- ✅ Decisões
- ✅ Mutação
- ✅ Crossover
- ✅ Fitness
- ✅ Save/Load
- ✅ Treinador genético
- ✅ Integração com simulação

### Exemplos Práticos:
```bash
python exemplo_ia.py
```

Demonstra:
1. Criação básica
2. Treinamento genético
3. Mutação e crossover
4. Processamento de sensores
5. Comparação de fitness

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

---

## 👨‍💻 Autor

**zaptod**
- GitHub: [@zaptod](https://github.com/zaptod)

---

## 🙏 Agradecimentos

- Pygame Community
- NumPy Contributors
- Comunidade Python

---

## 📞 Suporte

**Encontrou um bug?**
- Abra uma [Issue](https://github.com/zaptod/Arena_effect2.0/issues)

**Tem uma pergunta?**
- Consulte a [Documentação](SISTEMA_IA_NEURAL.md)
- Execute `python testar_ia.py` para diagnóstico

**Quer ver exemplos?**
- Execute `python exemplo_ia.py`

---

## 🎯 Experimente Agora!

```bash
cd Paginas
python main.py
```

**Veja personagens aprendendo a lutar sozinhos! 🤖⚔️**

---

<div align="center">

**[⭐ Star este projeto](https://github.com/zaptod/Arena_effect2.0)** se você gostou!

Made with ❤️ and 🧠 Neural Networks

</div>
