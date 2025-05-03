import streamlit as st
import hashlib
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"

def hash_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def carregar_usuarios():
    if not os.path.exists(CAMINHO_USUARIOS):
        return pd.DataFrame(columns=["usuario", "senha", "nome"])
    df = pd.read_csv(CAMINHO_USUARIOS, dtype=str)
    df.set_index("usuario", inplace=True)
    return df

def login_page():
    if st.session_state.get("usuario"):
        return

    aba = st.radio("Acesso", ["Entrar", "Cadastrar"], horizontal=True)

    if aba == "Entrar":
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            usuarios = carregar_usuarios()
            if usuario in usuarios.index and usuarios.loc[usuario, "senha"] == hash_senha(senha):
                st.session_state.usuario = usuario
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

def get_current_user():
    usuarios = carregar_usuarios()
    if "usuario" in st.session_state and st.session_state.usuario in usuarios.index:
        return usuarios.loc[st.session_state.usuario].to_dict()
    return None
