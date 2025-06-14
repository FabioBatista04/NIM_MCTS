"""
1. Seleção       
2. Expansão
3. Simulação
4. Backpropagação
"""

import random
from mcts import mcts
from Estado import Estado

pilhas = []

def show_pilhas(pilhas):
    altura_max = max(pilhas) if pilhas else 0
    for linha in range(altura_max, 0, -1):
        linha_str = ""
        for pilha in pilhas:
            if pilha >= linha:
                linha_str += " * "
            else:
                linha_str += "   "
        print(linha_str)
    print("".join(f"{i:^3}" for i in range(len(pilhas))))  # índices
    print("".join(f"{v:^3}" for v in pilhas))              # valores

def jogar_simulacao(num_partidas=100, iteracoes_mcts=2000):
    vitorias_j2 = 0                     # contador correto

    for _ in range(num_partidas):
        # ① cria um estado NOVO para cada partida
        estado = Estado([1, 3, 5], jogador=random.choice([1, 2]))

        while not estado.fim_de_jogo():
            if estado.jogador_atual() == 2:               # IA (MCTS)
                # ② passe um CLONE ao MCTS — evita efeitos colaterais
                jogada = mcts(estado.clone(), iteracoes=iteracoes_mcts)
            else:                                         # adversário aleatório
                jogada = estado.jogada_aleatoria()

            estado.aplicar_jogada(jogada)                 # altera o estado real

        print(f"Partida finalizada: {estado.pilhas} - Vencedor: Jogador {estado.vencedor()}")
        # ③ regra misère: vencedor() já retorna self.jogador
        if estado.vencedor() == 2:
            vitorias_j2 += 1

    taxa = vitorias_j2 / num_partidas
    print(f"Taxa de vitória do Jogador 2: {vitorias_j2}/{num_partidas}  ({taxa:.2%})")

def jogar(pilhas, quem_joga):
    while sum(pilhas) > 0:
        if quem_joga == "2":

            print("O computador está jogando...")
            estado = Estado(pilhas, 2)
            jogada = mcts(estado, iteracoes=500000)
            
            pilhas[jogada[0]] -= jogada[1]

            show_pilhas(pilhas)
            if sum(pilhas) == 0:
                print("O computador Perdeu!")
                return
            quem_joga = "1"
        else:            
            print(f"Escolha uma pilha (0 a {len(pilhas)-1}):")
            try:
                escolha = int(input())
                if escolha < 0 or escolha >= len(pilhas):
                    print("Escolha inválida. Tente novamente.")
                    continue
                if pilhas[escolha] == 0:
                    print("Pilha vazia. Tente novamente.")
                    continue
                print(f"Quantas peças você quer remover da pilha {escolha}?")
                quantidade = int(input())
                if quantidade <= 0 or quantidade > pilhas[escolha]:
                    print("Quantidade inválida. Tente novamente.")
                    continue
                pilhas[escolha] -= quantidade
                show_pilhas(pilhas)
                if sum(pilhas) == 0:
                    print("Você Perdeu!")
                    return
                quem_joga = "2"
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

def monta_pilhas(quantidade):
    global pilhas
    if quantidade < 21:
        pilhas = [1, 2, 3, 5, 7]
    else:
        acrescimo = 2
        current = 5
        pilhas = [1, 2, 3, 5]
        quantidade -= 11
        while quantidade > 0:
            if quantidade > current + acrescimo:
                pilhas.append(current + acrescimo)
                quantidade -= current + acrescimo
                current += acrescimo
            else:
                pilhas[-1] += quantidade
                quantidade = 0

def main():
    #selecionar_quantidade_elementos = input("Quantas pilhas você quer jogar? (acima de 21): ")

    #quem_joga = input("Quem começa jogando? (1 - você, 2 - computador): ")
    #try:
        #quantidade = int(selecionar_quantidade_elementos)
    #except ValueError:
        #quantidade = 21
    #monta_pilhas(quantidade)
    
    #show_pilhas(pilhas)
    
    #jogar(pilhas, quem_joga)
    jogar_simulacao()
    
if __name__ == "__main__":
    main()