import streamlit as st
import pandas as pd
from dados_produtos import carregar_produtos, salvar_produtos

def renderizar_produtos():
    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.error("Acesso negado. Faça login para continuar.")
        st.stop()

    st.markdown("<h4 style='margin-top: 0.8em;'>📦 Produtos</h4>", unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1.5])
    with col1:
        busca = st.text_input("", placeholder="Pesquisar produto...", label_visibility="collapsed")
    with col2:
        if st.button("➕ Cadastrar Produto"):
            st.info("(Formulário de cadastro ainda não implementado)")

    produtos = carregar_produtos()

    if busca:
        busca = busca.lower()
        produtos = produtos[
            produtos["nome"].str.lower().str.contains(busca)
            | produtos["codigo"].astype(str).str.contains(busca)
            | produtos["categoria"].str.lower().str.contains(busca)
        ]

    produtos = produtos.sort_values("nome")

    st.markdown("""
        <style>
            .tabela-box {
                border: 1px solid #d9d9d9;
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tabela-box">', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    col1.markdown("**Código**")
    col2.markdown("**Nome**")
    col3.markdown("**Categoria**")
    col4.markdown("**Preço Venda**")
    col5.markdown("**Estoque**")

    for _, row in produtos.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        col1.write(row["codigo"])
        col2.write(row["nome"])
        col3.write(row["categoria"])
        col4.write(f"R$ {row['preco_venda']}")
        col5.write(row["estoque"])

    st.markdown('</div>', unsafe_allow_html=True)
