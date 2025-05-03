import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores

def renderizar_fornecedores():
    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.error("Acesso negado. Faça login para continuar.")
        st.stop()

    # Cabeçalho
    col1, col2, col3 = st.columns([3, 1.5, 2])
    with col1:
        st.markdown("## 🏢 Fornecedores")
    with col2:
        if st.button("➕ Cadastrar"):
            st.switch_page("formulario_fornecedor.py")
    with col3:
        with st.form(key="form_busca"):
            col_search1, col_search2 = st.columns([4, 1])
            busca = col_search1.text_input("", placeholder="Pesquisar...", label_visibility="collapsed")
            buscar = col_search2.form_submit_button("🔍")

    # Carregar e filtrar dados
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
    por_pagina = 10
    total = len(fornecedores)
    paginas = max(1, (total - 1) // por_pagina + 1)
    pagina = st.session_state.get("pagina_fornecedores", 1)

    col_pg1, col_pg2, col_pg3 = st.columns([8, 0.5, 0.5])
    with col_pg2:
        if st.button("◀") and pagina > 1:
            pagina -= 1
    with col_pg3:
        if st.button("▶") and pagina < paginas:
            pagina += 1
    st.session_state["pagina_fornecedores"] = pagina

    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    fornecedores_pag = fornecedores.iloc[inicio:fim]

    # Tabela
    st.markdown("---")
    header_cols = st.columns([3, 2, 2.5, 2.5, 2, 1])
    headers = ["Razão Social", "Fantasia", "CNPJ", "E-mail", "Telefone", "Ações"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    for _, row in fornecedores_pag.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2.5, 2.5, 2, 1])
        col1.write(row["razao_social"])
        col2.write(row["nome_fantasia"])
        col3.write(row["cnpj"])
        col4.write(row["email"])
        col5.write(row["telefone"])
        col6.markdown("<span style='font-size:16px;'>👁️ ✏️ 🗑️</span>", unsafe_allow_html=True)

    st.markdown(f"<div style='text-align: right; font-size: 13px;'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
