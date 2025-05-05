# dados_produtos.py
import pandas as pd
import os

CAMINHO_PRODUTOS = "database/produtos.csv"

def inicializar_csv_produtos():
    if not os.path.exists(CAMINHO_PRODUTOS):
        colunas = ["nome", "categoria", "unidade", "preco", "descricao"]
        pd.DataFrame(columns=colunas).to_csv(CAMINHO_PRODUTOS, index=False)

def carregar_produtos():
    if os.path.exists(CAMINHO_PRODUTOS):
        return pd.read_csv(CAMINHO_PRODUTOS)
    else:
        return pd.DataFrame(columns=["nome", "categoria", "unidade", "preco", "descricao"])

def salvar_produtos(df):
    df.to_csv(CAMINHO_PRODUTOS, index=False)
