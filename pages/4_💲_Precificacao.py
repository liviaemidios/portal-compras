import streamlit as st
import pandas as pd

st.set_page_config(page_title="Precificação", layout="wide")

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
        .actions {
            display: flex;
            gap: 10px;
        }
        .actions input[type="text"] {
            padding: 6px 10px;
            border-radius: 5px;
            border: none;
            width: 180px;
        }
        .actions button {
            padding: 6px 12px;
            background-color: white;
            color: #3879bd;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
        .cabecalho-faixa-container {
            display: flex;
            background-color: #3879bd;
            border-radius: 5px;
            margin-top: 1rem;
        }
        .cabecalho-faixa-item {
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding: 10px 8px;
            text-align: center;
            border-right: 1px solid #ffffff33;
            flex-shrink: 0;
        }
        .cabecalho-faixa-item:last-child {
            border-right: none;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="top-bar">
        <h1>💲 Precificação</h1>
        <div class="actions">
            <input type="text" placeholder="Pesquisar produto...">
            <button>🔍</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Exemplo de tabela fictícia para testes
dados = pd.DataFrame([
    {"produto": "Álcool Gel 500ml", "fornecedor": "Fornecedor A", "preço": 9.50},
    {"produto": "Álcool Gel 500ml", "fornecedor": "Concorrente X", "preço": 9.20},
    {"produto": "Detergente Neutro", "fornecedor": "Fornecedor B", "preço": 2.99},
    {"produto": "Detergente Neutro", "fornecedor": "Concorrente Y", "preço": 3.20},
])

produtos = dados["produto"].unique()

for produto in produtos:
    st.markdown(f"### {produto}")
    tabela = dados[dados["produto"] == produto].sort_values("preço")
    st.dataframe(tabela, use_container_width=True)
