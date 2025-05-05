# formulario_fornecedor.py
import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores

st.set_page_config(page_title="Cadastro de Fornecedor", layout="wide")

st.markdown("""
    <style>
        .titulo-form {
            background-color: #3879bd;
            padding: 1rem;
            border-radius: 8px;
            color: white;
            font-size: 24px;
            text-align: center;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo-form'>📋 Cadastrar Novo Fornecedor</div>", unsafe_allow_html=True)

with st.form("form_cadastro"):
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
        st.switch_page("pages/2_🏢_Fornecedores.py")

    elif cancelar:
        st.switch_page("pages/2_🏢_Fornecedores.py")
