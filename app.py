import streamlit as st

st.set_page_config(page_title="Calculadora de Procesos Pro", layout="wide")

st.title("🍎 Control de Calibres y Pesos en Cascada")

# --- ENTRADAS ---
col1, col2 = st.columns([1, 2])
with col1:
    peso_obj = st.number_input("Peso Objetivo de la Caja (kg)", 15.0, 25.0, 19.2, 0.1)

with col2:
    calibres_sel = st.multiselect(
        "Selecciona Calibres", 
        [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], 
        default=[72, 80, 88, 100, 113, 125]
    )
    calibres_sel.sort() # Orden de mayor a menor tamaño (número menor a mayor)

if calibres_sel:
    # --- LÓGICA DE CÁLCULO DE RANGOS TEÓRICOS ---
    # Para que cada caja pese 'peso_obj', el fruto medio debe ser: (peso_obj * 1000 / calibre)
    # Calculamos los "puntos de corte" entre calibres. 
    # El punto de corte entre Calibre A y B es el promedio de sus frutos medios ideales.
    
    gramajes_ideales = [(peso_obj * 1000) / c for c in calibres_sel]
    
    cortes = []
    # 1. Mínimo del primer calibre (Margen de -15g)
    cortes.append(int(gramajes_ideales[0] - 15))
    
    # 2. Puntos intermedios
    for i in range(len(gramajes_ideales) - 1):
        # La unión es el punto medio entre lo que necesita un calibre y lo que necesita el siguiente
        punto_union = (gramajes_ideales[i] + gramajes_ideales[i+1]) / 2
        cortes.append(int(punto_union))
    
    # 3. Máximo del último calibre (Margen de +15g)
    cortes.append(int(gramajes_ideales[-1] + 15))

    st.divider()
    st.subheader("⚙️ Ajuste Fino de Cortes (Gramos)")
    
    # --- INTERFAZ DE AJUSTE ---
    puntos_editados = []
    # Usamos columnas para que no ocupen tanto espacio vertical
    cols_ajuste = st.columns(len(cortes))
    for i, valor_sugerido in enumerate(cortes):
        with cols_ajuste[i]:
            if i == 0: label = "Mín 1er Cal"
            elif i == len(cortes)-1: label = "Máx Últ Cal"
            else: label = f"Corte {calibres_sel[i-1]}/{calibres_sel[i]}"
            
            # Ajuste manual
            v = st.number_input(label, value=valor_sugerido, step=1, key=f"c_{i}")
            puntos_editados.append(v)

    st.divider()

    # --- RESULTADOS ---
    st.subheader("📦 Pesos Finales Calculados")
    res_cols = st.columns(len(calibres_sel))

    for i, cal in enumerate(calibres_sel):
        # Ahora el rango siempre va de menor a mayor
        # r_min es el corte i, r_max es el corte i+1
        # Pero como los calibres (72, 80...) van de mayor a menor peso,
        # invertimos la lógica para que el gramaje se vea correctamente:
        
        g_superior = puntos_editados[i]   # El calibre anterior es más pesado
        g_inferior = puntos_editados[i+1] # El calibre siguiente es más liviano
        
        # El promedio de la caja es:
        promedio_caja = (g_superior + g_inferior) / 2
        peso_final = (promedio_caja * cal) / 1000
        
        with res_cols[i]:
            diff = peso_final - peso_obj
            color = "normal" if abs(diff) < 0.1 else "inverse"
            
            st.metric(
                label=f"Calibre {cal}", 
                value=f"{peso_final:.2f} kg", 
                delta=f"{diff:.2f} kg vs Obj",
                delta_color=color
            )
            # Mostramos el rango de mayor a menor peso como se usa en packing
            st.write(f"**{g_superior}g - {g_inferior}g**")
            st.progress(min(max((peso_final - 15) / 10, 0.0), 1.0))

else:
    st.info("Selecciona los calibres para iniciar el cálculo.")
