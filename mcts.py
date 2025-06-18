from MCTSNode import MCTSNode
import random

quantidade_de_buscas = 0
quantidade_de_execucao = 0
profundidade_buscas = 0

def mcts(estado, iteracoes=100):
    raiz = MCTSNode(estado)
    global quantidade_de_buscas, quantidade_de_execucao, profundidade_buscas
    
    quantidade_de_execucao += 1
    for i in range(iteracoes):
        quantidade_de_buscas += 1
        no = raiz

        # 1. SELEÇÃO - navegar pela árvore usando UCB1
        while no.filhos and not no.estado.fim_de_jogo():
            no = no.selecionar_filho()
            profundidade_buscas += 1

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

def get_quantidade_de_buscas():
    return quantidade_de_buscas

def get_quantidade_de_execucao():
    return quantidade_de_execucao

def reset_quantidade_de_buscas():
    global quantidade_de_buscas
    quantidade_de_buscas = 0

def reset_quantidade_de_execucao():
    global quantidade_de_execucao
    quantidade_de_execucao = 0

def quantidade_media_buscas():
    if quantidade_de_execucao == 0:
        return 0
    return quantidade_de_buscas / quantidade_de_execucao

def get_profundidade_buscas():
    return profundidade_buscas

def reset_profundidade_buscas():
    global profundidade_buscas
    profundidade_buscas = 0

def get_profundidade_media():
    if quantidade_de_buscas == 0:
        return 0
    return profundidade_buscas / quantidade_de_buscas