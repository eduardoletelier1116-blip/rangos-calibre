import streamlit as st

st.set_page_config(page_title="Calibrador PRO", layout="wide")

st.title("📦 Calibrador Profesional 18 / 19 KG")

# ---------------- LISTAS OFICIALES ----------------

calibres_18 = [216,198,178,165,150,135,120,110,100,90,80,70,60]
calibres_19 = [216,198,175,163,150,138,125,113,100,88,80,72,64]

calibres_18.sort(reverse=True)
calibres_19.sort(reverse=True)

# ---------------- SELECCION MODO ----------------

modo = st.radio(
    "Seleccionar tipo de caja:",
    ["18 KG", "19 KG"],
    horizontal=True
)

# Inicializar pesos si no existen
if "peso_18" not in st.session_state:
    st.session_state["peso_18"] = 18.00

if "peso_19" not in st.session_state:
    st.session_state["peso_19"] = 19.00

if modo == "18 KG":
    lista_calibres = calibres_18
    key_prefix = "18"

    peso_objetivo = st.number_input(
        "Peso objetivo 18 KG",
        step=0.01,
        format="%.2f",
        key="peso_18"
    )
else:
    lista_calibres = calibres_19
    key_prefix = "19"

    peso_objetivo = st.number_input(
        "Peso objetivo 19 KG",
        step=0.01,
        format="%.2f",
        key="peso_19"
    )

# ---------------- SELECCION CALIBRES ACTIVOS ----------------

calibres_activos = st.multiselect(
    "Seleccionar calibres a trabajar",
    lista_calibres,
    default=lista_calibres
)

calibres_activos.sort(reverse=True)

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

# ---------------- INICIALIZAR RANGOS ----------------

if calibres_activos:

    if f"rangos_{key_prefix}" not in st.session_state:
        st.session_state[f"rangos_{key_prefix}"] = generar_rangos(calibres_activos, peso_objetivo)

    rangos = st.session_state[f"rangos_{key_prefix}"]
    peso_g = peso_objetivo * 1000

    st.divider()

    # ---------------- BLOQUES OPERADOR ----------------

    for i, calibre in enumerate(calibres_activos):

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
            hasta = rangos[calibres_activos[i - 1]]

        desde = rangos[calibre]
        peso_real = ((desde + hasta) / 2) * calibre / 1000
        diferencia = peso_real - peso_objetivo

        st.write(f"📊 Peso real: **{peso_real:.2f} kg**")
        st.write(f"🎯 Diferencia: **{diferencia:+.2f} kg**")
        st.divider()

    # ---------------- TABLA FINAL ----------------

    st.subheader("📋 Tabla Final")

    tabla = []

    for i, calibre in enumerate(calibres_activos):

        desde = rangos[calibre]

        if i == 0:
            hasta = round(peso_g / calibre)
        else:
            hasta = rangos[calibres_activos[i - 1]]

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
