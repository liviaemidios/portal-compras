# dados_concorrentes.py
import pandas as pd
import os

CAMINHO_CONCORRENTES = "database/concorrentes.csv"

def inicializar_csv_concorrentes():
    if not os.path.exists(CAMINHO_CONCORRENTES):
        colunas = [
            "razao_social", "nome_fantasia", "cnpj", "telefone", "email", "endereco",
            "inscricao_estadual", "inscricao_municipal", "pedido_minimo", "prazo_pagamento"
        ]
        pd.DataFrame(columns=colunas).to_csv(CAMINHO_CONCORRENTES, index=False)

def carregar_concorrentes():
    if os.path.exists(CAMINHO_CONCORRENTES):
        return pd.read_csv(CAMINHO_CONCORRENTES)
    else:
        return pd.DataFrame(columns=[
            "razao_social", "nome_fantasia", "cnpj", "telefone", "email", "endereco",
            "inscricao_estadual", "inscricao_municipal", "pedido_minimo", "prazo_pagamento"
        ])

def salvar_concorrentes(df):
    df.to_csv(CAMINHO_CONCORRENTES, index=False)
