# frontend/views/profesor.py
# Dashboard del profesor

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.api_client import get_materias, get_mis_estudiantes, registrar_nota
from utils.icons import icon_html


def mostrar_dashboard_profesor():
    """Muestra el dashboard completo del profesor."""

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {icon_html('professor')} {st.session_state.nombre}", unsafe_allow_html=True)
        st.markdown("**Rol:** Profesor")
        if st.button("Cerrar sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.markdown("---")

        # Obtener materias del profesor
        with st.spinner("Cargando materias..."):
            todas_materias = get_materias()
        mis_materias = [m for m in todas_materias if m.get("profesor") == st.session_state.nombre]

        if mis_materias:
            nombres = [m["nombre"] for m in mis_materias]
            materia_seleccionada = st.selectbox("Selecciona materia", nombres)
            materia_actual = next(m for m in mis_materias if m["nombre"] == materia_seleccionada)
        else:
            st.warning("No tienes materias asignadas.")
            return

    st.title("Panel del Profesor")
    st.subheader(f"Materia: {materia_actual['nombre']} ({materia_actual['codigo']})")
    st.markdown(
        f"<div style='color:#6c757d;font-size:0.95rem;'>{icon_html('calendar')} {materia_actual['horario']} | {icon_html('school')} {materia_actual['salon']}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Obtener estudiantes
    with st.spinner("Cargando lista de estudiantes..."):
        estudiantes = get_mis_estudiantes(materia_actual["id"])

    if not estudiantes:
        st.info("No hay estudiantes matriculados en esta materia.")
        return

    # ── Tabla de estudiantes y registro de notas ──────
    st.subheader("Estudiantes matriculados")

    for est in estudiantes:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{est['nombre']}** — `{est['codigo']}`")
            with col2:
                nota_actual = est.get("nota_definitiva")
                if nota_actual is not None:
                    st.markdown(f"Nota actual: **{nota_actual}**")
                else:
                    st.markdown("Nota: *Sin calificar*")
            with col3:
                nueva_nota = st.number_input(
                    "Nota",
                    min_value=0.0,
                    max_value=5.0,
                    step=0.1,
                    value=nota_actual if nota_actual else 0.0,
                    key=f"nota_{est['matricula_id']}"
                )
                if st.button("Guardar", key=f"save_{est['matricula_id']}"):
                    with st.spinner("Guardando nota..."):
                        resp, code = registrar_nota(est["matricula_id"], nueva_nota)
                    if code == 200:
                        st.toast(f"Nota guardada: {nueva_nota}", icon="✅")
                        st.rerun()
                    else:
                        st.toast(resp.get("detail", "Error al guardar nota"), icon="❌")

    st.markdown("---")

    # ── Gráfica de distribución ───────────────────────
    notas_existentes = [e["nota_definitiva"] for e in estudiantes if e.get("nota_definitiva") is not None]

    if notas_existentes:
        st.subheader("Distribución de notas")

        col1, col2 = st.columns(2)
        with col1:
            promedio = round(sum(notas_existentes) / len(notas_existentes), 2)
            st.metric("Promedio del grupo", promedio)
        with col2:
            aprobados = sum(1 for n in notas_existentes if n >= 3.0)
            porcentaje = round((aprobados / len(notas_existentes)) * 100, 1)
            st.metric("% Aprobación", f"{porcentaje}%")

        fig = px.histogram(
            x=notas_existentes,
            nbins=10,
            labels={"x": "Nota", "y": "Cantidad"},
            title="Distribución de notas",
            color_discrete_sequence=["#0d6efd"]
        )
        fig.update_layout(bargap=0.1)
        
        # Gráfico de pastel (Aprobados vs Reprobados)
        reprobados = len(notas_existentes) - aprobados
        df_pie = pd.DataFrame({
            "Estado": ["Aprobados", "Reprobados"],
            "Cantidad": [aprobados, reprobados]
        })
        fig_pie = px.pie(
            df_pie, 
            values='Cantidad', 
            names='Estado', 
            title="Proporción Aprobados/Reprobados", 
            color='Estado', 
            color_discrete_map={"Aprobados":"#198754", "Reprobados":"#dc3545"}
        )
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.plotly_chart(fig, use_container_width=True)
        with col_chart2:
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Aún no hay notas registradas para mostrar estadísticas.")
