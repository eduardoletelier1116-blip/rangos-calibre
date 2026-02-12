import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rangos por Calibre PRO", layout="wide")

st.title("📦 Calculadora Profesional de Rangos por Calibre")

# -----------------------
# CONFIGURACIÓN
# -----------------------

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

# -----------------------
# GENERAR RANGOS
# -----------------------

if st.button("🔄 Generar / Recalcular Rangos"):

    try:
        calibres = [int(c.strip()) for c in calibres_input.split(",") if c.strip()]
        calibres.sort(reverse=True)
    except:
        st.error("Revisa los calibres ingresados.")
        st.stop()

    peso_g = peso_objetivo * 1000

    # Promedios teóricos
    promedios = {c: peso_g / c for c in calibres}

    # Cortes entre calibres
    cortes = []
    for i in range(len(calibres) - 1):
        c1 = calibres[i]
        c2 = calibres[i + 1]
        corte = (promedios[c1] + promedios[c2]) / 2
        cortes.append(corte)

    data = []

    for i, calibre in enumerate(calibres):
        if i == 0:
            hasta = promedios[calibre]
            desde = cortes[i]
        elif i == len(calibres) - 1:
            hasta = cortes[i - 1]
            desde = promedios[calibre]
        else:
            hasta = cortes[i - 1]
            desde = cortes[i]

        data.append({
            "Calibre": calibre,
            "Desde (g)": round(desde),
            "Hasta (g)": round(hasta)
        })

    st.session_state.df = pd.DataFrame(data)

# -----------------------
# MOSTRAR TABLA EDITABLE
# -----------------------

if "df" in st.session_state:

    df_editado = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True
    )

    # Calcular peso real (2 decimales)
    df_editado["Peso real (kg)"] = (
        ((df_editado["Desde (g)"] + df_editado["Hasta (g)"]) / 2)
        * df_editado["Calibre"] / 1000
    ).round(2)

    st.subheader("📊 Resultado Final")
    st.dataframe(df_editado, use_container_width=True)
