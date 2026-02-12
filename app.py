import streamlit as st

st.set_page_config(page_title="Rangos PRO Móvil", layout="wide")

st.title("📦 Rangos de Calibre - Modo Operario")

# ---------------- PESO ----------------
peso_objetivo = st.number_input(
    "Peso objetivo (kg)",
    value=19.0,
    step=0.1,
    format="%.2f"
)

calibres_default = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

calibres_input = st.text_input(
    "Calibres (separados por coma)",
    value=",".join(map(str, calibres_default))
)

calibres = [int(c.strip()) for c in calibres_input.split(",") if c.strip()]
calibres.sort(reverse=True)

peso_g = peso_objetivo * 1000

# ---------------- INICIALIZAR SESSION ----------------
if "rangos" not in st.session_state:
    st.session_state.rangos = {}

    for i, calibre in enumerate(calibres):
        promedio = peso_g / calibre
        st.session_state.rangos[calibre] = round(promedio)

# ---------------- BLOQUES ----------------

st.divider()

for i, calibre in enumerate(calibres):

    st.subheader(f"Calibre {calibre}")

    col1, col2, col3 = st.columns([1,2,1])

    # Botón -
    if col1.button("➖", key=f"menos_{calibre}"):
        st.session_state.rangos[calibre] -= 1

    # Número editable
    nuevo_valor = col2.number_input(
        "Desde (g)",
        value=st.session_state.rangos[calibre],
        step=1,
        key=f"input_{calibre}"
    )

    st.session_state.rangos[calibre] = nuevo_valor

    # Botón +
    if col3.button("➕", key=f"mas_{calibre}"):
        st.session_state.rangos[calibre] += 1

    # -------- ESPEJO HACIA ABAJO --------
    if i < len(calibres) - 1:
        siguiente = calibres[i + 1]
        st.session_state.rangos[siguiente] = st.session_state.rangos[calibre]

    # -------- CALCULAR PESO REAL --------
    hasta = st.session_state.rangos[calibre]
    desde = st.session_state.rangos[calibre]

    peso_real = ((desde + hasta) / 2) * calibre / 1000

    st.write(f"📊 Peso real: **{peso_real:.2f} kg**")

    st.divider()
