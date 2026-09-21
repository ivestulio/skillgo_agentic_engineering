"""edges/ - as arestas: como o grafo decide para onde ir.

O QUE E
-------
Aresta e a ligacao entre nos. Duas formas:

- FIXA: `grafo.add_edge("a", "b")` - depois de a, sempre b.
- CONDICIONAL: uma funcao le o estado e devolve o NOME do proximo no.

A funcao condicional (o "roteador") e o que este diretorio guarda.

O QUE VAI AQUI
--------------
As funcoes de roteamento e os mapas de destino. Nada mais - roteador nao chama
modelo, nao busca, nao escreve no estado. So LE o estado e devolve uma string.

COMO CRIAR
----------
    def rotear(estado: MeuEstado) -> str:
        if estado.bloqueado:
            return "encerrar"
        return "continuar"

E no graph.py, declarando os destinos possiveis:

    grafo.add_conditional_edges("guardrail", rotear, ["continuar", "encerrar"])

A lista no final nao e decorativa: e ela que faz o Studio desenhar os dois caminhos.
Sem ela, o desenho fica incompleto.

MAPA EM VEZ DE IF
-----------------
Quando cada valor de um campo corresponde a um destino, um dicionario le melhor que
uma escada de ifs - e deixa a correspondencia explicita:

    PROXIMO_NO = {"aprovar": "finalizar", "revisar": "planejar", "rejeitar": "encerrar"}

    def rotear_decisao(estado) -> str:
        return PROXIMO_NO[estado.decisao.acao]

TETO DE CICLO
-------------
Se o grafo tem um loop que depende de resposta humana, ponha um limite:

    if estado.decisao.acao == "revisar" and estado.revisoes >= MAX_REVISOES:
        return "encerrar"

ARMADILHAS
----------
- NAO confie no limite de recursao do LangGraph para conter um loop humano. Ele e
  alto (mais de 10 mil) e e RECONCEDIDO POR INTEIRO a cada retomada. Um loop no
  ritmo de uma pessoa nunca o atinge. Se o seu ciclo precisa de teto, escreva o teto.

- Roteador nao escreve no estado. Quem incrementa contador e o NO, antes; o roteador
  so le. Tentar mudar estado no roteador nao funciona.

- Devolva sempre uma string que existe na lista de destinos. Um typo vira erro de
  execucao dificil de ler.
"""
