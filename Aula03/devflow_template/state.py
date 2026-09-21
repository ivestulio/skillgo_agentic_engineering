"""state.py - o estado: a memoria que atravessa o grafo.

O QUE E
-------
Um objeto unico que todo no recebe e pode atualizar. E o unico jeito de um no
passar informacao para o proximo. Pense nele como a ficha que acompanha o processo
do inicio ao fim.

Cada no recebe o estado inteiro e devolve um DICIONARIO PARCIAL - so os campos que
mudou. O LangGraph faz a fusao.

O QUE VAI AQUI
--------------
- A classe de estado (TypedDict ou BaseModel do pydantic).
- Opcionalmente um schema de ENTRADA separado, menor, com so o que o usuario envia.
- Constantes de controle do fluxo (limites, tetos).

COMO CRIAR
----------
    from typing import Annotated, List, Optional
    from pydantic import BaseModel, Field

    class Entrada(BaseModel):
        pedido: Pedido          # so isto aparece no formulario do Studio

    class MeuEstado(BaseModel):
        pedido: Pedido          # obrigatorio: vem da entrada
        resultado: Optional[str] = None   # o resto SEMPRE com default

REDUCERS: como um campo e atualizado
------------------------------------
Sem anotacao, o comportamento e "o ultimo escreve vence":

    contador: int = 0           # no devolve {"contador": 5} -> vira 5

Com `Annotated[..., funcao]`, os valores sao COMBINADOS em vez de substituidos:

    historico: Annotated[List[str], operator.add]   # acumula
    mensagens: Annotated[List[AnyMessage], add_messages]  # acumula mensagens

ARMADILHAS
----------
- TODO campo que nao vem na entrada precisa de default. Um no que roda antes de o
  campo ser preenchido recebe o estado sem ele, e sem default isso vira erro de
  validacao dificil de rastrear.

- Reducer que acumula em loop DUPLICA. Se o grafo volta a um no ja executado (um
  ciclo de revisao, por exemplo), `operator.add` concatena de novo. Se o campo
  representa um conjunto, prefira sem reducer e faca a juncao com dedupe dentro do no.

- `add_messages` nao apaga. Devolver `[]` para um canal de mensagens NAO limpa o
  historico - adiciona nada. Para limpar de verdade seria preciso `RemoveMessage`.
  Quase sempre e mais simples continuar a conversa acrescentando uma mensagem nova.
"""
