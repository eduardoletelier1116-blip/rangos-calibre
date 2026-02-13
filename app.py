# ---------------- SELECCION MODO ----------------

modo = st.radio(
    "Seleccionar tipo de caja:",
    ["18 KG", "19 KG"],
    horizontal=True
)

# Inicializar pesos si no existen
if "peso_18" not in st.session_state:
    st.session_state.peso_18 = 18.00

if "peso_19" not in st.session_state:
    st.session_state.peso_19 = 19.00

# Mostrar input según modo
if modo == "18 KG":
    lista_calibres = calibres_18
    key_prefix = "18"

    st.session_state.peso_18 = st.number_input(
        "Peso objetivo 18 KG",
        value=st.session_state.peso_18,
        step=0.01,
        format="%.2f",
        key="input_18"
    )

    peso_objetivo = st.session_state.peso_18

else:
    lista_calibres = calibres_19
    key_prefix = "19"

    st.session_state.peso_19 = st.number_input(
        "Peso objetivo 19 KG",
        value=st.session_state.peso_19,
        step=0.01,
        format="%.2f",
        key="input_19"
    )

    peso_objetivo = st.session_state.peso_19
