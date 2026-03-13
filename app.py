import streamlit as st

st.set_page_config(page_title="Calculadora Cascada Unificada", layout="wide")

st.title("🍎 Calculadora de Procesos Unificada")
st.markdown("Configura los calibres por peso objetivo y ajusta la cascada en una sola línea.")

# --- ENTRADAS DE CONFIGURACIÓN ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Configuración 1")
    peso_1 = st.number_input("Peso Objetivo 1 (kg)", 15.0, 25.0, 19.2, 0.1)
    calibres_1 = st.multiselect("Calibres para Peso 1", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], default=[100, 113, 125])

with col_b:
    st.subheader("Configuración 2")
    peso_2 = st.number_input("Peso Objetivo 2 (kg)", 15.0, 25.0, 20.2, 0.1)
    calibres_2 = st.multiselect("Calibres para Peso 2", [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], default=[138, 150])

# --- PROCESAMIENTO UNIFICADO ---
# Creamos un diccionario para saber qué peso le toca a cada calibre
mapa_pesos = {}
for c in calibres_1: mapa_pesos[c] = peso_1
for c in calibres_2: mapa_pesos[c] = peso_2 # Si un calibre está en ambos, manda el peso 2

# Lista total de calibres seleccionados (únicos y ordenados de mayor a menor tamaño)
todos_calibres = sorted(list(mapa_pesos.keys()))

if todos_calibres:
    # 1. Calcular gramajes medios ideales según el peso asignado a cada uno
    gramajes_ideales = [ (mapa_pesos[c] * 1000) / c for c in todos_calibres ]
    
    # 2. Generar puntos de corte (Cascada)
    puntos_auto = [int(gramajes_ideales[0] + 15)] # Margen superior
    for i in range(len(gramajes_ideales) - 1):
        union = (gramajes_ideales[i] + gramajes_ideales[i+1]) / 2
        puntos_auto.append(int(union))
    puntos_auto.append(int(gramajes_ideales[-1] - 15)) # Margen inferior

    st.divider()
    st.subheader("⚙️ Ajuste Fino de la Línea")
    
    # --- INTERFAZ DE AJUSTE (Una sola fila de inputs) ---
    puntos_finales = []
    cols_ajuste = st.columns(len(puntos_auto))
    for i, p_val in enumerate(puntos_auto):
        with cols_ajuste[i]:
            if i == 0: label = "Máx"
            elif i == len(puntos_auto)-1: label = "Mín"
            else: label = f"Corte {todos_calibres[i-1]}/{todos_calibres[i]}"
            
            # El key incluye el peso para resetear si cambias el objetivo
            v = st.number_input(label, value=p_val, step=1, key=f"corte_{i}_{mapa_pesos[todos_calibres[min(i, len(todos_calibres)-1)]]}")
            puntos_finales.append(v)

    st.divider()

    # --- RESULTADOS FINALES (Una sola fila de tarjetas) ---
    st.subheader("📦 Pesos Reales por Caja")
    res_cols = st.columns(len(todos_calibres))

    for i, cal in enumerate(todos_calibres):
        g_alto = puntos_finales[i]
        g_bajo = puntos_finales[i+1]
        promedio = (g_alto + g_bajo) / 2
        peso_calc = (promedio * cal) / 1000
        obj_especifico = mapa_pesos[cal]
        
        with res_cols[i]:
            diff = peso_calc - obj_especifico
            color = "normal" if abs(diff) < 0.1 else "inverse"
            
            st.metric(
                label=f"Calibre {cal}", 
                value=f"{peso_calc:.2f} kg", 
                delta=f"{diff:.2f} vs {obj_especifico}kg",
                delta_color=color
            )
            st.markdown(f"**{int(g_alto)}g - {int(g_bajo)}g**")
            st.progress(min(max((peso_calc - 15) / 10, 0.0), 1.0))

else:
    st.info("Selecciona calibres en cualquiera de las dos configuraciones para empezar.")

st.divider()
st.caption("Fórmula: ( (Punto Alto + Punto Bajo) / 2 ) * Calibre / 1000. La cascada se mantiene unificada en toda la línea.")
