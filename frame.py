import pygame
import sys
import os
import numpy as np

# Verificar se Estado está importado corretamente
try:
    from Estado import Estado
except ImportError:
    print("Erro ao importar Estado. Certifique-se de que o arquivo Estado.py está no diretório.")

# Inicializar o Pygame
pygame.init()

# Definir dimensões da janela
LARGURA = 800
ALTURA = 600

# Criar a janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("NIM - Monte Carlo Tree Search")

# Definir cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 120, 255)
VERDE = (0, 200, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
CINZA = (200, 200, 200)

# Carregar fonte
pygame.font.init()
fonte_pequena = pygame.font.SysFont('Arial', 20)
fonte_media = pygame.font.SysFont('Arial', 30)
fonte_grande = pygame.font.SysFont('Arial', 40)

class JogoNIM:
    def __init__(self, pilhas=None):
        # Configuração padrão do jogo NIM (3 pilhas com 3, 4 e 5 palitos)
        self.pilhas = [3, 4, 5] if pilhas is None else pilhas
        self.jogador_atual = 0  # 0 = Humano, 1 = IA
        self.selecionado = None  # (índice da pilha, quantidade a remover)
        self.mensagem = "Sua vez! Selecione uma pilha e quantidade."
        self.game_over = False
        self.vencedor = None
    
    def desenhar(self, tela):
        # Limpar a tela
        tela.fill(BRANCO)
        
        # Título
        texto_titulo = fonte_grande.render("Jogo do NIM", True, PRETO)
        tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 20))
        
        # Informações do jogador atual
        jogador = "Jogador" if self.jogador_atual == 0 else "Computador (MCTS)"
        texto_jogador = fonte_media.render(f"Vez de: {jogador}", True, AZUL if self.jogador_atual == 0 else VERMELHO)
        tela.blit(texto_jogador, (LARGURA // 2 - texto_jogador.get_width() // 2, 80))
        
        # Mensagem
        texto_msg = fonte_pequena.render(self.mensagem, True, PRETO)
        tela.blit(texto_msg, (LARGURA // 2 - texto_msg.get_width() // 2, 120))
        
        # Desenhar pilhas
        espaco_entre_pilhas = LARGURA // (len(self.pilhas) + 1)
        raio_palito = 15
        
        for i, qtd_palitos in enumerate(self.pilhas):
            # Posição base da pilha
            pos_x = espaco_entre_pilhas * (i + 1)
            pos_y = ALTURA - 150
            
            # Nome da pilha
            texto_pilha = fonte_pequena.render(f"Pilha {i+1}: {qtd_palitos}", True, PRETO)
            tela.blit(texto_pilha, (pos_x - texto_pilha.get_width() // 2, pos_y - 40))
            
            # Desenhar palitos
            for j in range(qtd_palitos):
                y_offset = -j * (raio_palito * 2 + 5)  # Empilhar os palitos verticalmente
                cor = VERDE
                
                # Destacar palitos selecionados
                if self.selecionado and i == self.selecionado[0] and j >= qtd_palitos - self.selecionado[1]:
                    cor = AMARELO
                
                pygame.draw.circle(tela, cor, (pos_x, pos_y + y_offset), raio_palito)
        
        # Mensagem de fim de jogo
        if self.game_over:
            overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            tela.blit(overlay, (0, 0))
            
            vencedor_txt = "Você venceu!" if self.vencedor == 0 else "Computador venceu!"
            texto_vencedor = fonte_grande.render(vencedor_txt, True, BRANCO)
            tela.blit(texto_vencedor, (LARGURA // 2 - texto_vencedor.get_width() // 2, ALTURA // 2 - 50))
            
            texto_reiniciar = fonte_media.render("Pressione R para reiniciar", True, BRANCO)
            tela.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 50))
    
    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r and self.game_over:
                    self.__init__()
                    return True
            
            if self.game_over:
                continue
            
            if self.jogador_atual == 0:  # Turno do jogador humano
                self.turno_jogador(evento)
            else:
                # Lógica da IA será implementada depois
                pass
        
        return True
    
    def turno_jogador(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            espaco_entre_pilhas = LARGURA // (len(self.pilhas) + 1)
            
            # Verificar se clicou em alguma pilha
            for i in range(len(self.pilhas)):
                pos_x = espaco_entre_pilhas * (i + 1)
                
                # Área de clique para cada pilha (retângulo imaginário)
                rect_pilha = pygame.Rect(pos_x - 50, ALTURA - 350, 100, 250)
                
                if rect_pilha.collidepoint(x, y):
                    if self.pilhas[i] > 0:
                        # Primeiro clique seleciona a pilha
                        if self.selecionado is None or self.selecionado[0] != i:
                            self.selecionado = (i, 1)
                            self.mensagem = f"Pilha {i+1} selecionada. Clique novamente para remover 1 palito ou selecione outra pilha."
                        else:
                            # Cliques subsequentes aumentam a quantidade a remover
                            qtd = self.selecionado[1] + 1
                            if qtd <= self.pilhas[i]:
                                self.selecionado = (i, qtd)
                                self.mensagem = f"Remover {qtd} palito(s) da Pilha {i+1}. Pressione ENTER para confirmar."
                            else:
                                self.selecionado = (i, 1)
                                self.mensagem = f"Remover 1 palito da Pilha {i+1}. Pressione ENTER para confirmar."
        
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            if self.selecionado:
                pilha_idx = self.selecionado[0]
                remover = self.selecionado[1]
                
                if remover <= self.pilhas[pilha_idx]:
                    self.pilhas[pilha_idx] -= remover
                    self.jogador_atual = 1  # Passa para o turno da IA
                    self.selecionado = None
                    self.mensagem = "Computador está pensando..."
                    
                    # Verificar fim de jogo
                    self.verificar_fim_jogo()

    def verificar_fim_jogo(self):
        if sum(self.pilhas) == 0:
            self.game_over = True
            self.vencedor = 1 - self.jogador_atual  # Quem fez o último movimento perde

# Instanciar o jogo
jogo = JogoNIM()

# Clock para controlar FPS
clock = pygame.time.Clock()

# Loop principal do jogo
rodando = True
while rodando:
    # Processar eventos
    rodando = jogo.processar_eventos(pygame.event.get())
    
    # Renderizar jogo
    jogo.desenhar(tela)
    
    # Atualizar a tela
    pygame.display.flip()
    
    # Controlar FPS (60 frames por segundo)
    clock.tick(60)

# Encerrar o Pygame
pygame.quit()
sys.exit()