# ===========================================================
# Identificacao do grupo: T32 [T?? para Tagus ou A?? para Alameda]
#
# Membros [istID, primeiro + ultimo nome]
# 1. ist1113963, Rodrigo Lopes
# 2. ist1114134, Bernardo Lima
# 3. ist1114489, Henrique Santos
$
# ===========================================================
# Descricao da ISA Implementada
# 
#
# == Formato das Instrucoes ==
#
#(bits:76543210)
# li:  00iiiiii
# addi:10iiiiii
# subi:01iiiiii
# abs: 110.....
# relu:111.....
# Os i's significam bits do imediato, e os pontos bits insignificantes
#
#
# Indicar a divisao dos campos da instrucao
# Justificar decisoes: Por que escolheram esse numero de bits? Ha instrucoes com formatos diferentes?
#
# Como o nº de instruções não cabe em 2 bits, algumas instruções terão de ser identificadas com 3 bits:
#  são as instruções que não usam imediato.
# A diferença entre as instruções que usam imediato e as que não usam é determinado pelos 2 primeiros bits
#  da instrução (bits 6 e 7): se ambos são 1, estamos perante uma instrução que não usa imediato. 
#  No circuito é usado uma porta AND para distinguir estes 2 tipos de instruções.
# Se os 2 bits iniciais são 1 (AND retorna 1), o bit de identificação da operação a realizar é o bit 5,
#  caso contrário é o bit 6.
# Como as instruções `li` e `addi`, internamente, realizam uma soma, têm o mesmo bit 6. A escolha se uma das 
#  parcelas é o valor atual do registo ou zero é definido por uma porta NOR entre os bits 6 e 7.
#
#
# == Sumario dos Estagios do Pipeline==
# Descrever brevemente cada estagio (componentes de hardware utilizados)
#
# Todos as instruções são realizadas em 1 ciclo apenas e não existem componentes dependentes de relógio a meio do processo.
# Logo, não exite pipeline.
#
#
# == Sinais de Controlo ==
# Explicar o que cada sinal ativa/desativa/seleciona e como sao gerados.
#
# Seletor da ALU: XY (2 bits)
#  X: bit7 AND bit6
#  Y: bit5 IF (bit7 AND bit6) ELSE bit6     (este valor é o output do MUX após ROM)
#
# MUX antes da ALU: 0x00 IF (bit7 NOR bit 6) ELSE Register Value
#
#
# ===========================================================
# Requisitos do enunciado que *nao* estao corretamente implementados:
# (indicar um por linha, ou responder "nenhum")
# - nenhum
#
#
# ===========================================================
# Top-3 das otimizacoes que a vossa solucao incorpora:
# (maximo 140 caracteres por cada otimizacao)
#
# 1. Tira partido dos comparadores de bits built-in no Logisim
#
# 2. Como todas as instruções são realizadas em 1 ciclo de relógio, o CPU
#    é bastante eficiente
#
# 3.
#
# ===========================================================
