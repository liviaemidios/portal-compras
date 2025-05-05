# pages/2_🏢_Fornecedores.py
import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores
import uuid

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

st.markdown("""
    <div class="top-bar">
        <h1>🏢 Fornecedores</h1>
        <div class="actions">
            <button onclick="window.location.href='formulario_fornecedor.py'">➕ Cadastrar</button>
            <input type="text" placeholder="Pesquisar...">
            <button>🔍</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Dados
fornecedores = carregar_fornecedores()
fornecedores = fornecedores.sort_values("razao_social").reset_index(drop=True)

# Cabeçalho
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
total = len(fornecedores)
paginas = max(1, (total - 1) // por_pagina + 1)
pagina = st.session_state.get("pagina_fornecedores", 1)

inicio = (pagina - 1) * por_pagina
fim = inicio + por_pagina
fornecedores_pag = fornecedores.iloc[inicio:fim]

for i, row in fornecedores_pag.iterrows():
    col1, col2, col3, col4, col5 = st.columns([4, 2.5, 2.5, 2, 1])
    col1.write(row["razao_social"])
    col2.write(row["cnpj"])
    col3.write(row["email"])
    col4.write(row["telefone_fixo"])

    uid = str(uuid.uuid4()).replace("-", "")
    visualizar = col5.button("👁️", key=f"ver_f_{uid}")
    editar = col5.button("✏️", key=f"edit_f_{uid}")
    excluir = col5.button("🗑️", key=f"del_f_{uid}")

    if visualizar:
        with st.expander(f"👁️ Visualizar - {row['razao_social']}", expanded=True):
            for col in fornecedores.columns:
                st.markdown(f"**{col.replace('_', ' ').title()}:** {row[col]}")

    if editar:
        st.query_params["editar"] = str(i + inicio)
        st.switch_page("formulario_fornecedor.py")

    if excluir:
        with st.expander(f"⚠️ Confirmar exclusão de {row['razao_social']}?", expanded=True):
            col_conf, col_canc = st.columns(2)
            if col_conf.button("✅ Confirmar", key=f"confirm_f_{uid}"):
                fornecedores.drop(index=i + inicio, inplace=True)
                salvar_fornecedores(fornecedores)
                st.success("Fornecedor excluído com sucesso.")
                st.experimental_rerun()
            if col_canc.button("❌ Cancelar", key=f"cancel_del_f_{uid}"):
                st.experimental_rerun()

# Navegação
col_esq, col_meio, col_dir = st.columns([1, 10, 1])
with col_esq:
    if st.button("◀", key="ant_f") and pagina > 1:
        st.session_state["pagina_fornecedores"] = pagina - 1
with col_meio:
    st.markdown(f"<div style='text-align: center;'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
with col_dir:
    if st.button("▶", key="prox_f") and pagina < paginas:
        st.session_state["pagina_fornecedores"] = pagina + 1
