"""nodes/ - os nos: cada passo que o agente executa.

O QUE E
-------
Um no e uma FUNCAO. Recebe o estado, faz uma coisa, devolve um dicionario com os
campos que mudou. So isso.

    def meu_no(estado: MeuEstado) -> dict:
        resultado = faz_alguma_coisa(estado.entrada)
        return {"resultado": resultado}

O que NAO devolve, nao muda. Nao e preciso repassar o estado inteiro.

O QUE VAI AQUI
--------------
Um arquivo por no, ou por grupo de nos relacionados. Nomes que dizem a ACAO:
`guardrail.py`, `revisao_humana.py`, `finalizar.py`.

Um no tipicamente: le do estado, chama um servico (modelo, busca, API), valida o que
voltou, e devolve o resultado. A logica pesada mora em `services/` ou `tools/` - o no
orquestra, nao implementa.

COMO CRIAR
----------
    from src.observability import log
    from src.services.llm import modelo
    from src.state import MeuEstado

    def classificar(estado: MeuEstado) -> dict:
        '''Uma linha dizendo o que este no faz.'''
        resposta = modelo().with_structured_output(Classificacao).invoke(
            [SystemMessage(content=SISTEMA), HumanMessage(content=prompt(estado.pedido))]
        )
        log("classificar").info("pedido %s -> %s", estado.pedido.id, resposta.severidade)
        return {"classificacao": resposta}

NO DE PAUSA HUMANA (human-in-the-loop)
--------------------------------------
    from langgraph.types import interrupt

    def revisao(estado: MeuEstado) -> dict:
        resposta = interrupt({          # <- PRIMEIRA instrucao do no
            "acoes": ["aprovar", "rejeitar"],
            "proposta": estado.classificacao.model_dump(),
        })
        decisao = DecisaoHumana.model_validate(resposta)
        return {"decisao": decisao}

O dicionario passado para `interrupt()` e o que a pessoa VE. Mande o necessario para
decidir - a proposta, os alertas, de onde veio - e nada alem.

ARMADILHAS
----------
- `interrupt()` PRECISA ser a primeira instrucao do no. Na retomada, o LangGraph
  re-executa o no inteiro desde o topo. Qualquer coisa acima da pausa - uma chamada
  ao modelo, um log, um contador - roda duas vezes.

- Nunca envolva o `interrupt()` num try/except generico: ele funciona levantando uma
  excecao interna, e um except a engole e quebra a pausa.

- Valide o que volta da pausa, mas nao deixe a validacao TRAVAR a thread. Payload
  torto de revisor humano acontece; degrade para um caminho seguro e registre.

- Nos sincronos (`def`) rodam em thread, fora do event loop - e o certo para clientes
  sincronos. So use `async def` se tudo por dentro for assincrono de verdade.
"""
