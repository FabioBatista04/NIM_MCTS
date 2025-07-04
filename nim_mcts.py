
import random
from mcts import mcts
from Estado import Estado
import frame 

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

def jogar_simulacao(num_partidas=100, iteracoes_mcts=50):
    vitorias_j2 = 0                     # contador correto

    for _ in range(num_partidas):
        estado = Estado([1, 3, 5], jogador=random.choice([1, 2]))

        while not estado.fim_de_jogo():
            if estado.jogador_atual() == 2:               
                
                jogada = mcts(estado.clone(), iteracoes=iteracoes_mcts)
            else:                                         
                jogada = estado.jogada_aleatoria()

            estado.aplicar_jogada(jogada)                 

        print(f"Partida finalizada: {estado.pilhas} - Vencedor: Jogador {estado.vencedor()}")
        # ③ regra misère: vencedor() já retorna self.jogador
        if estado.vencedor() == 2:
            vitorias_j2 += 1

    taxa = vitorias_j2 / num_partidas
    print(f"Taxa de vitória do Jogador 2: {vitorias_j2}/{num_partidas}  ({taxa:.2%})")

def jogar_terminal(pilhas, quem_joga):
    """Versão original do jogo no terminal"""
    while sum(pilhas) > 0:
        if quem_joga == "2":
            print("O computador está jogando...")
            estado = Estado(pilhas, 2)
            jogada = mcts(estado, iteracoes=100)
            
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
    """Executa o jogo com interface gráfica"""
    print("Iniciando NIM MCTS com interface gráfica...")
    frame.abrir_tela()  # Toda a lógica do jogo agora está na interface gráfica

def main_simulacao():
    """Executa simulações para testar a IA"""
    print("Executando simulações...")
    jogar_simulacao(num_partidas=100, iteracoes_mcts=100)

def main_terminal():
    """Executa o jogo no terminal (versão original)"""
    print("=== MODO TERMINAL ===")
    quantidade = int(input("Digite a quantidade total de elementos: "))
    quem_joga = input("Quem começa? (1=Você, 2=Computador): ")
    
    monta_pilhas(quantidade)
    show_pilhas(pilhas)
    jogar_terminal(pilhas, quem_joga)

if __name__ == "__main__":
    # Opções de execução
    modo = input("Escolha o modo:\n1 - Interface Gráfica\n2 - Terminal\n3 - Simulação\nOpção: ")
    
    if modo == "1":
        main()
    elif modo == "2":
        main_terminal()
    elif modo == "3":
        main_simulacao()
    else:
        print("Modo inválido. Executando interface gráfica...")
        main()