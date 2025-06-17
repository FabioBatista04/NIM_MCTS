import pygame
from Estado import Estado
from mcts import mcts

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
AZUL = (100, 149, 237)
CINZA_ESCURO = (150, 150, 150)
BORDACOR = (50, 50, 50)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Botão: (x, y, largura, altura)
BOTAO_VOCE = pygame.Rect(120, 80, 120, 50)
BOTAO_COMP = pygame.Rect(360, 80, 170, 50)

# Estados do jogo
ESTADO_INPUT = 0
ESTADO_SELECAO_JOGADOR = 1
ESTADO_JOGO = 2
ESTADO_SELECAO_QUANTIDADE = 3
ESTADO_FIM_JOGO = 4

# Variáveis globais do jogo
quem_joga = None
pilha_selecionada = -1
quantidade_selecionada = 0
estado_atual = ESTADO_INPUT
estado_jogo = None
jogador_atual = 1
mensagem_status = ""
vencedor = None

def desenha_botao(tela, fonte, rect, texto, selecionado, hover):
    cor = AZUL if selecionado else (CINZA_ESCURO if hover else CINZA)
    pygame.draw.rect(tela, cor, rect, border_radius=8)
    pygame.draw.rect(tela, BORDACOR, rect, 2, border_radius=8)
    txt = fonte.render(texto, True, PRETO)
    tela.blit(txt, (rect.x + (rect.width-txt.get_width())//2, rect.y + (rect.height-txt.get_height())//2))

def desenha_input(tela, fonte, rect, texto, ativo, valor, buffer, cursor_visivel):
    cor = AZUL if ativo else CINZA
    pygame.draw.rect(tela, cor, rect, border_radius=8)
    pygame.draw.rect(tela, BORDACOR, rect, 2, border_radius=8)
    txt = fonte.render(texto, True, PRETO)
    tela.blit(txt, (rect.x + 10, rect.y + 5))
    if ativo:
        mostrar = buffer
        if cursor_visivel:
            mostrar += "|"
    else:
        mostrar = str(valor)
    valor_txt = fonte.render(mostrar, True, PRETO)
    tela.blit(valor_txt, (rect.x + rect.width - valor_txt.get_width() - 10, rect.y + 5))

def desenha_pilhas(tela, pilhas, base_x=100, base_y=350, largura=40, altura=25):
    global pilha_selecionada
    max_altura = max(pilhas) if pilhas else 0
    fonte_menor = pygame.font.SysFont(None, 18)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for idx, valor in enumerate(pilhas):
        if valor == 0:
            continue
            
        # Desenha número da coluna abaixo da pilha
        coluna_txt = fonte_menor.render(f"{idx}", True, PRETO)
        tela.blit(coluna_txt, (base_x + idx * largura - 5, base_y + 15))
        
        # Verifica se o mouse está sobre esta pilha
        pilha_x = base_x + idx * largura
        mouse_sobre_pilha = abs(mouse_x - pilha_x) < 20
        
        # Define cor com base na seleção e posição do mouse
        cor_atual = PRETO
        if idx == pilha_selecionada:
            cor_atual = VERMELHO  # Vermelho para pilha selecionada
        elif mouse_sobre_pilha:
            cor_atual = AZUL  # Azul quando mouse está sobre a pilha
        
        # Desenha os elementos da pilha
        for h in range(valor):
            x = base_x + idx * largura
            y = base_y - h * altura
            pygame.draw.circle(tela, cor_atual, (x, y), 10)

def desenha_botoes_quantidade(tela, fonte, pilha_selecionada, pilhas):
    if pilha_selecionada == -1 or pilha_selecionada >= len(pilhas):
        return []
    
    max_quantidade = pilhas[pilha_selecionada]
    botoes = []
    
    # Desenha botões para cada quantidade possível
    for i in range(1, min(max_quantidade + 1, 6)):  # Máximo 5 botões
        x = 50 + (i - 1) * 100
        y = 50
        rect = pygame.Rect(x, y, 80, 40)
        botoes.append((rect, i))
        
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        
        cor = CINZA_ESCURO if hover else CINZA
        pygame.draw.rect(tela, cor, rect, border_radius=5)
        pygame.draw.rect(tela, BORDACOR, rect, 2, border_radius=5)
        
        txt = fonte.render(str(i), True, PRETO)
        tela.blit(txt, (rect.x + (rect.width-txt.get_width())//2, rect.y + (rect.height-txt.get_height())//2))
    
    return botoes

def fazer_jogada_ia():
    global estado_jogo, jogador_atual, mensagem_status
    
    print("IA está pensando...")
    mensagem_status = "IA está pensando..."
    
    # Usar MCTS para escolher a melhor jogada
    jogada = mcts(estado_jogo.clone(), iteracoes=100)
    pilha, quantidade = jogada
    
    print(f"IA escolheu: Pilha {pilha}, Quantidade {quantidade}")
    mensagem_status = f"IA removeu {quantidade} da pilha {pilha}"
    
    # Aplicar a jogada
    estado_jogo.aplicar_jogada(jogada)
    jogador_atual = estado_jogo.jogador_atual()

def verificar_fim_jogo():
    global estado_atual, vencedor, mensagem_status
    
    if estado_jogo.fim_de_jogo():
        vencedor = estado_jogo.vencedor()
        estado_atual = ESTADO_FIM_JOGO
        
        # No NIM misère, quem faz a última jogada perde
        if vencedor == 1:
            mensagem_status = "Você perdeu! Fez a última jogada."
        else:
            mensagem_status = "Você ganhou! A IA fez a última jogada."
        
        return True
    return False

INPUT_RECT = pygame.Rect(180, 160, 280, 50)

num_elementos = 11
input_ativo = False
input_buffer = ''

def abrir_tela():
    global quem_joga, num_elementos, input_ativo, input_buffer, pilha_selecionada
    global estado_atual, estado_jogo, jogador_atual, mensagem_status, quantidade_selecionada, vencedor
    
    pygame.init()
    tela = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('NIM MCTS')
    fonte = pygame.font.SysFont(None, 32)
    fonte_menor = pygame.font.SysFont(None, 24)
    rodando = True
    cursor_timer = 0
    cursor_visivel = True
    clock = pygame.time.Clock()
    botoes_quantidade = []
    
    # Reset das variáveis
    pilha_selecionada = -1
    estado_atual = ESTADO_INPUT
    mensagem_status = ""
    vencedor = None
    
    while rodando:
        tela.fill(BRANCO)
        mouse = pygame.mouse.get_pos()
        
        # Desenha interface baseada no estado atual
        if estado_atual == ESTADO_INPUT:
            desenha_etapa_input(tela, fonte, fonte_menor, input_ativo, num_elementos, input_buffer, cursor_visivel)
        
        elif estado_atual == ESTADO_SELECAO_JOGADOR:
            desenha_etapa_quem_comeca(tela, fonte, mouse, quem_joga)
        
        elif estado_atual == ESTADO_JOGO:
            # Desenha as pilhas
            pilhas_atuais = estado_jogo.pilhas
            desenha_pilhas(tela, pilhas_atuais)
            
            # Desenha informações do jogo
            if jogador_atual == 1:
                instrucao_txt = fonte_menor.render("Sua vez! Clique em uma pilha", True, PRETO)
            else:
                instrucao_txt = fonte_menor.render("Vez da IA", True, PRETO)
            tela.blit(instrucao_txt, (180, 30))
            
            # Desenha mensagem de status
            if mensagem_status:
                status_txt = fonte_menor.render(mensagem_status, True, PRETO)
                tela.blit(status_txt, (50, 10))
        
        elif estado_atual == ESTADO_SELECAO_QUANTIDADE:
            # Desenha as pilhas
            pilhas_atuais = estado_jogo.pilhas
            desenha_pilhas(tela, pilhas_atuais)
            
            # Desenha botões de quantidade
            instrucao_txt = fonte_menor.render(f"Quantos elementos remover da pilha {pilha_selecionada}?", True, PRETO)
            tela.blit(instrucao_txt, (50, 30))
            
            botoes_quantidade = desenha_botoes_quantidade(tela, fonte_menor, pilha_selecionada, pilhas_atuais)
        
        elif estado_atual == ESTADO_FIM_JOGO:
            # Desenha as pilhas vazias
            pilhas_atuais = estado_jogo.pilhas
            desenha_pilhas(tela, pilhas_atuais)
            
            # Desenha mensagem de fim de jogo
            fim_txt = fonte.render("FIM DE JOGO!", True, VERMELHO)
            tela.blit(fim_txt, (200, 50))
            
            resultado_txt = fonte_menor.render(mensagem_status, True, PRETO)
            tela.blit(resultado_txt, (150, 100))
            
            reiniciar_txt = fonte_menor.render("Feche a janela para sair", True, PRETO)
            tela.blit(reiniciar_txt, (180, 130))
        
        pygame.display.flip()
        
        # Processa eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            elif estado_atual == ESTADO_INPUT:
                processar_eventos_input(evento)
            
            elif estado_atual == ESTADO_SELECAO_JOGADOR:
                processar_eventos_selecao_jogador(evento)
            
            elif estado_atual == ESTADO_JOGO:
                processar_eventos_jogo(evento)
            
            elif estado_atual == ESTADO_SELECAO_QUANTIDADE:
                processar_eventos_selecao_quantidade(evento, botoes_quantidade)
        
        # Lógica do jogo
        if estado_atual == ESTADO_JOGO and estado_jogo:
            # Se é a vez da IA e o jogo não acabou
            if jogador_atual == 2 and not estado_jogo.fim_de_jogo():
                fazer_jogada_ia()
                verificar_fim_jogo()
        
        # Cursor piscando
        if input_ativo:
            cursor_timer += clock.get_time()
            if cursor_timer > 500:
                cursor_visivel = not cursor_visivel
                cursor_timer = 0
        else:
            cursor_visivel = False
        
        clock.tick(60)
    
    pygame.quit()

def processar_eventos_input(evento):
    global input_ativo, input_buffer, num_elementos, estado_atual
    
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if INPUT_RECT.collidepoint(evento.pos):
            input_ativo = True
        else:
            input_ativo = False
    
    if input_ativo and evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_RETURN:
            try:
                if input_buffer:
                    num_elementos = int(input_buffer)
                    estado_atual = ESTADO_SELECAO_JOGADOR
            except:
                num_elementos = 11
            input_buffer = ''
            input_ativo = False
        elif evento.key == pygame.K_BACKSPACE:
            input_buffer = input_buffer[:-1]
        elif evento.unicode.isdigit() and len(input_buffer) < 4:
            input_buffer += evento.unicode

def processar_eventos_selecao_jogador(evento):
    global quem_joga, estado_atual, estado_jogo, jogador_atual
    
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if BOTAO_VOCE.collidepoint(evento.pos):
            quem_joga = 1
            jogador_atual = 1
            inicializar_jogo()
        elif BOTAO_COMP.collidepoint(evento.pos):
            quem_joga = 2
            jogador_atual = 2
            inicializar_jogo()

def processar_eventos_jogo(evento):
    global pilha_selecionada, estado_atual
    
    if evento.type == pygame.MOUSEBUTTONDOWN and jogador_atual == 1:
        # Verificar clique nas pilhas
        base_x = 100
        largura = 40
        mouse_x, mouse_y = evento.pos
        
        # Calcular qual pilha foi clicada
        pilhas_atuais = estado_jogo.pilhas
        for i, quantidade in enumerate(pilhas_atuais):
            if quantidade == 0:  # Pular pilhas vazias
                continue
                
            pilha_x = base_x + i * largura
            if abs(mouse_x - pilha_x) < 20:
                pilha_selecionada = i
                estado_atual = ESTADO_SELECAO_QUANTIDADE
                print(f"Pilha {i} selecionada com {quantidade} elementos")
                break

def processar_eventos_selecao_quantidade(evento, botoes_quantidade):
    global pilha_selecionada, estado_atual, jogador_atual, mensagem_status
    
    if evento.type == pygame.MOUSEBUTTONDOWN:
        # Verificar clique nos botões de quantidade
        for rect, quantidade in botoes_quantidade:
            if rect.collidepoint(evento.pos):
                # Fazer a jogada
                jogada = (pilha_selecionada, quantidade)
                estado_jogo.aplicar_jogada(jogada)
                
                mensagem_status = f"Você removeu {quantidade} da pilha {pilha_selecionada}"
                print(f"Jogada aplicada: {jogada}")
                
                # Resetar seleção
                pilha_selecionada = -1
                jogador_atual = estado_jogo.jogador_atual()
                estado_atual = ESTADO_JOGO
                
                # Verificar fim de jogo
                verificar_fim_jogo()
                break

def inicializar_jogo():
    global estado_jogo, estado_atual
    
    # Criar as pilhas baseadas na quantidade de elementos
    pilhas_iniciais = montar_pilhas_grafico(num_elementos)
    
    # Criar o estado do jogo
    estado_jogo = Estado(pilhas_iniciais, jogador=quem_joga)
    
    # Mudar para o estado de jogo
    estado_atual = ESTADO_JOGO
    
    print(f"Jogo iniciado com pilhas: {pilhas_iniciais}")
    print(f"Primeiro jogador: {quem_joga}")

def montar_pilhas_grafico(quantidade):
    if quantidade < 21:
        return [1, 2, 3, 5, 7]
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
        return pilhas

def get_quem_joga():
    return quem_joga

def get_num_elementos():
    return num_elementos

def desenha_etapa_input(tela, fonte, fonte_menor, input_ativo, num_elementos, input_buffer, cursor_visivel):
    # Texto acima do input
    instrucao = fonte.render('Informe a quantidade de palitos', True, PRETO)
    tela.blit(instrucao, (INPUT_RECT.x + 10, INPUT_RECT.y - 40))
    desenha_input(tela, fonte, INPUT_RECT, 'Total de elementos:', input_ativo, num_elementos, input_buffer, cursor_visivel)
    # Texto abaixo do input
    instrucao2 = fonte_menor.render('Confirme pressionando ENTER', True, PRETO)
    tela.blit(instrucao2, (INPUT_RECT.x + 10, INPUT_RECT.y + INPUT_RECT.height + 10))

def desenha_etapa_quem_comeca(tela, fonte, mouse, quem_joga):
    hover_voce = BOTAO_VOCE.collidepoint(mouse)
    hover_comp = BOTAO_COMP.collidepoint(mouse)
    texto = fonte.render('Quem começa o jogo:', True, PRETO)
    tela.blit(texto, (180, 30))
    desenha_botao(tela, fonte, BOTAO_VOCE, 'Você', quem_joga==1, hover_voce)
    desenha_botao(tela, fonte, BOTAO_COMP, 'Computador', quem_joga==2, hover_comp)