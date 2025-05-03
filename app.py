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
    return pd.DataFrame(columns=["razao_social", "nome_fantasia", "cnpj", "telefone", "email", "endereco"])

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
            <button onclick=\"window.location.reload();\">➕ Cadastrar Novo Fornecedor</button>
            <input type='text' id='busca' name='busca' placeholder='Buscar...' style='height: 2.2rem; padding: 0 0.5rem;' />
            <button style='height: 2.2rem;'>🔍</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
            if st.button("Fechar visualização"):
                st.session_state.visualizando = None

    if st.session_state.editando is not None:
        if st.session_state.editando == -1:
            dados = {"razao_social": "", "nome_fantasia": "", "cnpj": "", "telefone": "", "email": "", "endereco": ""}
        else:
            dados = fornecedores.loc[st.session_state.editando]

        with st.expander("✏️ Editar Fornecedor", expanded=True):
            with st.form("form_edit_fornecedor"):
                razao_social = st.text_input("Razão Social", value=dados['razao_social'])
                nome_fantasia = st.text_input("Nome Fantasia", value=dados['nome_fantasia'])
                cnpj = st.text_input("CNPJ", value=dados['cnpj'])
                telefone = st.text_input("Telefone", value=dados['telefone'])
                email = st.text_input("E-mail", value=dados['email'])
                endereco = st.text_area("Endereço", value=dados['endereco'])
                col_a, col_b, col_c = st.columns(3)
                salvar = col_a.form_submit_button("Salvar")
                cancelar = col_b.form_submit_button("Cancelar")
                fechar = col_c.form_submit_button("Fechar")

                if salvar:
                    novo = pd.DataFrame([{
                        "razao_social": razao_social,
                        "nome_fantasia": nome_fantasia,
                        "cnpj": cnpj,
                        "telefone": telefone,
                        "email": email,
                        "endereco": endereco
                    }])
                    if st.session_state.editando == -1:
                        fornecedores = pd.concat([fornecedores, novo], ignore_index=True)
                    else:
                        fornecedores.loc[st.session_state.editando] = novo.iloc[0]
                    salvar_fornecedores(fornecedores)
                    st.success("Fornecedor salvo com sucesso!")
                    st.session_state.editando = None
                    st.rerun()
                elif cancelar or fechar:
                    st.session_state.editando = None
                    st.rerun()
