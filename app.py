import streamlit as st

st.set_page_config(page_title="Calculadora Packing Pro", layout="wide")

# CSS Avanzado para forzar la visibilidad de botones y permitir scroll
st.markdown("""
    <style>
    /* Evita que los números de peso se corten */
    [data-testid="stMetricValue"] { font-size: 1.4vw !important; }
    
    /* Fuerza un ancho mínimo a las columnas de ajuste para que el + y - no desaparezcan */
    [data-testid="column"] {
        min-width: 120px !important;
    }
    
    /* Permite scroll horizontal si hay demasiados calibres */
    .main .block-container {
        overflow-x: auto;
    }
    
    /* Estilo para los inputs numéricos */
    .stNumberInput div div input {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍎 Control de Calibres y Pesos")

# --- ESTADO DE LA APP ---
if 'num_grupos' not in st.session_state:
    st.session_state.num_grupos = 1

# --- CONFIGURACIÓN DE GRUPOS ---
mapa_pesos = {}
with st.container():
    for i in range(st.session_state.num_grupos):
        col_p, col_c = st.columns([1, 4])
        with col_p:
            p_obj = st.number_input(f"Peso Obj {i+1} (kg)", 15.0, 25.0, 19.20, 0.01, key=f"p_{i}")
        with col_c:
            c_sel = st.multiselect(f"Calibres Grupo {i+1}", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], key=f"s_{i}")
        for c in c_sel:
            mapa_pesos[c] = p_obj

col_b1, col_b2, _ = st.columns([1, 1, 4])
with col_b1:
    if st.button("➕ Añadir Grupo"):
        st.session_state.num_grupos += 1
        st.rerun()
with col_b2:
    if st.button("🗑️ Reiniciar"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- LÓGICA DE CÁLCULO ---
todos_calibres = sorted(list(mapa_pesos.keys()))

if todos_calibres:
    ideales = [(mapa_pesos[c] * 1000) / c for c in todos_calibres]
    cortes_sug = [int(ideales[0] + 15)]
    for i in range(len(ideales) - 1):
        cortes_sug.append(int((ideales[i] + ideales[i+1]) / 2))
    cortes_sug.append(int(ideales[-1] - 15))

    st.divider()
    
    # --- AJUSTE FINO (SCROLLABLE SI ES NECESARIO) ---
    st.subheader("⚙️ Ajuste Fino de Rangos (Gramos)")
    
    # Creamos un contenedor horizontal para los inputs
    puntos_f = []
    cols_adj = st.columns(len(cortes_sug))
    
    for i, v_sug in enumerate(cortes_sug):
        with cols_adj[i]:
            label = "Máx" if i == 0 else ("Mín" if i == len(cortes_sug)-1 else f"U {todos_calibres[i-1]}/{todos_calibres[i]}")
            # El step=1 y el CSS de min-width aseguran los botones
            val = st.number_input(label, value=v_sug, step=1, key=f"f_{i}_{len(todos_calibres)}")
            puntos_f.append(val)

    st.divider()

    # --- RESULTADOS ---
    st.subheader("📦 Pesos Reales (2 Decimales)")
    res_cols = st.columns(len(todos_calibres))

    for i, cal in enumerate(todos_calibres):
        promedio = (puntos_f[i] + puntos_f[i+1]) / 2
        peso_r = (promedio * cal) / 1000
        obj = mapa_pesos[cal]
        diff = peso_r - obj
        
        with res_cols[i]:
            st.metric(label=f"Cal {cal}", value=f"{peso_r:.2f}", delta=f"{diff:.2f}")
            st.caption(f"📏 {puntos_f[i]}g - {puntos_f[i+1]}g")
            st.progress(min(max((peso_r - 15) / 10, 0.0), 1.0))

else:
    st.info("Configura los calibres para ver los resultados.")
