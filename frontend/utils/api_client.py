# frontend/utils/api_client.py
# Funciones para llamar al backend

import httpx
import streamlit as st

BASE_URL = "http://localhost:8000"


def get_headers():
    """Retorna los headers de autorización con el token JWT."""
    return {"Authorization": f"Bearer {st.session_state.token}"}


# ── Auth ──────────────────────────────────────────────

def login(email: str, password: str):
    """Inicia sesión y retorna la respuesta del backend."""
    response = httpx.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password}
    )
    return response.json(), response.status_code


# ── Materias ──────────────────────────────────────────

def get_materias():
    """Obtiene la lista de todas las materias."""
    response = httpx.get(f"{BASE_URL}/materias", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return []


def get_mis_materias():
    """Obtiene las materias del estudiante autenticado."""
    response = httpx.get(f"{BASE_URL}/mis-materias", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return []


# ── Matrícula ─────────────────────────────────────────

def matricular(materia_id: int):
    """Matricula al estudiante en una materia."""
    response = httpx.post(
        f"{BASE_URL}/matricula",
        json={"materia_id": materia_id},
        headers=get_headers()
    )
    return response.json(), response.status_code


def withdraw_course(matricula_id: int):
    """Withdraws a student from an enrolled course."""
    response = httpx.delete(
        f"{BASE_URL}/matricula/{matricula_id}",
        headers=get_headers()
    )
    return response.json(), response.status_code


# ── Notas ─────────────────────────────────────────────

def get_mis_estudiantes(materia_id: int):
    """Obtiene los estudiantes de una materia del profesor."""
    response = httpx.get(
        f"{BASE_URL}/mis-estudiantes",
        params={"materia_id": materia_id},
        headers=get_headers()
    )
    if response.status_code == 200:
        return response.json()
    return []


def registrar_nota(matricula_id: int, nota: float):
    """Registra la nota de un estudiante."""
    response = httpx.post(
        f"{BASE_URL}/notas",
        json={"matricula_id": matricula_id, "nota": nota},
        headers=get_headers()
    )
    return response.json(), response.status_code


# ── Kardex ────────────────────────────────────────────

def get_kardex():
    """Obtiene el kardex del estudiante autenticado."""
    response = httpx.get(f"{BASE_URL}/kardex", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return None
