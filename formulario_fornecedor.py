# formulario_fornecedor.py
import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores

st.set_page_config(page_title="Cadastro de Fornecedor", layout="wide")

st.markdown("""
    <style>
        .formulario-container {
            background-color: #f5f5f5;
            padding: 2rem;
            border-radius: 10px;
        }
        .titulo-formulario {
            font-size: 26px;
            color: #3879bd;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo-formulario'>➕ Cadastro de Fornecedor</div>", unsafe_allow_html=True)

fornecedores = carregar_fornecedores()

id_editar = st.query_params.get("editar")

if id_editar is not None:
    id_editar = int(id_editar)
    dados = fornecedores.iloc[id_editar].to_dict()
else:
    dados = {col: "" for col in fornecedores.columns}

with st.form(key="form_fornecedor"):
    st.subheader("Dados da Empresa")
    dados["razao_social"] = st.text_input("Razão Social", value=dados["razao_social"])
    dados["nome_fantasia"] = st.text_input("Nome Fantasia", value=dados["nome_fantasia"])
    dados["cnpj"] = st.text_input("CNPJ", value=dados["cnpj"])
    dados["inscricao_estadual"] = st.text_input("Inscrição Estadual", value=dados["inscricao_estadual"])
    dados["inscricao_municipal"] = st.text_input("Inscrição Municipal", value=dados["inscricao_municipal"])
    dados["endereco"] = st.text_area("Endereço Completo", value=dados["endereco"])
    
    st.subheader("Contato Geral")
    dados["telefone"] = st.text_input("Telefone Fixo", value=dados["telefone"])
    dados["celular"] = st.text_input("Celular", value=dados["celular"])
    dados["email"] = st.text_input("E-mail", value=dados["email"])

    st.subheader("Condições Comerciais")
    dados["pedido_minimo"] = st.text_input("Pedido Mínimo", value=dados["pedido_minimo"])
    dados["prazo_pagamento"] = st.text_input("Prazo de Pagamento", value=dados["prazo_pagamento"])
    dados["formas_pagamento"] = st.text_input("Formas de Pagamento", value=dados["formas_pagamento"])
    dados["frete"] = st.text_input("Frete", value=dados["frete"])

    st.subheader("Responsável / Vendedor")
    dados["responsavel_nome"] = st.text_input("Nome do Responsável/Vendedor", value=dados["responsavel_nome"])
    dados["responsavel_telefone"] = st.text_input("Telefone do Responsável", value=dados["responsavel_telefone"])
    dados["responsavel_email"] = st.text_input("E-mail do Responsável", value=dados["responsavel_email"])

    dados["observacoes"] = st.text_area("Observações Adicionais", value=dados["observacoes"])

    col1, col2 = st.columns([1, 1])
    salvar = col1.form_submit_button("💾 Salvar")
    cancelar = col2.form_submit_button("❌ Cancelar")

    if salvar:
        novo_df = pd.DataFrame([dados])
        if id_editar is not None:
            fornecedores.iloc[id_editar] = dados
        else:
            fornecedores = pd.concat([fornecedores, novo_df], ignore_index=True)
        salvar_fornecedores(fornecedores)
        st.success("Fornecedor salvo com sucesso!")
        st.switch_page("pages/3_📁_Fornecedores.py")

    if cancelar:
        st.switch_page("pages/3_📁_Fornecedores.py")
