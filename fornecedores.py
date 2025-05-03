import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores

def renderizar_fornecedores():
    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.error("Acesso negado. Faça login para continuar.")
        st.stop()

    st.markdown("""
        <style>
            .header-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }
            .header-bar h2 {
                margin: 0;
                font-size: 24px;
                color: #3879bd;
            }
            .search-row {
                display: flex;
                gap: 10px;
                align-items: center;
                margin-top: 0.5rem;
            }
            .tabela-box {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 16px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            }
            .tabela-header {
                font-weight: 600;
                font-size: 15px;
                border-bottom: 1px solid #ccc;
                padding-bottom: 6px;
                margin-bottom: 8px;
            }
            .paginacao {
                text-align: right;
                font-size: 13px;
                padding-top: 10px;
                color: #444;
            }
        </style>
    """, unsafe_allow_html=True)

    # Cabeçalho com título, botão e busca
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.markdown("<div class='header-bar'><h2>🏢 Fornecedores</h2></div>", unsafe_allow_html=True)
    with col2:
        if st.button("➕ Cadastrar Novo Fornecedor"):
            st.switch_page("formulario_fornecedor.py")
    with col3:
        busca = st.text_input("", placeholder="🔍 Pesquisar fornecedor...", label_visibility="collapsed")

    fornecedores = carregar_fornecedores()

    if busca:
        busca = busca.lower()
        fornecedores = fornecedores[
            fornecedores["razao_social"].str.lower().str.contains(busca)
            | fornecedores["nome_fantasia"].str.lower().str.contains(busca)
            | fornecedores["cnpj"].str.contains(busca)
        ]

    fornecedores = fornecedores.sort_values("razao_social").reset_index(drop=True)

    # Paginação
    por_pagina = 15
    total = len(fornecedores)
    paginas = max(1, (total - 1) // por_pagina + 1)
    pagina = st.session_state.get("pagina_fornecedores", 1)

    col_pag1, col_pag2, col_pag3 = st.columns([9, 0.5, 0.5])
    with col_pag2:
        if st.button("◀") and pagina > 1:
            pagina -= 1
    with col_pag3:
        if st.button("▶") and pagina < paginas:
            pagina += 1
    st.session_state["pagina_fornecedores"] = pagina

    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    fornecedores_pag = fornecedores.iloc[inicio:fim]

    st.markdown("<div class='tabela-box'>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2.5, 2.5, 2, 1])
    col1.markdown("<div class='tabela-header'>Razão Social</div>", unsafe_allow_html=True)
    col2.markdown("<div class='tabela-header'>Fantasia</div>", unsafe_allow_html=True)
    col3.markdown("<div class='tabela-header'>CNPJ</div>", unsafe_allow_html=True)
    col4.markdown("<div class='tabela-header'>E-mail</div>", unsafe_allow_html=True)
    col5.markdown("<div class='tabela-header'>Telefone</div>", unsafe_allow_html=True)
    col6.markdown("<div class='tabela-header'>Ações</div>", unsafe_allow_html=True)

    for _, row in fornecedores_pag.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2.5, 2.5, 2, 1])
        col1.write(row["razao_social"])
        col2.write(row["nome_fantasia"])
        col3.write(row["cnpj"])
        col4.write(row["email"])
        col5.write(row["telefone"])
        col6.markdown("<span style='font-size:16px;'>👁️ ✏️ 🗑️</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='paginacao'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
