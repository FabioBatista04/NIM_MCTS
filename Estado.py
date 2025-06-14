import logging
import random
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Estado:
    def __init__(self, pilhas, jogador):
        self.pilhas = pilhas[:]
        self.jogador = jogador

    def jogador_atual(self):
        return self.jogador
    
    def clone(self):
        return Estado(self.pilhas[:], self.jogador)
    
    def jogadas_possiveis(self):
        jogadas = []
        for i, pilha in enumerate(self.pilhas):
            if pilha > 0:
                for j in range(1, pilha + 1):
                    jogadas.append((i, j))
        return jogadas
    
    def aplicar_jogada(self, jogada=None):
        pilha, remover = jogada
        self.pilhas[pilha] -= remover
        self.jogador = 2 if self.jogador == 1 else 1
        return jogada
    
    def jogada_aleatoria(self):
        jogadas = self.jogadas_possiveis()
        if jogadas:
            return random.choice(jogadas)
        
    def jogada_otima(self):        
        for i, pilha in enumerate(self.pilhas):
            for remover in range(1, pilha + 1):
                novo_estado = self.pilhas[:]
                novo_estado[i] -= remover
                nim_sum = 0
                for p in novo_estado:
                    nim_sum ^= p
                if nim_sum == 0:                   
                    return (i, remover)
        return None
    
    

    def fim_de_jogo(self):
        return sum(self.pilhas) == 0
    
    def vencedor(self):
        if self.fim_de_jogo():
            return self.jogador