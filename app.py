import streamlit as st

st.set_page_config(page_title="Calculadora Cascada Profesional", layout="wide")

st.title("🍎 Calculadora Cascada Editable por Grupo")

# -------------------------------------------------
# PESOS OBJETIVO
# -------------------------------------------------

col_p1, col_p2 = st.columns(2)

with col_p1:
    peso_A = st.number_input("Peso objetivo Grupo A (kg)", 18.0, 22.0, 19.2, 0.1, format="%.1f", key="pesoA")

with col_p2:
    peso_B = st.number_input("Peso objetivo Grupo B (kg)", 18.0, 22.0, 19.0, 0.1, format="%.1f", key="pesoB")

st.divider()

# -------------------------------------------------
# CALIBRES
# -------------------------------------------------

calibres_disponibles = [216,198,175,163,150,138,125,113,100,88,80,72]

col_s1, col_s2 = st.columns(2)

with col_s1:
    grupoA = sorted(
        st.multiselect("Calibres Grupo A", calibres_disponibles, default=[125,113,100], key="grupoA"),
        reverse=True
    )

with col_s2:
    grupoB = sorted(
        st.multiselect("Calibres Grupo B", calibres_disponibles, default=[88,80], key="grupoB"),
        reverse=True
    )

# Botón de reinicio
reset = st.button("🔄 Recalcular desde cero")

st.divider()

# -------------------------------------------------
# FUNCIÓN CASCADA LIMPIA
# -------------------------------------------------

def calcular_cascada(grupo, peso_objetivo, nombre):

    if not grupo:
        return

    st.subheader(f"Grupo {nombre}")

    limite_superior = None

    for i, calibre in enumerate(grupo):

        promedio_obj = (peso_objetivo * 1000) / calibre

        key_min = f"{nombre}_{calibre}_min"

        # REINICIO INTELIGENTE
        if reset or key_min not in st.session_state:

            if i == 0:
                minimo_inicial = round(promedio_obj - 10)
            else:
                minimo_inicial = round((2 * promedio_obj) - limite_superior)

            st.session_state[key_min] = minimo_inicial

        minimo = st.number_input(
            f"{nombre} - {calibre} Mín (g)",
            step=1,
            key=key_min
        )

        # CASCADA REAL
        if i == 0:
            maximo = round((2 * promedio_obj) - minimo)
        else:
            maximo = limite_superior

        promedio_real = (minimo + maximo) / 2
        peso_real = (promedio_real * calibre) / 1000
        diferencia = peso_real - peso_objetivo

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Mín (g)", f"{int(minimo)}")
        col2.metric("Máx (g)", f"{int(maximo)}")
        col3.metric("Peso Real", f"{peso_real:.1f} kg")
        col4.metric("Δ vs Obj", f"{diferencia:+.1f} kg")

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
