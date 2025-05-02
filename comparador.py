import streamlit as st
import pandas as pd
import os
from utils import carregar_csv, salvar_csv

CAMINHO_PRODUTOS = "database/produtos.csv"
CAMINHO_PRECOS = "database/precos.csv"

def iniciar_precos():
    if not os.path.exists(CAMINHO_PRECOS):
        df = pd.DataFrame(columns=["Código Produto", "Nome Produto", "Fornecedor", "Preço", "Data"])
        df.to_csv(CAMINHO_PRECOS, index=False)

def pagina_comparador():
    st.title("💰 Comparador de Preços")
    iniciar_precos()
    produtos = carregar_csv(CAMINHO_PRODUTOS)
    precos = carregar_csv(CAMINHO_PRECOS)

    if produtos.empty:
        st.warning("Nenhum produto cadastrado ainda.")
        return

    produto_selecionado = st.selectbox("Selecione um produto", produtos["Produto"].unique())
    produto_info = produtos[produtos["Produto"] == produto_selecionado].iloc[0]
    precos_filtrados = precos[precos["Nome Produto"] == produto_selecionado]

    if precos_filtrados.empty:
        st.info("Nenhum preço cadastrado para este produto ainda.")
    else:
        precos_filtrados = precos_filtrados.sort_values("Preço")
        st.subheader(f"Preços para: {produto_selecionado}")
        st.dataframe(precos_filtrados, use_container_width=True)

    st.markdown("---")
    st.subheader("Adicionar novo preço")
    with st.form("form_preco"):
        fornecedor = st.text_input("Fornecedor")
        preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
        data = st.date_input("Data da cotação")
        if st.form_submit_button("Salvar Preço"):
            novo = pd.DataFrame([[produto_info["Código"], produto_selecionado, fornecedor, preco, str(data)]], columns=precos.columns)
            precos = pd.concat([precos, novo], ignore_index=True)
            salvar_csv(CAMINHO_PRECOS, precos)
            st.success("Preço salvo com sucesso!")
            st.experimental_rerun()
