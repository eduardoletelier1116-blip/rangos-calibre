import streamlit as st

st.set_page_config(layout="wide")

st.title("Calculadora Profesional de Rangos por Calibre")

# ===============================
# CONFIGURACIÓN BASE
# ===============================

CALIBRES_BASE = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

# ===============================
# FUNCION PRINCIPAL
# ===============================

def bloque_peso(nombre, peso_key, calibres_key):

    st.subheader(nombre)

    peso_objetivo = st.number_input(
        f"Peso objetivo {nombre} (kg)",
        min_value=10.0,
        max_value=25.0,
        value=st.session_state.get(peso_key, 19.0),
        step=0.1,
        format="%.1f",
        key=peso_key
    )

    calibres = st.multiselect(
        f"Seleccionar calibres {nombre}",
        CALIBRES_BASE,
        default=st.session_state.get(calibres_key, CALIBRES_BASE),
        key=calibres_key
    )

    if not calibres:
        return

    calibres = sorted(calibres, reverse=True)

    gramos_objetivo = peso_objetivo * 1000

    rangos = {}
    limite_superior = None

    # Calcular automáticamente desde arriba
    for i, calibre in enumerate(calibres):

        peso_unitario = gramos_objetivo / calibre

        if i == 0:
            limite_superior = round(peso_unitario * 1.05, 0)

        limite_inferior = round(gramos_objetivo / calibre, 0)

        rangos[calibre] = {
            "desde": limite_inferior,
            "hasta": limite_superior
        }

        limite_superior = limite_inferior

    st.markdown("---")

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
            "Peso Real": round(peso_real,1)
        })

    st.markdown("### 📋 Tabla Resumen")
    st.dataframe(resumen, use_container_width=True)


# ===============================
# INTERFAZ DOBLE
# ===============================

colA, colB = st.columns(2)

with colA:
    bloque_peso("Peso A", "peso_A", "calibres_A")

with colB:
    bloque_peso("Peso B", "peso_B", "calibres_B")
