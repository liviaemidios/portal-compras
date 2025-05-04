import pandas as pd
import os

CAMINHO_CONCORRENTES = "database/concorrentes.csv"

def carregar_concorrentes():
    if os.path.exists(CAMINHO_CONCORRENTES):
        return pd.read_csv(CAMINHO_CONCORRENTES)
    else:
        return pd.DataFrame(columns=["razao_social", "nome_fantasia", "cnpj", "email", "telefone"])

def salvar_concorrentes(df):
    df.to_csv(CAMINHO_CONCORRENTES, index=False)
