import streamlit as st

st.set_page_config(page_title="Calculadora Packing Pro", layout="wide")

# Estilo CSS para optimizar el espacio, los botones de selección y métricas
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.6vw !important; }
    .stNumberInput div div input { font-weight: bold; }
    /* Estilo para los selectores tipo pill */
    button[data-baseweb="tab"] { font-size: 1.2rem; }
    label p { font-size: 1rem !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍎 Control de Calibres y Pesos")

# --- 1. PERSISTENCIA ---
if 'num_grupos' not in st.session_state:
    st.session_state.num_grupos = 1

# --- 2. CONFIGURACIÓN ---
mapa_pesos = {}
lista_calibres_total = [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216]

with st.container():
    for i in range(st.session_state.num_grupos):
        # Usamos un borde para diferenciar grupos
        with st.expander(f"Configuración Grupo {i+1}", expanded=True):
            col_p, col_c = st.columns([1, 4])
            with col_p:
                p_obj = st.number_input(f"Peso Obj (kg)", 15.0, 25.0, 19.20, 0.01, key=f"peso_val_{i}")
            with col_c:
                # Diseño de selección con etiquetas (Multi-select con estilo de selección rápida)
                c_sel = st.multiselect(
                    f"Seleccione Calibres", 
                    lista_calibres_total, 
                    key=f"cal_sel_{i}",
                    placeholder="Haz clic para añadir calibres..."
                )
            
            for c in c_sel:
                mapa_pesos[c] = p_obj

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

# --- 3. LÓGICA ---
todos_calibres = sorted(list(mapa_pesos.keys()))

if todos_calibres:
    ideales = [(mapa_pesos[c] * 1000) / c for c in todos_calibres]
    
    # Cascada inicial (Sobrecalibre y Precalibre)
    cortes_sugeridos = [int(ideales[0] + 15)] 
    for i in range(len(ideales) - 1):
        cortes_sugeridos.append(int((ideales[i] + ideales[i+1]) / 2))
    cortes_sugeridos.append(int(ideales[-1] - 15))

    st.divider()
    
    # --- 4. RANGOS (GRAMOS) ---
    st.subheader("Rangos (Gramos)")
    puntos_f = []
    cols_por_fila = 6
    
    for i in range(0, len(cortes_sugeridos), cols_por_fila):
        bloque = cortes_sugeridos[i : i + cols_por_fila]
        cols = st.columns(cols_por_fila)
        
        for j, v_auto in enumerate(bloque):
            idx = i + j
            with cols[j]:
                if idx == 0: label = "Sobrecalibre"
                elif idx == len(cortes_sugeridos)-1: label = "Precalibre"
                else: label = f"{todos_calibres[idx-1]} / {todos_calibres[idx]}"
                
                llave = f"fino_{idx}_{sum(mapa_pesos.values())}_{len(todos_calibres)}"
                val = st.number_input(label, value=int(v_auto), step=1, key=llave)
                puntos_f.append(val)

    st.divider()

    # --- 5. PESOS ---
    st.subheader("Pesos")
    res_cols = st.columns(len(todos_calibres))

    for i, cal in enumerate(todos_calibres):
        # Los puntos de ajuste (gramos)
        punto_a = puntos_f[i]
        punto_b = puntos_f[i+1]
        
        promedio = (punto_a + punto_b) / 2
        peso_r = (promedio * cal) / 1000
        obj_especifico = mapa_pesos[cal]
        diff = peso_r - obj_especifico
        
        with res_cols[i]:
            st.metric(label=f"Cal {cal}", value=f"{peso_r:.2f}", delta=f"{diff:.2f}")
            # RANGO INVERTIDO: Ahora se muestra de MENOR a MAYOR
            menor = min(punto_a, punto_b)
            mayor = max(punto_a, punto_b)
            st.caption(f"📏 {menor}g - {mayor}g")
            st.progress(min(max((peso_real := peso_r - 15) / 10, 0.0), 1.0))

else:
    st.info("Configura los calibres para operar.")
