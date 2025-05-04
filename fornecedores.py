import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores

def renderizar_fornecedores():
    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.error("Acesso negado. Faça login para continuar.")
        st.stop()

    # Estilos adicionais
    st.markdown("""
        <style>
            .titulo-header {
                font-size: 40px;
                font-weight: bold;
                color: #3879bd;
                margin-bottom: 0.5rem;
            }
            .botao-cadastrar {
                margin-top: 1.6rem;
            }
            .setas-pequenas button {
                font-size: 12px !important;
                padding: 0.25rem 0.5rem !important;
            }
            .cabecalho-faixa-container {
                display: flex;
                background-color: #3879bd;
                border-radius: 5px;
                margin-top: 1rem;
            }
            .cabecalho-faixa-item {
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 8px;
                text-align: center;
                border-right: 1px solid #ffffff33;
                flex-shrink: 0;
            }
            .cabecalho-faixa-item:last-child {
                border-right: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # Cabeçalho com título e botão
    col1, col2 = st.columns([4, 1.5])
    with col1:
        st.markdown("<div class='titulo-header'>🏢 Fornecedores</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='botao-cadastrar'>", unsafe_allow_html=True)
        if st.button("➕ Cadastrar"):
            st.switch_page("formulario_fornecedor.py")
        st.markdown("</div>", unsafe_allow_html=True)

    # Carregar dados
    fornecedores = carregar_fornecedores()

    # Linha com campo de busca à esquerda e setas à direita
    col_busca, col_vazio, col_seta_esq, col_seta_dir = st.columns([6, 2.5, 0.5, 0.5])

    with col_busca:
        with st.form(key="form_busca"):
            col_search1, col_search2 = st.columns([5, 1])
            busca = col_search1.text_input("", placeholder="Pesquisar...", label_visibility="collapsed")
            buscar = col_search2.form_submit_button("🔍")

    with col_seta_esq:
        if st.button("◀") and st.session_state.get("pagina_fornecedores", 1) > 1:
            st.session_state["pagina_fornecedores"] -= 1

    with col_seta_dir:
        total = len(fornecedores)
        paginas = max(1, (total - 1) // 10 + 1)
        if st.button("▶") and st.session_state.get("pagina_fornecedores", 1) < paginas:
            st.session_state["pagina_fornecedores"] += 1

    if busca:
        busca = busca.lower()
        fornecedores = fornecedores[
            fornecedores["razao_social"].str.lower().str.contains(busca)
            | fornecedores["nome_fantasia"].str.lower().str.contains(busca)
            | fornecedores["cnpj"].str.contains(busca)
        ]

    fornecedores = fornecedores.sort_values("razao_social").reset_index(drop=True)

    # Paginação aplicada
    por_pagina = 10
    total = len(fornecedores)
    paginas = max(1, (total - 1) // por_pagina + 1)
    pagina = st.session_state.get("pagina_fornecedores", 1)
    st.session_state["pagina_fornecedores"] = pagina

    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    fornecedores_pag = fornecedores.iloc[inicio:fim]

    # Cabeçalho da tabela em faixa azul contínua
    st.markdown("""
        <div class='cabecalho-faixa-container'>
            <div class='cabecalho-faixa-item' style='flex: 3;'>Razão Social</div>
            <div class='cabecalho-faixa-item' style='flex: 2;'>Fantasia</div>
            <div class='cabecalho-faixa-item' style='flex: 2.5;'>CNPJ</div>
            <div class='cabecalho-faixa-item' style='flex: 2.5;'>E-mail</div>
            <div class='cabecalho-faixa-item' style='flex: 2;'>Telefone</div>
            <div class='cabecalho-faixa-item' style='flex: 1;'>Ações</div>
        </div>
    """, unsafe_allow_html=True)

    # Linhas da tabela
    for _, row in fornecedores_pag.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2.5, 2.5, 2, 1])
        col1.write(row["razao_social"])
        col2.write(row["nome_fantasia"])
        col3.write(row["cnpj"])
        col4.write(row["email"])
        col5.write(row["telefone"])
        col6.markdown("<span style='font-size:16px;'>👁️ ✏️ 🗑️</span>", unsafe_allow_html=True)

    st.markdown(f"<div style='text-align: right; font-size: 13px;'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
