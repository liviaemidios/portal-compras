import streamlit as st
import hashlib
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"

def iniciar_usuarios():
    if not os.path.exists(CAMINHO_USUARIOS):
        df = pd.DataFrame(columns=["usuario", "senha", "nome", "email", "foto"])
        df.to_csv(CAMINHO_USUARIOS, index=False)

def hash_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def carregar_usuarios():
    if os.path.exists(CAMINHO_USUARIOS):
        df = pd.read_csv(CAMINHO_USUARIOS)
        return df.set_index("usuario")
    else:
        return pd.DataFrame(columns=["usuario", "senha", "nome", "email", "foto"]).set_index("usuario")

def login_page():
    iniciar_usuarios()
    st.title("🔐 Login do Sistema")
    aba = st.radio("", ["Entrar", "Cadastrar"])

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

    elif aba == "Cadastrar":
        with st.form("form_cadastro"):
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            usuario = st.text_input("Nome de usuário")
            senha = st.text_input("Senha", type="password")
            foto = st.text_input("URL da foto de perfil (opcional)")
            if st.form_submit_button("Cadastrar"):
                usuarios = carregar_usuarios()
                if usuario in usuarios.index:
                    st.warning("Esse nome de usuário já está em uso.")
                else:
                    novo = pd.DataFrame([[usuario, hash_senha(senha), nome, email, foto]], columns=["usuario", "senha", "nome", "email", "foto"])
                    usuarios = pd.concat([usuarios, novo])
                    usuarios.to_csv(CAMINHO_USUARIOS)
                    st.success("Usuário cadastrado com sucesso! Faça login.")

def get_current_user():
    usuarios = carregar_usuarios()
    if "usuario" in st.session_state and st.session_state.usuario in usuarios.index:
        return usuarios.loc[st.session_state.usuario].to_dict()
    return None
