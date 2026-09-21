"""schemas/ - contratos de dados: o formato de tudo que entra e sai.

O QUE E
-------
Classes pydantic que definem o formato de cada dado do agente. Sao o esqueleto do
projeto: validam a entrada ANTES de gastar um token, obrigam o LLM a responder num
formato conhecido, e entregam a cada etapa um objeto com forma garantida em vez de
texto solto.

Sem contrato, o LLM devolve uma string e o resto do codigo vira `if "alta" in texto`.
Com contrato, ele devolve um objeto e voce acessa `resultado.severidade`.

O QUE VAI AQUI
--------------
Um contrato por ponto do fluxo:
- ENTRADA: o que chega de fora (validado antes de qualquer processamento)
- SAIDA DO MODELO: um por etapa de raciocinio (usado em structured output)
- DECISAO HUMANA: o que a pessoa responde na pausa
- ENTREGAVEL: o resultado final

COMO CRIAR
----------
    from typing import List, Literal
    from pydantic import BaseModel, Field

    class Classificacao(BaseModel):
        '''Docstring: o LLM LE isto. Diga o que a classe representa.'''

        severidade: Literal["baixa", "media", "alta", "critica"] = Field(
            description="O LLM tambem le isto. Explique o criterio, nao repita o nome."
        )
        justificativa: str = Field(description="Em ate 5 frases, citando a regra usada")
        fontes: List[str] = Field(default_factory=list, description="IDs usados, ex.: doc#2")

`Literal` FECHA O VOCABULARIO. O modelo nao pode inventar "severidade: urgentissima",
e o roteador do grafo nunca recebe um valor que nao sabe tratar.

VALIDADOR, quando a regra nao cabe no tipo:

    @field_validator("criterios")
    @classmethod
    def _nao_vazios(cls, valor):
        limpos = [c.strip() for c in valor if c and c.strip()]
        if not limpos:
            raise ValueError("precisa de pelo menos um criterio")
        return limpos

METODO AUXILIAR, quando o contrato tem uma forma util para prompt:

    def criterios_numerados(self) -> List[str]:
        return [f"CA{i}: {c}" for i, c in enumerate(self.criterios, 1)]

ARMADILHAS
----------
- Docstrings e `description` NAO sao documentacao: viram o schema da ferramenta que
  o modelo recebe. Escrever "severidade: a severidade" desperdica a unica chance de
  explicar o criterio ao modelo.

- Contrato nao garante VERDADE, so FORMATO. O modelo pode devolver
  `severidade="critica"` com justificativa inventada. Conferir coerencia e trabalho
  do guardrail de saida.

- Pydantic v2: use `field_validator` + `@classmethod`, `model_validate`,
  `model_dump`. Os equivalentes v1 (`validator`, `parse_obj`, `.dict()`) mudaram.
"""
