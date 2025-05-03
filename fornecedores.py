import streamlit as st
import pandas as pd
import os
from login import login_page, get_current_user
from formulario_fornecedor import mostrar_formulario_fornecedor

CAMINHO_FORNECEDORES = "database/fornecedores.csv"

def carregar_fornecedores():
    if os.path.exists(CAMINHO_FORNECEDORES):
        return pd.read_csv(CAMINHO_FORNECEDORES, dtype=str)
    return pd.DataFrame(columns=[
        "razao_social", "nome_fantasia", "cnpj", "telefone", "email", "endereco",
        "inscricao_estadual", "inscricao_municipal", "pedido_minimo", "prazo_pagamento"
    ])

def salvar_fornecedores(df):
    df.to_csv(CAMINHO_FORNECEDORES, index=False)

def renderizar_fornecedores():
    if st.session_state.get("rerun"):
        st.session_state.rerun = False
        st.experimental_rerun()

    if not st.session_state.get("usuario"):
        login_page()
        st.stop()

    usuario = get_current_user()
    if usuario is None:
        st.error("Erro ao carregar o usuário.")
        st.stop()

    if "editando" not in st.session_state:
        st.session_state.editando = None
    if "visualizando" not in st.session_state:
        st.session_state.visualizando = None
    if "cadastrando" not in st.session_state:
        st.session_state.cadastrando = False

    # Cabeçalho alinhado
    col1, col2, col3, col4 = st.columns([3, 2.5, 3.5, 0.5])
    with col1:
        st.markdown("<h4 style='margin-top: 0.8em;'>🏢 Fornecedores</h4>", unsafe_allow_html=True)
    with col2:
        st.write("")
        if st.button("➕ Cadastrar"):
            st.session_state.cadastrando = True
    with col3:
        busca = st.text_input("", placeholder="Pesquisar fornecedor...", label_visibility="collapsed")
    with col4:
        st.write("")
        st.button("🔍")

    # Exibir formulário em modo pop-up
    if st.session_state.cadastrando:
        mostrar_formulario_fornecedor(modo="novo")

    if st.session_state.editando is not None:
        index = st.session_state.editando
        dados = carregar_fornecedores().iloc[index].to_dict()
        mostrar_formulario_fornecedor(modo="editar", dados=dados, index=index)

    # Lista de fornecedores
    fornecedores = carregar_fornecedores()

    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 3, 2, 1])
    col1.markdown("**Razão Social**")
    col2.markdown("**Fantasia**")
    col3.markdown("**CNPJ**")
    col4.markdown("**E-mail**")
    col5.markdown("**Telefone**")
    col6.markdown("**Ações**")

    for i, row in fornecedores.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 3, 2, 1])
        col1.write(row["razao_social"])
        col2.write(row["nome_fantasia"])
        col3.write(row["cnpj"])
        col4.write(row["email"])
        col5.write(row["telefone"])
        with col6:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("🔍", key=f"ver_{i}"):
                    st.session_state.visualizando = i
            with col_b:
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state.editando = i
            with col_c:
                if st.button("🗑️", key=f"del_{i}"):
                    fornecedores = fornecedores.drop(i).reset_index(drop=True)
                    salvar_fornecedores(fornecedores)
                    st.success("Fornecedor excluído com sucesso.")
                    st.experimental_rerun()
