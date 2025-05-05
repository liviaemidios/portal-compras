# setup.py
import os
import pandas as pd

def inicializar_csv_concorrentes():
    if not os.path.exists("base de dados/concorrentes.csv"):
        colunas = [
            "razao_social", "nome_fantasia", "cnpj", "telefone", "email",
            "endereco", "inscricao_estadual", "inscricao_municipal",
            "pedido_minimo", "prazo_pagamento", "formas_pagamento", "frete",
            "responsavel_nome", "responsavel_telefone", "responsavel_email", "observacoes"
        ]
        pd.DataFrame(columns=colunas).to_csv("base de dados/concorrentes.csv", index=False)

def inicializar_csv_fornecedores():
    if not os.path.exists("base de dados/fornecedores.csv"):
        colunas = [
            "razao_social", "nome_fantasia", "cnpj", "telefone", "celular", "email",
            "endereco", "inscricao_estadual", "inscricao_municipal",
            "pedido_minimo", "prazo_pagamento", "formas_pagamento", "frete",
            "responsavel_nome", "responsavel_telefone", "responsavel_email", "observacoes"
        ]
        pd.DataFrame(columns=colunas).to_csv("base de dados/fornecedores.csv", index=False)

def inicializar_csv_produtos():
    if not os.path.exists("base de dados/produtos.csv"):
        colunas = ["produto", "marca", "unidade", "preco", "fornecedor"]
        pd.DataFrame(columns=colunas).to_csv("base de dados/produtos.csv", index=False)

def inicializar_sistema():
    os.makedirs("base de dados", exist_ok=True)
    inicializar_csv_concorrentes()
    inicializar_csv_fornecedores()
    inicializar_csv_produtos()
