import pandas as pd
import os

def carregar_csv(caminho):
    if os.path.exists(caminho):
        return pd.read_csv(caminho)
    else:
        return pd.DataFrame()

def salvar_csv(caminho, df):
    df.to_csv(caminho, index=False)
