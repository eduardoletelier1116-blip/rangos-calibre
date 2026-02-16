import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>🍎 Calculadora Profesional de Rangos</h1>",
    unsafe_allow_html=True
)

CALIBRES_BASE = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

# ===============================
# PESOS POR GRUPO
# ===============================

col1, col2 = st.columns(2)

with col1:
    peso_A = st.number_input(
        "Peso Grupo A (kg)",
        min_value=10.0,
        max_value=25.0,
        value=19.0,
        step=0.1,
        format="%.1f"
    )

with col2:
    peso_B = st.number_input(
        "Peso Grupo B (kg)",
        min_value=10.0,
        max_value=25.0,
        value=18.0,
        step=0.1,
        format="%.1f"
    )

# ===============================
# SELECCIÓN
# ===============================

calibres_A = st.multiselect(
    "Calibres Grupo A",
    CALIBRES_BASE,
    default=[]
)

calibres_B = st.multiselect(
    "Calibres Grupo B",
    CALIBRES_BASE,
    default=[]
)

st.markdown("---")

# ===============================
# FUNCIÓN DE CÁLCULO CASCADA
# ===============================

def calcular_grupo(calibres, peso, grupo):

    if not calibres:
        return []

    calibres = sorted(calibres, reverse=True)
    limite_superior = None
    resultado = []

    for i, calibre in enumerate(calibres):

        promedio_teorico = (peso * 1000) / calibre

        key_min = f"{grupo}_{calibre}_min"

        if i == 0:
            # Primer calibre → rango centrado normal
            min_inicial = round(promedio_teorico - 12)
            maximo = round(promedio_teorico + 12)

        else:
            # Cascada correcta
            maximo = limite_superior
            min_inicial = round((2 * promedio_teorico) - maximo)

        if key_min not in st.session_state:
            st.session_state[key_min] = min_inicial

        minimo = st.number_input(
            f"{grupo} - Calibre {calibre} Mín (g)",
            step=1.0,
            key=key_min
        )

        promedio_real = (minimo + maximo) / 2
        peso_real = (promedio_real * calibre) / 1000

        col1, col2, col3, col4 = st.columns([1,1,1,1])

        with col1:
            st.write(f"### {grupo} - {calibre}")

        with col2:
            st.write(f"Mín: {int(minimo)} g")

        with col3:
            st.write(f"Máx: {int(maximo)} g")

        with col4:
            st.metric("Peso Real", f"{peso_real:.1f} kg")

        resultado.append({
            "Grupo": grupo,
            "Calibre": calibre,
            "Mínimo (g)": int(minimo),
            "Máximo (g)": int(maximo),
            "Promedio (g)": round(promedio_real,1),
            "Peso Real (kg)": round(peso_real,1)
        })

        # El mínimo actual pasa a ser el máximo del siguiente
        limite_superior = minimo

    return resultado
