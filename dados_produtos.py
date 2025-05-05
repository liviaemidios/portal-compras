# dados_produtos.py
import pandas as pd
import os

CAMINHO_PRODUTOS = "database/produtos.csv"

COLUNAS_PRODUTOS = [
    "produto", "marca", "unidade", "preco", "fornecedor"
]

def carregar_produtos():
    if not os.path.exists(CAMINHO_PRODUTOS):
        return pd.DataFrame(columns=COLUNAS_PRODUTOS)
    return pd.read_csv(CAMINHO_PRODUTOS, dtype=str)

def salvar_produtos(df):
    df.to_csv(CAMINHO_PRODUTOS, index=False)
