import streamlit as st

st.set_page_config(layout="wide")
st.title("Calculadora Profesional de Rangos por Calibre")

CALIBRES_BASE = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

# ===============================
# FILA SUPERIOR COMPLETA
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

# Selección de calibres arriba (en línea)
calibres_A = st.multiselect(
    "Calibres Peso A",
    CALIBRES_BASE,
    default=st.session_state.get("calibres_A", CALIBRES_BASE),
    key="calibres_A"
)

calibres_B = st.multiselect(
    "Calibres Peso B",
    CALIBRES_BASE,
    default=st.session_state.get("calibres_B", CALIBRES_BASE),
    key="calibres_B"
)

st.markdown("---")

# ===============================
# FUNCIÓN DE BLOQUE
# ===============================

def bloque(nombre, peso, calibres):

    if not calibres:
        st.warning(f"No hay calibres seleccionados en {nombre}")
        return

    calibres = sorted(calibres, reverse=True)
    gramos_objetivo = peso * 1000

    rangos = {}
    limite_superior = None

    # Cálculo automático descendente
    for i, calibre in enumerate(calibres):

        peso_unitario = gramos_objetivo / calibre

        if i == 0:
            limite_superior = round(peso_unitario * 1.05, 0)

        limite_inferior = round(peso_unitario, 0)

        rangos[calibre] = {
            "desde": limite_inferior,
            "hasta": limite_superior
        }

        limite_superior = limite_inferior

    st.subheader(nombre)

    resumen = []

    for calibre in calibres:

        col1, col2, col3, col4 = st.columns([1,1,1,1])

        with col1:
            st.markdown(f"### {calibre}")

        with col2:
            desde = st.number_input(
                "Desde",
                value=float(rangos[calibre]["desde"]),
                step=1.0,
                key=f"{nombre}_desde_{calibre}"
            )

        with col3:
            hasta = rangos[calibre]["hasta"]
            st.write(f"Hasta: {int(hasta)}")

        with col4:
            peso_real = (desde * calibre) / 1000
            st.metric("Peso real", f"{peso_real:.1f} kg")

        resumen.append({
            "Calibre": calibre,
            "Desde": int(desde),
            "Hasta": int(hasta),
            "Peso Real (kg)": round(peso_real,1)
        })

    st.markdown("### 📋 Tabla Resumen")
    st.dataframe(resumen, use_container_width=True)

# ===============================
# BLOQUES ABAJO EN COLUMNAS
# ===============================

colA, colB = st.columns(2)

with colA:
    bloque("Peso A", peso_A, calibres_A)

with colB:
    bloque("Peso B", peso_B, calibres_B)
