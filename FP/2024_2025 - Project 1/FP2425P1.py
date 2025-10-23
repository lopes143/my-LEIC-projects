# This is the Python script for your project

def eh_tabuleiro(tab):
    """
    Recebe um tabuleiro e retorna TRUE se o tabuleiro for válido ou FALSE se não o for.
    Nunca levanta exceções

    Parâmetros:
        tab (tuple): Tabuleiro a ser verificado
    Ouptut:
        output (bool): TRUE se for válido e FALSE se não o for
    """
    if isinstance(tab,tuple) and len(tab)>=2 and len(tab)<=100:
        # O tuplo mãe é um tabuleiro
        for tabulLine in tab:
            if isinstance(tabulLine, tuple) and len(tabulLine)>=2 and len(tabulLine)<=100:
                # É composto por subtuplos
                if len(tabulLine)==len(tab[0]):
                    # Cada subtuplo tem o msm nº de elemts do 1º subtuplo
                    for lineElem in tabulLine:
                        if type(lineElem)==int and (lineElem==1 or lineElem==0 or lineElem==-1):
                            # Cada posição do tabuleiro é válida
                            output=True
                        else:
                            return False
                else:
                    return False
            else:
                return False
    else:
        return False
    return output

def eh_posicao(pos):
    """
    Recebe uma posição e retorna TRUE se for válida ou FALSE se não for.
    Nunca levanta exceções

    Parâmetros:
        pos (int): Posição a ser verificada
    Ouptut:
        boolean: TRUE se for válida e FALSE se não for
    """
    if type(pos)==int and pos>0 and pos<=(100*100):
        return True
    else:
        return False

def obtem_dimensao(tab):
    """
    Recebe um tabuleiro e retorna um tuplo com o nº de linhas e de colunas.

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado

    Ouptut:
        tuple: 
            nLinhas: número de linhas
            nColunas: número de colunas
    """
    nLinhas = len(tab)
    nColunas = len(tab[0])
    return (nLinhas, nColunas)

def obtem_valor(tab, pos):
    """
    Recebe um tabuleiro e uma posição e retorna o valor contido nessa posição.

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição a ser verificada
    Ouptut:
        b (int): Valor da posição verificada
    """
    i = 0
    for a in tab:
        for b in a:
            i+=1
            #Quando vai lendo os argumentos, o i vai aumentando progressivamente
            #Assim o i corresponde à posição no número atualmente lido pelo for
            if i==pos:
                return b
    
def obtem_coluna(tab, pos):
    """
    Recebe um tabuleiro e uma posição e retorna um tuplo com todas as posiçẽs da coluna em que a posição de entrada está contida.

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição a ser verificada

    Ouptut:
        col (tuple): tuplo com todas as posições da coluna (ordenada)
    """
    col = ()
    nColuna = pos%obtem_dimensao(tab)[1]
    #Divide a posição pelo nº de linhas
    #Assim temos a ordem de posição na linha, que é o número da coluna
    for i in range(nColuna, (obtem_dimensao(tab)[0]*obtem_dimensao(tab)[1])+1, obtem_dimensao(tab)[1]):
        #Posição na coluna = posição do 1º elem na coluna + (dimensão da coluna * nº da linha)
        if i!=0:
            #Se a entrada da linha for a última, um zero vai ser adicionado, mas não pode
            col += (i, )
    return col

def obtem_linha(tab, pos):
    """
    Recebe um tabuleiro e uma posição e retorna um tuplo com todas as posiçẽs da linha em que a posição de entrada está contida.

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição a ser verificada

    Ouptut:
        lin (tuple): tuplo com todas as posições da linha (ordenada)
    """
    lin = ()
    nLinha = ((pos-1)//obtem_dimensao(tab)[1])+1
    # O nº da linha começa no 1
    firstLineValue = (nLinha-1)*(obtem_dimensao(tab)[1])+1
    # Aqui o valor da linha tem de começar no 0
    # Expressão: 4(l-1)+1
    for i in range(firstLineValue, firstLineValue+obtem_dimensao(tab)[1]):
        lin+= (i, )
    return lin

def obtem_diagonais(tab, pos):
    """
    Recebe um tabuleiro e uma posição e retorna um tuplo com 2 subtpulos, sendo o 1º todas as posiçẽs da diagonal e o 2º da antidiagonal em que a posição de entrada está contida.

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição a ser verificada

    Ouptut:
        sortDiag (tuple) = ( tuple(diag1), tuple(diag2) )
            diag1 (list): Posições da diagonal ordenados do menor para o maior
            diag2 (list): Posições da antidiagonal ordenados do maior para o menor
    """
    diag1 = []
    diag2 = []
    for i in range(pos, (obtem_dimensao(tab)[0]*obtem_dimensao(tab)[1])+1, obtem_dimensao(tab)[1]+1):
        #Diagonal principal à frente de pos
        diag1.append(i)
        if i==obtem_linha(tab, i)[-1] or i==obtem_coluna(tab, i)[-1]:
            #Se chegar ao extremo da coluna ou da linha
            break

    for i in range(pos, 0, -(obtem_dimensao(tab)[1]+1)):
        #Diagonal principal atrás de pos
        diag1.append(i)
        if i==obtem_linha(tab, i)[0] or i==obtem_coluna(tab, i)[0]:
            break

    for i in range(pos, (obtem_dimensao(tab)[0]*obtem_dimensao(tab)[1])+1, obtem_dimensao(tab)[1]-1):
        #Antidiagonal à frente de pos
        diag2.append(i)
        if i==obtem_linha(tab, i)[0] or i==obtem_coluna(tab, i)[-1]:
            break

    for i in range(pos, 0, -(obtem_dimensao(tab)[1]-1)):
        #Antidiagonal atrás de pos
        diag2.append(i)
        if i==obtem_linha(tab, i)[-1] or i==obtem_coluna(tab, i)[0]:
            break

    diag1.remove(pos)  #Remover a posição original que está duplicada
    diag2.remove(pos)
    diag1.sort()
    diag2.sort()
    diag2.reverse()  #A antidiagonal deve estar ordenada do maior para o menor
    diag1Tup=()
    diag2Tup=()
    for i in diag1:
        diag1Tup+=(i,)
    for i2 in diag2:
        diag2Tup+=(i2,)

    diag2.reverse()
    sortDiag = ((diag1Tup),(diag2Tup))

    return sortDiag

def tabuleiro_para_str(tab):
    """
    Recebe um tabuleiro e retorna uma cadeia de caracteres correspondente à representação visual (representação gráfica para humanos) do tabuleiro.

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado

    Ouptut:
        strOutput (str): Cadeia de caracteres com a representação visual, que inlui caracteres de escape (ex: "\\n")
    """
    line = []
    output=[]
    for i in tab:
        #Para cada linha
        for i2 in i:
            #Para cada elemento
            if i2==0:
                iconToAdd="+"
            elif i2==1:
                iconToAdd="X"
            elif i2==-1:
                iconToAdd="O"
            line.append(iconToAdd)    
            line.append("---")
        line.pop()
        #Remove o último "---"
        output.append(line.copy())
        output.append(["\n"])
        line.clear()
        for i2 in i:
            line.append("|")
            line.append("   ")
        line.pop()
        output.append(line.copy())
        output.append(["\n"])
        line.clear()
    output.pop()
    output.pop()
    output.pop()
    #Remove o último "\n", o último "|   |   | ..." e o útimo "\n" da linha anterior
    strOutput=""
    for a in output:
        for b in a:
            #Todos os elementos do output estão em sublistas
            #Este loop concatena-os para string
            strOutput += b
    return strOutput

def eh_posicao_valida(tab, pos):
    """
    Recebe um tabuleiro e uma posição e retorna TRUE se a posição for válida para o tabuleiro recebido ou FALSE se não o for.
    
    Verifica se os argumentos são válidos com as funções eh_tabuleiro e eh_posicao e gera uma exceção ValueError se os argumentos de entrada não o forem.
    
    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição a ser verificada

    Ouptut:
        boolean: TRUE se for válida e FALSE se não o for
    """
    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError('eh_posicao_valida: argumentos invalidos')
    elif pos<=(obtem_dimensao(tab)[0]*obtem_dimensao(tab)[1]):
        return True
    else:
        return False
    
def eh_posicao_livre(tab, pos):
    """
    Recebe um tabuleiro e uma posição e retorna TRUE se a posição estiver livre (isto é, se o valor da posição for 0) para o tabuleiro recebido ou FALSE se não o for.
    
    Verifica se os argumentos são válidos com as funções eh_tabuleiro e eh_posicao e gera uma exceção ValueError se os argumentos de entrada não o forem.
    
    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição a ser verificada

    Ouptut:
        boolean: TRUE se for válida e FALSE se não o for
    """
    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError('eh_posicao_livre: argumentos invalidos')
    if not eh_posicao_valida(tab, pos):
        raise ValueError('eh_posicao_livre: argumentos invalidos')
    # posToCheck é um contador para descobrir a posição
    posToCheck=0
    for i in tab:  # Ler linha a linha do tabuleiro
        for i2 in i:  # Ler elemento a elemento da linha
            posToCheck+=1
            if posToCheck==pos:
                #Estamos a avaliar o argumento com a posição certa
                if i2==0:
                    return True
                else:
                    return False

def obtem_posicoes_livres(tab):
    """
    Recebe um tabuleiro e retorna um tuplo com todas as posições livres do tabuleiro, ou seja, com o valor 0.
    
    Verifica a validade do tabuleiro com a função eh_tabuleiro e gera uma exceção ValueError se não for válido.
    
    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado

    Ouptut:
        tupFreePlaces (tuple): tuplo com todas as posições livres do tabuleiro ordenadas
    """
    if not eh_tabuleiro(tab):
        raise ValueError('obtem_posicoes_livres: argumento invalido')
    position=0  #Position é um contador
    tupFreePlaces=()  #Tuplo que contém os valores das posições vazias
    for i in tab:
        for i2 in i:
            position+=1
            if i2==0:
                tupFreePlaces+=(position, )

    return tupFreePlaces

def obtem_posicoes_jogador(tab, jog):
    """
    Recebe um tabuleiro e um inteiro indentificando um jogador retorna um tuplo com todas as posições ocupadas por esse jogador.
    
    Verifica se os argumentos são válidos com a função eh_tabuleiro, para além de verificar se o nº do jogador é valido, e gera uma exceção ValueError se algum argumento não o for.
    
    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        jog (int): Número do jogador (1 ou -1)

    Ouptut:
        tupPlayer (tuple): tuplo com as posições do jogador ordenadas
    """
    if not(eh_tabuleiro(tab) and jog in (1, -1)):
        #O tabuleiro tem de ser válido e o jogador só pode ser 1 ou -1
        raise ValueError("obtem_posicoes_jogador: argumentos invalidos")
    position=0
    tupPlayer=()  # Tuplo com as posições do jogador a avaliar
    for i in tab:
        for i2 in i:
            position+=1
            if i2==jog:
                tupPlayer+=(position, )
    
    return tupPlayer

def obtem_posicoes_adjacentes(tab, pos):
    """
    Recebe um tabuleiro e uma posição e retorna um tuplo com todas as posições adjacentes a essa posição.
    
    Verifica se os argumentos de entrada são válidos com as funções eh_tabuleiro e eh_posicao_valida e gera uma exceção ValueError se os argumentos não o forem.
    
    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição a ser analisada

    Ouptut:
        posicoesTup (tuple): tuplo com as posições adjacentes
    """
    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError("obtem_posicoes_adjacentes: argumentos invalidos")
    if not eh_posicao_valida(tab, pos):
        raise ValueError("obtem_posicoes_adjacentes: argumentos invalidos")
    posicoes = []
    if pos!=obtem_coluna(tab, pos)[0]:  #Adjacente acima
        #Não está junto à borda superior
        posicoes.append(int(pos-obtem_dimensao(tab)[1]))
        #Ao subtrair a posição ao nº de elmentos duma linha, tem-se a posição da linha acima
    
    if pos!=obtem_coluna(tab, pos)[-1]:  #Adjacente abaixo
        #Não está junto à borda inferior
        posicoes.append(int(pos+obtem_dimensao(tab)[1]))
        #Ao somar a posição ao nº de elmentos duma linha, tem-se a posição da linha abaixo
    
    if pos!=obtem_linha(tab, pos)[0]:  #Adjacente à esquerda
        #Não está junto à borda da esquerda
        posicoes.append(pos-1)
        #Subtrair um valor à posição atual dá-nos a posição da esquerda
    
    if pos!=obtem_linha(tab, pos)[-1]:  #Adjacente à direita
        #Não está junto à borda da direita
        posicoes.append(pos+1)
        #Adicionar um valor à posição atual dá-nos a posição da esquerda
    
    if pos!=obtem_coluna(tab, pos)[0] and pos!=obtem_linha(tab, pos)[0]:  #Adjacente ao canto superior esquerdo
        #Não está  no canto superior esquerdo
        posicoes.append(pos-obtem_dimensao(tab)[1]-1)
        #Dá-nos a posição da posição à esqurda da que está por cima da posição original
        #Ou seja, o canto superior esquerdo adjacente à posição inicial

    if pos!=obtem_coluna(tab, pos)[0] and pos!=obtem_linha(tab, pos)[-1]:  #Adjacente ao canto superior direito
        posicoes.append(pos-obtem_dimensao(tab)[1]+1)
    
    if pos!=obtem_coluna(tab, pos)[-1] and pos!=obtem_linha(tab, pos)[0]:  #Adjacente ao canto inferior esquerdo
        posicoes.append(pos+obtem_dimensao(tab)[1]-1)

    if pos!=obtem_coluna(tab, pos)[-1] and pos!=obtem_linha(tab, pos)[-1]:  #Adjacente ao canto inferior direito
        posicoes.append(pos+obtem_dimensao(tab)[1]+1)

    posicoes.sort()  #Ordenar as posições adjacentes
    posicoesTup=()  #Tuplo de saída

    for i in posicoes:
        posicoesTup+=(i,)

    return posicoesTup

def obtem_coordenadas(tab, pos):
    """
    [Função auxiliar] Recebe um tabuleiro e uma posição e retorna um tuplo com as coordenadas dessa posição.
    
    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição a ser analisada

    Ouptut:
        (xCoord, yCoord) (tuple):
            xCoord (int): número da linha
            yCoord (int): número da coluna
    """
    #Foi criado um sistema de coordenadas para descobrir as coordenadas de uma posição no tabuleiro
    xCount=0
    yCount=0
    for x in obtem_coluna(tab, pos):
        xCount+=1
        #O xCount é a posição do número lido da linha onde está a pos. orginal
        if x==pos:
            xCoord=xCount
    for y in obtem_linha(tab, pos):
        yCount+=1
        if y==pos:
            yCoord=yCount
    if xCoord<=obtem_dimensao(tab)[0] and yCoord<=obtem_dimensao(tab)[1]:
        return (xCoord, yCoord)
    else:
        raise ValueError("obtem_coordenadas: algo está mal na função")
        

def ordena_posicoes_tabuleiro(tab, tup):
    """
    Recebe um tabuleiro e uma posição e retorna um tuplo com as posições em ordem ascendente de posição à posição central do tabuleiro.
    As posições com igual distância estão ordenadas por nº de posição
    
    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        tup (tuple): Tuplo com as posições a serem ordenadas

    Ouptut:
        output (tuple): Tuplo com as posições ordenadas
    """

    if not (eh_tabuleiro(tab) and isinstance(tup, tuple)):
        raise ValueError("ordena_posicoes_tabuleiro: argumentos invalidos")
    for a in tup:
        #Verificar se todos os elementos do tuplo são posições válidas
        if not eh_posicao(a):
            raise ValueError("ordena_posicoes_tabuleiro: argumentos invalidos")
        if not eh_posicao_valida(tab, a):
            raise ValueError("ordena_posicoes_tabuleiro: argumentos invalidos")
    
    posCentral = (obtem_dimensao(tab)[0]//2)*obtem_dimensao(tab)[1]+(obtem_dimensao(tab)[1]//2)+1
    coordCentral = obtem_coordenadas(tab, posCentral) #Coordenadas da pos. central
    output=()

    for i in range(max(obtem_dimensao(tab)[0], obtem_dimensao(tab)[1])+1):
        #i corresponde à distância que vai a ser verificada
        #i vai ter todos os valores desde 0 até ao lado maior do tabuleiro, ou seja, o maior valor da distância de Chebyshev
        #fazer isto vai já deixar as posições ordenadas por distância, depois por posição
        for i2 in tup:
            # i2 vai ser todas as posições do tuplo
            iCoord=obtem_coordenadas(tab, i2) #Coordenadas da posição atual
            if max(abs(coordCentral[0]-iCoord[0]), abs(coordCentral[1]-iCoord[1]))==i:
                # a distâcia da posição lida ao centro (distância de Chebyshev) correspode à posição i
                output+=(i2, )
    
    return output

def marca_posicao(tab, pos, jog):
    """
    Recebe um tabuleiro, uma posição livre e um número de jogador e retorna o novo tabuleiro com uma peça desse jogador na posição escolhida.
    
    Parâmetros:
        tab (tuple): Tabuleiro a ser atualizado
        pos (int): Posição a ser atualizada
        jog (int): Número de jogador

    Ouptut:
        newTab (tuple): Novo tabuleiro (com a estrutura do inicial) com a posição desejada alterada
    """
    if not (eh_tabuleiro(tab) and isinstance(jog, int) and jog in (1, -1)):
        #Verificar se é tabuleiro, se é posição livre, se o nº jogador é inteiro e se é 1 ou -1
        raise ValueError("marca_posicao: argumentos invalidos")
    if not eh_posicao(pos):
        raise ValueError("marca_posicao: argumentos invalidos")
    if not eh_posicao_valida(tab, pos):
        raise ValueError("marca_posicao: argumentos invalidos")
    if not eh_posicao_livre(tab, pos):
        raise ValueError("marca_posicao: argumentos invalidos")
    
    newTab=() #Novo tabuleiro com a alteração
    line=()
    position=0
    for i in tab:
        line=()
        for i2 in i:
            position+=1
            if position==pos:
                line+=(jog,)
            else:
                line+=(i2, )
        newTab+=(line, )

    return newTab

def verifica_k_linhas_seq(elem, tab, pos, k):
    """Função auxiliar para a função verifica_k_linhas"""
    elemSeq=[] #Lista para guardar a sequência detetada temporariamente
    for i in elem:
        if len(elemSeq)>=k and (pos in elemSeq):
            #Já temos uma sequência que cumpre os requisitos, já nem é preciso correr mais a função
            return True
        elif len(elemSeq)==0:
            #A lista começa vazia, por isso temos de adicionar o primeiro elemento da lista e começar a avaliação para o segundo
            elemSeq.append(i)
        elif obtem_valor(tab, i)==obtem_valor(tab,elemSeq[-1]):
            #Estamos perante uma sequência, ou seja, o valor atualmente lido é igual ao anterior
            elemSeq.append(i)
        else:
            #O valor não é igual, ou seja, já não existe sequência
            elemSeq.clear()
            elemSeq.append(i) #Volta a adicionar o último valor para a próxima verificação funcionar
    
    if len(elemSeq)>=k and (pos in elemSeq):
        #Se houver sequência mas acabar o for loop, deve checar aqui se é sequência
        return True

    return False #Não encontrou nenhuma coluna/linha/diagonal

def verifica_k_linhas(tab, pos, jog, k):
    """
    Recebe um tabuleiro, uma posição, um número de jogador e um valor de k e retorna TRUE se houver alguma linha/coluna/diagonal no tabuleiro pertencente ao jogador e com o tamanho de k ou mais.
    
    Verifica a validade dos argumentos com as funções eh_tabuleiro, eh_posicao_valida e se o jogador e o k são válidos e gera uma exceção ValueError se os argumentos não o forem.

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        pos (int): Posição que deve pertencer à linha/coluna/diagonal
        jog (int): Número de jogador
        k (int): comprimento mínimo da linha/coluna/diagonal

    Ouptut:
        boolean: TRUE se houver alguma sequência, FALSE se não houver
    """
    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError("verifica_k_linhas: argumentos invalidos")
    if not (eh_posicao_valida(tab, pos) and jog in (1, -1) and k>0):
        raise ValueError("verifica_k_linhas: argumentos invalidos")
    if obtem_valor(tab, pos)!=jog:
        #A posição referida não pertence ao jogador referido
        return False
    
    if verifica_k_linhas_seq(obtem_coluna(tab, pos), tab, pos, k)==True:
        return True
    elif verifica_k_linhas_seq(obtem_linha(tab, pos), tab, pos, k)==True:
        return True
    elif verifica_k_linhas_seq(obtem_diagonais(tab, pos)[0], tab, pos, k)==True:
        return True
    elif verifica_k_linhas_seq(obtem_diagonais(tab, pos)[1], tab, pos, k)==True:
        return True
    else:
        return False
    

def eh_fim_jogo(tab, k):
    """
    Recebe um tabuleiro e um valor de k e verifica se o jogo terminou (alguém fez uma sequência, senão o tabuleiro está todo preenchido e acabou num empate) ou não.
    
    Verifica a validade dos argumentos com a função eh_tabuleiro e se o k é válido e gera uma exceção ValueError se não o forem.

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        k (int): comprimento mínimo da linha/coluna/diagonal

    Ouptut:
        boolean: TRUE se o jogo já acabou, FALSE se não acabou
    """
    if not (eh_tabuleiro(tab) and k>0):
        raise ValueError("eh_fim_jogo: argumentos invalidos")
    elif k>max(obtem_dimensao(tab)[0], obtem_dimensao(tab)[1], len(obtem_diagonais(tab, 1)[0])):
        return False #O k não pode ser maior que uma das dimensões do tabuleiro, mas não é nessessariamente um argumeto invalido
    for i in range(1, (obtem_dimensao(tab)[0]*obtem_dimensao(tab)[1])+1):
            if verifica_k_linhas(tab, i, 1, k) or verifica_k_linhas(tab, i, -1, k):
                #O jogo terminou porque alguém ganhou
                return True
    #Se não retornou True, é porque ninguém ganhou
    for i in tab:
            for i2 in i:
            #Agora vai verificar se de facto não existem posições disponiveis no tabuleiro
                if i2==0:
                #Ainda existe pelo menos uma posição livre, por isso o jogo não acabou
                    return False
    #Se ninguém ganhou mas não há espaços vazios, então o jogo acabou num empate
    return True

def escolhe_posicao_manual(tab):
    """
    Recebe um tabuleiro e devolve uma posição manualmente inserida pelo jogador
    
    Verifica se a posição inserida é válida para o tabuleiro de entrada, caso a posição inserida seja inválida, a função perguntará infinitamente até ser inserida uma posição válida para o tabuleiro dado.

    Parâmetros:
        tab (tuple): Tabuleiro de verificação

    Interações:
        x (int): Posição inserida pelo jogador. Tem de ser um inteiro e ser uma posição válida e livre

    Ouptut:
        x (int): Se a posição for válida para o tabuleiro dado, retorna esse valor.
    """
    if not eh_tabuleiro(tab):
        raise ValueError('escolhe_posicao_manual: argumento invalido')
    
    breakTrigger=False
    while not breakTrigger:
        x = input("Turno do jogador. Escolha uma posicao livre: ") #X é uma string mesmo que seja escrito um número
        if x.isdigit():
            #Se x é um número, converter para int
            x = int(x)
        else:
            #Se a entrada for inválida, tentar novamente
            continue
        if eh_posicao(x):        
            if eh_posicao_valida(tab, x):  #Verificar se o número é uma posição válida
                if eh_posicao_livre(tab, x):  #Verificar se o número é uma posição livre
                    breakTrigger=True
    return x

def escolhe_posicao_auto(tab, jog, k, lvl):
    """
    Recebe um tabuleiro , o tipo de peças, um valor de k e a dificuldade (facil/medio/dificil)
    
    Verifica se os inputs são válidos com as funções eh_tabuleiro e eh_fim_jogo

    Parâmetros:
        tab (tuple): Tabuleiro a ser analisado
        jog (int): O tipo de peças (brancas=1, pretas=-1) que pertence ao computador
        k (int): O valor de k do jogo, isto é, o compritmento-alvo da sequência para ganhar
        lvl (string): A esratégia do algoritmo do computador. Tem de ser 'facil', 'normal' ou 'dificil'

    Ouptut:
        j (int): Posição escolhida pelo algoritmo usando a estratégia pretendida
    """
    if not (eh_tabuleiro(tab) and jog in (1, -1) and k>0 and k<=max(obtem_dimensao(tab)[0], obtem_dimensao(tab)[1], len(obtem_diagonais(tab, 1)[0])) and lvl in ('facil', 'normal', 'dificil')) or eh_fim_jogo(tab, k):
        raise ValueError("escolhe_posicao_auto: argumentos invalidos")
    
    if lvl=="facil":  #Estratégia fácil
        for i in ordena_posicoes_tabuleiro(tab, tuple(range(1, (obtem_dimensao(tab)[0]*obtem_dimensao(tab)[1])+1))):
            #i corresponde ao valor do tuplo que contém as posições ordenadas de distância ao centro
            #o mais perto do centro é a prioridade
            for i2 in obtem_posicoes_jogador(tab, jog):
                #i2 corresponde ao valor do tuplo que contém todas as posições do jogador selecionado
                if (i in obtem_posicoes_adjacentes(tab, i2)) and eh_posicao_livre(tab, i):
                    #a posição mais perto do centro tem de ser adjacente a uma das peças do jogador selecionado
                    #e tem de estar livre
                    return i
                
        #se o programa está aqui é porque não arranjou nenhuma posição adjacente para jogar
        #ou seja, tem de jogar na posição livre mais perto do centro
        for j in ordena_posicoes_tabuleiro(tab, tuple(range(1, (obtem_dimensao(tab)[0]*obtem_dimensao(tab)[1])+1))):
            if eh_posicao_livre(tab, j):
                return j

def jogo_mnk(cfg_tab, jog, lvl):
    """
    A função pincipal do jogo. É esta que coordena a logística do jogo (turnos, representação do tabuleiro, verificação de vitória) ao chamar as funçãoes anteriormente definidas.
    
    Recebe os parâmetros para formar o tabuleiro (comprimento,largura,k), a cor das peças para o jogador e a estratégia a utilizar pelo computador.

    Parâmetros:
        cfg_tab (tuple): Configurações de criação do tabuleiro (linhas, colunas, k)
        jog (int): O tipo de peças (brancas=1, pretas=-1) que pertence ao jogador
        lvl (string): A esratégia do algoritmo do computador. Tem de ser 'facil', 'normal' ou 'dificil'

    Ouptut:
        (int/string): 1 ou -1 conforme quem ganhou, ou 'EMPATE' se ninguém ganhou.
        """
    if not (isinstance(cfg_tab, tuple) and jog in (1, -1) and lvl in ('facil', 'normal', 'dificil')):
        raise ValueError("jogo_mnk: argumentos invalidos")
    if not (len(cfg_tab)==3 and 2<=cfg_tab[0]<=100 and 2<=cfg_tab[1]<=100):  #Como o cfg_tab é um tuplo, já podemos fazer verificações exclusivas a tuplos
        raise ValueError("jogo_mnk: argumentos invalidos")
    
    #Construir o tabuleiro
    tab=()
    line=()
    for i in range(cfg_tab[0]):  #linhas - nº de subtuplos
        for i2 in range(cfg_tab[1]): #Colunas - elementos dos subtuplos
            line+=(0,)
        tab+=(line,)
        line=() #Limpar a linha atual pois já foi adicionada
    
    #Como já temos o tabuleiro, já podemos fazer verificações para o k
    if cfg_tab[2]>max(obtem_dimensao(tab)[0], obtem_dimensao(tab)[1], len(obtem_diagonais(tab, 1)[0])):
        raise ValueError("jogo_mnk: argumentos invalidos")
    
    playerToPlay=jog #Jogador que vai jogar a seguir
    print("Bem-vindo ao JOGO MNK.")
    if jog==1:
        print("O jogador joga com 'X'.")
        playerToPlay="me"
        myPieces=1
        pcPieces=-1
    elif jog==-1:
        print("O jogador joga com 'O'.")
        playerToPlay="pc"
        myPieces=-1
        pcPieces=1
    print(tabuleiro_para_str(tab))
    while not eh_fim_jogo(tab, cfg_tab[2]):
        if playerToPlay=="me":
            posToAdd=escolhe_posicao_manual(tab)
            tab=marca_posicao(tab, posToAdd, myPieces)
            playerToPlay="pc" #Eu já joguei, agora o próximo é o computador
            #Verificar se o jogador ganhou com esta jogada
            print(tabuleiro_para_str(tab))
            if verifica_k_linhas(tab,posToAdd, myPieces, cfg_tab[2]): #Se for true, eu ganhei
                print("VITORIA")
                return myPieces
        elif playerToPlay=="pc":
            posToAdd=escolhe_posicao_auto(tab, pcPieces, cfg_tab[2], lvl)
            tab=marca_posicao(tab, posToAdd, pcPieces)
            print(f"Turno do computador ({lvl}):")
            playerToPlay="me" #O computador jogou, por isso sou eu
            print(tabuleiro_para_str(tab))
            #Verificar se o pc ganhou com esta jogada
            if verifica_k_linhas(tab, posToAdd, pcPieces, cfg_tab[2]): #Se for true, o computador ganhou
                print("DERROTA")
                return pcPieces
    
    #Se o programa chegou aqui e não deu nenhum return, é porque o jogo acabou, mas ninguém ganhou
    #Ou seja, é um empate
    return "EMPATE"