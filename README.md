# NIM MCTS

Um projeto que implementa o jogo NIM utilizando o algoritmo Monte Carlo Tree Search (MCTS) para criar uma inteligência artificial competitiva.

## Sobre o Projeto

O jogo NIM é um jogo de estratégia matemática onde dois jogadores alternam turnos removendo objetos de pilhas distintas. O objetivo é evitar remover o último objeto (regra misère). Este projeto implementa:

- **Interface gráfica** com Pygame para uma experiência visual interativa
- **Modo terminal** para jogar via linha de comando
- **Simulações automatizadas** para testar a eficácia da IA
- **Algoritmo MCTS** para tomada de decisões inteligentes da IA

### Características

- IA baseada em Monte Carlo Tree Search
- Múltiplos modos de jogo (gráfico, terminal, simulação)
- Interface visual moderna com Pygame
- Configuração dinâmica do número de pilhas
- Sistema de logs para análise de desempenho

## Dependências

O projeto requer Python 3.7+ e as seguintes bibliotecas:

```txt
pygame==2.6.1
numpy==2.3.0
```

### Configuração do Ambiente

#### Windows

1. **Instalar Python 3.7+**: https://www.python.org/downloads/
2. **Configurar ambiente para Pygame**:

```cmd
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

```


#### macOS

1. **Instalar dependências do sistema**:

```bash
# Instalar Python e dependências para Pygame
brew install python3
```

#### Linux 

1. **Instalar dependências do sistema para Pygame**:

```bash
sudo apt update
sudo apt install python3-dev python3-pip
```

#### Como Executar

### Windows

```cmd
# Executar o jogo principal
python nim_mcts.py

# Ou usando Python 3 explicitamente
py nim_mcts.py
```

### macOS

```bash
# Executar o jogo principal
python3 nim_mcts.py
```

### Linux

```bash
# Executar o jogo principal
python3 nim_mcts.py

# Ou se python aponta para Python 3
python nim_mcts.py
```

## Modos de Jogo

Ao executar o programa, você poderá escolher entre três modos:

1. **Interface Gráfica**: Jogo visual com Pygame
2. **Terminal**: Versão em linha de comando
3. **Simulação**: Executa múltiplas partidas para análise da IA

## Estrutura do Projeto

```
NIM_MCTS/
├── nim_mcts.py      # Arquivo principal e lógica do jogo
├── Estado.py        # Classe que representa o estado do jogo
├── mcts.py          # Implementação do algoritmo MCTS
├── MCTSNode.py      # Classe para nós da árvore MCTS
├── frame.py         # Interface gráfica com Pygame
├── requirements.txt # Dependências do projeto
└── README.md      
```
