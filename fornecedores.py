import streamlit as st
import pandas as pd
from login import login_page, get_current_user
from formulario_fornecedor import mostrar_formulario_fornecedor
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores

def renderizar_fornecedores():
    if not st.session_state.get("usuario"):
        login_page()
        st.stop()

    usuario = get_current_user()
    if usuario is None:
        st.error("Erro ao carregar o usuário.")
        st.stop()

    params = st.query_params
    if "nova" in params:
        mostrar_formulario_fornecedor(modo="novo")
        return

    if "editar" in params:
        index = int(params["editar"])
        dados = carregar_fornecedores().iloc[index].to_dict()
        mostrar_formulario_fornecedor(modo="editar", dados=dados, index=index)
        return

    # Título e barra de ações
    col1, col2, col3, col4 = st.columns([3, 2.5, 3.5, 0.5])
    with col1:
        st.markdown("<h4 style='margin-top: 0.8em;'>🏢 Fornecedores</h4>", unsafe_allow_html=True)
    with col2:
        st.write("")
        if st.button("➕ Cadastrar"):
            st.query_params.update({"nova": "1"})
            st.experimental_rerun()
    with col3:
        busca = st.text_input("", placeholder="Pesquisar fornecedor...", label_visibility="collapsed")
    with col4:
        st.write("")
        st.button("🔍")

    # Carregar e ordenar fornecedores
    fornecedores = carregar_fornecedores()
    fornecedores = fornecedores.sort_values("razao_social").reset_index(drop=True)

    # Paginação
    itens_por_pagina = 15
    total = len(fornecedores)
    pagina_atual = st.number_input("Página", min_value=1, max_value=(total - 1) // itens_por_pagina + 1, step=1)
    inicio = (pagina_atual - 1) * itens_por_pagina
    fim = inicio + itens_por_pagina
    pagina_df = fornecedores.iloc[inicio:fim]

    # Estilo visual profissional
    st.markdown(
        """
        <style>
            .fornecedores-box {
                border: 1px solid #d9d9d9;
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
            }
            .fornecedores-header {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .fornecedores-row {
                padding: 5px 0;
                border-bottom: 1px solid #eee;
            }
            .fornecedores-actions button {
                padding: 0.1em 0.3em;
                font-size: 0.8em;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="fornecedores-box">', unsafe_allow_html=True)
    st.markdown('<div class="fornecedores-header">📋 Lista de Fornecedores</div>', unsafe_allow_html=True)

    # Cabeçalhos da tabela
    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 3, 2, 1])
    col1.markdown("**Razão Social**")
    col2.markdown("**Fantasia**")
    col3.markdown("**CNPJ**")
    col4.markdown("**E-mail**")
    col5.markdown("**Telefone**")
    col6.markdown("**Ações**")

    # Linhas da tabela
    for i, row in pagina_df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 3, 2, 1])
        col1.write(row["razao_social"])
        col2.write(row["nome_fantasia"])
        col3.write(row["cnpj"])
        col4.write(row["email"])
        col5.write(row["telefone"])
        with col6:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("🔍", key=f"ver_{i+inicio}"):
                    st.session_state.visualizando = i + inicio
            with col_b:
                if st.button("✏️", key=f"edit_{i+inicio}"):
                    st.query_params.update({"editar": str(i + inicio)})
                    st.experimental_rerun()
            with col_c:
                if st.button("🗑️", key=f"del_{i+inicio}"):
                    fornecedores = fornecedores.drop(i + inicio).reset_index(drop=True)
                    salvar_fornecedores(fornecedores)
                    st.success("Fornecedor excluído com sucesso.")
                    st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)
