# formulario_fornecedor.py
import streamlit as st
import pandas as pd
import os

CAMINHO_FORNECEDORES = "database/fornecedores.csv"

# Funções auxiliares
def carregar_fornecedores():
    if os.path.exists(CAMINHO_FORNECEDORES):
        return pd.read_csv(CAMINHO_FORNECEDORES)
    return pd.DataFrame(columns=[
        "razao_social", "nome_fantasia", "cnpj", "inscricao_estadual", "inscricao_municipal",
        "telefone_fixo", "celular", "email", "logradouro", "numero", "bairro", "cidade", "estado", "cep",
        "pedido_minimo", "prazo_pagamento", "formas_pagamento", "frete",
        "responsavel_nome", "responsavel_telefone", "responsavel_email", "observacoes"
    ])

def salvar_fornecedores(df):
    df.to_csv(CAMINHO_FORNECEDORES, index=False)

st.set_page_config(page_title="Cadastro de Fornecedor", layout="wide")

# Recuperar parâmetros da URL
params = st.query_params
modo_edicao = "editar" in params
indice_edicao = int(params.get("editar", ["-1"])[0]) if modo_edicao else -1

# Carrega dados se for edição
df = carregar_fornecedores()
if modo_edicao and 0 <= indice_edicao < len(df):
    dados = df.loc[indice_edicao]
    titulo = f"✏️ Editando fornecedor: {dados['razao_social']}"
else:
    dados = {}
    titulo = "➕ Novo cadastro de fornecedor"

if st.button("🔙 Voltar"):
    st.switch_page("pages/2_🏢_Fornecedores.py")

st.markdown(f"## {titulo}")

# Formulário
col1, col2 = st.columns(2)
razao_social = col1.text_input("Razão Social", value=dados.get("razao_social", ""))
nome_fantasia = col2.text_input("Nome Fantasia", value=dados.get("nome_fantasia", ""))
cnpj = col1.text_input("CNPJ", value=dados.get("cnpj", ""))
inscricao_estadual = col2.text_input("Inscrição Estadual", value=dados.get("inscricao_estadual", ""))
inscricao_municipal = col1.text_input("Inscrição Municipal", value=dados.get("inscricao_municipal", ""))

telefone_fixo = col2.text_input("Telefone Fixo", value=dados.get("telefone_fixo", ""))
celular = col1.text_input("Celular", value=dados.get("celular", ""))
email = col2.text_input("E-mail", value=dados.get("email", ""))

logradouro = col1.text_input("Logradouro", value=dados.get("logradouro", ""))
numero = col2.text_input("Número", value=dados.get("numero", ""))
bairro = col1.text_input("Bairro", value=dados.get("bairro", ""))
cidade = col2.text_input("Cidade", value=dados.get("cidade", ""))
estado = col1.text_input("Estado", value=dados.get("estado", ""))
cep = col2.text_input("CEP", value=dados.get("cep", ""))

pedido_minimo = col1.text_input("Pedido Mínimo", value=dados.get("pedido_minimo", ""))
prazo_pagamento = col2.text_input("Prazo de Pagamento", value=dados.get("prazo_pagamento", ""))
formas_pagamento = col1.text_input("Formas de Pagamento", value=dados.get("formas_pagamento", ""))
frete = col2.text_input("Frete", value=dados.get("frete", ""))

responsavel_nome = col1.text_input("Responsável/Vendedor", value=dados.get("responsavel_nome", ""))
responsavel_telefone = col2.text_input("Telefone do Responsável", value=dados.get("responsavel_telefone", ""))
responsavel_email = col1.text_input("E-mail do Responsável", value=dados.get("responsavel_email", ""))
observacoes = st.text_area("Observações", value=dados.get("observacoes", ""))

if st.button("💾 Salvar"):
    novo = pd.DataFrame([{ 
        "razao_social": razao_social, "nome_fantasia": nome_fantasia, "cnpj": cnpj,
        "inscricao_estadual": inscricao_estadual, "inscricao_municipal": inscricao_municipal,
        "telefone_fixo": telefone_fixo, "celular": celular, "email": email,
        "logradouro": logradouro, "numero": numero, "bairro": bairro,
        "cidade": cidade, "estado": estado, "cep": cep,
        "pedido_minimo": pedido_minimo, "prazo_pagamento": prazo_pagamento,
        "formas_pagamento": formas_pagamento, "frete": frete,
        "responsavel_nome": responsavel_nome, "responsavel_telefone": responsavel_telefone,
        "responsavel_email": responsavel_email, "observacoes": observacoes
    }])

    if modo_edicao:
        df.iloc[indice_edicao] = novo.iloc[0]
    else:
        df = pd.concat([df, novo], ignore_index=True)

    salvar_fornecedores(df)
    st.success("Fornecedor salvo com sucesso!")
    st.switch_page("pages/2_🏢_Fornecedores.py")
