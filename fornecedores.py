import streamlit as st
import pandas as pd
from login import login_page, get_current_user
from formulario_fornecedor import mostrar_formulario_fornecedor
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores
from urllib.parse import urlencode

def renderizar_fornecedores():
    if not st.session_state.get("usuario"):
        login_page()
        st.stop()

    usuario = get_current_user()
    if usuario is None:
        st.error("Erro ao carregar o usuário.")
        st.stop()

    # Verificar parâmetros da URL
    params = st.experimental_get_query_params()
    if "nova" in params:
        mostrar_formulario_fornecedor(modo="novo")
        return

    if "editar" in params:
        index = int(params["editar"][0])
        dados = carregar_fornecedores().iloc[index].to_dict()
        mostrar_formulario_fornecedor(modo="editar", dados=dados, index=index)
        return

    # Interface da lista de fornecedores
    col1, col2, col3, col4 = st.columns([3, 2.5, 3.5, 0.5])
    with col1:
        st.markdown("<h4 style='margin-top: 0.8em;'>🏢 Fornecedores</h4>", unsafe_allow_html=True)
    with col2:
        st.write("")
        if st.button("➕ Cadastrar"):
            st.experimental_set_query_params(nova="1")
            st.experimental_rerun()
    with col3:
        busca = st.text_input("", placeholder="Pesquisar fornecedor...", label_visibility="collapsed")
    with col4:
        st.write("")
        st.button("🔍")

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
                    st.experimental_set_query_params(editar=str(i))
                    st.experimental_rerun()
            with col_c:
                if st.button("🗑️", key=f"del_{i}"):
                    fornecedores = fornecedores.drop(i).reset_index(drop=True)
                    salvar_fornecedores(fornecedores)
                    st.success("Fornecedor excluído com sucesso.")
                    st.experimental_rerun()
