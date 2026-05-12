# frontend/views/estudiante.py
# Dashboard del estudiante

import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.api_client import get_mis_materias, get_materias, matricular, get_kardex
from utils.icons import icon_html


def mostrar_dashboard_estudiante():
    """Muestra el dashboard completo del estudiante."""

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {icon_html('graduation_cap')} {st.session_state.nombre}", unsafe_allow_html=True)
        st.markdown("**Rol:** Estudiante")
        if st.button("Cerrar sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.title("Panel del Estudiante")

    # Pestañas
    tab1, tab2, tab3 = st.tabs(["Mis Materias", "Matricularme", "Mi Kardex"])

    # ── Tab 1: Mis Materias ───────────────────────────
    with tab1:
        st.subheader("Mis materias matriculadas")
        with st.spinner("Cargando materias..."):
            mis_materias = get_mis_materias()

        if mis_materias:
            df = pd.DataFrame(mis_materias)
            df_display = df[["nombre", "codigo", "creditos", "horario", "salon", "nota_definitiva", "estado"]]
            df_display.columns = ["Materia", "Código", "Créditos", "Horario", "Salón", "Nota", "Estado"]
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("No estás matriculado en ninguna materia aún.")

    # ── Tab 2: Matricularme ───────────────────────────
    with tab2:
        st.subheader("Materias disponibles")
        with st.spinner("Cargando materias disponibles..."):
            materias = get_materias()

        if materias:
            for materia in materias:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**{materia['nombre']}** ({materia['codigo']})")
                        st.markdown(
                            f"<div style='color:#6c757d;font-size:0.95rem;'>{icon_html('calendar')} {materia['horario']} | {icon_html('school')} {materia['salon']} | {icon_html('professor')} {materia['profesor']}</div>",
                            unsafe_allow_html=True,
                        )
                    with col2:
                        st.metric("Cupos", materia['cupos_disponibles'])
                        if materia['cupos_disponibles'] <= 5:
                            st.markdown("<span style='color:red; font-size:0.8rem; font-weight:bold;'>¡Pocos cupos!</span>", unsafe_allow_html=True)
                    with col3:
                        st.metric("Créditos", materia['creditos'])
                        if st.button("Matricularme", key=f"mat_{materia['id']}"):
                            with st.spinner("Procesando matrícula..."):
                                resp, code = matricular(materia['id'])
                            if code == 200:
                                st.toast(resp.get("mensaje", "¡Matriculado exitosamente!"), icon="✅")
                                st.rerun()
                            else:
                                st.toast(resp.get("detail", "Error al matricularse"), icon="❌")
        else:
            st.info("No hay materias disponibles.")

    # ── Tab 3: Kardex ─────────────────────────────────
    with tab3:
        st.subheader("Mi Kardex Académico")
        with st.spinner("Cargando kardex..."):
            kardex = get_kardex()

        if kardex:
            # Barra de progreso (estimado 160 créditos para una carrera típica)
            creditos_aprobados = kardex.get("creditos_aprobados", 0)
            total_estimado = 160
            porcentaje = min(creditos_aprobados / total_estimado, 1.0)
            
            st.markdown(f"**Avance de la carrera ({creditos_aprobados}/{total_estimado} créditos estimados)**")
            st.progress(porcentaje)
            st.write("")
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Promedio", kardex.get("promedio_acumulado", "N/A"))
            with col2:
                st.metric("Créditos Aprobados", creditos_aprobados)
            with col3:
                st.metric("Créditos Matriculados", kardex.get("creditos_matriculados", 0))

            st.markdown("---")

            # Tabla de materias
            if kardex.get("materias"):
                df = pd.DataFrame(kardex["materias"])
                df.columns = ["Materia", "Código", "Créditos", "Nota", "Estado"]
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay información en tu kardex.")
