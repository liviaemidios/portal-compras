import streamlit as st
import pandas as pd
import os
from utils import carregar_csv, salvar_csv

CAMINHO_ARQUIVO = "database/distribuidoras.csv"

def iniciar_csv():
    if not os.path.exists(CAMINHO_ARQUIVO):
        df = pd.DataFrame(columns=["CNPJ", "Nome", "Região de Entrega", "Tempo Médio de Entrega", "Contato"])
        df.to_csv(CAMINHO_ARQUIVO, index=False)

def pagina_distribuidoras():
    st.title("🚚 Lista de Distribuidoras")
    iniciar_csv()
    df = carregar_csv(CAMINHO_ARQUIVO)

    busca = st.text_input("🔎 Buscar distribuidora por nome ou CNPJ")
    if busca:
        df = df[df.apply(lambda row: busca.lower() in row.astype(str).str.lower().to_string(), axis=1)]

    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("➕ Cadastrar nova distribuidora"):
            st.session_state.modo_dist = "nova"
    with col2:
        if "modo_dist" in st.session_state and st.session_state.modo_dist == "nova":
            with st.form("form_dist"):
                st.subheader("Cadastrar Distribuidora")
                cnpj = st.text_input("CNPJ")
                nome = st.text_input("Nome")
                regiao = st.text_input("Região de Entrega")
                tempo = st.text_input("Tempo Médio de Entrega")
                contato = st.text_input("Contato")
                if st.form_submit_button("Salvar"):
                    nova = pd.DataFrame([[cnpj, nome, regiao, tempo, contato]], columns=df.columns)
                    df = pd.concat([df, nova], ignore_index=True)
                    salvar_csv(CAMINHO_ARQUIVO, df)
                    st.success("Distribuidora cadastrada com sucesso!")
                    st.session_state.modo_dist = None
                    st.experimental_rerun()
