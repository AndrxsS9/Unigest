# frontend/views/login.py
# Pantalla de login

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.api_client import login


def mostrar_login():
    """Muestra la pantalla de inicio de sesión."""
    st.markdown("## 🔐 Iniciar Sesión")
    st.markdown("---")

    with st.form("login_form"):
        email = st.text_input("📧 Correo institucional", placeholder="usuario@uni.edu")
        password = st.text_input("🔑 Contraseña", type="password")
        submit = st.form_submit_button("Ingresar", use_container_width=True)

    if submit:
        if not email or not password:
            st.error("Por favor completa todos los campos.")
            return

        data, status_code = login(email, password)

        if status_code == 200:
            st.session_state.token = data["access_token"]
            st.session_state.rol = data["rol"]
            st.session_state.nombre = data["nombre"]
            st.session_state.user_id = data["id"]
            st.rerun()
        else:
            st.error(data.get("detail", "Error al iniciar sesión"))
