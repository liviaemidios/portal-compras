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
    .stButton > button {
        width: 100%;
        text-align: left;
        padding: 0.6rem 1rem;
        margin-bottom: 0.3rem;
        border-radius: 8px;
        border: none;
        background-color: #e9f2fb;
        color: #003366;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #d8e7f9;
        cursor: pointer;
    }
    .stButton.active > button {
        background-color: #3879bd !important;
        color: white !important;
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

    for nome, valor in menu.items():
        container = st.container()
        if st.session_state.pagina == valor:
            with container:
                st.markdown('<div class="stButton active">', unsafe_allow_html=True)
                if st.button(nome, key=f"menu_{valor}"):
                    st.session_state.pagina = valor
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            with container:
                st.markdown('<div class="stButton">', unsafe_allow_html=True)
                if st.button(nome, key=f"menu_{valor}"):
                    st.session_state.pagina = valor
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
    if "editando" not in st.session_state:
        st.session_state.editando = None

    if st.button("➕ Cadastrar Novo Fornecedor"):
        st.session_state.mostrar_formulario = not st.session_state.mostrar_formulario
        st.session_state.editando = None

    if st.session_state.mostrar_formulario or st.session_state.editando is not None:
        st.subheader("📋 Cadastro de Fornecedor")

        fornecedores_df = pd.read_csv(CAMINHO_FORNECEDORES, dtype=str) if os.path.exists(CAMINHO_FORNECEDORES) else pd.DataFrame(columns=["cnpj", "nome", "email", "telefone", "endereco"])

        if st.session_state.editando is not None:
            dados = fornecedores_df.loc[st.session_state.editando]
            cnpj = st.text_input("CNPJ", value=dados["cnpj"])
            nome = st.text_input("Nome da Empresa", value=dados["nome"])
            email = st.text_input("E-mail", value=dados["email"])
            telefone = st.text_input("Telefone", value=dados["telefone"])
            endereco = st.text_area("Endereço", value=dados["endereco"])
            botao_salvar = st.button("💾 Salvar Alterações")

            if botao_salvar:
                fornecedores_df.loc[st.session_state.editando] = [cnpj, nome, email, telefone, endereco]
                fornecedores_df.to_csv(CAMINHO_FORNECEDORES, index=False)
                st.success("Fornecedor atualizado com sucesso!")
                st.session_state.editando = None
                st.session_state.mostrar_formulario = False
                st.rerun()
        else:
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
                col1, col2, col3 = st.columns([5, 4, 3])
                col1.markdown(f"**{row['nome']}**  \n📧 {row['email']}  \n📞 {row['telefone']}")
                col2.markdown(f"CNPJ: {row['cnpj']}  \n📍 {row['endereco']}")
                with col3:
                    if st.button("🔍", key=f"ver_{i}", help="Visualizar detalhes"):
                        st.info(f"Detalhes do fornecedor:\n{row.to_string()}")
                    if st.button("✏️", key=f"edit_{i}", help="Editar"):
                        st.session_state.editando = i
                        st.session_state.mostrar_formulario = True
                        st.rerun()
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
