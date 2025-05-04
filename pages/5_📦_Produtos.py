import streamlit as st
import pandas as pd
from dados_produtos import carregar_produtos

st.set_page_config(page_title="Produtos", layout="wide")

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
        <h1>📦 Produtos</h1>
        <div class="actions">
            <input type="text" placeholder="Pesquisar...">
            <button>🔍</button>
            <button>➕ Cadastrar</button>
        </div>
    </div>
""", unsafe_allow_html=True)

produtos = carregar_produtos()
produtos = produtos.sort_values("descricao").reset_index(drop=True)

# Cabeçalho da tabela
st.markdown("""
    <div class='cabecalho-faixa-container'>
        <div class='cabecalho-faixa-item' style='flex: 4;'>Descrição</div>
        <div class='cabecalho-faixa-item' style='flex: 2;'>Categoria</div>
        <div class='cabecalho-faixa-item' style='flex: 2;'>Unidade</div>
        <div class='cabecalho-faixa-item' style='flex: 2;'>Estoque</div>
        <div class='cabecalho-faixa-item' style='flex: 2;'>Mínimo</div>
        <div class='cabecalho-faixa-item' style='flex: 1;'>Ações</div>
    </div>
""", unsafe_allow_html=True)

# Paginação
por_pagina = 10
total = len(produtos)
paginas = max(1, (total - 1) // por_pagina + 1)
pagina = st.session_state.get("pagina_produtos", 1)

inicio = (pagina - 1) * por_pagina
fim = inicio + por_pagina
produtos_pag = produtos.iloc[inicio:fim]

for _, row in produtos_pag.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 2, 1])
    col1.write(row["descricao"])
    col2.write(row["categoria"])
    col3.write(row["unidade"])
    col4.write(row["estoque"])
    col5.write(row["estoque_minimo"])
    col6.markdown("<span style='font-size:16px;'>👁️ ✏️ 🗑️</span>", unsafe_allow_html=True)

col_esq, col_meio, col_dir = st.columns([1, 10, 1])
with col_esq:
    if st.button("◀", key="ant_produto") and pagina > 1:
        st.session_state["pagina_produtos"] = pagina - 1
with col_meio:
    st.markdown(f"<div style='text-align: center;'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
with col_dir:
    if st.button("▶", key="prox_produto") and pagina < paginas:
        st.session_state["pagina_produtos"] = pagina + 1
