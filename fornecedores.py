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

    query_params = st.query_params
    if query_params.get("cadastrar") == ["true"]:
        st.session_state.cadastrando = True
        st.query_params.clear()

    st.markdown("""
    <style>
    .title-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .title-row h1 {
        font-size: 2.8rem;
        line-height: 2.8rem;
        margin: 0;
    }
    .actions {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    .table-header {
        background-color: #f0f2f6;
        font-weight: bold;
        border-bottom: 1px solid #ccc;
        padding: 0.5rem 0;
    }
    .table-row {
        border-bottom: 1px solid #e6e6e6;
        padding: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='title-row'>
        <h1>🏢 Fornecedores</h1>
        <div class='actions'>
            <button onclick="window.location.href='?cadastrar=true'" style='height: 2.2rem;'>➕ Cadastrar Novo Fornecedor</button>
            <input type='text' id='busca' name='busca' placeholder='Buscar...' style='height: 2.2rem; padding: 0 0.5rem;' />
            <button style='height: 2.2rem;'>🔍</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
                    st.experimental_rerun()
                elif cancelar:
                    st.session_state.cadastrando = False
                    st.experimental_rerun()

    fornecedores = carregar_fornecedores()
    st.markdown("### Lista de Fornecedores")

    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 3, 2, 1])
    col1.markdown("<div class='table-header'>Razão Social</div>", unsafe_allow_html=True)
    col2.markdown("<div class='table-header'>Fantasia</div>", unsafe_allow_html=True)
    col3.markdown("<div class='table-header'>CNPJ</div>", unsafe_allow_html=True)
    col4.markdown("<div class='table-header'>E-mail</div>", unsafe_allow_html=True)
    col5.markdown("<div class='table-header'>Telefone</div>", unsafe_allow_html=True)
    col6.markdown("<div class='table-header'>Ações</div>", unsafe_allow_html=True)

    for i, row in fornecedores.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 3, 2, 1])
        col1.markdown(f"<div class='table-row'>{row['razao_social']}</div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='table-row'>{row['nome_fantasia']}</div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='table-row'>{row['cnpj']}</div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='table-row'>{row['email']}</div>", unsafe_allow_html=True)
        col5.markdown(f"<div class='table-row'>{row['telefone']}</div>", unsafe_allow_html=True)
        with col6:
            if st.button("🔍", key=f"ver_{i}"):
                st.session_state.visualizando = i
            if st.button("✏️", key=f"edit_{i}"):
                st.session_state.editando = i
            if st.button("🗑️", key=f"del_{i}"):
                fornecedores = fornecedores.drop(i).reset_index(drop=True)
                salvar_fornecedores(fornecedores)
                st.success("Fornecedor excluído com sucesso.")
                st.experimental_rerun()
