import streamlit as st

st.set_page_config(page_title="Calculadora Cascada Profesional", layout="wide")

st.title("🍎 Calculadora Cascada por Grupo")

# -------------------------------------------------
# PESOS OBJETIVO
# -------------------------------------------------

col_p1, col_p2 = st.columns(2)

with col_p1:
    peso_A = st.number_input("Peso objetivo Grupo A (kg)", 18.0, 22.0, 19.2, 0.1, format="%.1f")

with col_p2:
    peso_B = st.number_input("Peso objetivo Grupo B (kg)", 18.0, 22.0, 19.0, 0.1, format="%.1f")

st.divider()

# -------------------------------------------------
# CALIBRES
# -------------------------------------------------

calibres_disponibles = [216,198,175,163,150,138,125,113,100,88,80,72]

col_s1, col_s2 = st.columns(2)

with col_s1:
    grupoA = sorted(
        st.multiselect("Calibres Grupo A", calibres_disponibles, default=[125,113,100]),
        reverse=True
    )

with col_s2:
    grupoB = sorted(
        st.multiselect("Calibres Grupo B", calibres_disponibles, default=[88,80]),
        reverse=True
    )

st.divider()

# -------------------------------------------------
# FUNCIÓN CASCADA REAL
# -------------------------------------------------

def calcular_cascada(grupo, peso_objetivo, nombre_grupo):

    if not grupo:
        return

    st.subheader(f"Grupo {nombre_grupo}")

    # mínimo editable del primer calibre
    min_base = st.number_input(
        f"Mínimo inicial Grupo {nombre_grupo} (g)",
        value=int((peso_objetivo*1000)/grupo[0] * 0.95),
        step=1,
        key=f"min_base_{nombre_grupo}"
    )

    rangos = {}
    minimo_actual = min_base

    for i, calibre in enumerate(grupo):

        promedio_objetivo = (peso_objetivo * 1000) / calibre

        # calcular max buscando que promedio se acerque
        maximo = (promedio_objetivo * 2) - minimo_actual

        rangos[calibre] = (round(minimo_actual), round(maximo))

        minimo_actual = maximo  # cascada

    # Mostrar resultados
    for calibre in grupo:

        min_g, max_g = rangos[calibre]
        promedio = (min_g + max_g) / 2
        peso_real = (promedio * calibre) / 1000

        st.markdown(f"### {nombre_grupo} - {calibre}")
        c1, c2, c3 = st.columns(3)

        c1.metric("Mín (g)", f"{min_g}")
        c2.metric("Máx (g)", f"{max_g}")
        c3.metric("Peso Real", f"{round(peso_real,1)} kg")

        st.divider()


# -------------------------------------------------
# EJECUCIÓN
# -------------------------------------------------

colA, colB = st.columns(2)

with colA:
    calcular_cascada(grupoA, peso_A, "A")

with colB:
    calcular_cascada(grupoB, peso_B, "B")
