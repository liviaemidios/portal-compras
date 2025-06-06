# pages/4_🏭_Concorrentes.py
import streamlit as st
import pandas as pd
import uuid
from dados_concorrentes import carregar_concorrentes, salvar_concorrentes

st.set_page_config(page_title="Concorrentes", layout="wide")

if "busca_concorrente" not in st.session_state:
    st.session_state.busca_concorrente = ""
if "pagina_concorrentes" not in st.session_state:
    st.session_state.pagina_concorrentes = 1

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
            flex-wrap: wrap;
        }
        .faixa-superior h1 {
            color: white;
            font-size: 26px;
            margin: 0;
        }
        .botoes-faixa {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        .botao-principal {
            background-color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
        }
        .campo-pesquisa {
            padding: 0.4rem;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="faixa-superior">
        <h1>🏭 Concorrentes</h1>
        <div class="botoes-faixa">
            <form action="formulario_concorrente" method="get">
                <button class="botao-principal" type="submit">➕ Cadastrar Concorrente</button>
            </form>
            <form method="get">
                <input class="campo-pesquisa" name="busca" placeholder="Pesquisar..." value="">
                <button class="botao-principal" type="submit">🔍</button>
            </form>
        </div>
    </div>
""", unsafe_allow_html=True)

concorrentes = carregar_concorrentes()
busca = st.query_params.get("busca", "").lower()
if busca:
    concorrentes = concorrentes[concorrentes.apply(lambda row: row.astype(str).str.lower().str.contains(busca).any(), axis=1)]

concorrentes = concorrentes.sort_values("razao_social").reset_index(drop=True)

st.markdown("""
    <div style='display:flex; background-color:#3879bd; color:white; font-weight:bold; padding:10px; border-radius:5px;'>
        <div style='flex: 4;'>Razão Social</div>
        <div style='flex: 2.5;'>CNPJ</div>
        <div style='flex: 2.5;'>E-mail</div>
        <div style='flex: 2;'>Telefone</div>
        <div style='flex: 1;'>Ações</div>
    </div>
""", unsafe_allow_html=True)

por_pagina = 10
total = len(concorrentes)
paginas = max(1, (total - 1) // por_pagina + 1)
pagina = st.session_state.pagina_concorrentes

inicio = (pagina - 1) * por_pagina
fim = inicio + por_pagina
concorrentes_pag = concorrentes.iloc[inicio:fim]

for i, row in concorrentes_pag.iterrows():
    col1, col2, col3, col4, col5 = st.columns([4, 2.5, 2.5, 2, 1])
    col1.write(row["razao_social"])
    col2.write(row["cnpj"])
    col3.write(row["email"])
    col4.write(row["telefone"])

    uid = str(uuid.uuid4()).replace("-", "")
    visualizar = col5.button("👁️", key=f"ver_c_{uid}")
    editar = col5.button("✏️", key=f"edit_c_{uid}")
    excluir = col5.button("🗑️", key=f"del_c_{uid}")

    if visualizar:
        with st.expander(f"👁️ Visualizar - {row['razao_social']}", expanded=True):
            for col in concorrentes.columns:
                st.markdown(f"**{col.replace('_', ' ').title()}:** {row[col]}")

    if editar:
        st.query_params["editar"] = str(i + inicio)
        st.switch_page("formulario_concorrente")

    if excluir:
        with st.expander(f"⚠️ Confirmar exclusão de {row['razao_social']}?", expanded=True):
            col_conf, col_canc = st.columns(2)
            if col_conf.button("✅ Confirmar", key=f"confirm_c_{uid}"):
                concorrentes.drop(index=i + inicio, inplace=True)
                salvar_concorrentes(concorrentes)
                st.success("Concorrente excluído com sucesso.")
                st.experimental_rerun()
            if col_canc.button("❌ Cancelar", key=f"cancel_del_c_{uid}"):
                st.experimental_rerun()

col_esq, col_meio, col_dir = st.columns([1, 10, 1])
with col_esq:
    if st.button("◀", key="ant_c") and pagina > 1:
        st.session_state.pagina_concorrentes = pagina - 1
with col_meio:
    st.markdown(f"<div style='text-align: center;'>Página {pagina} de {paginas}</div>", unsafe_allow_html=True)
with col_dir:
    if st.button("▶", key="prox_c") and pagina < paginas:
        st.session_state.pagina_concorrentes = pagina + 1
