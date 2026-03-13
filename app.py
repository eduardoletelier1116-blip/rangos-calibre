import streamlit as st

st.set_page_config(page_title="Calculadora Packing Pro", layout="wide")

# Estilo CSS optimizado
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.6vw !important; }
    .stNumberInput div div input { font-weight: bold; }
    label p { font-size: 1rem !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍎 Control de Calibres y Pesos")

# --- 1. PERSISTENCIA Y MAESTRO DE CALIBRES ---
if 'num_grupos' not in st.session_state:
    st.session_state.num_grupos = 1
if 'lista_maestra' not in st.session_state:
    st.session_state.lista_maestra = [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216]

# --- 2. GESTIÓN DE CALIBRES ---
with st.expander("🛠️ Configurar Lista Maestra de Calibres"):
    col_add, col_del = st.columns(2)
    with col_add:
        nuevo_c = st.number_input("Nuevo Calibre", min_value=1, max_value=500, step=1, key="add_val")
        if st.button("➕ Agregar a la lista"):
            if nuevo_c not in st.session_state.lista_maestra:
                st.session_state.lista_maestra.append(nuevo_c)
                st.session_state.lista_maestra.sort()
                st.rerun()
    with col_del:
        borrar_c = st.selectbox("Eliminar Calibre", st.session_state.lista_maestra, key="del_val")
        if st.button("🗑️ Quitar de la lista"):
            st.session_state.lista_maestra.remove(borrar_c)
            st.rerun()

# --- 3. CONFIGURACIÓN DE PESOS ---
mapa_pesos = {}
with st.container():
    for i in range(st.session_state.num_grupos):
        with st.expander(f"Configuración Grupo {i+1}", expanded=True):
            col_p, col_c = st.columns([1, 4])
            with col_p:
                p_obj = st.number_input(f"Peso Obj (kg)", 15.0, 25.0, 19.20, 0.01, key=f"peso_val_{i}")
            with col_c:
                c_sel = st.multiselect(
                    f"Seleccione Calibres", 
                    st.session_state.lista_maestra, 
                    key=f"cal_sel_{i}",
                    placeholder="Haz clic para añadir calibres..."
                )
            for c in c_sel:
                mapa_pesos[c] = p_obj

col_b1, col_b2, _ = st.columns([1, 1, 4])
with col_b1:
    if st.button("➕ Añadir Grupo de Peso"):
        st.session_state.num_grupos += 1
        st.rerun()
with col_b2:
    if st.button("🔄 Reiniciar Todo"):
        for key in list(st.session_state.keys()):
            if key != 'lista_maestra':
                del st.session_state[key]
        st.rerun()

# --- 4. LÓGICA DE CÁLCULO MEJORADA ---
todos_calibres = sorted(list(mapa_pesos.keys()))

if todos_calibres:
    ideales = [(mapa_pesos[c] * 1000) / c for c in todos_calibres]
    
    # 1. Sobrecalibre (Un 5% más que el ideal del primer calibre)
    sobrecalibre_sug = int(ideales[0] * 1.05)
    
    # 2. Uniones intermedias
    cortes_sugeridos = [sobrecalibre_sug]
    for i in range(len(ideales) - 1):
        cortes_sugeridos.append(int((ideales[i] + ideales[i+1]) / 2))
    
    # 3. Precalibre (Cálculo Inverso para clavar el objetivo del último calibre)
    # Si (Corte_anterior + Precalibre) / 2 * Cal / 1000 = Objetivo
    # Entonces: Precalibre = (Objetivo * 2000 / Cal) - Corte_anterior
    ultimo_corte_previo = cortes_sugeridos[-1]
    gramo_necesario_ultimo = (mapa_pesos[todos_calibres[-1]] * 2000 / todos_calibres[-1]) - ultimo_corte_previo
    cortes_sugeridos.append(int(gramo_necesario_ultimo))

    st.divider()
    
    # --- 5. RANGOS (GRAMOS) ---
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

    # --- 6. PESOS ---
    st.subheader("Pesos")
    res_cols = st.columns(len(todos_calibres))

    for i, cal in enumerate(todos_calibres):
        punto_a = puntos_f[i]
        punto_b = puntos_f[i+1]
        
        promedio = (punto_a + punto_b) / 2
        peso_r = (promedio * cal) / 1000
        obj_especifico = mapa_pesos[cal]
        diff = peso_r - obj_especifico
        
        with res_cols[i]:
            st.metric(label=f"Cal {cal}", value=f"{peso_r:.2f}", delta=f"{diff:.2f}")
            menor = min(punto_a, punto_b)
            mayor = max(punto_a, punto_b)
            st.caption(f"📏 {menor}g - {mayor}g")

else:
    st.info("Configura los calibres para operar.")
