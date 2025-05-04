import pandas as pd
import os

CAMINHO_PRODUTOS = "database/produtos.csv"

def carregar_produtos():
    if os.path.exists(CAMINHO_PRODUTOS):
        return pd.read_csv(CAMINHO_PRODUTOS)
    else:
        return pd.DataFrame(columns=["descricao", "categoria", "unidade", "estoque", "estoque_minimo"])

def salvar_produtos(df):
    df.to_csv(CAMINHO_PRODUTOS, index=False)
