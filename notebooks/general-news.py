import marimo

__generated_with = "0.23.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import os
    from kagiapi import KagiClient

    return (KagiClient,)


@app.cell
def _(KagiClient):
    kc = KagiClient(api_key="SLkgoQdfzuVWqm7lPeiMGOb518dN7C5fTcm0mz5YZCg.7OqQimWpEtyefITkOu5_qVOUnoAWSMgGfOmnkIgBjrM")
    return (kc,)


@app.cell
def _(kc):
    kc
    return


@app.cell
def _(kc):
    dir(kc)
    return


@app.cell
def _(kc):
    search_result = kc.enrich("New England")
    search_result
    return


@app.cell
def _(kc):
    fastgpt_query = "I want to know about news today and yesterday in Vermont. What do I absolutely need to know?"

    gpt_result = kc.fastgpt(query="vermont")
    gpt_result
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
