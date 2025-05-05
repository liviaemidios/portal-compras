# pages/7_📈_Relatórios.py
import streamlit as st

st.set_page_config(page_title="Relatórios", layout="wide")

st.markdown("""
    <style>
        .faixa-superior {
            background-color: #3879bd;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .faixa-superior h1 {
            color: white;
            font-size: 26px;
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="faixa-superior">
        <h1>📈 Relatórios</h1>
    </div>
""", unsafe_allow_html=True)

st.info("Em breve: área de relatórios com visualização e exportação de dados.")
