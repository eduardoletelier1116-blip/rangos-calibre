import streamlit as st

st.set_page_config(page_title="Calculadora Packing Pro", layout="wide")

# Recordaré que prefieres llamar "Sobrecalibre" al máximo y "Precalibre" al mínimo.
# También he configurado la persistencia para que no se borre la información al actualizar.

# Estilo para asegurar visualización y legibilidad
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8vw !important; }
    .stNumberInput div div input { font-size: 1.1rem !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍎 Control de Calibres y Pesos")

# --- INICIALIZACIÓN DE ESTADO PARA PERSISTENCIA ---
if 'num_grupos' not in st.session_state:
    st.session_state.num_grupos = 1
if 'mapa_pesos' not in st.session_state:
    st.session_state.mapa_pesos = {}

# --- CONFIGURACIÓN DE GRUPOS ---
with st.container():
    for i in range(st.session_state.num_grupos):
        col_p, col_c = st.columns([1, 4])
        with col_p:
            st.session_state[f"p_{i}"] = st.number_input(
                f"Peso Obj {i+1} (kg)", 15.0, 25.0, 
                st.session_state.get(f"p_{i}", 19.20), 0.01, key=f"input_p_{i}"
            )
        with col_c:
            st.session_state[f"s_{i}"] = st.multiselect(
                f"Calibres Grupo {i+1}", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], 
                default=st.session_state.get(f"s_{i}", []), key=f"input_s_{i}"
            )
        
        for c in st.session_state[f"s_{i}"]:
            st.session_state.mapa_pesos[c] = st.session_state[f"p_{i}"]

col_b1, col_b2, _ = st.columns([1, 1, 4])
with col_b1:
    if st.button("➕ Añadir Grupo"):
        st.session_state.num_grupos += 1
        st.rerun()
with col_b2:
    if st.button("🗑️ Reiniciar"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- LÓGICA DE CÁLCULO ---
todos_calibres = sorted(list(st.session_state.mapa_pesos.keys()))

if todos_calibres:
    ideales = [(st.session_state.mapa_pesos[c] * 1000) / c for c in todos_calibres]
    cortes_sug = [int(ideales[0] + 15)]
    for i in range(len(ideales) - 1):
        cortes_sug.append(int((ideales[i] + ideales[i+1]) / 2))
    cortes_sug.append(int(ideales[-1] - 15))

    st.divider()
    
    # --- AJUSTE FINO (FILAS DE 6) ---
    st.subheader("⚙️ Ajuste Fino de Rangos (Gramos)")
    
    puntos_f = []
    cols_por_fila = 6
    
    for i in range(0, len(cortes_sug), cols_por_fila):
        bloque_cortes = cortes_sug[i : i + cols_por_fila]
        cols = st.columns(cols_por_fila)
        
        for j, v_sug in enumerate(bloque_cortes):
            idx_real = i + j
            with cols[j]:
                # Nombres actualizados según tu solicitud
                if idx_real == 0: 
                    label = "Sobrecalibre"
                elif idx_real == len(cortes_sug)-1: 
                    label = "Precalibre"
                else: 
                    label = f"U {todos_calibres[idx_real-1]}/{todos_calibres[idx_real]}"
                
                # Persistencia del valor ajustado
                val = st.number_input(
                    label, value=st.session_state.get(f"f_{idx_real}", v_sug), 
                    step=1, key=f"input_f_{idx_real}"
                )
                st.session_state[f"f_{idx_real}"] = val
                puntos_f.append(val)

    st.divider()

    # --- RESULTADOS ---
    st.subheader("📦 Pesos Reales (2 Decimales)")
    res_cols = st.columns(len(todos_calibres))

    for i, cal in enumerate(todos_calibres):
        promedio = (puntos_f[i] + puntos_f[i+1]) / 2
        peso_r = (promedio * cal) / 1000
        obj = st.session_state.mapa_pesos[cal]
        diff = peso_r - obj
        
        with res_cols[i]:
            st.metric(label=f"Cal {cal}", value=f"{peso_r:.2f}", delta=f"{diff:.2f}")
            st.caption(f"📏 {puntos_f[i]}g - {puntos_f[i+1]}g")
            st.progress(min(max((peso_r - 15) / 10, 0.0), 1.0))

else:
    st.info("Configura los calibres para ver los resultados.")
