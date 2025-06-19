import pygame
import time
import random
from Estado import Estado
from mcts import mcts, get_quantidade_de_buscas, quantidade_media_buscas, get_profundidade_media, reset_quantidade_de_buscas, reset_quantidade_de_execucao, reset_profundidade_buscas
from MCTSNode import MCTSNode

# Cores e fontes
BRANCO, PRETO, CINZA, AZUL, VERDE, VERMELHO = (255,255,255), (0,0,0), (200,200,200), (100,149,237), (34,139,34), (255,0,0)

class JogoNim:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((600, 400))
        pygame.display.set_caption('NIM MCTS')
        self.fonte = pygame.font.SysFont(None, 32)
        self.fonte_pequena = pygame.font.SysFont(None, 24)
        self.clock = pygame.time.Clock()
        self.reiniciar_jogo()

    def reiniciar_jogo(self):
        self.num_elementos = 11
        self.estado_jogo = None
        self.jogador_atual = 1
        self.mensagem = ""
        self.estado = "input"
        self.input_ativo = False
        self.input_buffer = ""

    def desenhar_texto(self, texto, pos, cor=PRETO, fonte=None, centro=False):
        if fonte is None: fonte = self.fonte_pequena
        surface = fonte.render(texto, True, cor)
        rect = surface.get_rect(center=pos) if centro else surface.get_rect(topleft=pos)
        self.tela.blit(surface, rect)

    def desenhar_botao(self, rect, texto):
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        cor = AZUL if hover else CINZA
        pygame.draw.rect(self.tela, cor, rect, border_radius=8)
        pygame.draw.rect(self.tela, PRETO, rect, 2, border_radius=8)
        self.desenhar_texto(texto, rect.center, fonte=self.fonte, centro=True)
        return hover

    def desenhar_pilhas(self):
        if not self.estado_jogo: return None, 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pilha_clicada, quantidade_selecionada = None, 0
        
        for i, tamanho in enumerate(self.estado_jogo.pilhas):
            if tamanho == 0: continue
            x_pilha = 70 + i * 80
            mouse_sobre_pilha = abs(mouse_x - x_pilha) < 30
            
            elementos_destacados = 0
            if mouse_sobre_pilha:
                # Itera de baixo para cima (na tela) para encontrar o item sob o mouse
                for j in range(tamanho - 1, -1, -1):
                    y = 300 - j * 25
                    if mouse_y <= y + 12: # 12 é o raio
                        elementos_destacados = tamanho - j
                        break
            
            if mouse_sobre_pilha and elementos_destacados > 0:
                pilha_clicada = i
                quantidade_selecionada = elementos_destacados

            for j in range(tamanho):
                y = 300 - j * 25
                # Destaca se o elemento está na faixa a ser removida
                destacar = (mouse_sobre_pilha and (tamanho - j) <= elementos_destacados)
                cor = VERDE if destacar else AZUL
                pygame.draw.circle(self.tela, cor, (x_pilha, y), 12) # Raio 12
                pygame.draw.circle(self.tela, PRETO, (x_pilha, y), 12, 2)
            
            self.desenhar_texto(f"P{i} ({tamanho})", (x_pilha - 20, 325))
        return pilha_clicada, quantidade_selecionada

    def criar_pilhas(self, total):
        if total < 6: return [1, 2, 3]
        pilhas, restante = [], total
        while restante > 0:
            tamanho = restante if restante < 10 else random.randint(5, 10)
            pilhas.append(tamanho)
            restante -= tamanho
        return pilhas

    def fazer_jogada(self, pilha, quantidade, eh_humano=True):
        if eh_humano and (pilha is None or quantidade <= 0): return False
        
        jogada = (pilha, quantidade) if eh_humano else mcts(self.estado_jogo.clone(), iteracoes=100)
        if not eh_humano: time.sleep(0.5)

        self.estado_jogo.aplicar_jogada(jogada)
        self.mensagem = f"{'Você' if eh_humano else 'IA'} removeu {jogada[1]} da pilha {jogada[0]}"
        self.jogador_atual = self.estado_jogo.jogador_atual()
        self.verificar_fim()
        return True

    def verificar_fim(self):
        if self.estado_jogo and self.estado_jogo.fim_de_jogo():
            vencedor = self.estado_jogo.vencedor()
            self.mensagem = "Você perdeu!" if vencedor == 2 else "Você ganhou!"
            self.estado = "fim"
            
            # Exibe e reseta as estatísticas no console
            print("--- Fim de Jogo: Estatísticas MCTS ---")
            print(f"Profundidade máxima: {MCTSNode.get_profundidade_maxima()}")
            print(f"Profundidade média da árvore: {MCTSNode.get_profundidade_media()}")
            print(f"Quantidade de buscas: {get_quantidade_de_buscas()}")
            print(f"Média de buscas: {quantidade_media_buscas()}")
            print(f"Profundidade média das buscas: {get_profundidade_media()}")
            print("------------------------------------")
            
            MCTSNode.resetar_profundidade_maxima()
            MCTSNode.resetar_profundidade_total_iterada()
            MCTSNode.resetar_nos_criados()
            reset_quantidade_de_buscas()
            reset_quantidade_de_execucao()
            reset_profundidade_buscas()

    def processar_eventos(self, evento):
        if evento.type == pygame.QUIT: return False
        
        if self.estado == "input":
            rect = pygame.Rect(200, 150, 200, 40)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                self.input_ativo = rect.collidepoint(evento.pos)
            elif evento.type == pygame.KEYDOWN and self.input_ativo:
                if evento.key == pygame.K_RETURN:
                    if self.input_buffer: self.num_elementos = int(self.input_buffer)
                    self.estado = "selecao"
                elif evento.key == pygame.K_BACKSPACE: self.input_buffer = self.input_buffer[:-1]
                elif evento.unicode.isdigit(): self.input_buffer += evento.unicode

        elif self.estado == "selecao" and evento.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(150, 180, 120, 50).collidepoint(evento.pos):
                self.jogador_atual = 1
                self.estado_jogo = Estado(self.criar_pilhas(self.num_elementos), self.jogador_atual)
                self.estado = "jogando"
            elif pygame.Rect(330, 180, 120, 50).collidepoint(evento.pos):
                self.jogador_atual = 2
                self.estado_jogo = Estado(self.criar_pilhas(self.num_elementos), self.jogador_atual)
                self.estado = "jogando"

        elif self.estado == "jogando" and self.jogador_atual == 1 and evento.type == pygame.MOUSEBUTTONDOWN:
            pilha, quantidade = self.desenhar_pilhas()
            self.fazer_jogada(pilha, quantidade)
        
        elif self.estado == "fim" and evento.type == pygame.MOUSEBUTTONDOWN:
            self.reiniciar_jogo()

        return True

    def executar(self):
        rodando = True
        while rodando:
            self.tela.fill(BRANCO)
            
            if self.estado == "input":a
                self.desenhar_texto("Quantidade de palitos:", (300, 120), fonte=self.fonte, centro=True)
                rect = pygame.Rect(200, 150, 200, 40)
                pygame.draw.rect(self.tela, AZUL if self.input_ativo else CINZA, rect, border_radius=8)
                self.desenhar_texto(self.input_buffer, (210, 158))
            elif self.estado == "selecao":
                self.desenhar_texto("Quem começa?", (300, 120), fonte=self.fonte, centro=True)
                self.desenhar_botao(pygame.Rect(150, 180, 120, 50), "Você")
                self.desenhar_botao(pygame.Rect(330, 180, 120, 50), "IA")
            elif self.estado == "jogando":
                pilha, qtd = self.desenhar_pilhas()
                info = self.mensagem
                if self.jogador_atual == 1:
                    if pilha is not None and qtd > 0:
                        info = f"Remover {qtd} da pilha {pilha}"
                    else:
                        info = "Sua vez: passe o mouse sobre uma pilha"
                self.desenhar_texto(info, (20, 20))

                if self.jogador_atual == 2:
                    self.fazer_jogada(None, None, False)
            elif self.estado == "fim":
                self.desenhar_texto("FIM DE JOGO", (300, 150), fonte=self.fonte, centro=True)
                self.desenhar_texto(self.mensagem, (300, 200), centro=True)
                self.desenhar_texto("Clique para reiniciar", (300, 250), centro=True)

            for evento in pygame.event.get():
                rodando = self.processar_eventos(evento)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

def abrir_tela():
    JogoNim().executar()