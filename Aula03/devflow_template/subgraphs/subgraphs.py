"""subgraphs/ - subgrafos: um grafo inteiro usado como se fosse um no.

O QUE E
-------
Um StateGraph compilado e registrado como no de outro grafo. Por fora e uma caixa
so; por dentro tem seus proprios nos e arestas.

    grafo.add_node("raciocinio", construir_raciocinio())

QUANDO USAR
-----------
- O grafo principal ficou grande e um grupo de nos forma uma unidade conceitual.
- Voce quer que o desenho de cima conte a historia, e o detalhe fique um nivel abaixo.
- O mesmo conjunto de passos se repete em lugares diferentes.

Se o grafo tem 5 nos, NAO use subgrafo. A indirecao custa mais do que ajuda.

COMO CRIAR
----------
    def construir_raciocinio():
        grafo = StateGraph(MeuEstado)          # mesmo estado do grafo pai: mais simples
        grafo.add_node("classificar", classificar)
        grafo.add_node("buscar", buscar)
        grafo.add_conditional_edges(START, entrada, ["classificar", "planejar"])
        grafo.add_conditional_edges("classificar", decidir, ["buscar", "planejar"])
        grafo.add_edge("buscar", "classificar")
        grafo.add_edge("planejar", END)
        return grafo.compile()                 # COMPILADO antes de virar no

ENTRADA CONDICIONAL: o truque que resolve o retorno
---------------------------------------------------
Subgrafo so e entrado pelo START. Se um ciclo do grafo pai precisa voltar para um no
que esta NO MEIO do subgrafo, a solucao e rotear a partir do START:

    grafo.add_conditional_edges(
        START,
        lambda e: "planejar" if e.classificacao else "classificar",
        ["classificar", "planejar"],
    )

Assim a primeira passada entra pelo comeco, e a reentrada pula direto para a etapa
certa - preservando o que ja foi feito.

A condicao deve olhar um campo que DISTINGUE os dois casos. Se o no de revisao anula
`plano` para forcar o replanejamento, `plano is None` nao serve: use `classificacao`,
que so existe depois da primeira passada.

ARMADILHAS
----------
- Subgrafo com estado proprio exige mapear campos entre pai e filho. Usar o MESMO
  estado nos dois evita isso inteiro. So separe se tiver motivo concreto.

- No Studio, o subgrafo aparece fechado. Clique nele para expandir - e la que o loop
  de ferramenta fica visivel.

- Cuidado com reducer que acumula quando o subgrafo e reentrado: `operator.add` vai
  concatenar de novo o que ja estava la.
"""
