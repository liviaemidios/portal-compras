import streamlit as st
from login import login_page, get_current_user
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"
st.set_page_config(page_title="Portal de Compras", layout="wide")

# Recuperar login pela URL se necessário
query_params = st.query_params
if "usuario" not in st.session_state or not st.session_state.get("usuario"):
    if "usuario" in query_params:
        st.session_state.usuario = query_params["usuario"]

# Tela de login se não autenticado
if not st.session_state.get("usuario"):
    login_page()
    st.stop()

# Carrega dados do usuário logado
usuario = get_current_user()
if usuario is None:
    st.error("Erro ao carregar o usuário.")
    st.stop()

# Página ativa
if "pagina" not in st.session_state:
    st.session_state.pagina = "dashboard"

# Estilo menu lateral
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
    "🚪 Sair": "sair"
}

with st.sidebar:
    st.markdown(f"**Usuário:** {usuario['nome']}")
    foto = usuario.get("foto")
    if isinstance(foto, str) and foto.strip() and os.path.exists(foto):
        st.image(foto, width=120)
    else:
        st.image("logo.png", width=120)

    if st.button("👤 Meu Perfil"):
        st.session_state.pagina = "meu_perfil"

    st.markdown("---")
    for nome, valor in menu.items():
        ativo = "active" if st.session_state.pagina == valor else ""
        if st.markdown(f"<a class='sidebar-button {ativo}' href='#' onclick=\"window.location.reload()\">{nome}</a>", unsafe_allow_html=True):
            st.session_state.pagina = valor

# Conteúdo principal
if st.session_state.pagina == "dashboard":
    st.image("logo.png", width=200)
    st.title("Bem-vindo ao Portal de Compras Internas")
    st.info("Selecione uma das opções no menu à esquerda.")

elif st.session_state.pagina == "meu_perfil":
    st.subheader("👤 Meu Perfil")
    st.write(f"Nome: {usuario['nome']}")
    st.write(f"E-mail: {usuario['email']}")
    st.write(f"CPF: {usuario.get('cpf', '')}")
    st.write(f"Telefone: {usuario.get('tel_celular', '')}")

elif st.session_state.pagina == "sair":
    st.session_state.usuario = None
    st.session_state.pagina = None
    st.rerun()
