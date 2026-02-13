import streamlit as st

st.set_page_config(page_title="Calibrador PRO Mixto", layout="wide")

st.title("📦 Calibrador Profesional Mixto 18 / 19 KG")

# ---------------- FUNCION GENERADORA ----------------

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


# ---------------- CONFIGURACION GENERAL ----------------

calibres_default = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

calibres_input = st.text_input(
    "Calibres disponibles (separados por coma)",
    value=",".join(map(str, calibres_default))
)

calibres = [int(c.strip()) for c in calibres_input.split(",") if c.strip()]
calibres.sort(reverse=True)

col1, col2 = st.columns(2)

with col1:
    peso_19 = st.number_input("Peso objetivo 19 KG", value=19.0, step=0.1)

with col2:
    peso_18 = st.number_input("Peso objetivo 18 KG", value=18.0, step=0.1)

st.subheader("Seleccionar calibres por peso")

col3, col4 = st.columns(2)

with col3:
    calibres_19 = st.multiselect(
        "Calibres que irán a 19 KG",
        calibres,
        default=[c for c in calibres if c >= 100]
    )

with col4:
    calibres_18 = st.multiselect(
        "Calibres que irán a 18 KG",
        calibres,
        default=[c for c in calibres if c < 100]
    )

# ---------------- PROCESAMIENTO ----------------

def procesar_bloque(calibres_sel, peso_objetivo, key_prefix):

    if not calibres_sel:
        return

    calibres_sel.sort(reverse=True)

    if f"rangos_{key_prefix}" not in st.session_state:
        st.session_state[f"rangos_{key_prefix}"] = generar_rangos(calibres_sel, peso_objetivo)

    rangos = st.session_state[f"rangos_{key_prefix}"]
    peso_g = peso_objetivo * 1000

    st.header(f"⚖ Configuración {peso_objetivo} KG")

    for i, calibre in enumerate(calibres_sel):

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
            hasta = rangos[calibres_sel[i - 1]]

        desde = rangos[calibre]
        peso_real = ((desde + hasta) / 2) * calibre / 1000

        st.write(f"📊 Peso real: **{peso_real:.2f} kg**")
        st.divider()

    # TABLA
    st.subheader(f"📋 Tabla Final {peso_objetivo} KG")

    tabla = []

    for i, calibre in enumerate(calibres_sel):

        desde = rangos[calibre]

        if i == 0:
            hasta = round(peso_g / calibre)
        else:
            hasta = rangos[calibres_sel[i - 1]]

        peso_real = ((desde + hasta) / 2) * calibre / 1000

        tabla.append({
            "Calibre": calibre,
            "Desde (g)": desde,
            "Hasta (g)": hasta,
            "Peso real (kg)": round(peso_real, 2)
        })

    st.dataframe(tabla, use_container_width=True)


st.divider()

procesar_bloque(calibres_19, peso_19, "19")
st.divider()
procesar_bloque(calibres_18, peso_18, "18")
