# This is the Python script for your project

#TAD posicao
#Representação da posição é um tuplo, sendo o primeiro elemento a coluna e o segundo a linha, começando ambos em 1.
def cria_posicao(col, lin):
    """Recebe um caracter e um inteiro, correspondentes à coluna e linha da posição e devolve a posição correspondente formatada.
    O construtor verifica a validade dos argumentos e gera uma exceção _ValueError_ se não o forem.
    Parameters:
       col (str): Letra da coluna
       lin (int): Número da coluna
    Returns:
       posicao: A representação da posição é um tuplo (coluna, linha), em que a letra é convertida para um número"""
    if not (col in (list(chr(x) for x in range(97, 107))) and lin in list(range(1, 11))):
        raise ValueError('cria_posicao: argumentos invalidos')
    return ord(col)-96, lin

def obtem_pos_col(pos):
    """Recebe uma posição e devolve a respetiva letra da coluna.
    Parameters:
        pos (posicao): Posição
    Returns:
        str: Número da coluna"""
    return chr(pos[0]+96)

def obtem_pos_col_int(pos):
    """Mesmo funcionamento de `obtem_pos_col`, mas retorna o valor da implementação do TAD posição, que é um inteiro
    Parameters:
        pos (posicao): Posição
    Returns:
        int: Número da coluna"""
    return ord(obtem_pos_col(pos))-96


def obtem_pos_lin(pos):
    """Recebe uma posição e devolve o respetivo número da linha.
    Parameters:
        pos (posicao): Posição
    Returns:
        int: Número da linha"""
    return pos[1]

def eh_posicao(arg):
    """Verifica se o argumento é um TAD posição, retornando `True` se for ou `False` se não.
    Parameters:
        arg (any): Qualquer tipo de argumento
    Returns:
        bool: `True` se for uma posição ou `False` se não for"""
    if type(arg)==tuple and len(arg)==2:
        if type(arg[0])==type(arg[1])==int:
            if 1<=obtem_pos_col_int(arg)<=10 and 1<=obtem_pos_lin(arg)<=10:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def posicoes_iguais(p1, p2):
    """Verifica se `p1`` e `p2`` são posições e iguais, retornando `True` se sim ou `False` se não.
    Parameters:
        p1 (posicao): Posição a testar
        p2 (posicao): Posição a testar
    Returns:
        bool: `True` se forem iguais ou `False` se não forem"""
    return eh_posicao(p1) and eh_posicao(p2) and p1==p2

def posicao_para_str(p):
    """Recebe uma posição e retorna a cadeia de caracteres 
    Parameters:
        p (posicao): Posição de entrada
    Returns:
        str: Cadeia de caracteres do valor correspondente à posição (ex: `a2`, `c5`)"""
    return str(obtem_pos_col(p))+str(obtem_pos_lin(p))

def str_para_posicao(s):
    """Recebe uma cadeia de caracteres correspondente a uma posição e retorna a posição no formato do _TAD_
    Parameters:
        s (str): Cadeia de caracteres correspondente a uma posição
    Returns:
        position: Posição no formato do _TAD_"""
    return cria_posicao(s[0], int(s[1:]))

def eh_posicao_valida(pos, n):
    """Recebe uma posição e um valor de _n_ e retorna `True` se a posição for válida para o tabuleiro com _n_ órbitas ou `False` se for inválida.
    Parameters:
        pos (posicao): Posição a ser verificada
        n (int): Nº de órbitas do tabuleiro
    Returns:
        boolean: `True` se _pos_ for válida ou `False` se não for"""
    if not (eh_posicao(pos)):
        return False
    return 0<obtem_pos_col_int(pos)<=n*2 and 0<obtem_pos_lin(pos)<=n*2 and 2<=n<=5

def obtem_posicoes_adjacentes(pos, n, diag):
    """Recebe uma posição e um valor de n-órbitas do tabuleiro e retorna um tuplo com as posições do tabuleiro adjacentes à posição.
    Recebe também o indicador `diag` que identifica se são todas as posições adjacentes ou só as ortogonais
    Parameters:
        pos (posicao): Posição a ser verificada
        n (int): Nº de órbitas do tabuleiro
        diag (bool): Indicador se inclui diagonais (`True`) ou só ortogonais (`False`)
    Returns:
        tuple: Tuplo com as posições adjacentes ordenadas por sentido horário, começando pela posição acima de p"""
    #  8   1   2
    #  7  pos  3
    #  6   5   4
    adj=((obtem_pos_col_int(pos),  obtem_pos_lin(pos)-1), #1
         (obtem_pos_col_int(pos)+1,obtem_pos_lin(pos)-1), #2
         (obtem_pos_col_int(pos)+1,obtem_pos_lin(pos)),   #3
         (obtem_pos_col_int(pos)+1,obtem_pos_lin(pos)+1), #4
         (obtem_pos_col_int(pos),  obtem_pos_lin(pos)+1), #5
         (obtem_pos_col_int(pos)-1,obtem_pos_lin(pos)+1), #6
         (obtem_pos_col_int(pos)-1,obtem_pos_lin(pos)),   #7
         (obtem_pos_col_int(pos)-1,obtem_pos_lin(pos)-1)) #8
    out_tupl=()
    if diag:
        #Incuir diagonais
        for i in adj:
            if eh_posicao(i):
                if eh_posicao_valida(i, n):
                    out_tupl += (i, )
    elif not diag:
        #Só ortogonais
        #Como as diagonais no tuplo acima estão alternadas e os respetivos índices são pares, pode ser filtrado por uma verificação se o índice é par ou não
        #As ortogonais são as posições com índices pares (adj[0], adj[2], adj[4], adj[6])
        for i in range(0, len(adj)):
            if eh_posicao(adj[i]) and i%2==0:
                if eh_posicao_valida(adj[i], n):
                    out_tupl += (adj[i], )
    return out_tupl

def ordena_posicoes(tup, n):
    """Recebe um tuplo de posições e um valor de n-órbitas do tabuleiro e retorna um tuplo com as mesmas posições ordenadas de acordo com a leitura do tabuleiro de Orbito-n.
    Parameters:
        tup (tuple): Tuplo com as posições a serem ordenadas
        n (int): Nº de órbitas do tabuleiro
    Returns:
        tuple: Tuplo com as posições ordenadas de acordo com a leitura do tabuleiro de Orbito-n"""
    out_tup=()
    #Usa distância de Chebyshev, mas vai ter números com vírgula -> flutuantes
    pos_central = ((1+2*n)/2, (1+2*n)/2)
    for dist in [x/10 for x in range(5, 5+10*n, 10)]: #Distâncias: 0.5, 1.5, 2.5, 3.5, 4.5
        #dist corresponde à distância a ser verificada, começando pela mais pequena até à maior possível
        #este método vai já deixar as posições ordenadas por distância, depois por ordem de posição
        for linh in range(1, n*2+1): #Linhas
            for coln in range(1, n*2+1): #Colunas: no formato int
                if max(abs(coln - pos_central[0]), abs(linh - pos_central[1]))==dist and cria_posicao(chr(coln + 96), linh) in tup:
                    #O coln e linh vai passar por todas as posições do tabuleiro
                    #Se houver uma posição que tenha a posição a verificar, e que esteja no tuplo, é para adicionar ao tuplo de saída
                    out_tup += (cria_posicao(chr(coln+96),linh),)
    return out_tup

#TAD Pedra
#A representação da pedra é um inteiro: 1 para pedra preta, −1 para pedra branca e 0 para pedra neutra
def cria_pedra_branca():
    """Devolve uma pedra pertencente ao jogador branco.
    Returns:
        pedra: Pedra pertencente ao jogador branco"""
    return -1

def cria_pedra_preta():
    """Devolve uma pedra pertencente ao jogador preto.
    Returns:
        pedra: Pedra pertencente ao jogador preto"""
    return 1

def cria_pedra_neutra():
    """Devolve uma pedra neutra (não pertence a ninguém).
    Returns:
        pedra: Pedra neutra"""
    return 0

def eh_pedra(arg):
    """Verifica se o argumento é um TAD pedra, retornando `True` se for ou `False` se não.
    Parameters:
        arg (any): Qualquer tipo de argumento
    Returns:
        bool: `True` se for uma pedra ou `False` se não for"""
    return arg in (cria_pedra_branca(), cria_pedra_preta(), cria_pedra_neutra())

def eh_pedra_branca(ped):
    """Devolve `True` caso a pedra _ped_ pertença ao jogador branco ou `False` caso contrário.
    Returns:
        bool: `True` se a pedra for do jogador branco ou `False` se não for"""
    return ped==cria_pedra_branca()

def eh_pedra_preta(ped):
    """Devolve `True` caso a pedra _ped_ pertença ao jogador preto ou `False` caso contrário.
    Returns:
        bool: `True` se a pedra for do jogador preto ou `False` se não for"""
    return ped==cria_pedra_preta()

def pedras_iguais(ped1, ped2):
    """Devolve `True` caso os argumentos sejam pedras e sejam iguais ou `False` caso contrário.
    Returns:
        bool: `True` se as pedras são válidas e iguais ou `False` se não forem"""
    return eh_pedra(ped1) and eh_pedra(ped2) and ped1==ped2

def pedra_para_str(ped):
    """Recebe uma pedra e devolve a cadeia de caracteres que representa o jogador dono da pedra ('X', 'O' ou ' ').
    Parameters:
        ped (pedra): Pedra a ser verificada
    Returns:
        str: Cadeia de caracteres correspondente ao jogador dono da pedra"""
    if ped==cria_pedra_branca():
        return 'O'
    elif ped==cria_pedra_preta():
        return 'X'
    else:
        return ' '

def eh_pedra_jogador(ped):
    """Recebe uma pedra e devolve `True` se a pedra for de um jogador ou `False` se não for
    Parameters:
        ped (pedra): Pedra a ser verificada
    Returns:
        bool: `True` se a pedra for de um jogador ou `False` se não for"""
    return ped!=cria_pedra_neutra()

def pedra_para_int(ped):
    """Recebe uma pedra e devolve um inteiro valor (1, -1 ou 0) dependendo se a pedra é do jogador preto, branco ou neutra, respetivamente.
    Parameters:
        ped (pedra): Pedra a ser verificada
    Returns:
        int: Valor correspondente à pedra"""
    #Como a representação da pedra já é um inteiro, é só retornar o valor da pedra
    return ped

#TAD Tabuleiro
def cria_tabuleiro_vazio(n):
    """Recebe um valor de n-órbitas e devolve um tabuleiro vazio (sem posições ocupadas) de dimensão n.
    O construtor verifica a validade do argumento e gera uma exceção _ValueError_ se não for válido.
    O numer mínimo de órbitas é 2 e o máximo é 5.
    Parameters:
        n (int): Nº de órbitas do tabuleiro
    Returns:
        tabuleiro: Tabuleiro vazio de dimensão _n_"""
    if n not in list(range(2, 6)):
        raise ValueError('cria_tabuleiro_vazio: argumento invalido')
    tab={}
    #O tabuleiro é um dicionário cujas chaves são TADs posição e os valores TADs pedra
    #O tabuleiro, mesmo que vazio ou parcialmente cheio, já tem todas as chaves correspondentes às posições da dada dimensão
    for linh in range(1,2*n+1):
        for coln in range(1,2*n+1):
            coloca_pedra(tab, cria_posicao(chr(coln+96), linh), cria_pedra_neutra())
    return tab

def cria_tabuleiro(n, t_preto, t_branco):
    """Recebe um valor de n-órbitas, um tuplo com as posições das pedras pretas e um tuplo com as posições das pedras brancas e devolve um tabuleiro com as pedras nas posições indicadas.
    O construtor verifica a validade dos argumentos e gera uma exceção _ValueError_ se forem inválidos.
    Parameters:
        n (int): Nº de órbitas do tabuleiro
        t_preto (tuple): Tuplo com as posições das pedras pretas
        t_branco (tuple): Tuplo com as posições das pedras brancas
    Returns:
        tabuleiro: Tabuleiro com as pedras nas posições indicadas
    """
    if not (n in list(range(2, 6)) and type(t_preto) == tuple and type(t_branco) == tuple):
        raise ValueError('cria_tabuleiro: argumentos invalidos')
    for p, b in zip(t_preto, t_branco):
        #Verificar se as posições nos tuplos são válidas
        if not (eh_posicao(p) and eh_posicao(b)):
            raise ValueError('cria_tabuleiro: argumentos invalidos')
    tab = cria_tabuleiro_vazio(n)
    for i in t_preto:
        if obtem_pedra(tab, i)==cria_pedra_neutra():
            coloca_pedra(tab, i, cria_pedra_preta())
        else:
            #Se a posição a que for adicionar já estiver ocupada, dá erro
            #Supostamente não deveria dar erro aqui, visto que o tabuleiro começa vazio,
            #mas pelo sim pelo não tá cá
            raise ValueError('cria_tabuleiro: argumentos invalidos')
    for i2 in t_branco:
        if obtem_pedra(tab, i2)==cria_pedra_neutra():
            coloca_pedra(tab, i2, cria_pedra_branca())
        else:
            #Se a posição a que for adicionar já estiver ocupada, dá erro
            raise ValueError('cria_tabuleiro: argumentos invalidos')
    return tab

def cria_copia_tabuleiro(tab):
    """Recebe um tabuleiro e devolve uma cópia (não dependente) do tabuleiro.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser copiado
    Returns:
        tabuleiro: Cópia do tabuleiro"""
    return tab.copy()

def obtem_numero_orbitas(tab):
    """Recebe um tabuleiro e devolve o número de órbitas do mesmo.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
    Returns:
        int: Nº de órbitas do tabuleiro"""
    return int(obtem_pos_col_int(list(tab.keys())[-1])/2)
    #return len(obtem_linha_horizontal(tab, cria_posicao('a', 1)))
    #Como o tabuleiro é quadrado, o número de órbitas é igual ao dobro número de colunas/linhas.
    #O número de colunas/linhas pode ser obtido através do comprimento de uma linha/coluna, respetivamente.
    #Usei a posição (a, 1) porque é a primeira posição do tabuleiro, mas pode ser qualquer outra.


def obtem_pedra(tab, pos):
    """Recebe um tabuleiro e uma posição e devolve a pedra na posição indicada no tabuleiro. Se a posição estiver vazia, devolve uma pedra neutra.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        pos (posicao): Posição a ser verificada
    Returns:
        pedra: Pedra na posição indicada"""

    #O tabuleiro já tem todas as posições possíveis
    #Por isso é só retornar esse valor, mesmo que seja vazio (pedra neutra)
    return tab[pos]

def obtem_linha_horizontal(tab, pos):
    """Recebe um tabuleiro e uma posição e devolve um tuplo com as posições e pedras da linha horizontal que passa pela posição.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        pos (posicao): Posição a ser verificada
    Returns:
        tuple: Tuplo com as posições e pedras da linha horizontal"""

    output=()
    for i in tab.keys():
        if obtem_pos_lin(i)==obtem_pos_lin(pos):
            #O valor da linha é igual ao valor da posição
            #Logo pertence à mesma linha
            output+=((i,obtem_pedra(tab, i)),)
    return output

def obtem_linha_vertical(tab, pos):
    """Recebe um tabuleiro e uma posição e devolve um tuplo com as posições e pedras da linha vertical que passa pela posição.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        pos (posicao): Posição a ser verificada
    Returns:
        tuple: Tuplo com as posições e pedras da linha vertical"""
    output=()
    for i in tab.keys():
        if obtem_pos_col_int(i)==obtem_pos_col_int(pos):
            #O valor da coluna é igual ao valor da posição
            #Logo pertence à mesma coluna
            output+=((i,obtem_pedra(tab, i)),)
    return output

def obtem_linhas_diagonais(tab, pos):
    """Recebe um tabuleiro e uma posição e devolve um tuplo com as posições e pedras das duas diagonais que passam pela posição.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        pos (posicao): Posição a ser verificada
    Returns:
        tuple: Tuplo formado por 2 subtuplos, um com as posições da diagonal principal e outro com as posições da antidiagonal """

    linh, coln = obtem_pos_lin(pos), obtem_pos_col_int(pos)
    diag1 = diag2 = ()
    while coln>1 and linh>1:
        #Vai até à primeira posição da diagonal
        coln, linh = coln-1, linh-1
    while coln<=(obtem_numero_orbitas(tab)*2) and linh<=(obtem_numero_orbitas(tab)*2):
        #Itera até à última posição da diagonal

        diag1+= (((coln,linh),(obtem_pedra(tab, (coln, linh)))), )
        coln, linh = coln+1, linh+1

    linh, coln = obtem_pos_lin(pos),obtem_pos_col_int(pos)
    while coln>1 and linh<(obtem_numero_orbitas(tab)*2):
        #Vai até à primeira posição da antidiagonal
        coln, linh = coln-1, linh+1
    while coln<=(obtem_numero_orbitas(tab)*2) and linh>=1:
        #Itera até à última posição da antidiagonal

        diag2+= (((coln,linh),(obtem_pedra(tab, (coln, linh)))),)
        coln, linh = coln+1, linh-1

    return diag1, diag2

def obtem_posicoes_pedra(tab, ped):
    """Recebe um tabuleiro e uma pedra e devolve um tuplo com todas as posições ocupadas pelo mesmo tipo da pedra no tabuleiro.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        ped (pedra): Pedra a ser verificada
    Returns:
        tuple: Tuplo com todas as posições ocupadas pelo mesmo tipo da pedra."""
    ped_tup=()
    for i in list(tab.keys()):
        if obtem_pedra(tab, i)==ped:
            ped_tup+=(i,)
    return ordena_posicoes(ped_tup, obtem_numero_orbitas(tab))

def coloca_pedra(tab, pos, ped):
    """Recebe um tabuleiro, uma posição e uma pedra e modifica destrutivamente o tabuleiro, colocando a pedra na posição indicada, e devolve o próprio tabuleiro.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser modificado
        pos (posicao): Posição a ser modificada
        ped (pedra): Pedra a ser colocada na posição
    Returns:
        tabuleiro: Tabuleiro modificado"""
    tab[pos]=ped
    return tab

def remove_pedra(tab, pos):
    """Recebe um tabuleiro e uma posição e modifica destrutivamente o mesmo, removendo a pedra da posição indicada, e devolve o próprio tabuleiro.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser modificado
        pos (posicao): Posição a ser modificada
    Returns:
        tabuleiro: Tabuleiro modificado"""
    coloca_pedra(tab, pos, cria_pedra_neutra())
    return tab

def eh_tabuleiro(arg):
    """Recebe um argumento e verifica se é um TAD tabuleiro, retornando `True` se for ou `False` se não.
    Parameters:
        arg (any): Qualquer tipo de argumento
    Returns:
        bool: `True` se for um tabuleiro ou `False` se não for"""
    if type(arg)==dict:
        for i, i2 in zip(arg.keys(), arg.values()):
            if not (eh_posicao(i) and eh_pedra(i2)):
                return False
    else:
        return False
    #Se chegou aqui é porque o tabuleiro é válido
    return True

def tabuleiros_iguais(t1, t2):
    """Recebe dois argumentos e verifica se são tabuleiros e iguais, retornando `True` se forem ou `False` se não.
    Parameters:
        t1 (any): Qualquer tipo de argumento
        t2 (any): Qualquer tipo de argumento
    Returns:
        bool: `True` se forem tabuleiros e iguais ou `False` se não forem"""
    return eh_tabuleiro(t1) and eh_tabuleiro(t2) and t1==t2

def tabuleiro_para_str(tab):
    """Recebe um tabuleiro e devolve a representação visual do tabuleiro.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
    Returns:
        str: Cadeia de caracteres com a representação visual do tabuleiro"""
    current_lin=1
    output=[" ",]
    output_line=""

    #Construir o cabeçalho com as letras-colunas do tabuleiro
    for i in range(obtem_numero_orbitas(tab)*2): #O número de colunas é o dobro do número de órbitas
        output.append(f"   {chr(i+97)}")
    output.append("\n")

    #Realizar para todas as linhas
    for _ in obtem_linha_vertical(tab, (1, 1)):
        output.append(f"{current_lin:02d} ")
        for i2 in obtem_linha_horizontal(tab, (1, current_lin)):
            output.append(f"[{pedra_para_str(i2[1])}]")
            output.append("-")
        output.pop() #Remove o último "-"
        output.append("\n")

        if current_lin<len(obtem_linha_horizontal(tab, (1, 1))):
        #O valor da linha tem de ser menor que o valor da última linha
        #Porque na última linha nao realiza a adição dos traços verticais
            output.append(" ") #O primeiro espaço dos traços verticais
            for _ in obtem_linha_horizontal(tab, (1, current_lin)):
                output.append("   |")
            output.append("\n")
        current_lin+=1
    output.pop() #Remove o último "\n"
    for i in output:
        #Juntar todos os elementos da lista numa única string
        output_line+=str(i)

    return output_line

def move_pedra(tab, pos_init, pos_aft):
    """Recebe um tabuleiro, uma posição inicial e uma posição final e modifica destrutivamente o tabuleiro, movendo a pedra da posição inicial para a posição final.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser modificado
        pos_init (posicao): Posição inicial
        pos_aft (posicao): Posição final
    Returns:
        tabuleiro: Tabuleiro modificado"""
    #O valor da nova posição é o valor da posição antiga
    #A posição antiga passa a ficar desocupada, ou seja, é uma pedra neutra
    coloca_pedra(tab, pos_aft, obtem_pedra(tab, pos_init))
    remove_pedra(tab, pos_init)
    return tab

def obtem_posicao_seguinte(tab, pos, clockwise):
    """Recebe um tabuleiro, uma posição e devolve a posição da mesma órbita onde a posição se encontra a seguir no tabuleiro
    em sentido horário se _clockwise_ for `True` ou anti-horário se for `False`.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        pos (posicao): Posição a ser verificada
        clockwise (bool): Sentido de rotação
    Returns:
        posicao: Posição seguinte no sentido indicado"""

    def dist(pos1, posc):
        return max(abs(obtem_pos_col_int(pos1) - posc[0]), abs(obtem_pos_lin(pos1) - posc[1]))

    pos_central = ((1 + 2 * obtem_numero_orbitas(tab)) / 2, (1 + 2 * obtem_numero_orbitas(tab)) / 2)
    adj=obtem_posicoes_adjacentes(pos, obtem_numero_orbitas(tab),  False)
    #[Acima, direita, abaixo, esquerda]
    adj_mesma_dist=()

    for i in adj:
        if dist(i, pos_central)==dist(pos, pos_central):
            #A nova posição tem que ter a mesma distância ao centro que a posição inicial
            adj_mesma_dist+=(i,)
            #(direita, esquerda) ou (cima, baixo) ou (baixo, esquerda) ou (cima, esquerda), etc.
            #Vai ter sempre só 2 elementos

    if adj_mesma_dist[0] == (obtem_pos_col_int(pos),obtem_pos_lin(pos)-1) and adj_mesma_dist[1] == (obtem_pos_col_int(pos),obtem_pos_lin(pos)+1) and obtem_pos_col_int(pos)>pos_central[0]:
        #  /\    |
        #  |  ,  |  e está à direita do centro  >> Vai ser a segunda posição da lista para sentido horário
        #  |    \/
        return adj_mesma_dist[-1] if clockwise else adj_mesma_dist[0]

    elif adj_mesma_dist[0] == (obtem_pos_col_int(pos)+1,obtem_pos_lin(pos)) and adj_mesma_dist[1] == (obtem_pos_col_int(pos)-1,obtem_pos_lin(pos)) and obtem_pos_lin(pos)>pos_central[1]:

        #  --> , <-- e está abaixo do centro  >> Vai ser a segunda posição da lista para sentido horário
        return adj_mesma_dist[-1] if clockwise else adj_mesma_dist[0]

    elif adj_mesma_dist[0] == (obtem_pos_col_int(pos),obtem_pos_lin(pos)-1) and adj_mesma_dist[1] == (obtem_pos_col_int(pos)-1,obtem_pos_lin(pos)):

        #  /\
        #  |  ,  <--  (canto inferior direito da òrbita)  >> Vai ser a segunda posição da lista para sentido horário
        #  |
        return adj_mesma_dist[-1] if clockwise else adj_mesma_dist[0]

    else:
        return adj_mesma_dist[0] if clockwise else adj_mesma_dist[-1]


def roda_tabuleiro(tab):
    """Recebe um tabuleiro e modifica destrutivamente o mesmo, rodando todas as pedras uma posição no sentido anti-horário, e devolve o próprio tabuleiro.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser modificado
    Returns:
        tabuleiro: Tabuleiro rodado"""
    tab_new=cria_copia_tabuleiro(tab)
    todas_as_posicoes = obtem_posicoes_pedra(tab, cria_pedra_preta()) + obtem_posicoes_pedra(tab,cria_pedra_branca()) + obtem_posicoes_pedra(tab, cria_pedra_neutra())
    #todas_as_posicoes corresponde a todas as posições ocupadas por pedras, quer sejam pretas, brancas ou neutras.
    #Como os dois tabuleiros (inicial e rodado) têm a mesma dimensão, o tuplo de posições é o mesmo para ambos

    for i in todas_as_posicoes:
        #Ao copiar os valores para o novo tabuleiro, não deve haver conflitos entre pedras
        #Pois cada posição do tabuleiro inicial corresponde a uma e só uma posição no tabuleiro rodado para um determinado sentido
        coloca_pedra(tab_new, obtem_posicao_seguinte(tab, i, True), obtem_pedra(tab, i))
    for i in todas_as_posicoes:
        #Substituir os valores do tabuleiro temporário no tabuleiro original
        coloca_pedra(tab, i, obtem_pedra(tab_new, i))
    return tab

def verifica_linha_pedras(tab, pos, ped, k):
    """
    Recebe um tabuleiro, uma posição, uma pedra e um inteiro k e devolve `True` se existe pelo menos uma linha (horizontal, vertical ou diagonal)
    que contenha a posição _ped_ com _k_ ou mais pedras consecutivas do jogador com pedras _ped_, e `False` caso contrário.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        pos (posicao): Posição que deve pertencer à linha
        ped (pedra): Tipo de pedras da linha
        k (int): Nº de pedras consecutivas
    Returns:
        bool: `True` se existir uma linha com _k_ ou mais pedras consecutivas do jogador com pedras _ped_, ou `False` se não existir
    """
    def verifica_linha_pedras_aux(elem, tab1, pos1, ped1, k1):
        elem_seq=[] #Lista para guardar a sequência detetada temporariamente
        for i in elem:
            if len(elem_seq)>=k1 and pos1 in elem_seq:
                #Já temos uma sequência que cumpre os requisitos, já nem é preciso correr mais a função
                return True
            elif len(elem_seq)==0:
                #A lista começa vazia, por isso temos de adicionar o primeiro elemento da lista e começar a avaliação para o segundo
                elem_seq.append(i[0])
            elif i[1]==obtem_pedra(tab1, elem_seq[-1])==ped1:
                #Estamos perante uma sequência, ou seja, o valor atualmente lido é igual ao anterior e é do tipo de pedra pedida
                elem_seq.append(i[0])
            else:
                #O valor não é igual nem é da mesma pedra, ou seja, já não existe sequência
                elem_seq.clear()
                elem_seq.append(i[0]) #Volta a adicionar o último valor para a próxima verificação funcionar

        if len(elem_seq)>=k1 and (pos1 in elem_seq) and obtem_pedra(tab1, elem_seq[0])==ped1:
            #Pelo menos uma posição da sequência tem de ser da pedra pedida
            #Se houver sequência, mas acabar o for loop, deve checar aqui se é sequência
            return True
        #Se saiu do for loop e não retornou antes é porque não há sequência
        return False

    if verifica_linha_pedras_aux(obtem_linha_vertical(tab, pos), tab, pos, ped, k):
        return True
    elif verifica_linha_pedras_aux(obtem_linha_horizontal(tab, pos), tab, pos, ped, k):
        return True
    elif verifica_linha_pedras_aux(obtem_linhas_diagonais(tab, pos)[0], tab, pos, ped, k):
        return True
    elif verifica_linha_pedras_aux(obtem_linhas_diagonais(tab, pos)[1], tab, pos, ped, k):
        return True
    else:
        return False

def eh_vencedor(tab, ped):
    """É uma função auxiliar que recebe um tabuleiro e uma pedra de jogador, e devolve `True`
    se existe uma linha completa do tabuleiro de pedras do jogador ou `False` caso contrário.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        ped (pedra): Pedra do jogador
    Returns:
        bool: `True` se o jogador é vencedor ou `False` se não for"""

    for i in obtem_posicoes_pedra(tab, ped):
        if verifica_linha_pedras(tab, i, ped, 2*obtem_numero_orbitas(tab)):
            return True
    return False

def eh_fim_jogo(tab):
    """É uma função auxiliar que recebe um tabuleiro e devolve `True` se o jogo já terminou ou `False` caso contrário.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
    Returns:
        bool: `True` se o jogo terminou ou `False` se não terminou"""
    return  eh_vencedor(tab, cria_pedra_branca()) or eh_vencedor(tab, cria_pedra_preta())

def escolhe_movimento_manual(tab):
    """É uma função auxiliar que recebe um tabuleiro e permite escolher uma posição livre do tabuleiro onde colocar uma pedra.
    A função não modifica o seu argumento e devolve a posição correta, se for válida e livre.
    A função deve perguntar continuamente por uma posição até que o utilizador forneça uma posição válida e livre.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
    Returns:
        posicao: Posição escolhida pelo utilizador"""
    def verifica_posicao(expr):
        #Função auxiliar para verificar se a posição inserida pelo utilizador é válida
        #Nunca retorna erros:
        return True if (2<=len(expr)<=3 and expr[0] in tuple(chr(a) for a in range(97, 107)) and expr[1:] in tuple(str(y) for y in range(1, 11))) else False
    z=None
    break_trigger=False
    while not break_trigger:
        x = input("Escolha uma posicao livre:")
        if not verifica_posicao(x):
            continue
        else:
            z=str_para_posicao(x)
            if eh_posicao(z):
                if eh_posicao_valida(z, obtem_numero_orbitas(tab)):
                    #Verificar se a posição inserida é uma posição válida
                    #A expressão serve para calcular o número de órbitas
                    if not eh_pedra_jogador(obtem_pedra(tab, z)):  #Verificar se a posição inserida é uma posição livre
                        break_trigger=True
    return z

def escolhe_movimento_auto(tab, ped, lvl):
    """É uma função auxiliar que recebe um tabuleiro (em que o jogo não terminou ainda), uam pedra e a cadeia de caracteres _lvl_
    correspondente à estratégia, e devolve a posição escolhida automaticamente pelo computador de acordo com a estratégia selecionada
    para o jogador com as pedras _ped_.
    A função não modifica nenhum dos seus argumentos.
    As estratégias a seguir devem ser identificados pela cadeia de caracteres 'facil' e 'normal'.
    Parameters:
        tab (tabuleiro): Tabuleiro a ser verificado
        ped (pedra): Pedra do jogador
        lvl (str): Estratégia de jogo
    Returns:
        posicao: Posição escolhida pelo computador"""

    n=obtem_numero_orbitas(tab)
    k=2*n
    ped_adversario=cria_pedra_branca() if ped==cria_pedra_preta() else cria_pedra_preta()
    todas_as_posicoes = obtem_posicoes_pedra(tab, cria_pedra_preta()) + obtem_posicoes_pedra(tab,cria_pedra_branca()) + obtem_posicoes_pedra(tab, cria_pedra_neutra())
    # Tuplo com todas as posições do tabuleiro, alternativa a tab.keys(), que é exclusivo a dicionários
    # Como os tabuleiros inicial e rodados têm a mesma dimensão, o tuplo de posições é o mesmo para todos
    if lvl=='facil':
        tab_one_rotation = roda_tabuleiro(cria_copia_tabuleiro(tab))
        for i in ordena_posicoes(todas_as_posicoes, n):
            #i corresponde ao valor do tuplo que contém as posições ordenadas de menor>>maior órbita (ordem do tabuleiro)
            #Na menor órbita é a prioridade
            for i2 in obtem_posicoes_pedra(tab_one_rotation, ped):
                #i2 corresponde ao valor do tuplo que contém todas as posições do jogador selecionado
                if (i in obtem_posicoes_adjacentes(i2, n, True)) and not eh_pedra_jogador(obtem_pedra(tab_one_rotation, i)):
                    #A posição de menor órbita tem de ser adjacente a uma das peças do jogador selecionado
                    #e tem de estar livre
                    #O roda_tabuleiro obtém a posição seguinte no sentido anti-horário
                    #Para voltar a posição anterior, é só rodar no sentido horário
                    return obtem_posicao_seguinte(tab_one_rotation, i, True)

        #se o programa chegou aqui é porque não arranjou nenhuma posição adjacente para jogar,
        #ou seja, tem de jogar na posição livre mais perto do centro

        for j in ordena_posicoes(todas_as_posicoes, n):
            if not eh_pedra_jogador(obtem_pedra(tab, j)):
                return j

    elif lvl=='normal':
        tab_one_rotation = roda_tabuleiro(cria_copia_tabuleiro(tab))
        livres = obtem_posicoes_pedra(tab_one_rotation, cria_pedra_neutra())
        for l in range(k,0,-1):
            #Começa pelo maior valor de k e diminui até 0 se não encontrar nenhuma posição
            for pos1 in livres:
                tab1 = coloca_pedra(cria_copia_tabuleiro(tab_one_rotation),pos1,ped)
                if verifica_linha_pedras(tab1,pos1,ped,l):
                    #Se a pedra a colocar cria uma linha vencedora, então temos de a colocar no tabuleiro original
                    #para isso é obter a posição seguinte no sentido contrário à rotação (neste caso, sentido horário)
                    return obtem_posicao_seguinte(tab_one_rotation, pos1, True)

            #Se não encontrou nenhuma posição onde ganhe à 1.ª jogada, então tem de impedir o adversário
            tab_two_rotation = roda_tabuleiro(cria_copia_tabuleiro(tab_one_rotation))
            livres2 = obtem_posicoes_pedra(tab_two_rotation, cria_pedra_neutra())
            for pos2 in livres2:
                tab2 = coloca_pedra(cria_copia_tabuleiro(tab_two_rotation),pos2,ped_adversario)
                #O "-ped" obtém a pedra do adversário
                if verifica_linha_pedras(tab2,pos2,ped_adversario,l):
                    #Se a pedra do adversário faz linha após 2 rotações, então jogamos nessa posição no tab. original agora
                    #Para isso, temos de obter a posição seguinte 2 vezes no sentido contrário à rotação (sentido horário)
                    return obtem_posicao_seguinte(tab_two_rotation, obtem_posicao_seguinte(tab_two_rotation, pos2, True), True)

def orbito(n, modo, jog):
    """Função principal do jogo Orbito-n. Recebe um número de órbitas do tabuleiro, uma cadeia de caracteres que representa o modo de jogo
    e a representação externa de uma pedra (preta/branca), e devolve um inteiro identificando o jogador vencedor (1 para preto ou -1 para branco)
    ou 0 em caso de empate. O jogo começa sempre com o jogador com pedras pretas.
    A função deve verificar a validade dos argumentos e gerar uma exceção _ValueError_ se forem inválidos.

    - 'facil': Jogo de um jogador contra o computador que utiliza a estratégia fácil.
        O jogador joga com as pedras com representação externa. No fim do jogo a função
        mostra o resultado obtido pelo jogador: VITORIA, DERROTA ou EMPATE.
    - 'normal': Jogo de um jogador contra o computador que utiliza a estratégia normal.
        O jogador joga com as pedras com representação externa. No fim do jogo a função
        mostra o resultado obtido pelo jogador: VITORIA, DERROTA ou EMPATE.
    - '2jogadores': Jogo de dois jogadores. No fim do jogo a função mostra o resultado
        do jogo: VITORIA DO JOGADOR 'X', VITORIA DO JOGADOR 'O' ou EMPATE.
    Parameters:
        n (int): Nº de órbitas do tabuleiro
        modo (str): Modo de jogo
        jog (str): Representação externa da pedra do jogador
    Returns:
        pedra: Pedra do jogador vencedor (1 para preto ou -1 para branco) ou 0 em caso de empate"""
    if not (n in list(range(2,6)) and modo in ('facil', 'normal', '2jogadores') and jog in ('O', 'X')):
        raise ValueError('orbito: argumentos invalidos')
    print(f"Bem-vindo ao ORBITO-{n}.")
    if modo=='facil':
        print("Jogo contra o computador (facil).")
        print(f"O jogador joga com '{jog}'.")
    elif modo=='normal':
        print("Jogo contra o computador (normal).")
        print(f"O jogador joga com '{jog}'.")
    else:
        print("Jogo para dois jogadores.")

    player_to_play="me" if jog=='X' else "pc" #Começa sempre o jogador com as pedras pretas
    my_pieces=cria_pedra_preta() if jog=='X' else cria_pedra_branca()
    pc_pieces=cria_pedra_branca() if jog=='X' else cria_pedra_preta()
    tab = cria_tabuleiro_vazio(n)
    print(tabuleiro_para_str(tab))
    #Para o modo de 2 jogadores, o jogador1 é o my_pieces e o jogador2 é o pc_pieces
    while not eh_fim_jogo(tab):
        if player_to_play=="me":
            print("Turno do jogador.") if modo in ('facil', 'normal') else print(f"Turno do jogador {pedra_para_str(my_pieces)}.")
            pos_to_add=escolhe_movimento_manual(tab)
            coloca_pedra(tab, pos_to_add, my_pieces)
            roda_tabuleiro(tab)
            player_to_play="pc" #Eu já joguei/jogador1 jogou, agora o próximo é o computador/jogador2
            #Verificar se o eu/jogador1 ganhou com esta jogada
            print(tabuleiro_para_str(tab))
            if verifica_linha_pedras(tab,pos_to_add, my_pieces, 2*n): #Se for true, eu ganhei/jogador1 ganhou
                print("VITORIA") if modo in ('facil', 'normal') else print(f"VITORIA DO JOGADOR {pedra_para_str(my_pieces)}.")
                return my_pieces
        elif player_to_play=="pc":
            print(f"Turno do jogador {pedra_para_str(pc_pieces)}.") if modo=='2jogadores' else print(f"Turno do computador ({modo}).")
            pos_to_add=(escolhe_movimento_auto(tab, pc_pieces, modo) if modo in ('facil', 'normal') else escolhe_movimento_manual(tab))
            coloca_pedra(tab, pos_to_add, pc_pieces)
            roda_tabuleiro(tab)
            player_to_play="me" #O computador/jogador2 jogou, por isso sou eu
            print(tabuleiro_para_str(tab))
            #Verificar se o pc/jogador2 ganhou com esta jogada
            if verifica_linha_pedras(tab, pos_to_add, pc_pieces, 2*n): #Se for true, o computador/jogador1 ganhou
                print("DERROTA") if modo in ('facil', 'normal') else print(f"VITORIA DO JOGADOR {pedra_para_str(pc_pieces)}.")
                return pc_pieces

    #Se o programa chegou aqui e não deu nenhum return, é porque o jogo acabou, mas ninguém ganhou
    #Ou seja, é um empate
    print("EMPATE")
    return cria_pedra_neutra()

ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
t = cria_tabuleiro(2, ip, ib)
print(tabuleiro_para_str(t))
print("")
print(tabuleiro_para_str(roda_tabuleiro(t)))