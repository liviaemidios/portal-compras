import streamlit as st
from setup import inicializar_sistema
from login import login_page, get_current_user
import distribuidoras as mod_distribuidoras
import produtos as mod_produtos
import fornecedores as mod_fornecedores

inicializar_sistema()  # Garante que os arquivos CSV existam

st.set_page_config(page_title="Portal Interno de Compras", layout="wide")

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if st.session_state.usuario is None:
    login_page()
    st.stop()

usuario = get_current_user()

# Menu lateral
with st.sidebar:
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            padding-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(f"### 👤 {usuario['nome']}")

    menu = st.radio("", [
        "🏢 Fornecedores",
        "🚚 Distribuidoras",
        "📦 Produtos"
    ], label_visibility="collapsed")

# Rotas do menu
if menu == "🏢 Fornecedores":
    mod_fornecedores.renderizar_fornecedores()
elif menu == "🚚 Distribuidoras":
    mod_distribuidoras.renderizar_distribuidoras()
elif menu == "📦 Produtos":
    mod_produtos.renderizar_produtos()
