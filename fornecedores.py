import streamlit as st
import pandas as pd
import os
from utils import carregar_csv, salvar_csv

CAMINHO_ARQUIVO = "database/fornecedores.csv"

def iniciar_csv():
    if not os.path.exists(CAMINHO_ARQUIVO):
        df = pd.DataFrame(columns=["CNPJ", "Nome", "Categoria", "Contato", "E-mail"])
        df.to_csv(CAMINHO_ARQUIVO, index=False)

def pagina_fornecedores():
    st.title("📋 Lista de Fornecedores")
    iniciar_csv()
    df = carregar_csv(CAMINHO_ARQUIVO)

    if st.button("➕ Cadastrar novo fornecedor"):
        st.session_state.modo = "novo"

    busca = st.text_input("🔎 Buscar fornecedor por nome ou CNPJ")
    if busca:
        df = df[df.apply(lambda row: busca.lower() in row.astype(str).str.lower().to_string(), axis=1)]

    st.dataframe(df, use_container_width=True)

    if "modo" in st.session_state and st.session_state.modo == "novo":
        with st.form("form_cadastro"):
            st.subheader("Cadastrar Fornecedor")
            cnpj = st.text_input("CNPJ")
            nome = st.text_input("Nome")
            categoria = st.text_input("Categoria")
            contato = st.text_input("Telefone ou WhatsApp")
            email = st.text_input("E-mail")
            if st.form_submit_button("Salvar"):
                novo = pd.DataFrame([[cnpj, nome, categoria, contato, email]], columns=df.columns)
                df = pd.concat([df, novo], ignore_index=True)
                salvar_csv(CAMINHO_ARQUIVO, df)
                st.success("Fornecedor cadastrado com sucesso!")
                st.session_state.modo = None
                st.rerun()
