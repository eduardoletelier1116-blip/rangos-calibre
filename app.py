import streamlit as st

st.set_page_config(page_title="Calculadora Cascada Pro", layout="wide")

st.title("🍎 Calculadora de Calibres en Cascada")
st.markdown("Ajusta los puntos de corte. El máximo de un calibre es el mínimo del siguiente.")

# -------------------------------------------------
# CONFIGURACIÓN DE GRUPOS
# -------------------------------------------------
col_p1, col_p2 = st.columns(2)
with col_p1:
    peso_obj_A = st.number_input("Peso Objetivo Grupo A (kg)", 15.0, 25.0, 19.2, 0.1)
    # Calibres ordenados de menor a mayor gramaje (más frutos a menos frutos)
    grupoA = sorted(st.multiselect("Calibres Grupo A", [216,198,175,163,150,138,125,113,100,88,80,72], default=[125, 113, 100]), reverse=True)

with col_p2:
    peso_obj_B = st.number_input("Peso Objetivo Grupo B (kg)", 15.0, 25.0, 19.0, 0.1)
    grupoB = sorted(st.multiselect("Calibres Grupo B", [216,198,175,163,150,138,125,113,100,88,80,72], default=[88, 80]), reverse=True)

def procesar_grupo(calibres, peso_objetivo, nombre):
    if not calibres: return
    
    st.subheader(f"Grupo {nombre}")
    
    # Creamos los puntos de corte (límites)
    # Necesitamos N calibres + 1 límites
    cortes = []
    
    # Generar valores iniciales sugeridos
    valores_base = []
    for c in calibres:
        valores_base.append((peso_objetivo * 1000) / c)
    
    # El primer mínimo y los puntos intermedios
    current_min = int(valores_base[0] - 15)
    cortes.append(current_min)
    
    for i in range(len(valores_base)-1):
        # Punto medio entre calibres como sugerencia inicial
        punto_medio = int((valores_base[i] + valores_base[i+1]) / 2)
        cortes.append(punto_medio)
        
    # El último máximo
    cortes.append(int(valores_base[-1] + 15))

    # Interfaz de ajuste
    puntos_ajustados = []
    for i, valor in enumerate(cortes):
        lbl = "Mínimo Inicial" if i == 0 else (f"Corte Cal {calibres[i-1]} / {calibres[i]}" if i < len(calibres) else "Máximo Final")
        nuevo_punto = st.number_input(f"{nombre} - {lbl} (g)", value=valor, key=f"corte_{nombre}_{i}")
        puntos_ajustados.append(nuevo_punto)

    st.write("---")
    
    # Mostrar resultados en tabla
    cols = st.columns(len(calibres))
    for i, calibre in enumerate(calibres):
        r_min = puntos_ajustados[i]
        r_max = puntos_ajustados[i+1]
        promedio = (r_min + r_max) / 2
        peso_real = (promedio * calibre) / 1000
        
        with cols[i]:
            st.metric(f"Cal {calibre}", f"{peso_real:.2f} kg")
            st.caption(f"Rango: {r_min}g - {r_max}g")
            
            # Alerta visual
            dif = peso_real - peso_objetivo
            if abs(dif) > 0.2:
                st.warning(f"Desvío: {dif:.2f}")

st.divider()
colA, colB = st.columns(2)
with colA: procesar_grupo(grupoA, peso_obj_A, "A")
with colB: procesar_grupo(grupoB, peso_obj_B, "B")
