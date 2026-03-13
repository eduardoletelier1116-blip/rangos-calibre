import streamlit as st

st.set_page_config(page_title="Calculadora Cascada de Precisión", layout="wide")

st.title("🍎 Control de Calibres y Pesos de Precisión")
st.markdown("Configura múltiples objetivos y ajusta manualmente los rangos para llegar al peso exacto.")

# --- INICIALIZACIÓN DE ESTADO ---
if 'num_grupos' not in st.session_state:
    st.session_state.num_grupos = 1

# --- SECCIÓN DE ENTRADAS DINÁMICAS ---
mapa_pesos = {}

st.subheader("📋 Configuración de Calibres")
with st.container():
    for i in range(st.session_state.num_grupos):
        col_p, col_c = st.columns([1, 3])
        with col_p:
            # Permitimos ingresar el peso con 2 decimales en la entrada también
            p_obj = st.number_input(f"Peso Objetivo {i+1} (kg)", 15.0, 25.0, 19.20, 0.01, key=f"peso_{i}")
        with col_c:
            c_sel = st.multiselect(f"Calibres Grupo {i+1}", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], key=f"sel_{i}")
        
        for c in c_sel:
            mapa_pesos[c] = p_obj

col_btns = st.columns([1, 1, 4])
with col_btns[0]:
    if st.button("➕ Añadir Grupo"):
        st.session_state.num_grupos += 1
        st.rerun()
with col_btns[1]:
    if st.button("🗑️ Reiniciar"):
        st.session_state.num_grupos = 1
        st.rerun()

# --- PROCESAMIENTO UNIFICADO ---
todos_calibres = sorted(list(mapa_pesos.keys()))

if todos_calibres:
    # 1. Gramajes ideales (Cálculo interno inicial)
    gramajes_ideales = [ (mapa_pesos[c] * 1000) / c for c in todos_calibres ]
    
    # 2. Cortes automáticos iniciales (Cascada)
    puntos_sugeridos = [int(gramajes_ideales[0] + 15)]
    for i in range(len(gramajes_ideales) - 1):
        union = (gramajes_ideales[i] + gramajes_ideales[i+1]) / 2
        puntos_sugeridos.append(int(union))
    puntos_sugeridos.append(int(gramajes_ideales[-1] - 15))

    st.divider()
    st.subheader("⚙️ Ajuste Fino de Rangos (Modificable)")
    st.info("Cambia los gramos de cada corte para ajustar el peso final de la caja.")
    
    # --- INTERFAZ DE AJUSTE MANUAL ---
    puntos_finales = []
    cols_ajuste = st.columns(len(puntos_sugeridos))
    
    for i, p_val in enumerate(puntos_sugeridos):
        with cols_ajuste[i]:
            if i == 0: label = "Máximo"
            elif i == len(puntos_sugeridos)-1: label = "Mínimo"
            else: label = f"Unión {todos_calibres[i-1]}/{todos_calibres[i]}"
            
            # El usuario puede modificar estos valores libremente
            # La key depende de los calibres seleccionados para reiniciarse solo cuando cambia la estructura
            v = st.number_input(label, value=p_val, step=1, key=f"fino_{i}_{len(todos_calibres)}")
            puntos_finales.append(v)

    st.divider()

    # --- RESULTADOS FINALES CON 2 DECIMALES ---
    st.subheader("📦 Pesos Reales Calculados (2 Decimales)")
    res_cols = st.columns(len(todos_calibres))

    for i, cal in enumerate(todos_calibres):
        g_alto = puntos_finales[i]
        g_bajo = puntos_finales[i+1]
        promedio = (g_alto + g_bajo) / 2
        peso_real = (promedio * cal) / 1000
        obj_cal = mapa_pesos[cal]
        
        with res_cols[i]:
            diff = peso_real - obj_cal
            # Color verde si el error es menor a 100 gramos
            color = "normal" if abs(diff) < 0.1 else "inverse"
            
            # Mostramos el peso con :.2f para asegurar los 2 decimales
            st.metric(
                label=f"Calibre {cal}", 
                value=f"{peso_real:.2f} kg", 
                delta=f"{diff:.2f} vs {obj_cal:.2f}",
                delta_color=color
            )
            st.markdown(f"📏 **{int(g_alto)}g - {int(g_bajo)}g**")
            st.progress(min(max((peso_real - 15) / 10, 0.0), 1.0))

else:
    st.info("Configura los calibres arriba para generar la tabla de control.")
