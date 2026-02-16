import streamlit as st

st.set_page_config(page_title="Calculadora Cascada Profesional", layout="wide")

st.title("🍎 Calculadora Cascada Editable por Grupo")

# -------------------------------------------------
# PESOS OBJETIVO
# -------------------------------------------------

col_p1, col_p2 = st.columns(2)

with col_p1:
    peso_A = st.number_input("Peso objetivo Grupo A (kg)", 18.0, 22.0, 19.2, 0.1)

with col_p2:
    peso_B = st.number_input("Peso objetivo Grupo B (kg)", 18.0, 22.0, 19.0, 0.1)

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
# CASCADA CORRECTA SIN PROPAGACIÓN DE ERROR
# -------------------------------------------------

def calcular_cascada(grupo, peso_objetivo, nombre):

    if not grupo:
        return

    st.subheader(f"Grupo {nombre}")

    minimos = []

    for i, calibre in enumerate(grupo):

        promedio_obj = (peso_objetivo * 1000) / calibre
        key_min = f"{nombre}_{calibre}_min"

        # Valor inicial independiente
        if key_min not in st.session_state:
            st.session_state[key_min] = round(promedio_obj - 10)

        minimo = st.number_input(
            f"{nombre} - {calibre} Mín (g)",
            step=1,
            key=key_min
        )

        minimos.append(minimo)

    # -------------------------------------------------
    # Ahora reconstruimos la cascada completa correctamente
    # -------------------------------------------------

    limite_superior = None

    for i, calibre in enumerate(grupo):

        promedio_obj = (peso_objetivo * 1000) / calibre
        minimo = minimos[i]

        if i == 0:
            maximo = (2 * promedio_obj) - minimo
        else:
            maximo = limite_superior

        if minimo > maximo:
            minimo, maximo = maximo, minimo

        promedio_real = (minimo + maximo) / 2
        peso_real = (promedio_real * calibre) / 1000

        col1, col2, col3 = st.columns(3)

        col1.metric("Mín (g)", f"{int(minimo)}")
        col2.metric("Máx (g)", f"{int(maximo)}")
        col3.metric("Peso Real", f"{peso_real:.1f} kg")

        st.divider()

        limite_superior = minimo


# -------------------------------------------------
# EJECUCIÓN
# -------------------------------------------------

colA, colB = st.columns(2)

with colA:
    calcular_cascada(grupoA, peso_A, "A")

with colB:
    calcular_cascada(grupoB, peso_B, "B")
