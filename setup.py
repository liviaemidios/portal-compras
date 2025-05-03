from dados_fornecedores import inicializar_csv_fornecedores
from dados_produtos import inicializar_csv_produtos
from dados_distribuidoras import inicializar_csv_distribuidoras


def inicializar_sistema():
    print("🔧 Inicializando estrutura de dados...")
    inicializar_csv_fornecedores()
    inicializar_csv_produtos()
    inicializar_csv_distribuidoras()
    print("✅ Todos os arquivos foram criados ou já existiam.")


if __name__ == "__main__":
    inicializar_sistema()
