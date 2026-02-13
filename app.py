import streamlit as st

st.set_page_config(page_title="Calibrador PRO Doble", layout="wide")

st.title("📦 Calibrador Profesional Doble Peso")

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


# ---------------- FUNCION BLOQUE COMPLETO ----------------

def bloque_peso(nombre, peso_default, key_prefix):

    st.header(f"⚖ {nombre}")

    peso = st.number_input(
        f"Peso objetivo {nombre} (kg)",
        value=peso_default,
        step=0.1,
        format="%.2f",
        key=f"peso_{key_prefix}"
    )

    calibres_default = [216,198,175,163,150,138,125,113,100,88,80,72,64,56]

    calibres_input = st.text_input(
        f"Calibres {nombre} (separados por coma)",
        value=",".join(map(str, calibres_default)),
        key=f"calibres_{key_prefix}"
    )

    calibres = [int(c.strip()) for c in calibres_input.split(",") if c.strip()]
    calibres.sort(reverse=True)

    if f"rangos_{key_prefix}" not in st.session_state:
        st.session_state[f"rangos_{key_prefix}"] = generar_rangos(calibres, peso)

    if st.button(f"🔄 Recalcular {nombre}", key=f"recalcular_{key_prefix}"):
        st.session_state[f"rangos_{key_prefix}"] = generar_rangos(calibres, peso)

    rangos = st.session_state[f"rangos_{key_prefix}"]
    peso_g = peso * 1000

    st.divider()

    # -------- BLOQUES OPERARIO --------
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

        st.write(f"📊 Peso real: **{peso_real:.2f} kg**")
        st.divider()

    # -------- TABLA FINAL --------
    st.subheader(f"📋 Tabla Final {nombre}")

    tabla = []

    for i, calibre in enumerate(calibres):

        desde = rangos[calibre]

        if i == 0:
            hasta = round(peso_g / calibre)
        else:
            hasta = rangos[calibres[i - 1]]

        peso_real = ((desde + hasta) / 2) * calibre / 1000

        tabla.append({
            "Calibre": calibre,
            "Desde (g)": desde,
            "Hasta (g)": hasta,
            "Peso real (kg)": round(peso_real, 2)
        })

    st.dataframe(tabla, use_container_width=True)


# ---------------- EJECUTAR BLOQUES ----------------

bloque_peso("19 KG", 19.0, "19")
st.divider()
bloque_peso("18 KG", 18.0, "18")
