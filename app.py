import streamlit as st

# ✅ Deve vir logo no início
st.set_page_config(page_title="Portal Interno de Compras", layout="wide")

from login import login_page, get_current_user
import fornecedores as mod_fornecedores

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if st.session_state.usuario is None:
    login_page()
    st.stop()

usuario = get_current_user()
if usuario is None:
    st.error("Usuário não encontrado.")
    st.stop()

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# MENU LATERAL
with st.sidebar:
    st.markdown(f"**👤 {usuario['nome']}**")
    st.markdown("---")
    if st.button("🏠 Dashboard"):
        st.session_state.pagina = "inicio"
    if st.button("🏢 Fornecedores"):
        st.session_state.pagina = "fornecedores"
    if st.button("🚪 Sair"):
        st.session_state.usuario = None
        st.experimental_rerun()

# CONTEÚDO PRINCIPAL
if st.session_state.pagina == "inicio":
    st.markdown("# Bem-vindo ao Portal Interno de Compras")
    st.write("Use o menu lateral para navegar entre os módulos do sistema.")

elif st.session_state.pagina == "fornecedores":
    mod_fornecedores.renderizar_fornecedores()
