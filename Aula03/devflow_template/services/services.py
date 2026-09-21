"""services/ - os clientes externos: tudo que fala com o mundo fora do processo.

O QUE E
-------
A camada que encapsula API externa: o provedor de LLM, o banco de vetores, um
webservice. Um arquivo por servico.

A regra: o resto do projeto NAO sabe qual provedor voce usa. Trocar de LLM ou de
banco de vetores deve mexer aqui e em mais lugar nenhum.

O QUE VAI AQUI
--------------
    llm.py      cria o cliente do modelo
    busca.py    cliente do banco de vetores / busca semantica

COMO CRIAR - cliente de LLM
---------------------------
    from functools import lru_cache
    from langchain_openai import AzureChatOpenAI
    from src.config import exigir, settings

    @lru_cache(maxsize=1)
    def modelo():
        exigir("endpoint", "api_key", "deployment")   # checa aqui, nao no import
        return AzureChatOpenAI(
            azure_endpoint=settings.endpoint,
            api_key=settings.api_key,
            api_version=settings.api_version,
            azure_deployment=settings.deployment,
            temperature=0,
        )

`lru_cache` cria o cliente uma vez e reaproveita. `temperature=0` porque triagem e
classificacao pedem resposta estavel, nao criativa.

COMO CRIAR - cliente de busca
-----------------------------
    class Busca:
        def __init__(self):
            exigir("search_endpoint", "search_key")
            self._cliente = SearchClient(...)

        def buscar(self, pergunta: str, k: int = 3, filtro=None) -> list[dict]:
            resultados = self._cliente.search(...)
            return [
                {"id": f"{doc['arquivo']}#{doc['secao']}",   # id citavel!
                 "titulo": doc["titulo"],
                 "texto": doc["conteudo"].strip(),
                 "score": round(doc["@search.score"], 4)}
                for doc in resultados
            ]

O ID CITAVEL e o detalhe que sustenta a rastreabilidade: se cada trecho volta com um
identificador estavel, da para conferir depois se o modelo citou algo que existe.

ARMADILHAS
----------
- Checar credencial no IMPORT quebra o carregamento do grafo. Cheque na criacao do
  cliente - assim o grafo monta sem credencial e caminhos que nao chamam o servico
  continuam funcionando.

- Cliente sincrono dentro de no `async def` bloqueia o event loop. Mantenha os nos
  sincronos, ou troque para o cliente assincrono do provedor.

- Se o indice de busca ja existe e e alimentado por fora, NAO recrie do codigo. Um
  servico que so consulta e mais simples e nao arrisca sobrescrever o que ja esta la.
"""
