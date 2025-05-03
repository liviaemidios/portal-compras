import streamlit as st
import pandas as pd
from dados_fornecedores import carregar_fornecedores, salvar_fornecedores

def mostrar_formulario_fornecedor(modo="novo", dados=None, index=None):
    titulo = "Cadastro de Fornecedor" if modo == "novo" else "Editar Fornecedor"
    st.markdown(f"### {titulo}")

    with st.form(f"form_fornecedor_{modo}_{index}"):
        razao_social = st.text_input("Razão Social", value=dados.get("razao_social") if dados else "")
        nome_fantasia = st.text_input("Nome Fantasia", value=dados.get("nome_fantasia") if dados else "")
        cnpj = st.text_input("CNPJ", value=dados.get("cnpj") if dados else "")
        inscricao_estadual = st.text_input("Inscrição Estadual", value=dados.get("inscricao_estadual") if dados else "")
        inscricao_municipal = st.text_input("Inscrição Municipal", value=dados.get("inscricao_municipal") if dados else "")
        telefone = st.text_input("Telefone", value=dados.get("telefone") if dados else "")
        email = st.text_input("E-mail", value=dados.get("email") if dados else "")
        endereco = st.text_area("Endereço", value=dados.get("endereco") if dados else "")
        pedido_minimo = st.text_input("Valor Mínimo de Pedido", value=dados.get("pedido_minimo") if dados else "")
        prazo_pagamento = st.text_input("Prazo de Pagamento", value=dados.get("prazo_pagamento") if dados else "")

        col1, col2 = st.columns(2)
        salvar = col1.form_submit_button("Salvar")
        cancelar = col2.form_submit_button("Cancelar")

        if salvar:
            novo = {
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
            }
            df = carregar_fornecedores()
            if modo == "novo":
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            elif modo == "editar" and index is not None:
                for campo in novo:
                    df.at[index, campo] = novo[campo]
            salvar_fornecedores(df)
            st.success("Fornecedor salvo com sucesso!")
            st.query_params.clear()
            st.rerun()

        if cancelar:
            st.query_params.clear()
            st.rerun()
