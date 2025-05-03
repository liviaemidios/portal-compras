import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores

def renderizar_fornecedores():
    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.error("Acesso negado. Faça login para continuar.")
        st.stop()

    st.markdown("""
        <style>
            .tabela-container {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 0;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
                margin-top: 10px;
            }
            .tabela-titulo {
                background-color: #3879bd;
                color: white;
                padding: 12px 16px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 20px;
                font-weight: 600;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .tabela-botoes {
                display: flex;
                gap: 10px;
            }
            .tabela-paginacao {
                text-align: right;
                padding: 10px;
                font-size: 14px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Cabeçalho com botão e pesquisa
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.markdown("<div class='tabela-titulo'>Fornecedores</div>", unsafe_allow_html=True)
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

    col_pag = st.columns([8, 1, 1])
    with col_pag[1]:
        if st.button("◀") and pagina > 1:
            pagina -= 1
    with col_pag[2]:
        if st.button("▶") and pagina < paginas:
            pagina += 1
    st.session_state["pagina_fornecedores"] = pagina

    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    fornecedores_pag = fornecedores.iloc[inicio:fim]

    st.markdown("<div class='tabela-container'>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2.5, 2.5, 2, 1])
    col1.markdown("**Razão Social**")
    col2.markdown("**Fantasia**")
    col3.markdown("**CNPJ**")
    col4.markdown("**E-mail**")
    col5.markdown("**Telefone**")
    col6.markdown("**Ações**")

    for i, row in fornecedores_pag.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2.5, 2.5, 2, 1])
        col1.write(row["razao_social"])
        col2.write(row["nome_fantasia"])
        col3.write(row["cnpj"])
        col4.write(row["email"])
        col5.write(row["telefone"])
        col6.markdown("<span style='font-size:18px;'>👁️ ✏️ 🗑️</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='tabela-paginacao'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
