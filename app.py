import streamlit as st

st.set_page_config(page_title="Calculadora de Rangos por Calibre", layout="wide")

st.title("🍎 Calculadora de Rangos en Cascada")

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------

peso_objetivo = st.number_input(
    "Peso objetivo caja (kg)",
    value=19.2,
    step=0.1,
    format="%.1f"
)

st.divider()

# Lista completa de calibres disponibles
calibres_disponibles = [216,198,175,163,150,138,125,113,100,88,80,72]

col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    grupoA = st.multiselect(
        "Seleccionar calibres Grupo A",
        calibres_disponibles,
        default=[125,113,100]
    )

with col_sel2:
    grupoB = st.multiselect(
        "Seleccionar calibres Grupo B",
        calibres_disponibles,
        default=[88,80]
    )

recalcular = st.button("🔄 Recalcular")

st.divider()

# -----------------------------
# FUNCIÓN DE CÁLCULO CORRECTA
# -----------------------------

def calcular_rangos(calibre, peso_objetivo):
    """
    Calcula rango mínimo y máximo en cascada.
    El promedio del rango * calibre = peso objetivo.
    """

    # Promedio exacto necesario por fruta
    peso_promedio = (peso_objetivo * 1000) / calibre

    # Amplitud cascada (6% del promedio)
    amplitud = peso_promedio * 0.06

    minimo = peso_promedio - amplitud
    maximo = peso_promedio + amplitud

    peso_real = (peso_promedio * calibre) / 1000

    return round(minimo), round(maximo), round(peso_real, 1)


# -----------------------------
# MOSTRAR RESULTADOS
# -----------------------------

colA, colB = st.columns(2)

with colA:
    st.subheader("Grupo A")

    for calibre in sorted(grupoA, reverse=True):
        min_g, max_g, peso_real = calcular_rangos(calibre, peso_objetivo)

        st.markdown(f"### A - {calibre}")
        c1, c2, c3 = st.columns(3)

        c1.metric("Mín (g)", f"{min_g}")
        c2.metric("Máx (g)", f"{max_g}")
        c3.metric("Peso Real", f"{peso_real} kg")

        st.divider()

with colB:
    st.subheader("Grupo B")

    for calibre in sorted(grupoB, reverse=True):
        min_g, max_g, peso_real = calcular_rangos(calibre, peso_objetivo)

        st.markdown(f"### B - {calibre}")
        c1, c2, c3 = st.columns(3)

        c1.metric("Mín (g)", f"{min_g}")
        c2.metric("Máx (g)", f"{max_g}")
        c3.metric("Peso Real", f"{peso_real} kg")

        st.divider()
