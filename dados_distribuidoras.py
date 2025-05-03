import pandas as pd
import os

def inicializar_csv_distribuidoras():
    caminho = "database/distribuidoras.csv"
    if not os.path.exists("database"):
        os.makedirs("database")
    if not os.path.exists(caminho):
        df = pd.DataFrame(columns=[
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "telefone",
            "email",
            "endereco",
            "prazo_entrega",
            "frete_medio"
        ])
        df.to_csv(caminho, index=False)

def carregar_distribuidoras():
    inicializar_csv_distribuidoras()
    return pd.read_csv("database/distribuidoras.csv")

def salvar_distribuidoras(df):
    df.to_csv("database/distribuidoras.csv", index=False)
