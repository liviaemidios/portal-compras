import streamlit as st
from fornecedores import pagina_fornecedores
from distribuidoras import pagina_distribuidoras
from produtos import pagina_produtos
from comparador import pagina_comparador
from relatorios import pagina_relatorios
from login import login_page, get_current_user

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
        st.image(usuario["foto"], width=150)
        st.markdown(f"**Nome:** {usuario['nome']}")
        st.markdown(f"**E-mail:** {usuario['email']}")
    elif pagina == "🚪 Sair":
        st.session_state.usuario = None
        st.rerun()
