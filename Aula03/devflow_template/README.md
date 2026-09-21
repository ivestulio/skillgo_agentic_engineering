# DevFlow — template

Esqueleto comentado do agente. Cada arquivo `.py` contém **só uma explicação**: o que é
aquela peça, o que vai dentro, como criar e quais armadilhas esperar.

Não é código para rodar. É o roteiro para escrever o seu.

## Como usar

Comece pelo fluxo de dados, não pela estrutura de pastas:

| Ordem | Arquivo | Por quê começar aqui |
|---|---|---|
| 1 | [`schemas/schemas.py`](schemas/schemas.py) | Definir os contratos primeiro obriga a decidir o que entra e o que sai |
| 2 | [`state.py`](state.py) | O que precisa atravessar o grafo |
| 3 | [`nodes/nodes.py`](nodes/nodes.py) | Cada passo, isolado |
| 4 | [`edges/edges.py`](edges/edges.py) | Como os passos se ligam |
| 5 | [`graph.py`](graph.py) | Montar e rodar |

Depois, as peças que dão substância ao agente:

| Arquivo | Conceito |
|---|---|
| [`config.py`](config.py) | Configuração e credenciais num ponto só |
| [`services/services.py`](services/services.py) | Clientes externos: LLM, busca |
| [`tools/tools.py`](tools/tools.py) | O que o **modelo** decide chamar |
| [`prompts/prompts.py`](prompts/prompts.py) | O que o modelo lê |
| [`guardrails/guardrails.py`](guardrails/guardrails.py) | O que barra antes e confere depois |
| [`subgraphs/subgraphs.py`](subgraphs/subgraphs.py) | Um grafo usado como nó |
| [`observability/observability.py`](observability/observability.py) | Enxergar o que aconteceu |

## O que falta além dos `.py`

Para o agente rodar de verdade você ainda precisa de:

- **`langgraph.json`** — aponta o servidor para o grafo: `{"graphs": {"meu": "./src/graph.py:graph"}, "env": "./.env"}`
- **`.env`** / **`.env.example`** — as credenciais
- **`pyproject.toml`** — dependências (`langgraph`, o SDK do provedor, `pydantic`)
- **`.gitignore`** — comece com `.env`, `.venv/`, `__pycache__/`

## Uma observação sobre os arquivos

Cada `.py` tem só uma docstring de módulo. Isso é Python válido: dá para importar sem
erro, e a explicação fica acessível por `help()` ou pelo editor. Substitua a docstring
pelo seu código — ou mantenha a explicação no topo, ela não atrapalha.
