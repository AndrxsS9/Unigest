# frontend/views/login.py
# Pantalla de login

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.api_client import login
from utils.icons import icon_html


def mostrar_login():
    """Muestra la pantalla de inicio de sesión."""
    # Añadimos un poco de espacio superior
    st.write("")
    st.write("")
    st.write("")
    
    # Creamos columnas para centrar el formulario
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center; color: #0d6efd;'>{icon_html('lock')} UniGest</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6c757d;'>Sistema de Gestión Universitaria</p>", unsafe_allow_html=True)
            st.markdown("---")

            with st.form("login_form"):
                st.markdown(f"{icon_html('mail')} **Correo institucional**", unsafe_allow_html=True)
                email = st.text_input("", placeholder="usuario@uni.edu", label_visibility="collapsed")
                
                st.markdown(f"{icon_html('shield')} **Contraseña**", unsafe_allow_html=True)
                password = st.text_input("", type="password", label_visibility="collapsed")
                
                st.write("") # Espacio adicional
                submit = st.form_submit_button("Ingresar", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Por favor completa todos los campos.")
                    return

                with st.spinner("Autenticando..."):
                    data, status_code = login(email, password)

                if status_code == 200:
                    st.session_state.token = data["access_token"]
                    st.session_state.rol = data["rol"]
                    st.session_state.nombre = data["nombre"]
                    st.session_state.user_id = data["id"]
                    st.rerun()
                else:
                    st.error(data.get("detail", "Error al iniciar sesión"))
