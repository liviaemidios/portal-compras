import streamlit as st
from login import login_page, get_current_user
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"

st.set_page_config(page_title="Portal de Compras", layout="wide")

query_params = st.query_params
if "usuario" not in st.session_state or not st.session_state.get("usuario"):
    if "usuario" in query_params:
        st.session_state.usuario = query_params["usuario"]

if not st.session_state.get("usuario"):
    login_page()
    st.stop()

usuario = get_current_user()
if usuario is None:
    st.error("Erro: não foi possível carregar os dados do usuário.")
    st.stop()

st.sidebar.markdown(f"**Usuário:** {usuario['nome']}")
st.title("🎯 Painel Principal")
st.write("Bem-vinda ao sistema!")
