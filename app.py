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

if st.session_state.usuario is None:
    login_page()
else:
    usuario = get_current_user()
    st.sidebar.markdown(f"**Usuário:** {usuario['nome']}")
    pagina = st.sidebar.radio("Menu", ["👤 Meu Perfil", "🏠 Dashboard", "🏢 Fornecedores", "🚚 Distribuidoras", "📦 Produtos", "💰 Comparador de Preços", "📊 Relatórios", "🚪 Sair"])

    if pagina == "🏠 Dashboard":
        st.title("Bem-vindo ao Portal de Compras Internas")
        st.info("Selecione uma das opções no menu à esquerda.")

    elif pagina == "🏢 Fornecedores":
        pagina_fornecedores()

    elif pagina == "🚚 Distribuidoras":
        pagina_distribuidoras()

    elif pagina == "📦 Produtos":
        pagina_produtos()

    elif pagina == "💰 Comparador de Preços":
        pagina_comparador()

    elif pagina == "📊 Relatórios":
        pagina_relatorios()

    elif pagina == "👤 Meu Perfil":
        st.subheader("Meu Perfil")
        if usuario.get("foto") and os.path.exists(usuario["foto"]):
            st.image(usuario["foto"], width=150)
        else:
            st.info("Nenhuma foto cadastrada.")

        st.markdown(f"**Nome:** {usuario['nome']}")
        st.markdown(f"**E-mail:** {usuario['email']}")

        st.markdown("---")
        st.markdown("### 📸 Atualizar Foto de Perfil")
        nova_foto = st.file_uploader("Selecione uma imagem", type=["png", "jpg", "jpeg"])
        if nova_foto:
            pasta_fotos = "fotos_perfil"
            os.makedirs(pasta_fotos, exist_ok=True)
            caminho_foto = os.path.join(pasta_fotos, f"{st.session_state.usuario}.jpg")
            with open(caminho_foto, "wb") as f:
                f.write(nova_foto.getbuffer())

            # Atualiza CSV
            df = pd.read_csv(CAMINHO_USUARIOS)
            df.loc[df["usuario"] == st.session_state.usuario, "foto"] = caminho_foto
            df.to_csv(CAMINHO_USUARIOS, index=False)

            st.success("Foto de perfil atualizada com sucesso!")
            st.rerun()

    elif pagina == "🚪 Sair":
        st.session_state.usuario = None
        st.rerun()
