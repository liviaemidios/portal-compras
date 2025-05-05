# app.py
import streamlit as st
from setup import inicializar_sistema
import login

st.set_page_config(page_title="Portal Interno de Compras", layout="wide")

# Inicializa arquivos necessários
inicializar_sistema()

# Login
if "usuario" not in st.session_state:
    login.login_page()
else:
    pagina = st.sidebar.radio("Menu", [
        "🏠 Dashboard",
        "🏆 Licitações",
        "🏢 Fornecedores",
        "🏭 Concorrentes",
        "📦 Produtos",
        "💲 Precificação",
        "📈 Relatórios"
    ])

    if pagina == "🏠 Dashboard":
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
