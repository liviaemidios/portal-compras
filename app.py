with st.sidebar:
    st.markdown(f"**Usuário:** {usuario['nome']}")
    st.markdown("---")

    st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
            text-align: left;
            padding: 0.6rem 1rem;
            margin-bottom: 0.3rem;
            border-radius: 8px;
            border: none;
            background-color: #e9f2fb;
            color: #003366;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #d8e7f9;
            cursor: pointer;
        }
        .stButton.active > button {
            background-color: #3879bd !important;
            color: white !important;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    for nome, valor in menu.items():
        button_container = st.container()
        if st.session_state.pagina == valor:
            with button_container:
                st.markdown('<div class="stButton active">', unsafe_allow_html=True)
                if st.button(nome, key=f"menu_{valor}"):
                    st.session_state.pagina = valor
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            with button_container:
                st.markdown('<div class="stButton">', unsafe_allow_html=True)
                if st.button(nome, key=f"menu_{valor}"):
                    st.session_state.pagina = valor
                st.markdown('</div>', unsafe_allow_html=True)
