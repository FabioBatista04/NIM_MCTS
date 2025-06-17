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
VERDE = (34, 139, 34)  # Verde mais suave para melhor visualização
VERMELHO = (255, 0, 0)

# Botão: (x, y, largura, altura)
BOTAO_VOCE = pygame.Rect(120, 80, 120, 50)
BOTAO_COMP = pygame.Rect(360, 80, 170, 50)

# Estados do jogo
ESTADO_INPUT = 0
ESTADO_SELECAO_JOGADOR = 1
ESTADO_JOGO = 2
ESTADO_FIM_JOGO = 3

# Variáveis globais do jogo
quem_joga = None
pilha_selecionada = -1
estado_atual = ESTADO_INPUT
estado_jogo = None
jogador_atual = 1
mensagem_status = ""
vencedor = None
ia_pensando = False
timer_ia = 0

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
    
    mouse_sobre_pilha = False
    elementos_destacados = 0
    
    for idx, valor in enumerate(pilhas):
        if valor == 0:
            continue
            
        # Desenha número da coluna abaixo da pilha
        coluna_txt = fonte_menor.render(f"P{idx}", True, PRETO)
        tela.blit(coluna_txt, (base_x + idx * largura - 8, base_y + 20))
        
        # Verifica se o mouse está sobre esta pilha
        pilha_x = base_x + idx * largura
        mouse_sobre_esta_pilha = abs(mouse_x - pilha_x) < 20
        
        if mouse_sobre_esta_pilha:
            mouse_sobre_pilha = True
        
        # Calcula quantos elementos estão sendo destacados baseado na posição Y do mouse
        elementos_destacados_nesta_pilha = 0
        if mouse_sobre_esta_pilha and mouse_y <= base_y + 15:  # Margem para clique
            # Calcula qual elemento está mais próximo do mouse (de cima para baixo)
            for h in range(valor - 1, -1, -1):  # Do topo para a base
                elemento_y = base_y - h * altura
                if mouse_y <= elemento_y + 15:  # +15 para dar uma margem maior de clique
                    elementos_destacados_nesta_pilha = valor - h
                    elementos_destacados = elementos_destacados_nesta_pilha
                    break
        
        # Desenha os elementos da pilha
        for h in range(valor):
            x = base_x + idx * largura
            y = base_y - h * altura            # Define cor baseada no estado
            cor_elemento = AZUL  # Cor padrão dos elementos (mudou de PRETO para AZUL)
            cor_borda = AZUL  # Borda azul para elementos azuis
            
            if mouse_sobre_esta_pilha and elementos_destacados_nesta_pilha > 0:
                # Destaca elementos de cima para baixo
                elementos_do_topo = valor - h
                if elementos_do_topo <= elementos_destacados_nesta_pilha:
                    cor_elemento = VERDE  # Elementos que serão removidos (mudou de AZUL para VERDE)
                    cor_borda = VERDE
                # Removido o else que mudava a cor dos elementos que ficarão
            
            # Desenha o círculo com borda para melhor visualização
            pygame.draw.circle(tela, cor_elemento, (x, y), 12)
            pygame.draw.circle(tela, cor_borda, (x, y), 12, 2)
            
        # Desenha a quantidade de elementos na pilha
        qtd_txt = fonte_menor.render(f"({valor})", True, PRETO)
        tela.blit(qtd_txt, (base_x + idx * largura - 12, base_y + 35))
    
    return mouse_sobre_pilha, elementos_destacados

def get_pilha_e_quantidade_mouse(pilhas, mouse_x, mouse_y, base_x=100, base_y=350, largura=40, altura=25):
    """Retorna a pilha e quantidade de elementos baseado na posição do mouse"""
    for idx, valor in enumerate(pilhas):
        if valor == 0:
            continue
            
        pilha_x = base_x + idx * largura
        mouse_sobre_pilha = abs(mouse_x - pilha_x) < 20
        
        if mouse_sobre_pilha and mouse_y <= base_y + 15:
            # Calcula quantos elementos serão removidos
            for h in range(valor - 1, -1, -1):  # Do topo para a base
                elemento_y = base_y - h * altura
                if mouse_y <= elemento_y + 15:
                    quantidade = valor - h
                    return idx, quantidade
    
    return -1, 0

def fazer_jogada_ia():
    global estado_jogo, jogador_atual, mensagem_status, ia_pensando, timer_ia
    
    if not ia_pensando:
        # Inicia o timer de "pensamento"
        ia_pensando = True
        timer_ia = 0
        mensagem_status = "IA está pensando..."
        print("IA está pensando...")
        return
    
    # IA já terminou de "pensar", faz a jogada
    print("IA fazendo jogada...")
    mensagem_status = "IA fazendo jogada..."
    
    # Usar MCTS para escolher a melhor jogada
    jogada = mcts(estado_jogo.clone(), iteracoes=100)
    pilha, quantidade = jogada
    
    print(f"IA escolheu: Pilha {pilha}, Quantidade {quantidade}")
    mensagem_status = f"IA removeu {quantidade} da pilha {pilha}"
    
    # Aplicar a jogada
    estado_jogo.aplicar_jogada(jogada)
    jogador_atual = estado_jogo.jogador_atual()
    
    # Resetar estado da IA
    ia_pensando = False
    timer_ia = 0

def verificar_fim_jogo():
    global estado_atual, vencedor, mensagem_status
    
    if estado_jogo.fim_de_jogo():
        vencedor = estado_jogo.vencedor()
        estado_atual = ESTADO_FIM_JOGO
        
        # No NIM misère, quem faz a última jogada perde
        if vencedor == 2:
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
    global estado_atual, estado_jogo, jogador_atual, mensagem_status, vencedor
    global ia_pensando, timer_ia
    
    pygame.init()
    tela = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('NIM MCTS')
    fonte = pygame.font.SysFont(None, 32)
    fonte_menor = pygame.font.SysFont(None, 24)
    rodando = True
    cursor_timer = 0
    cursor_visivel = True
    clock = pygame.time.Clock()
      # Reset das variáveis
    pilha_selecionada = -1
    estado_atual = ESTADO_INPUT
    mensagem_status = ""
    vencedor = None
    ia_pensando = False
    timer_ia = 0
    
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
            mouse_sobre_pilha, elementos_destacados = desenha_pilhas(tela, pilhas_atuais)
            
            # Desenha informações do jogo
            if jogador_atual == 1:
                if mouse_sobre_pilha and elementos_destacados > 0:
                    pilha_idx, _ = get_pilha_e_quantidade_mouse(pilhas_atuais, mouse[0], mouse[1])
                    instrucao_txt = fonte_menor.render(f"Remover {elementos_destacados} elemento(s) da pilha {pilha_idx} - Clique para confirmar", True, PRETO)
                else:
                    instrucao_txt = fonte_menor.render("Sua vez! Passe o mouse sobre uma pilha e clique para jogar", True, PRETO)
            else:
                instrucao_txt = fonte_menor.render("Vez da IA", True, PRETO)
            tela.blit(instrucao_txt, (50, 30))
            
            # Desenha mensagem de status
            if mensagem_status:
                status_txt = fonte_menor.render(mensagem_status, True, PRETO)
                tela.blit(status_txt, (50, 10))
        
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
          # Lógica do jogo
        if estado_atual == ESTADO_JOGO and estado_jogo:
            # Se é a vez da IA e o jogo não acabou
            if jogador_atual == 2 and not estado_jogo.fim_de_jogo():
                if ia_pensando:
                    # Incrementa o timer da IA
                    timer_ia += clock.get_time()
                    if timer_ia >= 4000:  # 4 segundos em milissegundos
                        fazer_jogada_ia()  # Agora faz a jogada de verdade
                        verificar_fim_jogo()
                else:
                    fazer_jogada_ia()  # Inicia o processo de "pensamento"
        
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
    global pilha_selecionada, estado_atual, jogador_atual, mensagem_status
    
    if evento.type == pygame.MOUSEBUTTONDOWN and jogador_atual == 1:
        # Obter a pilha e quantidade baseada na posição do mouse
        mouse_x, mouse_y = evento.pos
        pilha_idx, quantidade = get_pilha_e_quantidade_mouse(estado_jogo.pilhas, mouse_x, mouse_y)
        
        if pilha_idx != -1 and quantidade > 0:
            # Fazer a jogada
            jogada = (pilha_idx, quantidade)
            estado_jogo.aplicar_jogada(jogada)
            
            mensagem_status = f"Você removeu {quantidade} elemento(s) da pilha {pilha_idx}"
            print(f"Jogada aplicada: {jogada}")
            
            # Resetar seleção
            pilha_selecionada = -1
            jogador_atual = estado_jogo.jogador_atual()
            
            # Verificar fim de jogo
            verificar_fim_jogo()

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
    if quantidade > 80:
        quantidade = 80
    if quantidade < 21:
        return [1, 2, 3, 5, 7]
    else:
        acrescimo = 2
        current = 5
        pilhas = [1, 2, 3, 5]
                
        while quantidade > 0:
            import random
            elementos_pilha = random.randint(5, 10)  # Elementos randômicos entre 5 e 10
            pilhas.append(elementos_pilha)
            quantidade -= elementos_pilha
            
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