import streamlit as st

st.set_page_config(page_title="Calculadora Automática de Calibres", layout="wide")

st.title("🍎 Calculadora de Procesos Automática")
st.markdown("Los rangos se calculan **automáticamente** al ingresar calibres para dar el peso objetivo.")

# --- ENTRADAS DE CONFIGURACIÓN ---
col1, col2 = st.columns([1, 2])
with col1:
    peso_obj = st.number_input("Peso Objetivo (kg)", 15.0, 25.0, 19.2, 0.1, key="peso_obj")

with col2:
    calibres_sel = st.multiselect(
        "Selecciona Calibres", 
        [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], 
        default=[72, 80, 88, 100],
        key="calibres_sel"
    )
    calibres_sel.sort()

# --- LÓGICA DE CÁLCULO AUTOMÁTICO ---
if calibres_sel:
    # Calculamos los puntos de corte ideales basados en el peso objetivo
    # Gramaje medio ideal = (Peso_Obj * 1000) / Calibre
    gramajes_ideales = [(peso_obj * 1000) / c for c in calibres_sel]
    
    cortes_calculados = []
    # 1. El primer mínimo (Margen de seguridad del 5%)
    cortes_calculados.append(int(gramajes_ideales[0] + (gramajes_ideales[0] * 0.05)))
    
    # 2. Uniones (Promedio entre lo que necesita un calibre y el siguiente)
    for i in range(len(gramajes_ideales) - 1):
        union = (gramajes_ideales[i] + gramajes_ideales[i+1]) / 2
        cortes_calculados.append(int(union))
    
    # 3. El último máximo (Margen de seguridad del 5%)
    cortes_calculados.append(int(gramajes_ideales[-1] - (gramajes_ideales[-1] * 0.05)))

    # --- INTERFAZ DE AJUSTE MANUAL ---
    st.divider()
    st.subheader("⚙️ Ajuste Fino de Cortes (Gramos)")
    
    puntos_finales = []
    cols_ajuste = st.columns(len(cortes_calculados))
    
    for i, valor_auto in enumerate(cortes_calculados):
        with cols_ajuste[i]:
            if i == 0: label = f"Máx Inicial ({calibres_sel[0]})"
            elif i == len(cortes_calculados)-1: label = f"Mín Final ({calibres_sel[-1]})"
            else: label = f"Corte {calibres_sel[i-1]}/{calibres_sel[i]}"
            
            # El valor por defecto es el calculado automáticamente
            v = st.number_input(label, value=valor_auto, step=1, key=f"c_input_{i}_{peso_obj}")
            puntos_finales.append(v)

    st.divider()

    # --- RESULTADOS FINALES ---
    st.subheader("📦 Pesos por Caja Resultantes")
    res_cols = st.columns(len(calibres_sel))

    for i, cal in enumerate(calibres_sel):
        # El rango de un calibre i está entre el punto i y el punto i+1
        g_alto = puntos_finales[i]
        g_bajo = puntos_finales[i+1]
        
        promedio_caja = (g_alto + g_bajo) / 2
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
            st.markdown(f"**Rango:** {int(g_alto)}g - {int(g_bajo)}g")
            
            # Barra de estado
            st.progress(min(max((peso_final - 15) / 10, 0.0), 1.0))

else:
    st.info("Agrega calibres para ver el cálculo automático.")

st.divider()
st.caption("Nota: Los calibres están ordenados de fruta grande (72) a fruta pequeña (216).")
