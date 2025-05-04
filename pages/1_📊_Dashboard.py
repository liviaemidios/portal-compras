import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

st.markdown("""
    <style>
        .titulo-dashboard {
            font-size: 32px;
            font-weight: bold;
            color: #3879bd;
            margin-bottom: 20px;
        }
        .texto-bemvindo {
            font-size: 18px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo-dashboard'>📊 Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='texto-bemvindo'>Bem-vindo ao Portal Interno de Compras!<br>Use o menu à esquerda para navegar pelas seções do sistema.</div>", unsafe_allow_html=True)
