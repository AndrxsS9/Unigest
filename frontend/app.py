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

# ── Configuración de la página ────────────────────────
st.set_page_config(
    page_title="UniGest — Gestión Universitaria",
    page_icon="🎓",
    layout="wide"
)

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
