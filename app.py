import streamlit as st

st.set_page_config(page_title="Calculadora Cascada Dinámica", layout="wide")

st.title("🍎 Calculadora de Procesos Multicontrol")
st.markdown("Añade grupos de peso según los requerimientos y ajusta la cascada unificada.")

# --- INICIALIZACIÓN DE ESTADO ---
if 'num_grupos' not in st.session_state:
    st.session_state.num_grupos = 1

# --- SECCIÓN DE ENTRADAS DINÁMICAS ---
mapa_pesos = {}

st.subheader("📋 Configuración de Calibres")
# Usamos un contenedor para organizar los grupos
with st.container():
    # Creamos columnas para que los inputs no ocupen todo el ancho si son pocos
    for i in range(st.session_state.num_grupos):
        col_p, col_c = st.columns([1, 3])
        with col_p:
            p_obj = st.number_input(f"Peso Objetivo {i+1} (kg)", 15.0, 25.0, 19.2, 0.1, key=f"peso_{i}")
        with col_c:
            c_sel = st.multiselect(f"Calibres Grupo {i+1}", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], key=f"sel_{i}")
        
        # Guardamos la relación calibre -> peso
        for c in c_sel:
            mapa_pesos[c] = p_obj

# Botón para añadir más grupos
if st.button("➕ Añadir Grupo de Peso"):
    st.session_state.num_grupos += 1
    st.rerun()

# --- PROCESAMIENTO UNIFICADO ---
todos_calibres = sorted(list(mapa_pesos.keys()))

if todos_calibres:
    # 1. Gramajes ideales
    gramajes_ideales = [ (mapa_pesos[c] * 1000) / c for c in todos_calibres ]
    
    # 2. Cortes automáticos (Cascada)
    puntos_auto = [int(gramajes_ideales[0] + 15)]
    for i in range(len(gramajes_ideales) - 1):
        union = (gramajes_ideales[i] + gramajes_ideales[i+1]) / 2
        puntos_auto.append(int(union))
    puntos_auto.append(int(gramajes_ideales[-1] - 15))

    st.divider()
    st.subheader("⚙️ Ajuste Fino de la Línea Completa")
    
    # --- INTERFAZ DE AJUSTE ---
    puntos_finales = []
    # Mostramos los cortes en columnas para scrollear horizontalmente si son muchos
    cols_ajuste = st.columns(len(puntos_auto))
    for i, p_val in enumerate(puntos_auto):
        with cols_ajuste[i]:
            if i == 0: label = "Máx"
            elif i == len(puntos_auto)-1: label = "Mín"
            else: label = f"Corte {todos_calibres[i-1]}/{todos_calibres[i]}"
            
            # El key cambia si cambian los calibres seleccionados para forzar el recálculo
            v = st.number_input(label, value=p_val, step=1, key=f"corte_{i}_{len(todos_calibres)}")
            puntos_finales.append(v)

    st.divider()

    # --- RESULTADOS FINALES ---
    st.subheader("📦 Pesos Reales Resultantes")
    res_cols = st.columns(len(todos_calibres))

    for i, cal in enumerate(todos_calibres):
        g_alto = puntos_finales[i]
        g_bajo = puntos_finales[i+1]
        promedio = (g_alto + g_bajo) / 2
        peso_calc = (promedio * cal) / 1000
        obj_cal = mapa_pesos[cal]
        
        with res_cols[i]:
            diff = peso_calc - obj_cal
            color = "normal" if abs(diff) < 0.1 else "inverse"
            
            st.metric(
                label=f"Calibre {cal}", 
                value=f"{peso_calc:.2f} kg", 
                delta=f"{diff:.2f} vs {obj_cal}kg",
                delta_color=color
            )
            st.markdown(f"**{int(g_alto)}g - {int(g_bajo)}g**")
            st.progress(min(max((peso_calc - 15) / 10, 0.0), 1.0))

else:
    st.info("Configura al menos un peso y un calibre para generar la cascada.")

st.divider()
if st.button("🗑️ Reiniciar Todo"):
    st.session_state.num_grupos = 1
    st.rerun()
