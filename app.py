import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Rangos Calibre",
    page_icon="🍎"
)

st.markdown(
    """
    <h1 style='text-align:center;'>
        🍎 Calculadora Profesional de Rangos por Calibre 📦
    </h1>
    """,
    unsafe_allow_html=True
)

CALIBRES_BASE = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

# ===============================
# PESOS ARRIBA CON RECALCULAR
# ===============================

col1, col2 = st.columns(2)

with col1:
    sub1, sub2 = st.columns([4,1])
    with sub1:
        peso_A = st.number_input(
            "Peso A (kg)",
            min_value=10.0,
            max_value=25.0,
            value=19.0,
            step=0.1,
            format="%.1f",
            key="peso_A"
        )
    with sub2:
        recalcular_A = st.button("🔄", key="recalc_A")

with col2:
    sub3, sub4 = st.columns([4,1])
    with sub3:
        peso_B = st.number_input(
            "Peso B (kg)",
            min_value=10.0,
            max_value=25.0,
            value=18.0,
            step=0.1,
            format="%.1f",
            key="peso_B"
        )
    with sub4:
        recalcular_B = st.button("🔄", key="recalc_B")

# ===============================
# LIMPIAR RANGOS SI SE RECALCULA
# ===============================

if recalcular_A or recalcular_B:
    for key in list(st.session_state.keys()):
        if key.startswith("desde_"):
            del st.session_state[key]

# ===============================
# SELECCIÓN DE CALIBRES
# ===============================

calibres_A = st.multiselect(
    "Calibres Peso A",
    CALIBRES_BASE,
    default=CALIBRES_BASE,
    key="calibres_A"
)

calibres_B = st.multiselect(
    "Calibres Peso B",
    CALIBRES_BASE,
    default=[],
    key="calibres_B"
)

st.markdown("---")

# ===============================
# UNIFICAR TABLA
# ===============================

tabla = []

for c in calibres_A:
    tabla.append({"calibre": c, "peso": peso_A, "grupo": "A"})

for c in calibres_B:
    tabla.append({"calibre": c, "peso": peso_B, "grupo": "B"})

if not tabla:
    st.warning("No hay calibres seleccionados.")
    st.stop()

tabla = sorted(tabla, key=lambda x: x["calibre"], reverse=True)

# ===============================
# CÁLCULO EXACTO SIN MÁRGENES
# ===============================

limite_superior = None
resumen = []

for i, fila in enumerate(tabla):

    calibre = fila["calibre"]
    peso = fila["peso"]
    grupo = fila["grupo"]

    gramos_objetivo = peso * 1000
    peso_unitario_teorico = gramos_objetivo / calibre

    key_name = f"desde_{calibre}_{grupo}"

    # Crear valor inicial exacto si no existe
    if key_name not in st.session_state:
        st.session_state[key_name] = round(peso_unitario_teorico, 0)

    desde = st.number_input(
        "Desde",
        step=1.0,
        key=key_name
    )

    # Hasta en cascada
    if i == 0:
        hasta = round(peso_unitario_teorico, 0)
    else:
        hasta = limite_superior

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

    with col1:
        st.markdown(f"### {calibre}")

    with col2:
        st.write(f"{peso:.1f} kg")

    with col3:
        st.write(f"Hasta: {int(hasta)}")

    with col4:
        peso_real = (desde * calibre) / 1000
        st.metric("Peso real", f"{peso_real:.1f} kg")

    resumen.append({
        "Calibre": calibre,
        "Grupo": grupo,
        "Peso Objetivo": peso,
        "Desde": int(desde),
        "Hasta": int(hasta),
        "Peso Real (kg)": round(peso_real,1)
    })

    limite_superior = desde

st.markdown("### 📋 Tabla Final Unificada")
st.dataframe(resumen, use_container_width=True)
