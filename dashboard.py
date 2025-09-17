import streamlit as st
from PIL import Image
import os

# Importar lógica de predicción y protocolos desde nuestros módulos
from precog.model import predecir_riesgo
from protocols.reglas import decidir_protocolo, PROTOCOLS

# ================================
# CONFIGURACIÓN DE PÁGINA
# ================================
st.set_page_config(
    page_title="ChronoLogistics - Dashboard de Crisis",
    layout="wide",
    page_icon="⚡",
)

# ================================
# FUNCIONES AUXILIARES
# ================================

def cargar_mapa():
    """Carga la imagen de Madrid desde /data."""
    try:
        ruta = os.path.join("data", "madrid.jpg")
        if not os.path.exists(ruta):
            ruta = os.path.join("data", "madrid.png")
        if not os.path.exists(ruta):
            st.error("⚠️ No se encontró el mapa de Madrid en /data/")
            return None
        return Image.open(ruta)
    except Exception as e:
        st.error(f"Error al cargar el mapa: {e}")
        return None

def mostrar_ficha_protocolo(proto):
    """Muestra la ficha técnica de un protocolo específico."""
    ficha = PROTOCOLS.get(proto, {})
    st.subheader(f"📑 Ficha Técnica - {proto}")
    st.write(f"**Disparador:** {ficha.get('trigger', 'N/A')}")
    st.write("**Acciones:**")
    for act in ficha.get("actions", []):
        st.markdown(f"- {act}")

# ================================
# INTERFAZ PRINCIPAL
# ================================
st.title("⚡ ChronoLogistics - Dashboard Operativo en Vivo")
st.markdown("**Centro de mando y control en tiempo real.**")

tabs = st.tabs(["🛰 Precog: Monitor de Riesgo", "🌍 Chronos: Visión 2040", "🛡 K-Lang: Manual de Batalla"])

# ================================
# PESTAÑA 1: PRECOG
# ================================
with tabs[0]:
    st.header("🛰 Precog: Monitor de Riesgo Táctico")

    # Mostrar mapa
    st.subheader("Mapa de Calor de Riesgo")
    mapa = cargar_mapa()
    if mapa:
        st.image(mapa, caption="Triángulo del Peligro - Región de Madrid", use_container_width=True)

    st.subheader("Simulador de Riesgo Interactivo")
    col1, col2, col3 = st.columns(3)
    with col1:
        velocidad_media = st.slider("Velocidad Media (km/h)", 0, 150, 80)
    with col2:
        intensidad_lluvia = st.slider("Intensidad de Lluvia (mm/h)", 0, 200, 100)
    with col3:
        humedad = st.slider("Humedad (%)", 0, 100, 70)

    # Calcular riesgo usando nuestro modelo
    nivel_riesgo = predecir_riesgo(velocidad_media, intensidad_lluvia, humedad, [0.8, 0.6, 0.9])
    color = "🔴" if nivel_riesgo > 70 else "🟡" if nivel_riesgo > 40 else "🟢"
    st.metric("Nivel de Riesgo en Cascada", f"{nivel_riesgo:.1f}% {color}")

# ================================
# PESTAÑA 2: CHRONOS
# ================================
with tabs[1]:
    st.header("🌍 Chronos: Visión Estratégica 2040")

    vision = st.radio("Selecciona Estrategia:", ["Fortaleza Verde", "Búnker Tecnológico"], horizontal=True)

    if vision == "Fortaleza Verde":
        st.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Madrid_green.jpg", caption="Visión Fortaleza Verde")
        st.markdown("**Defensa:** Una ciudad resiliente y sostenible, infraestructura verde y logística baja en carbono.")
    else:
        st.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Data_center.jpg", caption="Visión Búnker Tecnológico")
        st.markdown("**Defensa:** Protección total de activos digitales, automatización avanzada y ciudad blindada.")

# ================================
# PESTAÑA 3: K-LANG
# ================================
with tabs[2]:
    st.header("🛡 K-Lang: Manual de Batalla Interactivo")

    # Selector de protocolo
    protocolo = st.radio("Selecciona protocolo para consultar ficha:", list(PROTOCOLS.keys()), horizontal=True)
    mostrar_ficha_protocolo(protocolo)

    st.subheader("Simulador de Protocolos")
    sim_viento = st.slider("Velocidad del Viento (km/h)", 0, 150, 30)
    sim_inund = st.slider("Nivel de Inundación (cm)", 0, 100, 5)
    sim_temp = st.slider("Temperatura (°C)", -10, 50, 20)

    resultado = decidir_protocolo(sim_viento, sim_inund, sim_temp)

    st.markdown(f"### 🔥 Protocolo Activo: **{resultado['protocol']}** ({resultado['tag']})")
    st.write(f"**Motivo:** {resultado['reason']}")
    st.write("**Acciones Recomendadas:**")
    for act in resultado["actions"]:
        st.markdown(f"- {act}")

