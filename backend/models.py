# backend/models.py
# Modelos ORM (tablas)

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    semestre = Column(Integer, default=1)

    # Relación con matrículas
    matriculas = relationship("Matricula", back_populates="estudiante")


class Profesor(Base):
    __tablename__ = "profesores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    departamento = Column(String, nullable=False)

    # Relación con materias
    materias = relationship("Materia", back_populates="profesor")


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, unique=True, nullable=False)
    creditos = Column(Integer, nullable=False)
    cupos_totales = Column(Integer, nullable=False)
    cupos_disponibles = Column(Integer, nullable=False)
    horario = Column(String, nullable=False)
    salon = Column(String, nullable=False)
    profesor_id = Column(Integer, ForeignKey("profesores.id"), nullable=False)

    # Relaciones
    profesor = relationship("Profesor", back_populates="materias")
    matriculas = relationship("Matricula", back_populates="materia")


class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    fecha_matricula = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="activa")  # "activa" / "retirada"
    nota_definitiva = Column(Float, nullable=True)
    aprobada = Column(Boolean, nullable=True)

    # Relaciones
    estudiante = relationship("Estudiante", back_populates="matriculas")
    materia = relationship("Materia", back_populates="matriculas")
