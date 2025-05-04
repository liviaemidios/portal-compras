import streamlit as st
import pandas as pd
from dados_concorrentes import carregar_concorrentes

st.set_page_config(page_title="Concorrentes", layout="wide")

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

# Faixa superior
st.markdown("""
    <div class="top-bar">
        <h1>🏭 Concorrentes</h1>
        <div class="actions">
            <input type="text" placeholder="Pesquisar...">
            <button>🔍</button>
            <button onclick="window.location.href='formulario_concorrente.py'">➕ Cadastrar</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Carrega dados
concorrentes = carregar_concorrentes()
concorrentes = concorrentes.sort_values("razao_social").reset_index(drop=True)

# Cabeçalho da tabela
st.markdown("""
    <div class='cabecalho-faixa-container'>
        <div class='cabecalho-faixa-item' style='flex: 4;'>Razão Social</div>
        <div class='cabecalho-faixa-item' style='flex: 2.5;'>CNPJ</div>
        <div class='cabecalho-faixa-item' style='flex: 2.5;'>E-mail</div>
        <div class='cabecalho-faixa-item' style='flex: 2;'>Telefone</div>
        <div class='cabecalho-faixa-item' style='flex: 1;'>Ações</div>
    </div>
""", unsafe_allow_html=True)

# Paginação
por_pagina = 10
total = len(concorrentes)
paginas = max(1, (total - 1) // por_pagina + 1)
pagina = st.session_state.get("pagina_concorrentes", 1)

inicio = (pagina - 1) * por_pagina
fim = inicio + por_pagina
concorrentes_pag = concorrentes.iloc[inicio:fim]

for _, row in concorrentes_pag.iterrows():
    col1, col2, col3, col4, col5 = st.columns([4, 2.5, 2.5, 2, 1])
    col1.write(row["razao_social"])
    col2.write(row["cnpj"])
    col3.write(row["email"])
    col4.write(row["telefone"])
    col5.markdown("<span style='font-size:16px;'>👁️ ✏️ 🗑️</span>", unsafe_allow_html=True)

# Navegação
col_esq, col_meio, col_dir = st.columns([1, 10, 1])
with col_esq:
    if st.button("◀", key="ant_conc") and pagina > 1:
        st.session_state["pagina_concorrentes"] = pagina - 1
with col_meio:
    st.markdown(f"<div style='text-align: center;'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
with col_dir:
    if st.button("▶", key="prox_conc") and pagina < paginas:
        st.session_state["pagina_concorrentes"] = pagina + 1
