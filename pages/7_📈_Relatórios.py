import streamlit as st

st.set_page_config(page_title="Relatórios", layout="wide")

st.markdown("""
    <style>
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #3879bd;
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .top-bar h1 {
            margin: 0;
            font-size: 24px;
            color: white;
        }
        .conteudo {
            font-size: 16px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Título com faixa azul
st.markdown("""
    <div class="top-bar">
        <h1>📈 Relatórios</h1>
    </div>
""", unsafe_allow_html=True)

# Conteúdo inicial
st.markdown("<div class='conteudo'>Em breve você poderá gerar relatórios de compras, fornecedores, concorrentes e precificação aqui.</div>", unsafe_allow_html=True)
