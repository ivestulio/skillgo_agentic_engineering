"""observability/ - observabilidade: enxergar o que o agente fez.

O QUE E
-------
Agente e nao-deterministico: a mesma entrada pode produzir caminhos diferentes. Sem
tracing, "por que ele classificou como critica?" nao tem resposta.

Duas coisas distintas:
- LOG: linha de texto, para acompanhar no terminal.
- TRACE: arvore de spans, com entrada, saida e duracao de cada passo.

O QUE VAI AQUI
--------------
    logging.py        formato unico de log
    mlflow_client.py  conexao e autolog
    tracing.py        spans manuais
    metrics.py        numeros de qualidade da execucao

COMO CRIAR - ligar o autolog
----------------------------
    import mlflow

    def configurar():
        if not settings.tracking_uri:
            return                      # sem tracing configurado: segue sem
        mlflow.set_tracking_uri(settings.tracking_uri)
        mlflow.set_experiment(settings.experimento)
        mlflow.langchain.autolog()      # cobre o LangGraph: um span por no

Nao existe `mlflow.langgraph.autolog()`. A integracao do LangChain ja captura o
grafo inteiro, com o nome de cada no.

Chame `configurar()` UMA VEZ, no import do modulo do grafo.

COMO CRIAR - span manual
------------------------
O autolog ve os nos. Ele nao ve o que acontece DENTRO deles. Para o que importa,
abra um span:

    @contextmanager
    def span_busca(consulta: str):
        if not _ativo:
            yield lambda *a: None       # degrada: sem MLflow, nao faz nada
            return
        with mlflow.start_span(name="busca", span_type=SpanType.RETRIEVER) as span:
            span.set_inputs({"consulta": consulta})
            yield lambda mantidos, descartados: span.set_attributes(
                {"mantidos": len(mantidos), "descartados": len(descartados)}
            )

E assim que se enxerga, no trace, o modelo decidindo buscar.

METRICA EM SERVIDOR: tag, nao log_metric
----------------------------------------
    mlflow.update_current_trace(tags={"decisao": "aprovar", "fontes": "4"})

`mlflow.log_metric` escreve num Run, nao no span - o numero nao apareceria junto do
trace que ele descreve. E um servidor de vida longa nao tem "run" que faca sentido
abrir e fechar por requisicao. Para agregar depois, consulte as traces:

    mlflow.search_traces(filter_string="tags.decisao = 'aprovar'")

ARMADILHAS
----------
- Observabilidade NUNCA pode derrubar o agente. Envolva em try/except e degrade em
  silencio: MLflow fora do ar no meio da aula nao pode parar a demonstracao.

- Abrir span com MLflow nao configurado faz ele criar um `mlruns/` local por conta
  propria. Controle com uma flag ligada so quando a conexao deu certo.

- Log e trace nao competem. Log serve para acompanhar ao vivo; trace para investigar
  depois. Tenha os dois.
"""
