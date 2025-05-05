import streamlit as st
import pandas as pd
import os

CAMINHO_CONCORRENTES = "database/concorrentes.csv"

def carregar_concorrentes():
    if os.path.exists(CAMINHO_CONCORRENTES):
        return pd.read_csv(CAMINHO_CONCORRENTES)
    else:
        return pd.DataFrame(columns=[
            "razao_social", "nome_fantasia", "cnpj", "telefone", "email",
            "endereco", "inscricao_estadual", "inscricao_municipal", "pedido_minimo", "prazo_pagamento"
        ])

def salvar_concorrentes(df):
    df.to_csv(CAMINHO_CONCORRENTES, index=False)

st.set_page_config(page_title="Cadastrar Concorrente", layout="wide")

st.markdown("## ➕ Cadastro de Concorrente")

st.markdown("---")
st.markdown("### Dados da Empresa")
razao_social = st.text_input("Razão Social")
nome_fantasia = st.text_input("Nome Fantasia")
cnpj = st.text_input("CNPJ")

st.markdown("### Contato")
telefone = st.text_input("Telefone")
email = st.text_input("E-mail")
endereco = st.text_input("Endereço")

st.markdown("### Dados Cadastrais")
inscricao_estadual = st.text_input("Inscrição Estadual")
inscricao_municipal = st.text_input("Inscrição Municipal")
pedido_minimo = st.text_input("Pedido Mínimo (R$)")
prazo_pagamento = st.text_input("Prazo de Pagamento")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Salvar Concorrente"):
        concorrentes = carregar_concorrentes()
        novo = pd.DataFrame([{
            "razao_social": razao_social,
            "nome_fantasia": nome_fantasia,
            "cnpj": cnpj,
            "telefone": telefone,
            "email": email,
            "endereco": endereco,
            "inscricao_estadual": inscricao_estadual,
            "inscricao_municipal": inscricao_municipal,
            "pedido_minimo": pedido_minimo,
            "prazo_pagamento": prazo_pagamento
        }])
        concorrentes = pd.concat([concorrentes, novo], ignore_index=True)
        salvar_concorrentes(concorrentes)
        st.success("✅ Concorrente cadastrado com sucesso!")
        st.experimental_rerun()

with col2:
    if st.button("🔙 Voltar"):
        st.switch_page("pages/3_🏭_Concorrentes.py")

