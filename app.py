import streamlit as st
import pandas as pd
import os
from login import login_page, get_current_user

CAMINHO_FORNECEDORES = "database/fornecedores.csv"

st.set_page_config(page_title="Portal de Compras", layout="wide")

if not st.session_state.get("usuario"):
    login_page()
    st.stop()

usuario = get_current_user()
if usuario is None:
    st.error("Erro ao carregar o usuário.")
    st.stop()

if "pagina" not in st.session_state:
    st.session_state.pagina = "fornecedores"
if "editando" not in st.session_state:
    st.session_state.editando = None
if "visualizando" not in st.session_state:
    st.session_state.visualizando = None
if "cadastrando" not in st.session_state:
    st.session_state.cadastrando = False

st.markdown("""
<style>
.small-icon {
    font-size: 0.8rem;
    padding: 0.2rem 0.4rem;
    margin: 0 0.2rem;
}
.search-box input {
    width: 150px !important;
    display: inline;
}
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

def carregar_fornecedores():
    if os.path.exists(CAMINHO_FORNECEDORES):
        return pd.read_csv(CAMINHO_FORNECEDORES, dtype=str)
    return pd.DataFrame(columns=["razao_social", "nome_fantasia", "cnpj", "telefone", "email", "endereco", "inscricao_estadual", "inscricao_municipal", "pedido_minimo", "prazo_pagamento"])

def salvar_fornecedores(df):
    df.to_csv(CAMINHO_FORNECEDORES, index=False)

st.sidebar.markdown(f"**Usuário:** {usuario['nome']}")
st.sidebar.markdown("---")
if st.sidebar.button("🏢 Fornecedores"):
    st.session_state.pagina = "fornecedores"

if st.session_state.pagina == "fornecedores":
    st.markdown("""
    <div class='title-row'>
        <h1>🏢 Fornecedores</h1>
        <div class='actions'>
            <form method='post'>
                <button name='cadastrar' type='submit'>➕ Cadastrar Novo Fornecedor</button>
            </form>
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
                    st.rerun()
                elif cancelar:
                    st.session_state.cadastrando = False
                    st.rerun()

    fornecedores = carregar_fornecedores()

    busca = st.session_state.get("busca", "")
    if busca:
        fornecedores = fornecedores[fornecedores.apply(lambda row: busca.lower() in row.astype(str).str.lower().to_string(), axis=1)]

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
                st.rerun()

    if st.session_state.visualizando is not None:
        fornecedor = fornecedores.loc[st.session_state.visualizando]
        with st.expander("🔍 Detalhes do Fornecedor", expanded=True):
            st.markdown(f"**Razão Social:** {fornecedor['razao_social']}")
            st.markdown(f"**Fantasia:** {fornecedor['nome_fantasia']}")
            st.markdown(f"**CNPJ:** {fornecedor['cnpj']}")
            st.markdown(f"**E-mail:** {fornecedor['email']}")
            st.markdown(f"**Telefone:** {fornecedor['telefone']}")
            st.markdown(f"**Endereço:** {fornecedor['endereco']}")
            st.markdown(f"**Inscrição Estadual:** {fornecedor.get('inscricao_estadual', '')}")
            st.markdown(f"**Inscrição Municipal:** {fornecedor.get('inscricao_municipal', '')}")
            st.markdown(f"**Pedido Mínimo:** {fornecedor.get('pedido_minimo', '')}")
            st.markdown(f"**Prazo de Pagamento:** {fornecedor.get('prazo_pagamento', '')}")
            if st.button("Fechar visualização"):
                st.session_state.visualizando = None
