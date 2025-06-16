import pygame

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
AZUL = (100, 149, 237)
CINZA_ESCURO = (150, 150, 150)
BORDACOR = (50, 50, 50)

# Botão: (x, y, largura, altura)
BOTAO_VOCE = pygame.Rect(120, 80, 120, 50)
BOTAO_COMP = pygame.Rect(360, 80, 170, 50)  # mais largo

quem_joga = None

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

def desenha_pilhas(tela, pilhas, base_x=100, base_y=350, largura=40, altura=25, cor=PRETO):
    # pilhas: lista de inteiros, cada valor é a altura da pilha
    max_altura = max(pilhas) if pilhas else 0
    for idx, valor in enumerate(pilhas):
        for h in range(valor):
            x = base_x + idx * largura
            y = base_y - h * altura
            pygame.draw.circle(tela, cor, (x, y), 10)

INPUT_RECT = pygame.Rect(180, 160, 280, 50)

num_elementos = 11
input_ativo = False
input_buffer = ''

def abrir_tela():
    global quem_joga, num_elementos, input_ativo, input_buffer
    pygame.init()
    tela = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('NIM MCTS')
    fonte = pygame.font.SysFont(None, 32)
    fonte_menor = pygame.font.SysFont(None, 24)
    rodando = True
    mostrar_botoes = False  # só mostra botões após confirmação
    mostrar_pilhas = False  # só mostra pilhas após seleção
    cursor_timer = 0
    cursor_visivel = True
    clock = pygame.time.Clock()
    pilhas_grafico = []
    while rodando:
        tela.fill(BRANCO)
        mouse = pygame.mouse.get_pos()
        if not mostrar_botoes:
            # Texto acima do input
            instrucao = fonte.render('Informe a quantidade de palitos', True, PRETO)
            tela.blit(instrucao, (INPUT_RECT.x + 10, INPUT_RECT.y - 40))
            desenha_input(tela, fonte, INPUT_RECT, 'Total de elementos:', input_ativo, num_elementos, input_buffer, cursor_visivel)
            # Texto abaixo do input
            instrucao2 = fonte_menor.render('Confirme pressionando ENTER', True, PRETO)
            tela.blit(instrucao2, (INPUT_RECT.x + 10, INPUT_RECT.y + INPUT_RECT.height + 10))
        elif not mostrar_pilhas:
            hover_voce = BOTAO_VOCE.collidepoint(mouse)
            hover_comp = BOTAO_COMP.collidepoint(mouse)
            texto = fonte.render('Quem começa o jogo:', True, PRETO)
            tela.blit(texto, (180, 30))
            desenha_botao(tela, fonte, BOTAO_VOCE, 'Você', quem_joga==1, hover_voce)
            desenha_botao(tela, fonte, BOTAO_COMP, 'Computador', quem_joga==2, hover_comp)
        else:
            if not pilhas_grafico or sum(pilhas_grafico) != num_elementos:
                pilhas_grafico = montar_pilhas_grafico(num_elementos)
            desenha_pilhas(tela, pilhas_grafico)
            # Não desenha input novamente aqui
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if not mostrar_botoes:
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
                                mostrar_botoes = True  # só libera botões após confirmação
                        except:
                            num_elementos = 11
                        input_buffer = ''
                        input_ativo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        input_buffer = input_buffer[:-1]
                    elif evento.unicode.isdigit() and len(input_buffer) < 4:
                        input_buffer += evento.unicode
            elif not mostrar_pilhas:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if BOTAO_VOCE.collidepoint(evento.pos):
                        quem_joga = 1
                        mostrar_botoes = False
                        mostrar_pilhas = True
                        # rodando = False  # remova para manter pilhas na tela
                    elif BOTAO_COMP.collidepoint(evento.pos):
                        quem_joga = 2
                        mostrar_botoes = False
                        mostrar_pilhas = True
                        # rodando = False
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

def montar_pilhas_grafico(quantidade):
    # Mesmo algoritmo do monta_pilhas do nim_mcts.py
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
