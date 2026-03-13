import streamlit as st

st.set_page_config(page_title="Calculadora Cascada Inteligente", layout="wide")

st.title("🍎 Calculadora de Calibres Dinámica")
st.markdown("Los rangos se calculan automáticamente para cumplir el **Peso Objetivo**.")

# --- ENTRADAS PRINCIPALES ---
col1, col2 = st.columns(2)
with col1:
    peso_obj = st.number_input("Peso Objetivo de la Caja (kg)", 15.0, 25.0, 19.5, 0.1)

with col2:
    # Calibres ordenados de mayor a menor tamaño (menor a mayor número)
    calibres_seleccionados = st.multiselect(
        "Selecciona Calibres", 
        [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], 
        default=[88, 100, 113]
    )
    # Ordenamos para que la cascada tenga sentido físico (fruta grande a pequeña)
    calibres_seleccionados.sort()

if calibres_seleccionados:
    # --- LÓGICA DE INICIALIZACIÓN AUTOMÁTICA ---
    # Calculamos los gramajes promedio ideales para cada calibre
    gramajes_fijados = [ (peso_obj * 1000) / c for c in calibres_seleccionados ]
    
    # Creamos los puntos de unión (la cascada)
    # El primer mínimo es el promedio del primer calibre menos un margen (ej. 8%)
    puntos = [int(gramajes_fijados[0] * 0.92)] 
    
    # Los puntos intermedios son el promedio entre los promedios ideales de calibres vecinos
    for i in range(len(gramajes_fijados) - 1):
        union = int((gramajes_fijados[i] + gramajes_fijados[i+1]) / 2)
        puntos.append(union)
    
    # El último máximo es el promedio del último calibre más un margen
    puntos.append(int(gramajes_fijados[-1] * 1.08))

    st.divider()
    st.subheader("⚙️ Ajuste Fino de la Cascada")
    st.info("Al mover un punto de unión, ajustas dos calibres al mismo tiempo para mantener la continuidad.")

    # --- INTERFAZ DE PUNTOS DE CORTE ---
    puntos_finales = []
    cols_ajuste = st.columns(len(puntos))
    
    for i, p_inicial in enumerate(puntos):
        with cols_ajuste[i]:
            if i == 0:
                label = "Mín. Inicial"
            elif i == len(puntos) - 1:
                label = "Máx. Final"
            else:
                label = f"Corte {calibres_seleccionados[i-1]}/{calibres_seleccionados[i]}"
            
            # El usuario puede mover el punto manualmente
            val = st.number_input(label, value=int(p_inicial), step=1, key=f"p_{i}")
            puntos_finales.append(val)

    st.divider()

    # --- VISUALIZACIÓN DE RESULTADOS ---
    st.subheader("📦 Pesos Finales Calculados")
    res_cols = st.columns(len(calibres_seleccionados))

    for i, cal in enumerate(calibres_seleccionados):
        r_min = puntos_finales[i]
        r_max = puntos_finales[i+1]
        promedio_real = (r_min + r_max) / 2
        peso_caja = (promedio_real * cal) / 1000
        
        with res_cols[i]:
            diff = peso_caja - peso_obj
            # Alerta visual si se aleja del objetivo
            status = "normal" if abs(diff) < 0.15 else "inverse"
            
            st.metric(
                label=f"Calibre {cal}", 
                value=f"{peso_caja:.2f} kg", 
                delta=f"{diff:.2f} kg vs Obj",
                delta_color=status
            )
            st.caption(f"Rango: {r_min}g - {r_max}g")
            st.progress(min(max((peso_caja - 15) / 10, 0.0), 1.0)) # Barra visual de llenado

else:
    st.warning("Selecciona al menos un calibre para calcular los rangos.")

st.divider()
st.write("💡 **Tip:** Si el peso de un calibre queda muy bajo, aumenta el valor del 'Corte' a su derecha.")
