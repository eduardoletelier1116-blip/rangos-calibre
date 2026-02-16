import streamlit as st

st.set_page_config(layout="wide")

st.title("🍎 Rango Mínimo y Máximo por Calibre")

CALIBRES_BASE = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

peso_objetivo = st.number_input(
    "Peso Objetivo Caja (kg)",
    min_value=10.0,
    max_value=25.0,
    value=19.0,
    step=0.1,
    format="%.1f"
)

tolerancia = st.number_input(
    "Tolerancia ± gramos por fruta",
    min_value=0.0,
    max_value=10.0,
    value=2.0,
    step=0.5
)

calibres = st.multiselect(
    "Seleccionar Calibres",
    CALIBRES_BASE,
    default=CALIBRES_BASE
)

if not calibres:
    st.stop()

calibres = sorted(calibres, reverse=True)

tabla = []

for calibre in calibres:

    promedio = (peso_objetivo * 1000) / calibre

    minimo = round(promedio - tolerancia, 1)
    maximo = round(promedio + tolerancia, 1)

    promedio_verificacion = (minimo + maximo) / 2
    peso_verificado = (promedio_verificacion * calibre) / 1000

    tabla.append({
        "Calibre": calibre,
        "Peso Objetivo (kg)": peso_objetivo,
        "Mínimo (g)": minimo,
        "Máximo (g)": maximo,
        "Promedio (g)": round(promedio_verificacion,1),
        "Peso Resultado (kg)": round(peso_verificado,1)
    })

st.markdown("### 📋 Rangos listos para máquina")
st.dataframe(tabla, use_container_width=True)
