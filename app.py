import streamlit as st

st.set_page_config(page_title="Calculadora Packing Pro", layout="wide")

# Estilo para asegurar visualización y evitar cortes de texto
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.6vw !important; }
    .stNumberInput div div input { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍎 Control de Calibres y Pesos")

# --- 1. INICIALIZACIÓN DE VARIABLES (PERSISTENCIA) ---
if 'num_grupos' not in st.session_state:
    st.session_state.num_grupos = 1

# --- 2. CONFIGURACIÓN DE GRUPOS ---
mapa_pesos = {}
with st.container():
    for i in range(st.session_state.num_grupos):
        col_p, col_c = st.columns([1, 4])
        with col_p:
            # El valor se guarda en session_state automáticamente por el 'key'
            p_obj = st.number_input(f"Peso Obj {i+1} (kg)", 15.0, 25.0, 19.20, 0.01, key=f"peso_val_{i}")
        with col_c:
            c_sel = st.multiselect(f"Calibres Grupo {i+1}", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], key=f"cal_sel_{i}")
        
        for c in c_sel:
            mapa_pesos[c] = p_obj

col_b1, col_b2, _ = st.columns([1, 1, 4])
with col_b1:
    if st.button("➕ Añadir Grupo"):
        st.session_state.num_grupos += 1
        st.rerun()
with col_b2:
    if st.button("🗑️ Reiniciar"):
        # Limpia todo el estado para empezar de cero
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- 3. LÓGICA DE CÁLCULO ---
todos_calibres = sorted(list(mapa_pesos.keys()))

if todos_calibres:
    # Calculamos los gramajes ideales para cada calibre seleccionado
    ideales = [(mapa_pesos[c] * 1000) / c for c in todos_calibres]
    
    # Definimos los cortes sugeridos (cascada inicial)
    cortes_sugeridos = [int(ideales[0] + 15)] # Sobrecalibre
    for i in range(len(ideales) - 1):
        cortes_sugeridos.append(int((ideales[i] + ideales[i+1]) / 2)) # Uniones
    cortes_sugeridos.append(int(ideales[-1] - 15)) # Precalibre

    st.divider()
    
    # --- 4. AJUSTE FINO (FILAS DE 6) ---
    st.subheader("⚙️ Ajuste Fino de Rangos (Gramos)")
    
    puntos_f = []
    cols_por_fila = 6
    
    for i in range(0, len(cortes_sugeridos), cols_por_fila):
        bloque = cortes_sugeridos[i : i + cols_por_fila]
        cols = st.columns(cols_por_fila)
        
        for j, v_auto in enumerate(bloque):
            idx = i + j
            with cols[j]:
                # Nombre según tu preferencia
                if idx == 0: label = "Sobrecalibre"
                elif idx == len(cortes_sugeridos)-1: label = "Precalibre"
                else: label = f"U {todos_calibres[idx-1]}/{todos_calibres[idx]}"
                
                # KEY DINÁMICA: Si cambia el peso objetivo o la lista de calibres, se resetea al sugerido
                # Si no, mantiene lo que el usuario escribió.
                llave_fino = f"fino_ajuste_{idx}_{sum(mapa_pesos.values())}_{len(todos_calibres)}"
                
                val = st.number_input(label, value=int(v_auto), step=1, key=llave_fino)
                puntos_f.append(val)

    st.divider()

    # --- 5. RESULTADOS ---
    st.subheader("📦 Pesos Reales (2 Decimales)")
    res_cols = st.columns(len(todos_calibres))

    for i, cal in enumerate(todos_calibres):
        promedio = (puntos_f[i] + puntos_f[i+1]) / 2
        peso_r = (promedio * cal) / 1000
        obj_especifico = mapa_pesos[cal]
        diff = peso_r - obj_especifico
        
        with res_cols[i]:
            st.metric(label=f"Cal {cal}", value=f"{peso_r:.2f}", delta=f"{diff:.2f}")
            st.caption(f"📏 {puntos_f[i]}g - {puntos_f[i+1]}g")
            st.progress(min(max((peso_r - 15) / 10, 0.0), 1.0))

else:
    st.info("Configura los calibres arriba para iniciar el cálculo.")
