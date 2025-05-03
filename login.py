import streamlit as st
import hashlib
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"

def iniciar_usuarios():
    if not os.path.exists(CAMINHO_USUARIOS):
        df = pd.DataFrame(columns=[
            "usuario", "senha", "nome", "email", "foto",
            "cpf", "rg", "data_nascimento", "endereco",
            "tel_fixo", "tel_celular"
        ])
        df.to_csv(CAMINHO_USUARIOS, encoding="utf-8", index=False)

def hash_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def carregar_usuarios():
    df = pd.read_csv(CAMINHO_USUARIOS, dtype=str)
    df.set_index("usuario", inplace=True)
    return df

def login_page():
    if st.session_state.get("usuario"):
        return

    iniciar_usuarios()
    aba = st.radio("", ["Entrar", "Cadastrar"], horizontal=True)

    if aba == "Entrar":
        usuario = st.text_input("Usuário").strip().lower()
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            usuarios = carregar_usuarios()
            if usuario in usuarios.index and usuarios.loc[usuario, "senha"] == hash_senha(senha):
                st.session_state.usuario = usuario
                st.session_state.pagina = "dashboard"
                st.query_params.update({"usuario": usuario})
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    elif aba == "Cadastrar":
        with st.form("form_cadastro"):
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            usuario = st.text_input("Nome de usuário").strip().lower()
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Cadastrar"):
                usuarios = carregar_usuarios()
                if usuario in usuarios.index:
                    st.warning("Esse nome de usuário já está em uso.")
                else:
                    novo = pd.DataFrame([{
                        "usuario": usuario,
                        "senha": hash_senha(senha),
                        "nome": nome,
                        "email": email,
                        "foto": "",
                        "cpf": "",
                        "rg": "",
                        "data_nascimento": "",
                        "endereco": "",
                        "tel_fixo": "",
                        "tel_celular": ""
                    }])
                    usuarios = pd.concat([usuarios.reset_index(), novo], ignore_index=True)
                    usuarios.to_csv(CAMINHO_USUARIOS, index=False, encoding="utf-8")
                    st.success("Usuário cadastrado com sucesso! Faça login.")

def get_current_user():
    usuarios = carregar_usuarios()
    if "usuario" in st.session_state and st.session_state.usuario in usuarios.index:
        return usuarios.loc[st.session_state.usuario].to_dict()
    return None
