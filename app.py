import streamlit as st

st.set_page_config(page_title="Calculadora de Procesos - Manzanas", layout="wide")

st.title("🍎 Control de Calibres y Pesos en Cascada")
st.markdown("Ajusta los puntos de corte para regular el peso final de la caja.")

# --- SECCIÓN DE ENTRADA ---
col_cfg1, col_cfg2 = st.columns(2)

with col_cfg1:
    peso_obj = st.number_input("Peso Objetivo de la Caja (kg)", 15.0, 25.0, 19.5, 0.1)
    calibres = sorted(st.multiselect(
        "Selecciona los Calibres en la línea", 
        [216, 198, 175, 163, 150, 138, 125, 113, 100, 88, 80, 72], 
        default=[113, 100, 88]
    ), reverse=True)

# --- LÓGICA DE CÁLCULO ---
if calibres:
    # 1. Calcular gramajes ideales para el peso objetivo
    # Gramaje ideal = (Peso kg * 1000) / Calibre
    gramajes_ideales = {c: (peso_obj * 1000) / c for c in calibres}
    
    # 2. Crear puntos de corte automáticos (promedio entre gramajes ideales vecinos)
    # El primer mínimo y el último máximo tienen un margen de 15g por defecto
    cortes_iniciales = [int(gramajes_ideales[calibres[0]] - 15)] # Mínimo del primer calibre
    
    for i in range(len(calibres) - 1):
        punto_union = int((gramajes_ideales[calibres[i]] + gramajes_ideales[calibres[i+1]]) / 2)
        cortes_iniciales.append(punto_union)
        
    cortes_iniciales.append(int(gramajes_ideales[calibres[-1]] + 15)) # Máximo del último calibre

    st.divider()
    st.subheader("⚙️ Ajuste Fino de Rangos (Gramos)")
    
    # --- INTERFAZ DE AJUSTE ---
    puntos_ajustados = []
    cols_ajuste = st.columns(len(cortes_iniciales))
    
    for i, valor_base in enumerate(cortes_iniciales):
        with cols_ajuste[i]:
            if i == 0:
                label = f"Mínimo Cal {calibres[0]}"
            elif i == len(cortes_iniciales) - 1:
                label = f"Máximo Cal {calibres[-1]}"
            else:
                label = f"Unión {calibres[i-1]}/{calibres[i]}"
            
            valor = st.number_input(label, value=valor_base, step=1, key=f"corte_{i}")
            puntos_ajustados.append(valor)

    st.divider()
    
    # --- RESULTADOS FINALES ---
    st.subheader("📦 Resultado de Pesos por Caja")
    res_cols = st.columns(len(calibres))
    
    for i, calibre in enumerate(calibres):
        r_min = puntos_ajustados[i]
        r_max = puntos_ajustados[i+1]
        promedio = (r_min + r_max) / 2
        peso_final = (promedio * calibre) / 1000
        
        with res_cols[i]:
            # Diferencia con el objetivo para ayudar al usuario
            diff = peso_
