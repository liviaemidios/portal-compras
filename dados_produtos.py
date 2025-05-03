import pandas as pd
import os

def inicializar_csv_produtos():
    caminho = "database/produtos.csv"
    if not os.path.exists("database"):
        os.makedirs("database")
    if not os.path.exists(caminho):
        df = pd.DataFrame(columns=[
            "codigo",
            "nome",
            "categoria",
            "unidade",
            "preco_compra",
            "preco_venda",
            "estoque",
            "estoque_minimo",
            "fornecedor",
            "distribuidora"
        ])
        df.to_csv(caminho, index=False)

def carregar_produtos():
    inicializar_csv_produtos()
    return pd.read_csv("database/produtos.csv")

def salvar_produtos(df):
    df.to_csv("database/produtos.csv", index=False)
