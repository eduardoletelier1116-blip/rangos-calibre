import streamlit as st

st.set_page_config(page_title="Calibrador PRO Dual", layout="wide")

st.title("📦 Calibrador Profesional 18 / 19 KG")

# ---------------- LISTAS OFICIALES ----------------

calibres_18_base = [216,198,178,165,150,135,120,110,100,90,80,70,60]
calibres_19_base = [216,198,175,163,150,138,125,113,100,88,80,72,64]

calibres_18_base.sort(reverse=True)
calibres_19_base.sort(reverse=True)

# ---------------- INICIALIZAR ESTADOS ----------------

if "peso_18" not in st.session_state:
    st.session_state.peso_18 = 18.00

if "peso_19" not in st.session_state:
    st.session_state.peso_19 = 19.00

if "rangos_18" not in st.session_state:
    st.session_state.rangos_18 = {}

if "rangos_19" not in st.session_state:
    st.session_state.rangos_19 = {}

# ---------------- PESOS OBJETIVO ----------------

col1, col2 = st.columns(2)

with col1:
    peso_18 = st.number_input(
        "Peso objetivo 18 KG",
        step=0.01,
        format="%.2f",
        key="peso_18"
    )

with col2:
    peso_19 = st.number_input(
        "Peso objetivo 19 KG",
        step=0.01,
        format="%.2f",
        key="peso_19"
    )

st.divider()

# ---------------- SELECCION CALIBRES ----------------

col3, col4 = st.columns(2)

with col3:
    st.subheader("Calibres para 18 KG")
    calibres_18 = st.multiselect(
        "",
        calibres_18_base,
        default=calibres_18_base
    )

with col4:
    st.subheader("Calibres para 19 KG")
    calibres_19 = st.multiselect(
        "",
        calibres_19_base,
        default=calibres_19_base
    )

calibres_18.sort(reverse=True)
calibres_19.sort(reverse=True)

# ---------------- FUNCION GENERAR RANGOS ----------------

def generar_rangos(calibres, peso_objetivo):
    peso_g = peso_objetivo * 1000
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

# ---------------- BLOQUE CALCULO ----------------

def bloque(calibres, peso_objetivo, key_prefix):

    if not calibres:
        return

    if not st.session_state[f"rangos_{key_prefix}"]:
        st.session_state[f"rangos_{key_prefix}"] = generar_rangos(calibres, peso_objetivo)

    rangos = st.session_state[f"rangos_{key_prefix}"]
    peso_g = peso_objetivo * 1000

    st.header(f"⚖ Configuración {peso_objetivo:.2f} KG")

    for i, calibre in enumerate(calibres):

        st.subheader(f"Calibre {calibre}")

        col1, col2, col3 = st.columns([1,2,1])

        if col1.button("➖", key=f"menos_{key_prefix}_{calibre}"):
            rangos[calibre] -= 1

        col2.markdown(
            f"<h2 style='text-align:center'>{rangos[calibre]} g</h2>",
            unsafe_allow_html=True
        )

        if col3.button("➕", key=f"mas_{key_prefix}_{calibre}"):
            rangos[calibre] += 1

        if i == 0:
            hasta = round(peso_g / calibre)
        else:
            hasta = rangos[calibres[i - 1]]

        desde = rangos[calibre]
        peso_real = ((desde + hasta) / 2) * calibre / 1000
        diferencia = peso_real - peso_objetivo

        st.write(f"📊 Peso real: **{peso_real:.2f} kg**")
        st.write(f"🎯 Diferencia: **{diferencia:+.2f} kg**")
        st.divider()

    # Tabla final
    tabla = []

    for i, calibre in enumerate(calibres):

        desde = rangos[calibre]

        if i == 0:
            hasta = round(peso_g / calibre)
        else:
            hasta = rangos[calibres[i - 1]]

        peso_real = ((desde + hasta) / 2) * calibre / 1000
        diferencia = peso_real - peso_objetivo

        tabla.append({
            "Calibre": calibre,
            "Desde (g)": desde,
            "Hasta (g)": hasta,
            "Peso real (kg)": round(peso_real, 2),
            "Diferencia (kg)": round(diferencia, 2)
        })

    st.dataframe(tabla, use_container_width=True)


st.divider()

col5, col6 = st.columns(2)

with col5:
    bloque(calibres_18, peso_18, "18")

with col6:
    bloque(calibres_19, peso_19, "19")
