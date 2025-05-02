import streamlit as st
import pandas as pd
import os
from utils import carregar_csv, salvar_csv

CAMINHO_ARQUIVO = "database/produtos.csv"

def iniciar_csv():
    if not os.path.exists(CAMINHO_ARQUIVO):
        df = pd.DataFrame(columns=["Código", "Produto", "Unidade", "Categoria", "Marca"])
        df.to_csv(CAMINHO_ARQUIVO, index=False)

def pagina_produtos():
    st.title("📦 Cadastro de Produtos")
    iniciar_csv()
    df = carregar_csv(CAMINHO_ARQUIVO)

    busca = st.text_input("🔎 Buscar produto por nome, código ou categoria")
    if busca:
        df = df[df.apply(lambda row: busca.lower() in row.astype(str).str.lower().to_string(), axis=1)]

    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("➕ Cadastrar novo produto"):
            st.session_state.modo_prod = "novo"
    with col2:
        if "modo_prod" in st.session_state and st.session_state.modo_prod == "novo":
            with st.form("form_prod"):
                st.subheader("Cadastrar Produto")
                codigo = st.text_input("Código")
                nome = st.text_input("Nome do Produto")
                unidade = st.text_input("Unidade (ex: UN, CX, KG)")
                categoria = st.text_input("Categoria")
                marca = st.text_input("Marca")
                if st.form_submit_button("Salvar"):
                    novo = pd.DataFrame([[codigo, nome, unidade, categoria, marca]], columns=df.columns)
                    df = pd.concat([df, novo], ignore_index=True)
                    salvar_csv(CAMINHO_ARQUIVO, df)
                    st.success("Produto cadastrado com sucesso!")
                    st.session_state.modo_prod = None
                    st.experimental_rerun()
