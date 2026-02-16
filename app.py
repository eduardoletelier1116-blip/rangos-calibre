import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>🍎 Calculadora Profesional de Rangos</h1>",
    unsafe_allow_html=True
)

CALIBRES_BASE = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

# ===============================
# PESO OBJETIVO
# ===============================

peso_objetivo = st.number_input(
    "Peso Objetivo (kg)",
    min_value=10.0,
    max_value=25.0,
    value=19.0,
    step=0.1,
    format="%.1f"
)

calibres = st.multiselect(
    "Seleccionar Calibres",
    CALIBRES_BASE,
    default=CALIBRES_BASE
)

if not calibres:
    st.stop()

calibres = sorted(calibres, reverse=True)

st.markdown("---")

# ===============================
# CÁLCULO EN CASCADA EDITABLE
# ===============================

limite_superior = None
tabla = []

for i, calibre in enumerate(calibres):

    gramos_objetivo = peso_objetivo * 1000
    promedio_teorico = gramos_objetivo / calibre

    key_name = f"desde_{calibre}"

    # Valor inicial correcto si no existe
    if key_name not in st.session_state:
        st.session_state[key_name] = round(promedio_teorico)

    desde = st.number_input(
        f"Calibre {calibre} - Desde (mín g)",
        step=1.0,
        key=key_name
    )

    # CASCADA
    if i == 0:
        hasta = round(promedio_teorico)
    else:
        hasta = limite_superior

    promedio_real = (desde + hasta) / 2
    peso_real = (promedio_real * calibre) / 1000

    col1, col2, col3, col4 = st.columns([1,1,1,1])

    with col1:
        st.write(f"### {calibre}")

    with col2:
        st.write(f"Mín: {int(desde)} g")

    with col3:
        st.write(f"Máx: {int(hasta)} g")

    with col4:
        st.metric("Peso Real", f"{peso_real:.1f} kg")

    tabla.append({
        "Calibre": calibre,
        "Mínimo (g)": int(desde),
        "Máximo (g)": int(hasta),
        "Promedio (g)": round(promedio_real,1),
        "Peso Real (kg)": round(peso_real,1)
    })

    limite_superior = desde

st.markdown("### 📋 Tabla Final para Máquina")
st.dataframe(tabla, use_container_width=True)
