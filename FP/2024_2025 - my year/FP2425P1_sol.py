# Fundamentos da Programação 2024/25
# MNK - Projeto 1
# Alberto Abad - Outubro 2024


#2.1.1
# Assumir tabuleiro maixmo de 100x100 <--
def eh_tabuleiro(tab):
    return isinstance(tab, tuple) and 2 <= len(tab) <= 100 and \
        all((isinstance(lin, tuple) and 2 <= len(lin) <= 100 and  len(lin) == len(tab[0])) 
            for lin in tab) and \
            all(type(val) == int and val in (0, 1, -1) for lin in tab for val in lin)
    
# 2.1.2
def eh_posicao(pos):
    return type(pos) == int and 1 <= pos <=100*100
 
# 2.1.3
def obtem_dimensao(tab):
    return len(tab), len(tab[0])

# 2.1.4
def obtem_valor(tab, pos):
    i, j = pos2idx(tab, pos)
    return tab[i][j]

# aux
def pos2idx(tab, pos):
    _, n = obtem_dimensao(tab)
    return (pos-1)//n,  (pos-1)%n

#aux
def idx2pos(tab, idx):
    _, n = obtem_dimensao(tab)
    return idx[0]*n + idx[1] + 1

#2.1.5 
def obtem_coluna(tab, pos):
    _ , col = pos2idx(tab, pos)
    res = ()
    for lin in range(len(tab)):
        res += (idx2pos(tab, (lin,col)),)      
    return res

#2.1.6 
def obtem_linha(tab, pos):
    lin, _ = pos2idx(tab, pos)
    return tuple(idx2pos(tab,(lin, col)) for col in range(len(tab[0])))

#2.1.7
def obtem_diagonais(tab, pos):
    max_i, max_j = obtem_dimensao(tab)
    diagonals = ()
    
    for sign in (+1, -1): # +1 diagonal; -1 antidiagonal
        this_line = ()
        i ,j = pos2idx(tab, pos) 
        offset = min(i,j) if sign == 1 else min(max_i-1-i, j) # compute the offset to first column or first/last row (diag/antidiag)
        i, j = i-sign*offset, j-offset                        # place in the first position of the diagonal/antidiag
        for d in range(min(max_i,max_j)):                     # add all the positions adding (+1,+1) or (-1,+1)
            if 0 <= i+sign*d < max_i and 0 <= j+d < max_j:    # eh uma posicao Ok
                this_line += (idx2pos(tab, (i+sign*d,j+d)),)
        
        diagonals += (this_line,)
    
    return diagonals

#2.1.8
def tabuleiro_para_str(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('tabuleiro_para_str: argumento invalido')
    
    num2str = {0:'+', 1: 'X', -1:'O'}
    cad = ''
    lins, cols = obtem_dimensao(tab)
    
    lin_template1 = ''.join('{}---' for c in range(cols-1)) + '{}'
    lin_template2 = ''.join('|   ' for c in range(cols-1)) + '|'
    
    for l in range(lins-1):
        cad += lin_template1 + '\n'
        cad += lin_template2 + '\n'
    cad += lin_template1
    
    return cad.format(*(num2str[v] for lin in tab for v in lin))
    

# 2.2.1
def eh_posicao_valida(tab, pos):
    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError('eh_posicao_valida: argumentos invalidos')
    m, n = obtem_dimensao(tab)
    return 1 <= pos <= m*n

#2.2.2
def eh_posicao_livre(tab, pos):
    if not (eh_tabuleiro(tab) and eh_posicao(pos) and eh_posicao_valida(tab, pos)):
        raise ValueError('eh_posicao_livre: argumentos invalidos')
    i, j = pos2idx(tab, pos)
    return tab[i][j] == 0
 
# AUX 
def obtem_posicoes(tab, valor):
    lins, cols = obtem_dimensao(tab)
    res = ()
    for i in range(lins):
        for j in range(cols):
            if obtem_valor(tab, idx2pos(tab, (i,j))) == valor:
                res += (idx2pos(tab, (i,j)),)
    return res

#2.2.3
def obtem_posicoes_livres(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('obtem_posicoes_livres: argumento invalido')
    return obtem_posicoes(tab, 0)
    

#2.2.4
def obtem_posicoes_jogador(tab, value):
    if not (eh_tabuleiro(tab) and type(value) == int and value in (-1, 1)):
        raise ValueError('obtem_posicoes_jogador: argumentos invalidos')
    return obtem_posicoes(tab, value)

#2.2.5
def obtem_posicoes_adjacentes(tab, pos):
    if not (eh_tabuleiro(tab) and eh_posicao(pos) and eh_posicao_valida(tab, pos)):
        raise ValueError('obtem_posicoes_adjacentes: argumentos invalidos')
    lins, cols = obtem_dimensao(tab)
    i, j = pos2idx(tab, pos)
    res = ()
    
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if not (di == 0 and dj == 0): #nao incluir a propria posicao
                x, y = i + di, j + dj
                if 0 <= x < lins and 0 <= y < cols: # garantir limites
                    res += (idx2pos(tab, (x,y)),)
    return res

#2.2.6
def ordena_posicoes_tabuleiro(tab, lst):
    def chebyshev_distance(p1, p2):
        p1_x, p1_y = pos2idx(tab, p1)
        p2_x, p2_y = pos2idx(tab, p2)
        return max((abs(p1_x-p2_x), abs(p1_y-p2_y)))
        
    if not (eh_tabuleiro(tab) and isinstance(lst, tuple) and \
        all((eh_posicao(pos) and eh_posicao_valida(tab, pos)) for pos in lst)):
        raise ValueError('ordena_posicoes_tabuleiro: argumentos invalidos')
    
    m, n = obtem_dimensao(tab)
    c = (m // 2) * n + n // 2 + 1 # centro do tab
    
    return tuple(sorted(lst, key=lambda x:(chebyshev_distance(x,c),x)))
  
#2.2.7  
def marca_posicao(tab, pos, value):
    if not (eh_tabuleiro(tab) and eh_posicao(pos) and eh_posicao_valida(tab, pos) \
        and eh_posicao_livre(tab, pos) and value in (-1,1)):
        raise ValueError('marca_posicao: argumentos invalidos')
    
    lins, cols = obtem_dimensao(tab)
    new_tab = ()
    for i in range(lins):
        new_line = ()
        for j in range(cols):
            new_line += (value,) if idx2pos(tab, (i,j)) == pos else (tab[i][j],)
        new_tab += (new_line,)
    return new_tab 
 
#2.2.8    
def verifica_k_linhas(tab, pos, jog, k):
    if not (eh_tabuleiro(tab) and eh_posicao(pos) and eh_posicao_valida(tab,pos) \
        and type(k) == int and 1 <= k <= 100 and type(jog) == int and jog in (1, -1)):
        raise ValueError('verifica_k_linhas: argumentos invalidos')
  
    for linha in (obtem_linha(tab, pos), obtem_coluna(tab, pos)) + obtem_diagonais(tab, pos):
        idx = linha.index(pos) # indice da posicao
        for i in range(k):
            this_line = linha[idx-i:idx+k-i]
            if sum(obtem_valor(tab, each_pos) for each_pos in this_line) == k*jog:
                return True  
    return False
   
# 2.3.1   
def eh_fim_jogo(tab, k):
    if not (eh_tabuleiro(tab) and type(k) == int and 1 <= k <= 100):
        raise ValueError('eh_fim_jogo: argumentos invalidos')

    return obtem_ganhador(tab, k) != 0 or len(obtem_posicoes_livres(tab)) == 0
   
# AUX
def obtem_ganhador(tab, k):    
    for player in (1, -1):
        for pos in obtem_posicoes_jogador(tab, player):
            if verifica_k_linhas(tab, pos, player, k):
                return player
    return 0

# 2.3.2
def escolhe_posicao_manual(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('escolhe_posicao_manual: argumento invalido') 
    
    while True:
        num = input('Turno do jogador. Escolha uma posicao livre: ') 
        if num.isdigit():
            pos = int(num)
            if eh_posicao(pos) and eh_posicao_valida(tab, pos) and eh_posicao_livre(tab, pos):
                return pos 
    
# AUX - facil
def escolhe_facil(tab, player, k): # Esta funcao devolve TODAS as posições que cumprem com o critério facil
    res = set()
    # isto se já há uma peça propria colocada
    for pos in obtem_posicoes_jogador(tab, player):
        for adj in obtem_posicoes_adjacentes(tab, pos):
            if eh_posicao_livre(tab, adj):
                res.add(adj)
    
    # se nao nenhuma posicao livre adjacente a uma peça propria, 
    # escolho qualquer peça livre
    if not res:
        res = obtem_posicoes_livres(tab)
        
    return ordena_posicoes_tabuleiro(tab, tuple(res))
    
# AUX - normal
def escolhe_normal(tab, player, k): # Esta funcao devolve TODAS as posições que cumprem com o critério normal
    res_player = set()
    res_other = set()
    
    m = k
    posicoes_livres = obtem_posicoes_livres(tab)
    while not res_player and not res_other: # enquanto encontrar uma posicao que cumpre com o criterio, termino com a iteração
        res_player, res_other = set(), set()
        for pos in posicoes_livres:
            new_tab = marca_posicao(tab, pos, player)  # se esta posicao permite obter m pedras em linha para o player, a registro
            if verifica_k_linhas(new_tab, pos, player, m): # se tivesse feito as posiçoes em ordem, batava com devolver a primeira
                res_player.add(pos)
            new_tab = marca_posicao(tab, pos, -player) # se esta posicao permite obter m pedras em linha para o -player, a registro
            if verifica_k_linhas(new_tab, pos, -player, m):
                res_other.add(pos)
        m -= 1
                    
    res = tuple(res_player) if res_player else tuple(res_other) # se há posicoes no conjunto do jogador, devolvo essas, se não, as do adversario
    return ordena_posicoes_tabuleiro(tab, res)     
 
# AUX - dificil 
def escolhe_dificil(tab, player, k):
    def simula_completo(tab, player, k): # funcao que simula um jogo completo até o fim para dois jogadores "normais"
        current = player
        while not eh_fim_jogo(tab, k): 
            pos = escolhe_posicao_auto(tab, current, k, 'normal')
            tab = marca_posicao(tab, pos, current)
            current = -current

        return obtem_ganhador(tab, k) 
    
    sims = {}
    
    posicoes_livres = ordena_posicoes_tabuleiro(tab, obtem_posicoes_livres(tab)) # nesta função vou deveolver apenas a primeira posição que 
                                                                                 # cumprir com o criterio, mas por consistencia com as anteriores
                                                                                 # devolvo um tuplo de posicoes
    # TEST FIRST DIRECT WIN 
    for pos in posicoes_livres: 
        new_tab = marca_posicao(tab, pos, player)
        if obtem_ganhador(new_tab, k) == player: ## RETORNA O PRIMEIRO MOVIMENTO, não procuro todas as soluções
            return (pos,)
        
    # THEN BLOCK ADVERSARY WINNING
    for pos in posicoes_livres:     
        new_tab = marca_posicao(tab, pos, -player) # Check bloqueo
        if obtem_ganhador(new_tab, k) == -player:
            return (pos,)
    
    # DO THE SIMULATION
    for pos in posicoes_livres:     
        new_tab = marca_posicao(tab, pos, player)
        sims[pos] = simula_completo(new_tab, -player, k) ## SIMULA JOGO ATE O FIM E REGISTRA O RESULTADO
        
        if sims[pos] == player: # se ganha, podemos devolver
            return (pos,)
    
    # se cheguar aqui, nao há nenhuma posiçao que permita ganhar
    if 0 in sims.values(): # há pelo menos uma que permita empate?
        return ordena_posicoes_tabuleiro(tab, tuple(k for k in sims if sims[k] == 0))     
    else: # derrota de player em qualquer posicao, poderia devolver a 1a posicao livre ordenada 
        return posicoes_livres  

# 2.3.3
def escolhe_posicao_auto(tab, player, k, level):
    if not (eh_tabuleiro(tab) and (type(k) == int and k > 0 ) and (not eh_fim_jogo(tab, k)) and 
        type(player) == int and player in (1, -1) and 
            type(k) == int and k > 0 and level in ('facil', 'normal', 'dificil')):
        raise ValueError('escolhe_posicao_auto: argumentos invalidos') 
    
    
    auto = {'facil': escolhe_facil,
            'normal': escolhe_normal,
            'dificil': escolhe_dificil} 
    
    candidates = auto[level](tab, player, k)
    return candidates[0] # a primeira posicao que cumpre a estrategia escolhida
 
# 2.3.4
def jogo_mnk(config, player, level):
    if not (type(config) == tuple and len(config) == 3 and 
        all(type(c) == int for c in config) and
        2 <= config[0] <= 100 and 2 <= config[1] <= 100 and 
        config[2] >= 1 and type(player) == int and player in (-1,1) and
        type(level) == str and level in ('facil', 'normal', 'dificil')):
            raise ValueError('jogo_mnk: argumentos invalidos') 
    
    m, n, k = config
    
    tab = (((0,)*n),)*m
    
    print("Bem-vindo ao JOGO MNK.")
    print(f"O jogador joga com '{'X' if player == 1 else 'O'}'.")
    
    current = 1
    
    print(tabuleiro_para_str(tab))
    while not eh_fim_jogo(tab, k):
        if player == current:
            pos = escolhe_posicao_manual(tab)
        else:
            print(f'Turno do computador ({level}):')
            pos = escolhe_posicao_auto(tab, current, k, level)
        
        tab = marca_posicao(tab, pos, current)
        print(tabuleiro_para_str(tab))
        
        current = -current

    winner = obtem_ganhador(tab, k)
    if player == winner:
        print("VITORIA")
    elif winner != 0:
        print("DERROTA")
    else:
        print("EMPATE")
    
    return winner
    