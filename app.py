import streamlit as st
from login import login_page, get_current_user
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"
CAMINHO_FORNECEDORES = "database/fornecedores.csv"

st.set_page_config(page_title="Portal de Compras", layout="wide")

# Verifica login
if not st.session_state.get("usuario"):
    login_page()
    st.stop()

usuario = get_current_user()
if usuario is None:
    st.error("Erro ao carregar o usuário.")
    st.stop()

# Página ativa
if "pagina" not in st.session_state:
    st.session_state.pagina = "dashboard"

# Estilo do menu
st.markdown("""
<style>
.sidebar-container div {
    display: block;
    padding: 0.6rem 1rem;
    margin: 0.3rem 0;
    border-radius: 8px;
    color: #003366;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s;
}
.sidebar-container div:hover {
    background-color: #d8e7f9;
}
.sidebar-container .active {
    background-color: #3879bd;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Menu lateral
menu = {
    "🏠 Dashboard": "dashboard",
    "🏢 Fornecedores": "fornecedores",
    "👤 Meu Perfil": "perfil",
    "🚪 Sair": "sair"
}

with st.sidebar:
    st.markdown(f"**Usuário:** {usuario['nome']}")
    st.markdown("---")
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    for nome, valor in menu.items():
        ativo = "active" if st.session_state.pagina == valor else ""
        if st.button(f"{nome}", key=f"menu_{valor}"):
            st.session_state.pagina = valor
        st.markdown(f'<div class="{ativo}">{nome}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Conteúdo das páginas
if st.session_state.pagina == "dashboard":
    st.title("📊 Dashboard")
    st.success(f"Bem-vinda, {usuario['nome']}!")
    st.info("Este é seu painel inicial.")

elif st.session_state.pagina == "fornecedores":
    st.title("🏢 Fornecedores")

    if "mostrar_formulario" not in st.session_state:
        st.session_state.mostrar_formulario = False

    if st.button("➕ Cadastrar Novo Fornecedor"):
        st.session_state.mostrar_formulario = not st.session_state.mostrar_formulario

    if st.session_state.mostrar_formulario:
        st.subheader("📋 Cadastro de Fornecedor")

        with st.form("form_fornecedor"):
            cnpj = st.text_input("CNPJ")
            nome = st.text_input("Nome da Empresa")
            email = st.text_input("E-mail")
            telefone = st.text_input("Telefone")
            endereco = st.text_area("Endereço")
            submit = st.form_submit_button("Salvar")

            if submit:
                novo = pd.DataFrame([{
                    "cnpj": cnpj,
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "endereco": endereco
                }])
                if os.path.exists(CAMINHO_FORNECEDORES):
                    df_antigo = pd.read_csv(CAMINHO_FORNECEDORES, dtype=str)
                    df_final = pd.concat([df_antigo, novo], ignore_index=True)
                else:
                    df_final = novo
                df_final.to_csv(CAMINHO_FORNECEDORES, index=False)
                st.success("Fornecedor cadastrado com sucesso!")
                st.rerun()

    st.markdown("### 🔍 Buscar fornecedor")
    busca = st.text_input("Buscar por nome, CNPJ ou e-mail").lower()

    if os.path.exists(CAMINHO_FORNECEDORES):
        fornecedores = pd.read_csv(CAMINHO_FORNECEDORES, dtype=str)

        if busca:
            fornecedores = fornecedores[
                fornecedores.apply(lambda row: busca in row.astype(str).str.lower().to_string(), axis=1)
            ]

        for i, row in fornecedores.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([4, 3, 2, 3])
                col1.markdown(f"**{row['nome']}**  \n📧 {row['email']}  \n📞 {row['telefone']}")
                col2.markdown(f"CNPJ: {row['cnpj']}  \n📍 {row['endereco']}")
                with col3:
                    if st.button("🔍", key=f"ver_{i}", help="Visualizar detalhes"):
                        st.info(f"Detalhes do fornecedor:\n{row.to_string()}")
                    if st.button("✏️", key=f"edit_{i}", help="Editar (em breve)"):
                        st.warning("Função de edição ainda não implementada.")
                    if st.button("🗑️", key=f"del_{i}", help="Excluir"):
                        fornecedores = fornecedores.drop(i)
                        fornecedores.to_csv(CAMINHO_FORNECEDORES, index=False)
                        st.success("Fornecedor excluído com sucesso.")
                        st.rerun()
    else:
        st.info("Nenhum fornecedor cadastrado ainda.")

elif st.session_state.pagina == "perfil":
    st.title("👤 Meu Perfil")
    st.write(f"Nome: {usuario['nome']}")
    st.write(f"Usuário: {st.session_state.usuario}")

elif st.session_state.pagina == "sair":
    st.session_state.usuario = None
    st.session_state.pagina = None
    st.rerun()

else:
    st.warning("Página não encontrada.")
