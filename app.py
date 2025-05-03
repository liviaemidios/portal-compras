import streamlit as st
from login import login_page, get_current_user
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"
st.set_page_config(page_title="Portal de Compras", layout="wide")

# Verifica login
if not st.session_state.get("usuario"):
    login_page()
    st.stop()

usuario = get_current_user()
if usuario is None:
    st.error("Erro ao carregar o usuário.")
    st.stop()

# Controla a página ativa
if "pagina" not in st.session_state:
    st.session_state.pagina = "dashboard"

# Verifica se há parâmetro na URL
if "pagina" in st.query_params:
    st.session_state.pagina = st.query_params["pagina"]

# Estilo do menu
st.markdown("""
<style>
.sidebar-button {
    display: block;
    padding: 0.6rem 1rem;
    margin: 0.3rem 0;
    background-color: #e9f2fb;
    border-radius: 8px;
    color: #003366;
    font-weight: 500;
    text-decoration: none;
    transition: background-color 0.3s;
}
.sidebar-button:hover {
    background-color: #d8e7f9;
    cursor: pointer;
}
.sidebar-button.active {
    background-color: #3879bd;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Menu lateral
menu = {
    "🏠 Dashboard": "dashboard",
    "👤 Meu Perfil": "perfil",
    "🚪 Sair": "sair"
}

with st.sidebar:
    st.markdown(f"**Usuário:** {usuario['nome']}")
    st.markdown("---")

    for nome, valor in menu.items():
        ativo = "active" if st.session_state.pagina == valor else ""
        st.markdown(
            f"<div class='sidebar-button {ativo}' onclick=\"window.location.href='?pagina={valor}'\">{nome}</div>",
            unsafe_allow_html=True
        )

# Conteúdo das páginas
if st.session_state.pagina == "dashboard":
    st.title("📊 Dashboard")
    st.success(f"Bem-vinda, {usuario['nome']}!")
    st.info("Este é seu painel inicial.")

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
