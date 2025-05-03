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
if "subpagina" not in st.session_state:
    st.session_state.subpagina = "lista"
if "editando" not in st.session_state:
    st.session_state.editando = None

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
    st.session_state.subpagina = "lista"

# Página de fornecedores
if st.session_state.pagina == "fornecedores":
    if st.session_state.subpagina == "lista":
        st.title("🏢 Fornecedores")

        st.markdown("### 🔍 Buscar fornecedor")
        busca = st.text_input("Buscar por razão social, fantasia, CNPJ ou e-mail").lower()

        if st.button("➕ Cadastrar Novo Fornecedor"):
            st.session_state.subpagina = "cadastro"
            st.stop()

        fornecedores = carregar_fornecedores()

        if busca:
            fornecedores = fornecedores[fornecedores.apply(lambda row: busca in row.astype(str).str.lower().to_string(), axis=1)]

        st.markdown("### Lista de Fornecedores")
        for i, row in fornecedores.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([5, 4, 3])
                col1.markdown(f"**{row['razao_social']}**  \\ Fantasia: {row['nome_fantasia']}  \\ 📞 {row['telefone']}")
                col2.markdown(f"📧 {row['email']}  \\ CNPJ: {row['cnpj']}")
                with col3:
                    if st.button("🔍", key=f"ver_{i}", help="Visualizar detalhes"):
                        st.info(f"{row.to_string()}")
                    if st.button("✏️", key=f"edit_{i}", help="Editar"):
                        st.session_state.editando = i
                        st.session_state.subpagina = "cadastro"
                        st.stop()
                    if st.button("🗑️", key=f"del_{i}", help="Excluir"):
                        fornecedores = fornecedores.drop(i).reset_index(drop=True)
                        salvar_fornecedores(fornecedores)
                        st.success("Fornecedor excluído com sucesso.")
                        st.rerun()

    elif st.session_state.subpagina == "cadastro":
        st.title("📋 Cadastro de Fornecedor")

        fornecedores = carregar_fornecedores()
        editar = st.session_state.editando is not None

        if editar:
            dados = fornecedores.loc[st.session_state.editando]
        else:
            dados = {"razao_social": "", "nome_fantasia": "", "cnpj": "", "telefone": "", "email": "", "endereco": ""}

        if st.button("🔙 Voltar"):
            st.session_state.subpagina = "lista"
            st.session_state.editando = None
            st.rerun()

        with st.form("form_fornecedor"):
            razao_social = st.text_input("Razão Social", value=dados["razao_social"])
            nome_fantasia = st.text_input("Nome Fantasia", value=dados["nome_fantasia"])
            cnpj = st.text_input("CNPJ", value=dados["cnpj"])
            telefone = st.text_input("Telefone", value=dados["telefone"])
            email = st.text_input("E-mail", value=dados["email"])
            endereco = st.text_area("Endereço", value=dados["endereco"])
            submit = st.form_submit_button("Salvar")

            if submit:
                novo = pd.DataFrame([{
                    "razao_social": razao_social,
                    "nome_fantasia": nome_fantasia,
                    "cnpj": cnpj,
                    "telefone": telefone,
                    "email": email,
                    "endereco": endereco
                }])

                if editar:
                    fornecedores.loc[st.session_state.editando] = novo.iloc[0]
                else:
                    fornecedores = pd.concat([fornecedores, novo], ignore_index=True)

                salvar_fornecedores(fornecedores)
                st.success("Fornecedor salvo com sucesso!")
                st.session_state.subpagina = "lista"
                st.session_state.editando = None
                st.rerun()
