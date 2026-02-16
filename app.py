import streamlit as st

st.set_page_config(layout="wide")
st.title("Calculadora Profesional de Rangos por Calibre")

CALIBRES_BASE = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

# ===============================
# PESOS ARRIBA
# ===============================

col1, col2 = st.columns(2)

with col1:
    peso_A = st.number_input(
        "Peso A (kg)",
        min_value=10.0,
        max_value=25.0,
        value=st.session_state.get("peso_A", 19.0),
        step=0.1,
        format="%.1f",
        key="peso_A"
    )

with col2:
    peso_B = st.number_input(
        "Peso B (kg)",
        min_value=10.0,
        max_value=25.0,
        value=st.session_state.get("peso_B", 18.0),
        step=0.1,
        format="%.1f",
        key="peso_B"
    )

# ===============================
# SELECCIÓN ARRIBA
# ===============================

calibres_A = st.multiselect(
    "Calibres Peso A",
    CALIBRES_BASE,
    default=st.session_state.get("calibres_A", CALIBRES_BASE),
    key="calibres_A"
)

calibres_B = st.multiselect(
    "Calibres Peso B",
    CALIBRES_BASE,
    default=st.session_state.get("calibres_B", []),
    key="calibres_B"
)

st.markdown("---")

# ===============================
# UNIFICAR Y ORDENAR
# ===============================

tabla = []

for c in calibres_A:
    tabla.append({"calibre": c, "peso": peso_A, "grupo": "A"})

for c in calibres_B:
    tabla.append({"calibre": c, "peso": peso_B, "grupo": "B"})

if not tabla:
    st.warning("No hay calibres seleccionados.")
    st.stop()

# Ordenar mayor a menor
tabla = sorted(tabla, key=lambda x: x["calibre"], reverse=True)

# ===============================
# CÁLCULO DE RANGOS EN CASCADA
# ===============================

limite_superior = None
resumen = []

for i, fila in enumerate(tabla):

    calibre = fila["calibre"]
    peso = fila["peso"]
    grupo = fila["grupo"]

    gramos_objetivo = peso * 1000
    peso_unitario = gramos_objetivo / calibre

    if i == 0:
        limite_superior = round(peso_unitario * 1.05, 0)

    limite_inferior = round(peso_unitario, 0)

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

    with col1:
        st.markdown(f"### {calibre}")

    with col2:
        st.write(f"{peso:.1f} kg")

    with col3:
        desde = st.number_input(
            "Desde",
            value=float(limite_inferior),
            step=1.0,
            key=f"desde_{calibre}_{grupo}"
        )

    with col4:
        st.write(f"Hasta: {int(limite_superior)}")

    with col5:
        peso_real = (desde * calibre) / 1000
        st.metric("Peso real", f"{peso_real:.1f} kg")

    resumen.append({
        "Calibre": calibre,
        "Grupo": grupo,
        "Peso Objetivo": peso,
        "Desde": int(desde),
        "Hasta": int(limite_superior),
        "Peso Real (kg)": round(peso_real,1)
    })

    limite_superior = desde  # cascada real dinámica

st.markdown("### 📋 Tabla Final Unificada")
st.dataframe(resumen, use_container_width=True)
