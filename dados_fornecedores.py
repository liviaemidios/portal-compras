import pandas as pd
import os

def inicializar_csv_fornecedores():
    caminho = "database/fornecedores.csv"
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
            "inscricao_estadual",
            "inscricao_municipal",
            "pedido_minimo",
            "prazo_pagamento"
        ])
        df.to_csv(caminho, index=False)

def carregar_fornecedores():
    inicializar_csv_fornecedores()
    return pd.read_csv("database/fornecedores.csv")

def salvar_fornecedores(df):
    df.to_csv("database/fornecedores.csv", index=False)

