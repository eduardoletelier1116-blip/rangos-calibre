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

# ---------------- GENERAR RANGOS CORRECTOS ----------------
def generar_rangos():
    promedios = {c: peso_g / c for c in calibres}
    cortes = []

    for i in range(len(calibres) - 1):
        c1 = calibres[i]
        c2 = calibres[i + 1]
        corte = (promedios[c1] + promedios[c2]) / 2
        cortes.append(round(corte))

    rangos = {}

    for i, calibre in enumerate(calibres):
        if i == 0:
            rangos[calibre] = cortes[i]
        elif i == len(calibres) - 1:
            rangos[calibre] = round(promedios[calibre])
        else:
            rangos[calibre] = cortes[i]

    return rangos


if "rangos" not in st.session_state:
    st.session_state.rangos = generar_rangos()

if st.button("🔄 Recalcular desde peso objetivo"):
    st.session_state.rangos = generar_rangos()

# ---------------- BLOQUES ----------------

st.divider()

for i, calibre in enumerate(calibres):

    st.subheader(f"Calibre {calibre}")

    col1, col2, col3 = st.columns([1,2,1])

    if col1.button("➖", key=f"menos_{calibre}"):
        st.session_state.rangos[calibre] -= 1

    nuevo_valor = col2.number_input(
        "Desde (g)",
        value=st.session_state.rangos[calibre],
        step=1,
        key=f"input_{calibre}"
    )

    st.session_state.rangos[calibre] = nuevo_valor

    if col3.button("➕", key=f"mas_{calibre}"):
        st.session_state.rangos[calibre] += 1

    # -------- PESO REAL --------
    if i == 0:
        hasta = round(peso_g / calibre)
    else:
        hasta = st.session_state.rangos[calibres[i - 1]]

    desde = st.session_state.rangos[calibre]

    peso_real = ((desde + hasta) / 2) * calibre / 1000

    st.write(f"📊 Peso real: **{peso_real:.2f} kg**")

    st.divider()

# -------- ESPEJO GLOBAL (DESPUÉS DE DIBUJAR) --------
for i in range(len(calibres) - 1):
    actual = calibres[i]
    siguiente = calibres[i + 1]
    st.session_state.rangos[siguiente] = st.session_state.rangos[actual]
