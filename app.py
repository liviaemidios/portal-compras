import streamlit as st
from login import login_page, get_current_user

st.set_page_config(page_title="Portal de Compras", layout="wide")

# Verifica se está logado
if not st.session_state.get("usuario"):
    login_page()
    st.stop()

usuario = get_current_user()
if usuario is None:
    st.error("Erro ao carregar o usuário.")
    st.stop()

# Conteúdo da página inicial
st.sidebar.title("Menu")
st.sidebar.markdown(f"👤 {usuario['nome']}")
if st.sidebar.button("Sair"):
    st.session_state.usuario = None
    st.rerun()

st.title("Painel Inicial")
st.success(f"Bem-vinda, {usuario['nome']}!")
