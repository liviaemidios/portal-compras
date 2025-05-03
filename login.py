import streamlit as st
import hashlib
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"

def iniciar_usuarios():
    if not os.path.exists(CAMINHO_USUARIOS):
        df = pd.DataFrame(columns=[
            "senha", "nome", "email", "foto",
            "cpf", "rg", "data_nascimento", "endereco",
            "tel_fixo", "tel_celular"
        ])
        df.index.name = "usuario"
        df.to_csv(CAMINHO_USUARIOS, encoding="utf-8")

def hash_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def carregar_usuarios():
    # ✅ Lê o arquivo com a coluna 'usuario' como índice
    return pd.read_csv(CAMINHO_USUARIOS, index_col="usuario", dtype=str)

def login_page():
    iniciar_usuarios()

    st.markdown("""
        <style>
            .block-container { padding-top: 3rem; }
            .login-box {
                background-color: #f9f9f9;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                margin: auto;
            }
            .login-title {
                text-align: center;
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.image("logo.png", width=150)
    aba = st.radio("", ["Entrar", "Cadastrar"], horizontal=True)

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    if aba == "Entrar":
        st.markdown("<div class='login-title'>Acesso ao Portal</div>", unsafe_allow_html=True)
        usuario = st.text_input("Usuário").strip().lower()
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            usuarios = carregar_usuarios()
            st.write("DEBUG >> Tentando logar:", usuario)
            st.write("DEBUG >> Usuários disponíveis:", list(usuarios.index))
            if usuario in usuarios.index and usuarios.loc[usuario, "senha"] == hash_senha(senha):
                st.session_state.usuario = usuario
                st.session_state.pagina = "dashboard"
                st.success("Login realizado com sucesso.")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    elif aba == "Cadastrar":
        st.markdown("<div class='login-title'>Cadastro de Novo Usuário</div>", unsafe_allow_html=True)
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
                    }], index=[usuario])
                    usuarios = pd.concat([usuarios, novo])
                    usuarios.to_csv(CAMINHO_USUARIOS, encoding="utf-8")
                    st.success("Usuário cadastrado com sucesso! Faça login.")

    st.markdown("</div>", unsafe_allow_html=True)

def get_current_user():
    usuarios = carregar_usuarios()
    st.write("DEBUG >> session_state.usuario:", st.session_state.get("usuario"))
    st.write("DEBUG >> usuarios.index:", list(usuarios.index))
    if "usuario" in st.session_state and st.session_state.usuario in usuarios.index:
        return usuarios.loc[st.session_state.usuario].to_dict()
    return None
