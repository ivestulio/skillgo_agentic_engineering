"""tools/ - as ferramentas: o que o MODELO pode decidir chamar.

O QUE E
-------
Ferramenta e uma funcao que voce entrega ao modelo. Ele decide SE usa, QUANDO e com
quais argumentos. Essa e a diferenca entre um fluxo fixo e um agente.

Compare:

    FIXO:       buscar -> classificar          (sempre busca, mesmo sem precisar)
    FERRAMENTA: classificar <-> buscar         (busca se o modelo julgar necessario)

O QUE VAI AQUI
--------------
As funcoes decoradas com `@tool` e a logica que elas encapsulam. Uma ferramenta por
capacidade: buscar na base, consultar uma API, calcular algo.

COMO CRIAR
----------
    from langchain_core.tools import tool

    @tool
    def buscar_base(consulta: str, area: Literal["politica", "tecnica"]) -> str:
        '''Consulta a base de conhecimento interna.

        Use sempre que precisar de uma regra ou numero que nao esteja no pedido.
        E o UNICO jeito de obter fontes citaveis.

        A base contem: politica de engenharia (severidade, prioridade, esforco);
        arquitetura dos servicos; padroes de teste; historico de incidentes.

        Args:
            consulta: o que voce quer saber, em linguagem natural. Seja especifico -
                a busca e semantica, entao "regra de unicidade de cupom no recalculo"
                recupera melhor que "cupom".
            area: "politica" busca regras; "tecnica" busca arquitetura e testes.

        Returns:
            Os trechos, cada um com o ID entre colchetes. Cite esses IDs em `fontes`.
        '''
        return formatar(buscar(consulta, area))

A DOCSTRING E O PRODUTO
-----------------------
Ela nao e comentario: e o texto que o modelo LE para decidir chamar a ferramenta.
Uma docstring vaga produz um agente que nunca busca, ou que busca sempre. Diga:
o que a ferramenta faz, QUANDO usar, o que existe la dentro, e como formular o
argumento.

LIGANDO AO MODELO
-----------------
    modelo().bind_tools([buscar_base])

Truque util: ligar TAMBEM o contrato de saida como ferramenta e forcar uma escolha.

    modelo().bind_tools([buscar_base, Classificacao], tool_choice="any")

Agora o modelo e obrigado a chamar uma das duas: ou busca mais, ou entrega a
resposta final. O loop termina quando ele escolhe responder.

ARMADILHAS
----------
- TODA tool_call precisa de uma ToolMessage respondendo ao seu tool_call_id,
  INCLUSIVE a que entrega a resposta final. Se sobrar uma em aberto, a proxima
  chamada a API devolve 400: "An assistant message with 'tool_calls' must be
  followed by tool messages". O sintoma so aparece quando o historico e reenviado -
  num replanejamento, por exemplo - o que torna o bug facil de nao ver em teste.

- Dar liberdade de nao buscar significa aceitar resposta sem fonte. Decida o que
  fazer: permitir e SINALIZAR, ou exigir. As duas sao defensaveis; escolher em
  silencio nao e.

- Se a ferramenta acumula resultados no estado ao longo de um loop, cuide da
  duplicata. Junte com dedupe por id.
"""
