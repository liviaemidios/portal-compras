import streamlit as st
import pandas as pd
import os
from login import login_page, get_current_user

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

    # Cabeçalho com título à esquerda e busca à direita
    col1, col2, col3, col4 = st.columns([2.5, 1.8, 5, 0.7])

    with col1:
        st.markdown("## 🏢 Fornecedores")

    with col2:
        if st.button("➕ Cadastrar"):
            st.session_state.cadastrando = True

    with col3:
        busca = st.text_input("", placeholder="Pesquisar fornecedor...", label_visibility="collapsed")

    with col4:
        st.write("")
        st.button("🔍")

    # Formulário de cadastro
    if st.session_state.cadastrando:
        with st.expander("➕ Cadastrar Novo Fornecedor", expanded=True):
            with st.form("form_cadastrar_fornecedor"):
                st.subheader("Dados da Empresa")
                razao_social = st.text_input("Razão Social")
                nome_fantasia = st.text_input("Nome Fantasia")
                cnpj = st.text_input("CNPJ")
                inscricao_estadual = st.text_input("Inscrição Estadual")
                inscricao_municipal = st.text_input("Inscrição Municipal")

                st.subheader("Contato")
                telefone = st.text_input("Telefone")
                email = st.text_input("E-mail")
                endereco = st.text_area("Endereço")

                st.subheader("Condições Comerciais")
                pedido_minimo = st.text_input("Valor Mínimo de Pedido")
                prazo_pagamento = st.text_input("Prazo de Pagamento")

                col_a, col_b = st.columns(2)
                salvar = col_a.form_submit_button("Salvar")
                cancelar = col_b.form_submit_button("Cancelar")

                if salvar:
                    novo = pd.DataFrame([{
                        "razao_social": razao_social,
                        "nome_fantasia": nome_fantasia,
                        "cnpj": cnpj,
                        "telefone": telefone,
                        "email": email,
                        "endereco": endereco,
                        "inscricao_estadual": inscricao_estadual,
                        "inscricao_municipal": inscricao_municipal,
                        "pedido_minimo": pedido_minimo,
                        "prazo_pagamento": prazo_pagamento
                    }])
                    fornecedores = carregar_fornecedores()
                    fornecedores = pd.concat([fornecedores, novo], ignore_index=True)
                    salvar_fornecedores(fornecedores)
                    st.success("Fornecedor cadastrado com sucesso!")
                    st.session_state.cadastrando = False
                    st.session_state.rerun = True
                    st.stop()
                elif cancelar:
                    st.session_state.cadastrando = False
                    st.session_state.rerun = True
                    st.stop()

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
            if st.button("🔍", key=f"ver_{i}"):
                st.session_state.visualizando = i
            if st.button("✏️", key=f"edit_{i}"):
                st.session_state.editando = i
            if st.button("🗑️", key=f"del_{i}"):
                fornecedores = fornecedores.drop(i).reset_index(drop=True)
                salvar_fornecedores(fornecedores)
                st.success("Fornecedor excluído com sucesso.")
                st.session_state.rerun = True
                st.stop()
