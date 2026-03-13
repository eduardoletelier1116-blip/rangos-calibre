import streamlit as st

st.set_page_config(page_title="Calculadora de Calibres Pro", layout="wide", page_icon="🍎")

st.title("🍎 Calculadora de Pesos y Calibres Dinámica")
st.markdown("""
Ajusta los rangos de gramos para cada calibre. El **Peso Real** se calculará automáticamente 
en base al promedio de los rangos que definas.
""")

# -------------------------------------------------
# CONFIGURACIÓN INICIAL
# -------------------------------------------------
calibres_disponibles = [216, 198, 175, 163, 150, 138, 125, 113, 100, 88, 80, 72]

col_p1, col_p2 = st.columns(2)
with col_p1:
    peso_obj_A = st.number_input("Peso Objetivo Grupo A (kg)", 15.0, 25.0, 19.5, 0.1)
    grupoA = sorted(st.multiselect("Calibres Grupo A", calibres_disponibles, default=[125, 113, 100]), reverse=True)

with col_p2:
    peso_obj_B = st.number_input("Peso Objetivo Grupo B (kg)", 15.0, 25.0, 19.0, 0.1)
    grupoB = sorted(st.multiselect("Calibres Grupo B", calibres_disponibles, default=[88, 80]), reverse=True)

st.divider()

# -------------------------------------------------
# FUNCIÓN DE CÁLCULO DINÁMICO
# -------------------------------------------------
def render_grupo(grupo, peso_objetivo, nombre_grupo):
    if not grupo:
        st.info(f"Selecciona calibres para el Grupo {nombre_grupo}")
        return

    st.subheader(f"📊 Detalle Grupo {nombre_grupo} (Objetivo: {peso_objetivo} kg)")
    
    for calibre in grupo:
        with st.container():
            # Cálculo inicial sugerido para los sliders (Margen de +/- 10% aprox)
            promedio_ideal = (peso_objetivo * 1000) / calibre
            margen_sugerido = promedio_ideal * 0.1
            
            val_min_init = int(promedio_ideal - margen_sugerido)
            val_max_init = int(promedio_ideal + margen_sugerido)

            col1, col2, col3 = st.columns([2, 3, 2])

            with col1:
                st.markdown(f"### Calibre **{calibre}**")
                # Sliders para ajustar rangos
                rango = st.slider(
                    f"Ajustar Rango (g) - Cal {calibre}",
                    min_value=int(promedio_ideal * 0.5), # Límites lógicos del slider
                    max_value=int(promedio_ideal * 1.5),
                    value=(val_min_init, val_max_init),
                    key=f"slider_{nombre_grupo}_{calibre}"
                )
            
            # Cálculos basados en el slider
            rango_min, rango_max = rango
            promedio_real = (rango_min + rango_max) / 2
            peso_real_calculado = (promedio_real * calibre) / 1000

            with col2:
                # Visualización de métricas
                m1, m2 = st.columns(2)
                m1.metric("Mínimo", f"{rango_min}g")
                m2.metric("Máximo", f"{rango_max}g")
                st.caption(f"Promedio actual: {promedio_real:.1f}g")

            with col3:
                # Color de alerta si el peso se desvía mucho del objetivo
                diferencia = abs(peso_real_calculado - peso_objetivo)
                color = "normal" if diferencia < 0.3 else "inverse"
                
                st.metric(
                    "PESO FINAL", 
                    f"{peso_real_calculado:.2f} kg", 
                    delta=f"{peso_real_calculado - peso_objetivo:.2f} kg vs Obj",
                    delta_color=color
                )

            st.divider()

# -------------------------------------------------
# RENDERIZADO DE COLUMNAS
# -------------------------------------------------
cA, cB = st.columns(2)

with cA:
    render_grupo(grupoA, peso_obj_A, "A")

with cB:
    render_grupo(grupoB, peso_obj_B, "B")
