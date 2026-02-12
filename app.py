import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rangos PRO", layout="wide")

st.title("📦 Calculadora Profesional de Rangos")

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

if st.button("🔄 Generar Rangos"):

    calibres = [int(c.strip()) for c in calibres_input.split(",") if c.strip()]
    calibres.sort(reverse=True)

    peso_g = peso_objetivo * 1000
    promedios = {c: peso_g / c for c in calibres}

    cortes = []
    for i in range(len(calibres) - 1):
        c1 = calibres[i]
        c2 = calibres[i + 1]
        corte = (promedios[c1] + promedios[c2]) / 2
        cortes.append(corte)

    data = []

    for i, calibre in enumerate(calibres):
        if i == 0:
            hasta = round(promedios[calibre])
            desde = round(cortes[i])
        elif i == len(calibres) - 1:
            hasta = round(cortes[i - 1])
            desde = round(promedios[calibre])
        else:
            hasta = round(cortes[i - 1])
            desde = round(cortes[i])

        data.append({
            "Calibre": calibre,
            "Desde (g)": desde,
            "Hasta (g)": hasta
        })

    st.session_state.df = pd.DataFrame(data)

if "df" in st.session_state:

    df_editado = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Desde (g)": st.column_config.NumberColumn(step=1, format="%d"),
            "Hasta (g)": st.column_config.NumberColumn(step=1, format="%d")
        }
    )

    # ESPEJO: al mover DESDE afecta el HASTA del siguiente
    for i in range(len(df_editado) - 1):
        df_editado.loc[i+1, "Hasta (g)"] = df_editado.loc[i, "Desde (g)"]

    df_editado["Peso real (kg)"] = (
        ((df_editado["Desde (g)"] + df_editado["Hasta (g)"]) / 2)
        * df_editado["Calibre"] / 1000
    ).round(2)

    st.subheader("📊 Resultado Final")
    st.dataframe(df_editado, use_container_width=True)
