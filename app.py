import streamlit as st
from fornecedores import pagina_fornecedores
from distribuidoras import pagina_distribuidoras
from produtos import pagina_produtos
from comparador import pagina_comparador
from relatorios import pagina_relatorios
from login import login_page, get_current_user
import pandas as pd
import os

CAMINHO_USUARIOS = "database/usuarios.csv"

st.set_page_config(page_title="Portal de Compras", layout="wide")

# DEBUG TEMPORÁRIO
st.markdown("<small style='color:gray;'>Sessão: {}</small>".format(st.session_state.get("usuario", "Nenhum")), unsafe_allow_html=True)

st.markdown("""
<style>
.sidebar-button {
    display: block;
    padding: 0.6rem 1rem;
    margin: 0.3rem 0;
    background-color: #e9f2fb;
    border-radius: 8px;
    color: #003366;
    font-weight: 500;
    text-decoration: none;
    transition: background-color 0.3s;
}
.sidebar-button:hover {
    background-color: #d8e7f9;
    cursor: pointer;
}
.sidebar-button.active {
    background-color: #3879bd;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "dashboard"

if st.session_state.usuario is None:
    login_page()
else:
    usuario = get_current_user()

    if usuario is None:
        st.error("Erro: não foi possível carregar os dados do usuário.")
        st.write("DEBUG >> st.session_state.usuario:", st.session_state.get("usuario"))
        st.stop()

    menu = {
        "🏠 Dashboard": "dashboard",
        "🏢 Fornecedores": "fornecedores",
        "🚚 Distribuidoras": "distribuidoras",
        "📦 Produtos": "produtos",
        "💰 Comparador de Preços": "comparador",
        "📊 Relatórios": "relatorios",
        "🚪 Sair": "sair"
    }

    with st.sidebar:
        st.markdown(f"**Usuário:** {usuario['nome']}")
        foto = usuario.get("foto")
        if isinstance(foto, str) and foto.strip() and os.path.exists(foto):
            st.image(foto, width=120)
        else:
            st.image("logo.png", width=120)

        if st.button("👤 Meu Perfil"):
            st.session_state.pagina = "meu_perfil"

        st.markdown("---")

        for nome, valor in menu.items():
            ativo = "active" if st.session_state.pagina == valor else ""
            if st.markdown(f"<a class='sidebar-button {ativo}' href='#' onclick=\"window.location.reload()\">{nome}</a>", unsafe_allow_html=True):
                st.session_state.pagina = valor

    if st.session_state.pagina == "meu_perfil":
        st.subheader("👤 Meu Perfil")

        if isinstance(foto, str) and foto.strip() and os.path.exists(foto):
            st.image(foto, width=150)
            if st.button("🗑️ Remover Foto"):
                try:
                    os.remove(foto)
                except:
                    pass
                df = pd.read_csv(CAMINHO_USUARIOS, dtype=str)
                df.loc[df["usuario"] == st.session_state.usuario, "foto"] = ""
                df.to_csv(CAMINHO_USUARIOS, index=False)
                st.success("Foto removida com sucesso.")
                st.rerun()
        else:
            st.info("Nenhuma foto de perfil cadastrada.")

        st.markdown(f"**Nome:** {usuario['nome']}")
        st.markdown(f"**E-mail:** {usuario['email']}")

        with st.form("form_perfil"):
            cpf = st.text_input("CPF", value=usuario.get("cpf", ""))
            rg = st.text_input("RG", value=usuario.get("rg", ""))
            data_nasc = st.date_input("Data de Nascimento", value=pd.to_datetime(usuario.get("data_nascimento", "2000-01-01")))
            endereco = st.text_area("Endereço", value=usuario.get("endereco", ""))
            fixo = st.text_input("Telefone Fixo", value=usuario.get("tel_fixo", ""))
            celular = st.text_input("Telefone Celular", value=usuario.get("tel_celular", ""))

            nova_foto = st.file_uploader("Atualizar Foto de Perfil", type=["png", "jpg", "jpeg"])
            if st.form_submit_button("Salvar Perfil"):
                df = pd.read_csv(CAMINHO_USUARIOS, dtype=str)
                idx = df[df["usuario"] == st.session_state.usuario].index[0]

                df.at[idx, "cpf"] = cpf
                df.at[idx, "rg"] = rg
                df.at[idx, "data_nascimento"] = data_nasc
                df.at[idx, "endereco"] = endereco
                df.at[idx, "tel_fixo"] = fixo
                df.at[idx, "tel_celular"] = celular

                if nova_foto:
                    os.makedirs("fotos_perfil", exist_ok=True)
                    caminho_foto = f"fotos_perfil/{st.session_state.usuario}.jpg"
                    with open(caminho_foto, "wb") as f:
                        f.write(nova_foto.getbuffer())
                    df.at[idx, "foto"] = caminho_foto

                df.to_csv(CAMINHO_USUARIOS, index=False)
                st.success("Perfil atualizado com sucesso!")
                st.session_state.pagina = None
                st.rerun()

    elif st.session_state.pagina == "dashboard":
        st.image("logo.png", width=200)
        st.title("Bem-vindo ao Portal de Compras Internas")
        st.info("Selecione uma das opções no menu à esquerda.")

    elif st.session_state.pagina == "fornecedores":
        pagina_fornecedores()

    elif st.session_state.pagina == "distribuidoras":
        pagina_distribuidoras()

    elif st.session_state.pagina == "produtos":
        pagina_produtos()

    elif st.session_state.pagina == "comparador":
        pagina_comparador()

    elif st.session_state.pagina == "relatorios":
        pagina_relatorios()

    elif st.session_state.pagina == "sair":
        st.session_state.usuario = None
        st.session_state.pagina = None
        st.rerun()
