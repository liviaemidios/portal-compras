# pages/2_🏢_Fornecedores.py
import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores
import uuid

st.set_page_config(page_title="Fornecedores", layout="wide")

# Estado de pesquisa
if "busca_fornecedor" not in st.session_state:
    st.session_state.busca_fornecedor = ""
if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = False

# Bloco visual da faixa azul no topo
st.markdown("""
    <style>
        .faixa-azul {
            background-color: #3879bd;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .linha-faixa {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .linha-faixa h1 {
            color: white;
            margin: 0;
            font-size: 24px;
        }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <div class="faixa-azul">
            <div class="linha-faixa">
                <h1>🏢 Fornecedores</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 2.5, 1])
    with col1:
        if st.button("➕ Cadastrar Fornecedor"):
            st.session_state.mostrar_formulario = not st.session_state.mostrar_formulario

    with col2:
        with st.form("form_pesquisa", clear_on_submit=False):
            busca = st.text_input("", value=st.session_state.busca_fornecedor, label_visibility="collapsed", placeholder="Pesquisar fornecedor...")
            col_pesq1, col_pesq2 = st.columns([4, 1])
            with col_pesq2:
                pesquisar = st.form_submit_button("🔍")
            if pesquisar:
                st.session_state.busca_fornecedor = busca

# Formulário de cadastro tipo modal
if st.session_state.mostrar_formulario:
    with st.expander("📋 Cadastrar Novo Fornecedor", expanded=True):
        with st.form("form_cadastro_fornecedor"):
            col1, col2, col3 = st.columns(3)
            razao_social = col1.text_input("Razão Social")
            nome_fantasia = col2.text_input("Nome Fantasia")
            cnpj = col3.text_input("CNPJ")

            col4, col5, col6 = st.columns(3)
            telefone_fixo = col4.text_input("Telefone Fixo")
            telefone_celular = col5.text_input("Celular")
            email = col6.text_input("E-mail")

            endereco = st.text_input("Endereço Completo")

            col7, col8 = st.columns(2)
            inscricao_estadual = col7.text_input("Inscrição Estadual")
            inscricao_municipal = col8.text_input("Inscrição Municipal")

            col9, col10 = st.columns(2)
            pedido_minimo = col9.text_input("Pedido Mínimo")
            prazo_pagamento = col10.text_input("Prazo de Pagamento")

            forma_pagamento = st.text_input("Formas de Pagamento")
            frete = st.text_input("Frete")

            st.markdown("**Contato do Responsável/Vendedor**")
            col11, col12, col13 = st.columns(3)
            nome_contato = col11.text_input("Nome")
            tel_contato = col12.text_input("Telefone")
            email_contato = col13.text_input("E-mail")

            observacoes = st.text_area("Observações Adicionais")

            col_salvar, col_cancelar = st.columns([1, 1])
            salvar = col_salvar.form_submit_button("Salvar")
            cancelar = col_cancelar.form_submit_button("Cancelar")

            if salvar:
                novo = pd.DataFrame([{
                    "razao_social": razao_social,
                    "nome_fantasia": nome_fantasia,
                    "cnpj": cnpj,
                    "telefone_fixo": telefone_fixo,
                    "telefone_celular": telefone_celular,
                    "email": email,
                    "endereco": endereco,
                    "inscricao_estadual": inscricao_estadual,
                    "inscricao_municipal": inscricao_municipal,
                    "pedido_minimo": pedido_minimo,
                    "prazo_pagamento": prazo_pagamento,
                    "forma_pagamento": forma_pagamento,
                    "frete": frete,
                    "nome_contato": nome_contato,
                    "tel_contato": tel_contato,
                    "email_contato": email_contato,
                    "observacoes": observacoes
                }])
                df = carregar_fornecedores()
                df = pd.concat([df, novo], ignore_index=True)
                salvar_fornecedores(df)
                st.success("Fornecedor cadastrado com sucesso!")
                st.session_state.mostrar_formulario = False
                st.experimental_rerun()
            elif cancelar:
                st.session_state.mostrar_formulario = False
                st.experimental_rerun()

# Dados
fornecedores = carregar_fornecedores()
if st.session_state.busca_fornecedor:
    busca_lower = st.session_state.busca_fornecedor.lower()
    fornecedores = fornecedores[fornecedores.apply(lambda row: row.astype(str).str.lower().str.contains(busca_lower).any(), axis=1)]

fornecedores = fornecedores.sort_values("razao_social").reset_index(drop=True)

# Cabeçalho da lista
st.markdown("""
    <div class='cabecalho-faixa-container' style='display:flex; background-color:#3879bd; border-radius:5px; margin-top:1rem;'>
        <div class='cabecalho-faixa-item' style='flex: 4; color:white; font-weight:bold; padding:10px;'>Razão Social</div>
        <div class='cabecalho-faixa-item' style='flex: 2.5; color:white; font-weight:bold; padding:10px;'>CNPJ</div>
        <div class='cabecalho-faixa-item' style='flex: 2.5; color:white; font-weight:bold; padding:10px;'>E-mail</div>
        <div class='cabecalho-faixa-item' style='flex: 2; color:white; font-weight:bold; padding:10px;'>Telefone</div>
        <div class='cabecalho-faixa-item' style='flex: 1; color:white; font-weight:bold; padding:10px;'>Ações</div>
    </div>
""", unsafe_allow_html=True)

# Paginacao
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
        st.session_state.mostrar_formulario = True
        st.experimental_rerun()

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
