import streamlit as st

st.set_page_config(page_title="Calculadora de Rangos por Calibre", layout="wide")

st.title("🍎 Calculadora de Rangos en Cascada")

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------

peso_objetivo = st.number_input("Peso objetivo caja (kg)", value=19.2, step=0.1, format="%.1f")

st.divider()

grupoA_input = st.text_input("Calibres Grupo A (separados por coma)", "125,113,100")
grupoB_input = st.text_input("Calibres Grupo B (separados por coma)", "88,80")

def parse_calibres(texto):
    return sorted([int(x.strip()) for x in texto.split(",") if x.strip().isdigit()], reverse=True)

grupoA = parse_calibres(grupoA_input)
grupoB = parse_calibres(grupoB_input)

recalcular = st.button("🔄 Recalcular")

st.divider()

# -----------------------------
# FUNCIÓN DE CÁLCULO REAL
# -----------------------------

def calcular_rangos(calibre, peso_objetivo):
    """
    Calcula rango mínimo y máximo en cascada
    El promedio del rango * calibre = peso objetivo
    """
    peso_promedio = (peso_objetivo * 1000) / calibre

    # amplitud cascada (ajustable si quieres más precisión)
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

    for calibre in grupoA:
        min_g, max_g, peso_real = calcular_rangos(calibre, peso_objetivo)

        st.markdown(f"### A - {calibre}")
        c1, c2, c3 = st.columns([1,1,1])

        c1.metric("Mín (g)", f"{min_g}")
        c2.metric("Máx (g)", f"{max_g}")
        c3.metric("Peso Real", f"{peso_real} kg")

        st.divider()


with colB:
    st.subheader("Grupo B")

    for calibre in grupoB:
        min_g, max_g, peso_real = calcular_rangos(calibre, peso_objetivo)

        st.markdown(f"### B - {calibre}")
        c1, c2, c3 = st.columns([1,1,1])

        c1.metric("Mín (g)", f"{min_g}")
        c2.metric("Máx (g)", f"{max_g}")
        c3.metric("Peso Real", f"{peso_real} kg")

        st.divider()
