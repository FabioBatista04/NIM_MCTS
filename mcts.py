from MCTSNode import MCTSNode
import random

def mcts(estado, iteracoes=1000):
    
    raiz = MCTSNode(estado)

    for i in range(iteracoes):
        no = raiz

        # 1. SELEÇÃO - navegar pela árvore usando UCB1
        while no.filhos and not no.estado.fim_de_jogo():
            no = no.selecionar_filho()

        # 2. EXPANSÃO - expandir se o nó não é terminal e não foi expandido
        if not no.estado.fim_de_jogo() and not no.filhos:   # <── só se ainda não tiver filhos
            no.expandir()
            no = random.choice(no.filhos)

        # 3. SIMULAÇÃO - jogar até o fim
        resultado = no.simular()

        # 4. BACKPROPAGAÇÃO - atualizar estatísticas
        no.backpropagar(resultado)

    # Escolher a melhor jogada baseada no número de visitas
    if not raiz.filhos:
        jogadas = estado.jogadas_possiveis()
        return random.choice(jogadas) if jogadas else None
    
    # Escolher o filho mais visitado (estratégia robusta)
    melhor_filho = max(raiz.filhos, key=lambda f: f.visitas)
    
    return melhor_filho.jogada