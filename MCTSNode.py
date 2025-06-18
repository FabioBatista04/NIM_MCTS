import random
import math

class MCTSNode:
    profundidade_maxima = 0
    profundidade_total_iterada = 0
    nos_criados = 0
    def __init__(self, estado, pai=None, jogada=None):
        self.estado = estado
        self.pai = pai
        self.jogada = jogada
        self.filhos = []
        self.visitas = 0
        self.vitorias = 0
        self.profundidade = 0 if pai is None else pai.profundidade + 1

        MCTSNode.profundidade_maxima = max(MCTSNode.profundidade_maxima, self.profundidade)
        MCTSNode.nos_criados += 1
        MCTSNode.profundidade_total_iterada += self.profundidade

    def expandir(self):
        jogadas_possiveis = self.estado.jogadas_possiveis()
        for jogada in jogadas_possiveis:
            novo_estado = self.estado.clone()
            novo_estado.aplicar_jogada(jogada)
            filho = MCTSNode(novo_estado, pai=self, jogada=jogada)
            self.filhos.append(filho)

    def selecionar_filho(self):
        # 1. Prioriza filhos nunca visitados
        nao_visitados = [f for f in self.filhos if f.visitas == 0]
        if nao_visitados:
            return random.choice(nao_visitados)

        # 2. UCB1 do ponto de vista **do pai**  (misère ou normal, tanto faz)
        C         = math.sqrt(2)
        log_total = math.log(self.visitas + 1)

        melhor_ucb   = -float("inf")
        melhor_filho = None

        for filho in self.filhos:
            win_oponente = filho.vitorias / filho.visitas          # vitórias do adversário
            exploit      = 1 - win_oponente                        # vitórias do pai
            explore      = C * math.sqrt(log_total / filho.visitas)
            ucb          = exploit + explore

            if ucb > melhor_ucb:
                melhor_ucb, melhor_filho = ucb, filho

        return melhor_filho

    def simular(self):
        simulado = self.estado.clone()
        jogador_atual = simulado.jogador_atual()
        
        while not simulado.fim_de_jogo():            
            # Jogada aleatória
            jogadas = simulado.jogadas_possiveis()
            if not jogadas:
                break
            jogada = random.choice(jogadas)
            simulado.aplicar_jogada(jogada)
        
        vencedor = simulado.vencedor()
        
        # Retorna 1 se o jogador atual do nó venceu, 0 caso contrário
        return 1 if vencedor == jogador_atual else 0

    def backpropagar(self, resultado):
        self.visitas += 1
        self.vitorias += resultado
        
        if self.pai:
            # O resultado para o pai é o oposto do resultado para o filho
            # Se o filho venceu (resultado=1), o pai perdeu (1-resultado=0)
            self.pai.backpropagar(1 - resultado)

    @classmethod
    def resetar_profundidade_maxima(cls):
        cls.profundidade_maxima = 0

    @classmethod
    def get_profundidade_maxima(cls):
        return cls.profundidade_maxima
    
    @classmethod
    def get_profundidade_media(cls):
        if cls.nos_criados == 0:
            return 0
        return cls.profundidade_total_iterada / cls.nos_criados
    
    @classmethod
    def get_nos_criados(cls):
        return cls.nos_criados
        
    @classmethod
    def resetar_nos_criados(cls):
        cls.nos_criados = 0

    @classmethod
    def resetar_profundidade_total_iterada(cls):
        cls.profundidade_total_iterada = 0
