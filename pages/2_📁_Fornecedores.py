import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores

st.set_page_config(page_title="Fornecedores", layout="wide")

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

# Topo com título, busca e botão
st.markdown("""
    <div class="top-bar">
        <h1>🏢 Fornecedores</h1>
        <div class="actions">
            <input type="text" placeholder="Pesquisar...">
            <button>🔍</button>
            <button>➕ Cadastrar</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Carrega dados
fornecedores = carregar_fornecedores()
fornecedores = fornecedores.sort_values("razao_social").reset_index(drop=True)

# Cabeçalho da tabela
st.markdown("""
    <div class='cabecalho-faixa-container'>
        <div class='cabecalho-faixa-item' style='flex: 3;'>Razão Social</div>
        <div class='cabecalho-faixa-item' style='flex: 2;'>Fantasia</div>
        <div class='cabecalho-faixa-item' style='flex: 2.5;'>CNPJ</div>
        <div class='cabecalho-faixa-item' style='flex: 2.5;'>E-mail</div>
        <div class='cabecalho-faixa-item' style='flex: 2;'>Telefone</div>
        <div class='cabecalho-faixa-item' style='flex: 1;'>Ações</div>
    </div>
""", unsafe_allow_html=True)

# Paginação
por_pagina = 10
total = len(fornecedores)
paginas = max(1, (total - 1) // por_pagina + 1)
pagina = st.session_state.get("pagina_fornecedores", 1)

inicio = (pagina - 1) * por_pagina
fim = inicio + por_pagina
fornecedores_pag = fornecedores.iloc[inicio:fim]

for _, row in fornecedores_pag.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2.5, 2.5, 2, 1])
    col1.write(row["razao_social"])
    col2.write(row["nome_fantasia"])
    col3.write(row["cnpj"])
    col4.write(row["email"])
    col5.write(row["telefone"])
    col6.markdown("<span style='font-size:16px;'>👁️ ✏️ 🗑️</span>", unsafe_allow_html=True)

col_esq, col_meio, col_dir = st.columns([1, 10, 1])
with col_esq:
    if st.button("◀") and pagina > 1:
        st.session_state["pagina_fornecedores"] = pagina - 1
with col_meio:
    st.markdown(f"<div style='text-align: center;'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
with col_dir:
    if st.button("▶") and pagina < paginas:
        st.session_state["pagina_fornecedores"] = pagina + 1
