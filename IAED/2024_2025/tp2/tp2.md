# Perguntas Teste Prático - IAED 2024/2025

- Deverá submeter a sua solução no Fenix.
- __Deverá submeter dentro do prazo a solução que tiver, mesmo que incompleta. Serão consideradas soluções parciais (não completamente funcionais) das perguntas.__

## Teste Prático - (11h00-11h50)

Responda às seguintes perguntas.

__1.__ Altere o comando __c__ de criação de um lote de vacinas. Se o comando __c__ for invocado com um nome de vacina que comece com uma letra minúscula (caracter entre *a* e *z*), então deve mostrar a mensagem de erro `vaccine name cannot begin with a lowercase letter` e o lote não é criado. Não é necessário indicar a mensagem em português.

__2.__ Altere o comando __r__. Se o comando for usado num lote sem inoculações, então o lote não é removido, mas fica sem doses disponíveis.

__3.__ Defina um novo comando __v__ para alterar a data de validade de um lote registado no sistema. O comando __v__ é sempre seguido pelo identificador do lote e a nova data, com o formato: `v <lote> <dia>-<mes>-<ano>`.
Se o lote não existir, deve indicar `<lote>: no such batch`. Se a nova data de validade for inválida ou anterior à data atual do sistema, então deve indicar `invalid date`.
Se não houver erro, então a data de validade do lote é alterada e na saída mostra o número de doses disponíveis no lote.
Não é necessário indicar as mensagens em português.
