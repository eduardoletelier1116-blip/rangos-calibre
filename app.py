import streamlit as st

st.set_page_config(page_title="Calculadora Pro - Cascada Unificada", layout="wide")

st.title("🍎 Calculadora de Procesos Unificada")
st.markdown("Ajusta los calibres en una sola línea, con la posibilidad de asignar pesos objetivo distintos.")

# --- CONFIGURACIÓN GLOBAL ---
col_glob1, col_glob2 = st.columns([1, 2])

with col_glob1:
    peso_gen = st.number_input("Peso Objetivo General (kg)", 15.0, 25.0, 19.2, 0.1)

with col_glob2:
    calibres_sel = st.multiselect(
        "Selecciona Calibres", 
        [72, 80, 88, 100, 113, 125, 138, 150, 163, 175, 198, 216], 
        default=[88, 100, 113, 125, 150]
    )
    calibres_sel.sort()

# --- SECCIÓN DE EXCEPCIONES ---
with st.expander("⚖️ Asignar Peso Específico a Calibres (Opcional)"):
    st.write("Si un calibre debe pesar distinto al general (ej. el 150), cámbialo aquí:")
    pesos_especificos = {}
    cols_exc = st.columns(len(calibres_sel))
    for i, cal in enumerate(calibres_sel):
        with cols_exc[i]:
            # Por defecto es el peso general, pero el usuario puede cambiarlo
            p_esp = st.number_input(f"Peso Cal {cal}", 15.0, 25.0, peso_gen, 0.1, key=f"exc_{cal}")
            pesos_especificos[cal] = p_esp

# --- LÓGICA DE CÁLCULO AUTOMÁTICO ---
if calibres_sel:
    # 1. Gramajes ideales basados en su peso específico asignado
    gramajes_ideales = [ (pesos_especificos[c] * 1000) / c for c in calibres_sel ]
    
    # 2. Puntos de corte automáticos (Cascada)
    puntos = [int(gramajes_ideales[0] + (gramajes_ideales[0] * 0.05))] # Máx Inicial
    for i in range(len(gramajes_ideales) - 1):
        union = (gramajes_ideales[i] + gramajes_ideales[i+1]) / 2
        puntos.append(int(union))
    puntos.append(int(gramajes_ideales[-1] - (gramajes_ideales[-1] * 0.05))) # Mín Final

    st.divider()
    st.subheader("⚙️ Ajuste Fino de Cortes")
    
    # --- INTERFAZ DE AJUSTE (Puntos de Unión) ---
    puntos_finales = []
    cols_ajuste = st.columns(len(puntos))
    for i, p_auto in enumerate(puntos):
        with cols_ajuste[i]:
            if i == 0: label = "Máx Inicial"
            elif i == len(puntos)-1: label = "Mín Final"
            else: label = f"Corte {calibres_sel[i-1]}/{calibres_sel[i]}"
            
            # El valor se resetea si cambia el peso objetivo específico de ese calibre
            # Usamos una clave que combine los pesos de los calibres involucrados
            p_relacionado = pesos_especificos[calibres_sel[i if i < len(calibres_sel) else i-1]]
            v = st.number_input(label, value=p_auto, step=1, key=f"p_{i}_{p_relacionado}")
            puntos_finales.append(v)

    st.divider()

    # --- RESULTADOS FINALES (Toda la línea junta) ---
    st.subheader("📦 Pesos Finales Calculados")
    res_cols = st.columns(len(calibres_sel))

    for i, cal in enumerate(calibres_sel):
        g_alto = puntos_finales[i]
        g_bajo = puntos_finales[i+1]
        promedio = (g_alto + g_bajo) / 2
        peso_final = (promedio * cal) / 1000
        obj_cal = pesos_especificos[cal]
        
        with res_cols[i]:
            diff = peso_final - obj_cal
            color = "normal" if abs(diff) < 0.1 else "inverse"
            
            st.metric(
                label=f"Calibre {cal}", 
                value=f"{peso_final:.2f} kg", 
                delta=f"{diff:.2f} vs {obj_cal}kg",
                delta_color=color
            )
            st.markdown(f"**{int(g_alto)}g - {int(g_bajo)}g**")
            st.progress(min(max((peso_final - 15) / 10, 0.0), 1.0))

else:
    st.info("Selecciona calibres para iniciar.")

st.divider()
st.caption("Esta vista mantiene la cascada técnica: el mínimo de un calibre es el máximo del siguiente.")
