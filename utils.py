# utils.py
import streamlit as st
import pandas as pd

CAMINHO_USUARIOS = "base de dados/usuarios.csv"

def carregar_usuario_logado():
    if "usuario" in st.session_state and st.session_state.usuario:
        usuarios = pd.read_csv(CAMINHO_USUARIOS, dtype=str)
        usuarios.set_index("usuario", inplace=True)
        return usuarios.loc[st.session_state.usuario].to_dict()
    return None

def hash_senha(senha):
    import hashlib
    return hashlib.md5(senha.encode()).hexdigest()

def verificar_credenciais(usuario, senha):
    try:
        usuarios = pd.read_csv(CAMINHO_USUARIOS, dtype=str)
        usuarios.set_index("usuario", inplace=True)
        if usuario in usuarios.index:
            return usuarios.loc[usuario]["senha"] == hash_senha(senha)
        return False
    except:
        return False

def menu_lateral(usuario):
    with st.sidebar:
        st.image("logo.png", width=120)
        st.markdown(f"**{usuario['nome']}**")
        st.markdown(f"{usuario.get('email', '')}")
        st.markdown("---")

        pagina = st.radio("Menu", [
            "🏠 Dashboard",
            "🏆 Licitações",
            "🏢 Fornecedores",
            "🏭 Concorrentes",
            "📦 Produtos",
            "💲 Precificação",
            "📈 Relatórios",
            "👤 Meu Perfil"
        ])

        if pagina == "👤 Meu Perfil":
            st.switch_page("perfil_usuario.py")
        elif pagina == "🏠 Dashboard":
            st.switch_page("pages/1_📊_Dashboard.py")
        elif pagina == "🏆 Licitações":
            st.switch_page("pages/2_🏆_Licitações.py")
        elif pagina == "🏢 Fornecedores":
            st.switch_page("pages/3_📁_Fornecedores.py")
        elif pagina == "🏭 Concorrentes":
            st.switch_page("pages/4_🏭_Concorrentes.py")
        elif pagina == "📦 Produtos":
            st.switch_page("pages/5_📦_Produtos.py")
        elif pagina == "💲 Precificação":
            st.switch_page("pages/6_💲_Precificação.py")
        elif pagina == "📈 Relatórios":
            st.switch_page("pages/7_📈_Relatórios.py")
