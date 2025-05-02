import streamlit as st
import pandas as pd
import os
from utils import carregar_csv

CAMINHO_PRECOS = "database/precos.csv"

def pagina_relatorios():
    st.title("📊 Relatórios Estratégicos de Compras")

    if not os.path.exists(CAMINHO_PRECOS):
        st.warning("Nenhuma informação de preços disponível ainda.")
        return

    precos = carregar_csv(CAMINHO_PRECOS)
    if precos.empty:
        st.warning("Nenhum dado de preços cadastrado.")
        return

    st.subheader("1. Produtos com maior variação de preço")
    variacoes = precos.groupby("Nome Produto")["Preço"].agg(["min", "max"])
    variacoes["Diferença"] = variacoes["max"] - variacoes["min"]
    variacoes = variacoes.sort_values("Diferença", ascending=False).reset_index()
    st.dataframe(variacoes, use_container_width=True)

    st.subheader("2. Quantidade de cotações por fornecedor")
    fornecedores = precos["Fornecedor"].value_counts().reset_index()
    fornecedores.columns = ["Fornecedor", "Número de Cotações"]
    st.dataframe(fornecedores, use_container_width=True)

    st.subheader("3. Produtos mais cotados")
    mais_cotados = precos["Nome Produto"].value_counts().reset_index()
    mais_cotados.columns = ["Produto", "Número de Cotações"]
    st.dataframe(mais_cotados, use_container_width=True)

    st.markdown("---")
    st.caption("Relatórios gerados com base nas informações de preços cadastradas no sistema.")
