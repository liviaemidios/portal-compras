import pandas as pd
import os

CAMINHO_FORNECEDORES = "database/fornecedores.csv"

def carregar_fornecedores():
    if os.path.exists(CAMINHO_FORNECEDORES):
        return pd.read_csv(CAMINHO_FORNECEDORES, dtype=str)
    return pd.DataFrame(columns=[
        "razao_social", "nome_fantasia", "cnpj", "telefone", "email", "endereco",
        "inscricao_estadual", "inscricao_municipal", "pedido_minimo", "prazo_pagamento"
    ])

def salvar_fornecedores(df):
    df.to_csv(CAMINHO_FORNECEDORES, index=False)
