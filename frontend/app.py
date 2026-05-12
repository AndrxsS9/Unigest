# frontend/app.py
# Entrada Streamlit, manejo de sesión

import streamlit as st
import sys
import os

# Agregar la carpeta frontend al path
sys.path.insert(0, os.path.dirname(__file__))

from views.login import mostrar_login
from views.estudiante import mostrar_dashboard_estudiante
from views.profesor import mostrar_dashboard_profesor
from utils.icons import PAGE_ICON_URI

# ── Configuración de la página ────────────────────────
st.set_page_config(
    page_title="UniGest — Gestión Universitaria",
    page_icon=PAGE_ICON_URI,
    layout="wide"
)

# ── Estilos CSS Globales ──────────────────────────────
st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Contenedores tipo tarjeta */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 1.5rem;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    /* Botones primarios */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Titulos */
    h1, h2, h3 {
        color: #2b3035;
        font-weight: 700;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #0d6efd;
    }
</style>
""", unsafe_allow_html=True)

# ── Inicializar estado de sesión ──────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "rol" not in st.session_state:
    st.session_state.rol = None
if "nombre" not in st.session_state:
    st.session_state.nombre = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ── Enrutamiento por sesión ───────────────────────────
if st.session_state.token is None:
    # Usuario no autenticado → mostrar login
    mostrar_login()
elif st.session_state.rol == "estudiante":
    mostrar_dashboard_estudiante()
elif st.session_state.rol == "profesor":
    mostrar_dashboard_profesor()
else:
    st.error("Rol no reconocido. Por favor, inicia sesión de nuevo.")
    if st.button("Volver al login"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
