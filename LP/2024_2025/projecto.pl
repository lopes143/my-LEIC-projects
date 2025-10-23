% lp24 - ist1113963 Rodrigo Lopes - projecto 
:- use_module(library(clpfd)). % para poder usar transpose/2
:- set_prolog_flag(answer_write_options,[max_depth(0)]). % ver listas completas
:- [puzzles]. % Ficheiro dado. A avaliação terá mais puzzles.
:- [codigoAuxiliar]. % Ficheiro dado. Não alterar.
% Atenção: nao deves copiar nunca os puzzles para o teu ficheiro de código
% Nao remover nem modificar as linhas anteriores. Obrigado.
% Segue-se o código
%%%%%%%%%%%%

/* visualiza(Lista)
O predicado visualiza verifica se 'Lista' é uma lista
 escreve, por linha, cada elemento da lista no ecrã.
*/
visualiza([H|T]):-
    %Processo iterativo para mostrar cada elemento da lista
    writeln(H),
    visualiza(T),!. %Iterar para o resto da lista
visualiza([]). %Condição de paragem - lista vazia

/* visualizaLinha(Lista)
O predicado visualizaLinha verifica se 'Lista' é uma lista e escreve cada elemento
 da lista no ecrã, aparecendo antes da linha em causa um ":" e um espaço.
*/
visualizaLinha(Lista):-
    %Processo iterativo onde engordamos o predicado e criamos um contador da linha atual
    visualizaLinha(Lista,1).
visualizaLinha([H|T],NumLinha):-
    write(NumLinha), %Escreve o contador atual
    write(": "),
    writeln(H), %E o elemento respetivo
    NewNumLinha is NumLinha+1, %A linha aumenta um valor para a próxima iteração
    visualizaLinha(T,NewNumLinha),!. %Iterar pro resto da lista
visualizaLinha([],_). %A lista vazia é a nossa condição de paragem

/* insereObjecto((L,C), Tabuleiro, Obj)
O predicado insere o objeto 'Obj' nas coordenadas '(L,C)' no tabuleiro 'Tab'.
De notar que o predicado nunca falha, mesmo se as coordenadas não existirem no tabuleiro
 ou já existe algum objeto nessas coordenadas (nesses casos não faz nada).
*/
insereObjecto((L,C),Tab,Obj):-
    nth1(L,Tab,Line), %Procurar a linha correspondente às coordenadas
    nth1(C,Line,Elem), %Procurar o elemento correspondente às coordenadas
    Elem\==p,Elem\==e,Elem=Obj,!; 
    %Tenta unificar o elemento do tabuleiro com o objecto que queremos se não for um ponto ou estrela.
    true. %Se não for possível unificar, devolve verdadeiro de qualquer forma, sem fazer nada

/* insereVariosObjectos(ListaCoords, Tabuleiro, ListaObjs)
O predicado insere os objectos da 'ListaObjs' no tabuleiro 'Tab', nas respetivas coordenadas da lista 'ListaCoords'.
É semelhante ao insereObjecto, mas para múltiplas coordenadas e objectos.
De notar que as listas de coordenadas e objetos são percorridas ao mesmo tempo
 e o predicado falha se ambas não tiverem o mesmo tamanho.
*/
insereVariosObjectos([H1|T1],Tab,[H2|T2]):-
    %Processo iterativo de inserção de cada objecto no seu par de coordenadas
    %[H1|T1]: ListaCoords
    %[H2|T2]: ListaObjs
    insereObjecto(H1,Tab,H2), 
    insereVariosObjectos(T1,Tab,T2),!. %Itera para o resto das coordenadas e objetos
insereVariosObjectos([],_,[]). %Condição de paragem: listas vazias
    %Se ambas as listas não tiverem o mesmo tamanho (uma vai acabar primeiro que a outra)
    % o prolog não vai ter nenhum predicado que explique uma lista ter acabado e outra não,
    % logo vai falhar.

/* inserePontosVolta(Tabuleiro, (L,C))
O predicado insere pontos à volta do par de coordenadas dado, isto é, terá pontos
 em cima, baixo, esquerda, direita e as 4 diagonais.
*/
inserePontosVolta(Tab, (L,C)):-
    /* P1  P2  P3
       P4   X  P5
       P6  P7  P8 */
    LU is L-1, CL is C-1, %L_up , C_left
    LD is L+1, CR is C+1, %L_down, C_right

    %Dividios as coordenadas em 2 partes pra não passar o limite horizontal de caracteres
    %                       P1      P2      P3     P4
    insereVariosObjectos([(LU,CL),(LU,C),(LU,CR),(L,CL)],Tab,[p,p,p,p]),
    %                       P5      P6     P7      P8
    insereVariosObjectos([(L,CR),(LD,CL),(LD,C),(LD,CR)],Tab,[p,p,p,p]),!.

/* inserePontos(Tabuleiro, ListaCoord)
O predicado insere pontos nas coordenadas da lista 'ListaCoord'.
Basicamente aplica iterativamente o insereObjecto, ao inserir um ponto em cada coordenada.
De notar que o objecto nas coordenadas atuais não for uma var. livre, ou já for um ponto, ignora e continua.
*/
inserePontos(Tab,[H|T]):-
    %[H|T]: ListaCoord
    %Função recursiva que usa o predicado de adicionar um valor à cordenada - neste caso um ponto
    insereObjecto(H,Tab,p),
    inserePontos(Tab,T),!.
inserePontos(_,[]). %Condição de paragem: lista vazia

/* objectosEmCoordenadas(ListaCoords, Tabuleiro, ListaObjs)
O predicado avalia se os objetos da 'ListaObjs' são os das respetivas coordenadas da 'ListaCoords'
 no tabuleiro 'Tab'.
Se 'ListaObjs' for var. livre (polimodalidade), procura os elementos das coordenadas no tabuleiro
 e põe-os la 'ListaObjs'.
Se alguma coordenada não existir no tabuleiro, o predicado falha.
*/
objectosEmCoordenadas([H1|T1],Tab,[H2|T2]):-
    H1=(X,Y), %Estrair os valores da linha/coluna do par de coordenadas atual
    nth1(X,Tab,Line), %Obter linha
    nth1(Y,Line,Elem), %Obter elemento da linha
    Elem=H2, %O elemento da linha tem que ser igual ao elemento da lista de objectos
    objectosEmCoordenadas(T1,Tab,T2),!; %Se sim, aplicamos a iteração para o resto
    false. %Se não for verdadeiro, deve retornar false
objectosEmCoordenadas([],_,[]). %Condição de paragem: Listas vazias
    
/* coordObjectos(Objecto, Tabuleiro, ListaCoords, ListaCoordObjs, NumObjectos)
O predicado recebe uma lista de coordenadas, um tabuleiro e um tipo de objecto e procura nessas coordenadas
 as que correspondem ao objeto-alvo. ListaCoordObjs será a lista das coordenadas que correspondem ao objeto
 e NumObjs um número da quantidade de objetos que encontrou na lista de coordenadas.
*/
coordObjectos(Obj,Tab,ListaCoords,ListaCoordObjs,NumObjs):-
    sort(ListaCoords, ListaCoordsSorted),
    coordObjectos(Obj,Tab,ListaCoordsSorted,ListaCoordObjs,NumObjs,[],0).
    %Engordamos o predicado para resolver iterativamente
    % [] é o Acc - Acumulador da lista das coordenadas (ListaCoordObjs)
    % 0 é o Acc2 - Acumulador do número de elementos (NumObjs)
coordObjectos(Obj,Tab,[H1|T1],ListaCoordObjs,NumObjs,Acc,Acc2):-
    objectosEmCoordenadas([H1],Tab,[A]),
    (var(A),var(Obj);A==Obj),
    %Se tivermos à procura de var. livres, o objecto encontrado também tem de o ser
    %Caso contrário, o objecto encontrado tem de ser igual ao que queremos
    append(Acc,[H1],NewAcc),
    NewAcc2 is Acc2+1,!,
    coordObjectos(Obj,Tab,T1,ListaCoordObjs,NumObjs,NewAcc,NewAcc2),!; %Continua a iteração pro resto da lista
    %Se não for sucedido (o objecto nas coordenadas n é o que queremos), então passa para o próximo
    coordObjectos(Obj,Tab,T1,ListaCoordObjs,NumObjs,Acc,Acc2),!. 
coordObjectos(_,_,[],ListaCoords,NumObjs,Lista,Contador):-
    %Condição de paragem - Lista Vazia (é neste predicado que se trata da polimodalidade)
    %Se o NumObjs for uma variável a definir, então unificamos
    % senão verificamos se o que o q foi processado é igual ao input no predicado.
    %p. e.: se eu aplico o predicato com uma seq. de coords de tamanho 3 (de 3 var. livres), mas o contador é 2,
    % o predicado deve falhar, pq nos deu 3 coords, mas tou a verificar para 2
    %A mesma coisa para a lista de coordenadas - ListaCoords
    (var(NumObjs),NumObjs=Contador;NumObjs==Contador),
    (var(ListaCoords),ListaCoords=Lista;ListaCoords==Lista).

/* coordenadasVars(Tabuleiro, ListaVars)
O predicado lê o tabuleiro e ListaVars deve ser uma lista com todas as coordenadas
 do tabuleiro com variáveis livres.
*/
coordenadasVars(Tab,ListaVars):-
    length(Tab, Len), 
    coordLinhas(Len,A), 
    %Para gerarmos uma lista com todas as coordenadas ordenadas por linhas, temos de calcular primeiro
    % o comprimento do lado do tabuleiro, pois o 'coordLinhas' só aceita esse número.
    flatten(A,A2), %A é uma lista de sublistas por isso colapsamos tudo numa só, sem sublistas
    coordObjectos(_,Tab,A2,LCO,_), %Obtemos todas as coordenadas do tabuleiro que são livres
    (var(ListaVars),LCO=ListaVars;LCO==ListaVars),!.
    %Se ListaVars for uma variável livre/a definir (polimodalidade), queremos descobrir
    % as coordenadas das variáveis, logo unificamos o q calculámos com o argumento.
    %Caso ListaVars esteja definido, é para verificar se está certo, logo usamos o operador de igualdade.

/* fechaListaCoordenadas(Tabuleiro, ListaCoord)
O predicado avalia o tabuleiro para 3 estratégias básicas, onde é possível despachar alguns casos
 e simplificar o jogo. Aplica essas estratégias a uma lista de coordenadas dada.
As hipóteses são ordenadas, por isso se uma se aplicar, já não aplica outra.
No caso de nenhuma se puder aplicar, retorna true à mesma e o tabuleiro mantém-se inalterado.
*/
fechaListaCoordenadas(Tab,ListaCoord):-
    %h1
    (coordObjectos(e,Tab,ListaCoord,_,2), 
    %O predicado só dá verdadeiro se houverem exatamente 2 estrelas na lista de coordenadas,
    % e nesse caso obtemos tbm as coordenadas das estrelas
    inserePontos(Tab,ListaCoord), %Adicionamos os restos dos pontos
    !);
    %h2
    (coordObjectos(e,Tab,ListaCoord,_,1), %Existe uma única estrela nas coordenadas especificadas
    coordObjectos(_,Tab,ListaCoord,LCO,1), %E um único espaço vazio
    LCO=[A], %O LCO é uma lista com 1 elemento, por isso temos
    % de extrair esse mesmo elemento sem ser em formato de lista
    insereObjecto(A,Tab,e),
    inserePontosVolta(Tab,A),
    !);
    %h3
    (coordObjectos(e,Tab,ListaCoord,_,0), %Não existe nenhuma estrela
    coordObjectos(_,Tab,ListaCoord,EspLivres,2), %Existem exatamente 2 espaços livres
    insereVariosObjectos(EspLivres,Tab,[e,e]), %Insere 2 estrelas nesses espaços livres
    EspLivres=[A,B], %Como são 2 coordenadas em formato de lista, separamo-las
    inserePontosVolta(Tab,A), %Inserimos pontos à volta de cada uma
    inserePontosVolta(Tab,B),
    !);
    true.

/* fecha(Tabuleiro, ListaListasCoord)
O predicado recebe um tabuleiro e uma lista de sublistas com coordenadas e 
 e aplica o predicado 'fechaListaCoordenadas' a cada sublista.
*/
fecha(Tab,[H|T]):-
    %Método iterativo para processamento das sublistas
    fechaListaCoordenadas(Tab,H),
    fecha(Tab,T),!.
fecha(_,[]). %Condição de paragem - lista vazia

/* sublista(Lista, Sublista, Comprimento)
Predicado auxiliar que cria sublistas de comprimento N da lista grande em que
 todos os elementos são variáveis.
Sublista tem o comprimento pretendido e a soma do q vier antes da lista
 e depois (msm sendo nada) tem de ser a lista grande
*/
sublistaDeVariaveis(L,SL,N,Tab):- 
    append([_,SL,_],L), %A soma dos elementos anteriores e sucessores são a lista-mãe.
    length(SL,N), %A sublista criada tem o comprimento desejado
    coordObjectos(_,Tab,SL,_,N). %A sublista é composta só por var. livres
    
/* encontraSequencia(Tabuleiro, N, ListaCoords, Seq)
Predicado que recebe um tabuleiro e uma lista de coordenadas ('ListaCoords') e procura uma
 sequência de tamanho N de variáveis livres seguidas.
De notar que se o programa encontrar uma sequência de var. livres maior que N, ou seja,
 existem várias soluções, o predicado falha.
*/
encontraSequencia(Tab,N,ListaCoords,Seq):-
    length(ListaCoords, Na),Na>=N,
    %Obtemos o comprimento da lista de coordenadas. Para se possível calcular uma sequência,
    % esse comprimento tem de ser maior ou igual à lista-sequência que queremos
    coordObjectos(_,Tab,ListaCoords,_,Nb), %Calcular o nº de var. livres na lista de coordenadas
    Nb=<N, %Não pode haver mais coordenadas
    findall(SublistasCoords,sublistaDeVariaveis(ListaCoords,SublistasCoords,N,Tab),TodasAsSolucoes),
    %Obtemos as várias sequências de comprimento N da lista de coordenadas.
    %Se existe uma sequência, terá de ser uma delas.
    %O predicado sublistaDeVariaveis filtra tbm se forem todos os elem. da sublista var. livres
    %No entanto, só pode existir 1 solução possível, pelo q o findall vai procurar todas as soluções encontradas
    length(TodasAsSolucoes,1),
    TodasAsSolucoes=[Sol],
    %Se existir só 1 solução, o nosso output é essa sequência,
    % mas como tá em formato de lista, temos de a extrair
    Seq=Sol. %Unificamos o resultado com o argumento de entrada

/* aplicaPadraoI(Tabuleiro, [(L1,C1), (L2,C2), (L3,C3)])
O predicado recebe uma lista de 3 coordenadas, verifica se é sequência e aplica o padrão I:
 coloca 2 estrelas em cada extremidade da sequência e 1 ponto no meio, metendo tbm pontos à volta
 de cada estrela.
*/
aplicaPadraoI(Tab,[A,B,C]):-
    encontraSequencia(Tab,3,[A,B,C],_), %Verificar se a lista de coordenadas é uma sequência possível
    insereVariosObjectos([A,C], Tab, [e,e]), %Inserir as estrelas na 1ª e última posição
    inserePontosVolta(Tab, A), %Inserir pontos à volta da 1ª posição
    inserePontosVolta(Tab, C), %E da última
    %Como o espaço do meio é adjacente a qualquer uma das estrelas, já tem o seu ponto
    !.

/* aplicaPadroes(Tabuleiro, ListaListaCoords)
O predicado recebe uma lista com sublistas de coordenadas e aplica iterativamente os padrões I e T,
 consoante sejam sequência de 3 ou 4, respetivamente, a cada sublista.
Se não encontrar estes 2 padrões na sublista, passa à frente.
*/
aplicaPadroes(Tab,[H|T]):- %Versão iterativa
    ((encontraSequencia(Tab,3,H,Seq),coordObjectos(e,Tab,H,_,0),aplicaPadraoI(Tab,Seq),!);
    %Encontrar seq. de 3 e aplicar o padrão I, se encontrado
    %Mas como o aplicaPadraoI acrescenta 2 estrelas, não pode haver nenhuma na linha/coluna/região,
    % mesmo que se encontram 3 espaços vazios
    (encontraSequencia(Tab,4,H,Seq2),aplicaPadraoT(Tab,Seq2),!);
    %Encontrar seq. de 4 e aplicar o padrão T, se encontrado
    true),!, %Caso nenhum dos de cima se verifique, devolve true à mesma, pra aplicar sempre o próximo predicado
    aplicaPadroes(Tab,T). %Aplica-se o mesmo predicado ao resto da lista
aplicaPadroes(_,[]). %Condição de paragem - lista de coordenadas vazia

/* resolve(Estruturas, Tabuleiro)
Predicado final que resolve o tabuleiro aplicando os padrões e fechando as coordenadas.
Em suma, este predicado tenta recursivamente resolver o tabuleiro aplicando os padrões e fechando onde é possível.
*/
resolve(Estr,Tab):-
    coordenadasVars(Tab,ListaVars),length(ListaVars, InitNumVarLivres),
    %Criamos um contador que corresponde ao número de variáveis livres que existem no tabuleiro.
    %E engordamos o predicado
    resolve(Estr,Tab,InitNumVarLivres).
resolve(Estr,Tab,NumVarLivres):-
    coordTodas(Estr, CoordTodas), %Obtemos todas as listas de linhas,colunas e regiões
    aplicaPadroes(Tab,CoordTodas),!, %Aplicamos os padrões a todas as linhas/colunas/regiões
    fecha(Tab,CoordTodas),!, %E fechamos as linhas/colunas/regiões, se possível
    coordenadasVars(Tab,ListaVars), %Após a resolução, verificamos o nº de variáveis livres
    length(ListaVars,NewNumVarLivres),
    (NewNumVarLivres<NumVarLivres,resolve(Estr,Tab,NewNumVarLivres),!;
    %Se o número diminuiu, a resolução teve sucesso, logo tentamos mais uma vez
    NewNumVarLivres==NumVarLivres,true).
    %Se o número se manteve igual, não é possível resolver mais, logo o 'resolve' acaba aqui.

%Fim do Projeto