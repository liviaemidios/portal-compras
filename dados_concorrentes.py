# dados_concorrentes.py
import pandas as pd
import os

CAMINHO_CONCORRENTES = "database/concorrentes.csv"

COLUNAS_CONCORRENTES = [
    "razao_social", "nome_fantasia", "cnpj", "telefone", "email",
    "endereco", "inscricao_estadual", "inscricao_municipal",
    "pedido_minimo", "prazo_pagamento", "formas_pagamento", "frete",
    "responsavel_nome", "responsavel_telefone", "responsavel_email", "observacoes"
]

def carregar_concorrentes():
    if not os.path.exists(CAMINHO_CONCORRENTES):
        return pd.DataFrame(columns=COLUNAS_CONCORRENTES)
    return pd.read_csv(CAMINHO_CONCORRENTES, dtype=str)

def salvar_concorrentes(df):
    df.to_csv(CAMINHO_CONCORRENTES, index=False)
