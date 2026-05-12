# backend/schemas.py
# Schemas Pydantic (request/response)

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Auth ──────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    nombre: str
    id: int


# ── Materias ──────────────────────────────────────────

class MateriaResponse(BaseModel):
    id: int
    nombre: str
    codigo: str
    creditos: int
    cupos_disponibles: int
    horario: str
    salon: str
    profesor: str

    class Config:
        from_attributes = True


# ── Matrícula ─────────────────────────────────────────

class MatriculaCreate(BaseModel):
    materia_id: int


class MatriculaResponse(BaseModel):
    mensaje: str
    materia: str
    horario: str


class MiMateriaResponse(BaseModel):
    id: int
    materia_id: int
    nombre: str
    codigo: str
    creditos: int
    horario: str
    salon: str
    nota_definitiva: Optional[float] = None
    estado: str

    class Config:
        from_attributes = True


# ── Notas ─────────────────────────────────────────────

class NotaCreate(BaseModel):
    matricula_id: int
    nota: float


class NotaResponse(BaseModel):
    mensaje: str
    estudiante: str
    nota: float
    aprobada: bool


class EstudianteMateriaResponse(BaseModel):
    matricula_id: int
    estudiante_id: int
    nombre: str
    codigo: str
    nota_definitiva: Optional[float] = None
    aprobada: Optional[bool] = None

    class Config:
        from_attributes = True


# ── Kardex ────────────────────────────────────────────

class KardexMateriaResponse(BaseModel):
    nombre: str
    codigo: str
    creditos: int
    nota: Optional[float] = None
    estado: str


class KardexResponse(BaseModel):
    estudiante: str
    codigo: str
    semestre: int
    materias: list[KardexMateriaResponse]
    promedio_acumulado: Optional[float] = None
    creditos_aprobados: int
    creditos_matriculados: int
