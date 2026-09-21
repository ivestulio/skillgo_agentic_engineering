"""graph.py - o grafo: onde tudo e ligado.

O QUE E
-------
O ponto de entrada do agente. Aqui voce declara QUAIS sao os passos (nos) e COMO
eles se ligam (arestas). Nada de logica de negocio: este arquivo so monta.

Se alguem quiser entender o agente em 30 segundos, e este arquivo que abre.

O QUE VAI AQUI
--------------
1. Criar o StateGraph com o schema de estado.
2. Registrar cada no com add_node.
3. Ligar com add_edge (fixo) ou add_conditional_edges (decide em tempo de execucao).
4. Compilar e expor numa variavel de modulo - e ela que o langgraph.json aponta.

COMO CRIAR
----------
    from langgraph.graph import END, START, StateGraph

    def build_graph() -> StateGraph:
        grafo = StateGraph(MeuEstado, input_schema=MinhaEntrada)

        grafo.add_node("primeiro", primeiro_no)
        grafo.add_node("segundo", segundo_no)

        grafo.add_edge(START, "primeiro")
        grafo.add_conditional_edges("primeiro", meu_roteador, ["segundo", "encerrar"])
        grafo.add_edge("segundo", END)

        return grafo

    graph = build_graph().compile(name="meu-agente")

Separar `build_graph()` de `graph` nao e firula: o servidor do LangGraph precisa do
objeto compilado, mas testes e scripts precisam compilar com um checkpointer proprio.
Com as duas coisas, os dois casos funcionam sem gambiarra.

ARMADILHAS
----------
- NAO passe checkpointer para .compile() aqui. O servidor do LangGraph injeta a
  persistencia dele, e passar uma faz o `langgraph dev` FALHAR ao carregar o grafo.
  Fora do servidor use: build_graph().compile(checkpointer=InMemorySaver()).

- Use imports ABSOLUTOS. O servidor carrega este arquivo como modulo sem pacote pai,
  entao `from .nodes import x` quebra. Escreva `from src.nodes import x`.

- Nos devem ser funcoes SINCRONAS (`def`, nao `async def`) se por dentro usam
  clientes sincronos. O LangGraph roda `def` numa thread, fora do event loop; um
  `async def` com I/O bloqueante dentro trava o servidor.
"""
