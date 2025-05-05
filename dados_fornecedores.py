# dados_fornecedores.py
import pandas as pd
import os

CAMINHO_FORNECEDORES = "database/fornecedores.csv"

COLUNAS_FORNECEDORES = [
    "razao_social", "nome_fantasia", "cnpj", "telefone", "celular", "email",
    "endereco", "inscricao_estadual", "inscricao_municipal",
    "pedido_minimo", "prazo_pagamento", "formas_pagamento", "frete",
    "responsavel_nome", "responsavel_telefone", "responsavel_email", "observacoes"
]

def carregar_fornecedores():
    if not os.path.exists(CAMINHO_FORNECEDORES):
        return pd.DataFrame(columns=COLUNAS_FORNECEDORES)
    return pd.read_csv(CAMINHO_FORNECEDORES, dtype=str)

def salvar_fornecedores(df):
    df.to_csv(CAMINHO_FORNECEDORES, index=False)
