import streamlit as st

st.set_page_config(page_title="Calculadora Multigrupo Manzanas", layout="wide")

st.title("🍎 Control de Calibres por Grupos de Peso")
st.markdown("Configura pesos diferentes para distintos grupos manteniendo la cascada interna.")

def generar_cascada(nombre_grupo, peso_obj, calibres_sel):
    if not calibres_sel:
        st.info(f"Selecciona calibres para el {nombre_grupo}")
        return

    calibres_sel.sort() # De más grande a más pequeño
    
    # 1. Cálculo de promedios ideales
    gramajes_ideales = [(peso_obj * 1000) / c for c in calibres_sel]
    
    # 2. Definición de cortes automáticos
    cortes_iniciales = [int(gramajes_ideales[0] + (gramajes_ideales[0] * 0.05))]
    for i in range(len(gramajes_ideales) - 1):
        union = (gramajes_ideales[i] + gramajes_ideales[i+1]) / 2
        cortes_iniciales.append(int(union))
    cortes_iniciales.append(int(gramajes_ideales[-1] - (gramajes_ideales[-1] * 0.05)))

    # 3. Interfaz de Ajuste
    st.subheader(f"⚙️ Ajuste {nombre_grupo} (Objetivo: {peso_obj} kg)")
    puntos_finales = []
    cols_ajuste = st.columns(len(cortes_iniciales))
    
    for i, valor_auto in enumerate(cortes_iniciales):
        with cols_ajuste[i]:
            # Label simplificado para no saturar la vista
            label = "Mín" if i == len(cortes_iniciales)-1 else (f"Corte" if i > 0 else "Máx")
            v = st.number_input(f"{label} p{i}", value=valor_auto, step=1, key=f"c_{nombre_grupo}_{i}_{peso_obj}")
            puntos_finales.append(v)

    # 4. Resultados
    res_cols = st.columns(len(calibres_sel))
    for i, cal in enumerate(calibres_sel):
        g_alto = puntos_finales[i]
        g_bajo = puntos_finales[i+1]
        promedio = (g_alto + g_bajo) / 2
        peso_final = (promedio * cal) / 1000
        
        with res_cols[i]:
            diff = peso_final - peso_obj
            color = "normal" if abs(diff) < 0.1 else "inverse"
            st.metric(f"Cal {cal}", f"{peso_final:.2f} kg", f"{diff:.2f}", delta_color=color)
            st.caption(f"**{int(g_alto)}g - {int(g_bajo)}g**")
    st.divider()

# --- INTERFAZ PRINCIPAL ---

# Definición de Grupo A
colA1, colA2 = st.columns([1, 2])
with colA1:
    p_obj_A = st.number_input("Peso Objetivo Grupo A", 15.0, 25.0, 19.2, 0.1)
with colA2:
    cal_A = st.multiselect("Calibres Grupo A", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], default=[88, 100, 113], key="sel_a")

generar_cascada("Grupo A", p_obj_A, cal_A)

# Definición de Grupo B
colB1, colB2 = st.columns([1, 2])
with colB1:
    p_obj_B = st.number_input("Peso Objetivo Grupo B", 15.0, 25.0, 20.2, 0.1)
with colB2:
    cal_B = st.multiselect("Calibres Grupo B", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], default=[150], key="sel_b")

generar_cascada("Grupo B", p_obj_B, cal_B)
