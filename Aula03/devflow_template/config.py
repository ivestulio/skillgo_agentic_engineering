"""config.py - configuracao: um unico ponto de leitura do ambiente.

O QUE E
-------
Onde as variaveis do .env viram atributos tipados. A regra: NENHUM outro arquivo do
projeto le `os.environ`. Todos importam daqui.

Isso vale a pena por tres motivos: voce descobre o que o projeto precisa lendo um
arquivo so; trocar de provedor mexe em um lugar; e teste consegue substituir a
configuracao sem mexer no ambiente.

O QUE VAI AQUI
--------------
- A classe Settings com um atributo por variavel de ambiente.
- Uma instancia unica, importada pelo resto do projeto.
- Opcionalmente, uma checagem de credencial faltando.

COMO CRIAR
----------
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(env_file=".env", extra="ignore")

        api_endpoint: str = ""
        api_key: str = ""
        modelo: str = "gpt-4o"

    settings = Settings()

O nome do atributo vira o nome da variavel em MAIUSCULAS: `api_key` le `API_KEY`.

CHECAGEM DE CREDENCIAL
----------------------
Util, mas o ONDE importa:

    def exigir(*campos):
        faltando = [c.upper() for c in campos if not getattr(settings, c, "")]
        if faltando:
            raise RuntimeError(f"Faltam variaveis no .env: {', '.join(faltando)}")

Chame na CRIACAO DO CLIENTE, nunca no import do modulo. O grafo precisa poder ser
montado sem credencial nenhuma - o servidor importa o modulo na subida, e caminhos
que nao chamam o modelo (um guardrail que bloqueia, por exemplo) devem rodar assim.

ARMADILHAS
----------
- Mensagem de erro que aponta para a variavel errada custa caro. Se voce usa Azure
  OpenAI com chave vazia, o SDK reclama de `OPENAI_API_KEY` - que nao e a sua
  variavel. Checar antes e dizer o nome certo economiza muito tempo de aluno.

- O .env e lido UMA VEZ, na subida do processo. Editou? Reinicie o servidor. O
  reload automatico recarrega CODIGO, nao ambiente - e isso engana bastante.
"""
