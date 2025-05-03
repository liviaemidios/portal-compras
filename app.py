import streamlit as st
from fornecedores import pagina_fornecedores
from distribuidoras import pagina_distribuidoras
from produtos import pagina_produtos
from comparador import pagina_comparador
from relatorios import pagina_relatorios
from login import login_page, get_current_user
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"

st.set_page_config(page_title="Portal de Compras", layout="wide")

if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina" not in st.session_state:
    st.session_state.pagina = None

if st.session_state.usuario is None:
    login_page()
else:
    usuario = get_current_user()

    with st.sidebar:
        st.markdown(f"**Usuário:** {usuario['nome']}")
        if st.button("👤 Meu Perfil"):
            st.session_state.pagina = "meu_perfil"
        pagina = st.radio("Menu", [
            "🏠 Dashboard",
            "🏢 Fornecedores",
            "🚚 Distribuidoras",
            "📦 Produtos",
            "💰 Comparador de Preços",
            "📊 Relatórios",
            "🚪 Sair"
        ])

    if st.session_state.pagina == "meu_perfil":
        st.subheader("👤 Meu Perfil")

        if usuario.get("foto") and os.path.exists(usuario["foto"]):
            st.image(usuario["foto"], width=150)
            if st.button("🗑️ Remover Foto"):
                try:
                    os.remove(usuario["foto"])
                except:
                    pass
                df = pd.read_csv(CAMINHO_USUARIOS)
                df.loc[df["usuario"] == st.session_state.usuario, "foto"] = ""
                df.to_csv(CAMINHO_USUARIOS, index=False)
                st.success("Foto removida com sucesso.")
                st.rerun()
        else:
            st.info("Nenhuma foto de perfil cadastrada.")

        st.markdown(f"**Nome:** {usuario['nome']}")
        st.markdown(f"**E-mail:** {usuario['email']}")

        with st.form("form_perfil"):
            cpf = st.text_input("CPF", value=usuario.get("cpf", ""))
            rg = st.text_input("RG", value=usuario.get("rg", ""))
            data_nasc = st.date_input("Data de Nascimento", value=pd.to_datetime(usuario.get("data_nascimento", "2000-01-01")))
            endereco = st.text_area("Endereço", value=usuario.get("endereco", ""))
            fixo = st.text_input("Telefone Fixo", value=usuario.get("tel_fixo", ""))
            celular = st.text_input("Telefone Celular", value=usuario.get("tel_celular", ""))

            nova_foto = st.file_uploader("Atualizar Foto de Perfil", type=["png", "jpg", "jpeg"])
            if st.form_submit_button("Salvar Perfil"):
                df = pd.read_csv(CAMINHO_USUARIOS)
                idx = df[df["usuario"] == st.session_state.usuario].index[0]

                df.at[idx, "cpf"] = cpf
                df.at[idx, "rg"] = rg
                df.at[idx, "data_nascimento"] = data_nasc
                df.at[idx, "endereco"] = endereco
                df.at[idx, "tel_fixo"] = fixo
                df.at[idx, "tel_celular"] = celular

                if nova_foto:
                    os.makedirs("fotos_perfil", exist_ok=True)
                    caminho_foto = f"fotos_perfil/{st.session_state.usuario}.jpg"
                    with open(caminho_foto, "wb") as f:
                        f.write(nova_foto.getbuffer())
                    df.at[idx, "foto"] = caminho_foto

                df.to_csv(CAMINHO_USUARIOS, index=False)
                st.success("Perfil atualizado com sucesso!")
                st.session_state.pagina = None
                st.rerun()

    elif pagina == "🏠 Dashboard":
        st.image("https://i.imgur.com/mA7iFd8.png", width=200)
        st.title("Bem-vindo ao Portal de Compras Internas")
        st.info("Selecione uma das opções no menu à esquerda.")

    elif pagina == "🏢 Fornecedores":
        st.session_state.pagina = None
        pagina_fornecedores()

    elif pagina == "🚚 Distribuidoras":
        st.session_state.pagina = None
        pagina_distribuidoras()

    elif pagina == "📦 Produtos":
        st.session_state.pagina = None
        pagina_produtos()

    elif pagina == "💰 Comparador de Preços":
        st.session_state.pagina = None
        pagina_comparador()

    elif pagina == "📊 Relatórios":
        st.session_state.pagina = None
        pagina_relatorios()

    elif pagina == "🚪 Sair":
        st.session_state.usuario = None
        st.session_state.pagina = None
        st.rerun()
