# ---------------- SELECCION MODO ----------------

modo = st.radio(
    "Seleccionar tipo de caja:",
    ["18 KG", "19 KG"],
    horizontal=True
)

# Inicializar si no existen
if "peso_18" not in st.session_state:
    st.session_state["peso_18"] = 18.00

if "peso_19" not in st.session_state:
    st.session_state["peso_19"] = 19.00


if modo == "18 KG":
    lista_calibres = calibres_18
    key_prefix = "18"

    peso_objetivo = st.number_input(
        "Peso objetivo 18 KG",
        step=0.01,
        format="%.2f",
        key="peso_18"
    )

else:
    lista_calibres = calibres_19
    key_prefix = "19"

    peso_objetivo = st.number_input(
        "Peso objetivo 19 KG",
        step=0.01,
        format="%.2f",
        key="peso_19"
    )
