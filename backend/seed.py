# backend/seed.py
# Datos iniciales de prueba

import sys
import os

# Agregar la carpeta raíz al path para imports relativos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.database import engine, SessionLocal, Base
from backend.models import Estudiante, Profesor, Materia
from backend.auth import hash_password


def seed():
    """Crea las tablas e inserta datos iniciales de prueba."""
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")

    db = SessionLocal()

    try:
        # Verificar si ya hay datos
        if db.query(Profesor).first():
            print("⚠️  La base de datos ya contiene datos. No se insertaron duplicados.")
            return

        # ── Profesores ────────────────────────────────────
        profesores = [
            Profesor(
                nombre="Prof. Martínez",
                email="prof.martinez@uni.edu",
                password_hash=hash_password("profesor123"),
                departamento="Ciencias Exactas"
            ),
            Profesor(
                nombre="Prof. Ramos",
                email="prof.ramos@uni.edu",
                password_hash=hash_password("profesor123"),
                departamento="Ingeniería de Sistemas"
            ),
            Profesor(
                nombre="Prof. Herrera",
                email="prof.herrera@uni.edu",
                password_hash=hash_password("profesor123"),
                departamento="Humanidades"
            ),
        ]
        db.add_all(profesores)
        db.flush()  # Para obtener los IDs generados
        print(f"✅ {len(profesores)} profesores insertados.")

        # ── Materias ──────────────────────────────────────
        materias = [
            Materia(
                nombre="Cálculo Diferencial",
                codigo="MAT101",
                creditos=4,
                cupos_totales=30,
                cupos_disponibles=30,
                horario="Lun/Mie 8:00-10:00",
                salon="Edificio A - 301",
                profesor_id=profesores[0].id
            ),
            Materia(
                nombre="Álgebra Lineal",
                codigo="MAT201",
                creditos=4,
                cupos_totales=25,
                cupos_disponibles=25,
                horario="Mar/Jue 8:00-10:00",
                salon="Edificio A - 205",
                profesor_id=profesores[0].id
            ),
            Materia(
                nombre="Programación Orientada a Objetos",
                codigo="SIS201",
                creditos=3,
                cupos_totales=35,
                cupos_disponibles=35,
                horario="Mar/Jue 10:00-12:00",
                salon="Lab. Sistemas 1",
                profesor_id=profesores[1].id
            ),
            Materia(
                nombre="Bases de Datos",
                codigo="SIS301",
                creditos=3,
                cupos_totales=30,
                cupos_disponibles=30,
                horario="Lun/Mie 14:00-16:00",
                salon="Lab. Sistemas 2",
                profesor_id=profesores[1].id
            ),
            Materia(
                nombre="Inglés I",
                codigo="ING101",
                creditos=2,
                cupos_totales=40,
                cupos_disponibles=40,
                horario="Vie 8:00-10:00",
                salon="Edificio B - 102",
                profesor_id=profesores[2].id
            ),
            Materia(
                nombre="Ética Profesional",
                codigo="HUM101",
                creditos=2,
                cupos_totales=45,
                cupos_disponibles=45,
                horario="Vie 10:00-12:00",
                salon="Edificio B - 201",
                profesor_id=profesores[2].id
            ),
        ]
        db.add_all(materias)
        print(f"✅ {len(materias)} materias insertadas.")

        # ── Estudiantes ───────────────────────────────────
        estudiantes = [
            Estudiante(
                nombre="Ana García",
                codigo="20230145",
                email="ana.garcia@uni.edu",
                password_hash=hash_password("estudiante123"),
                semestre=3
            ),
            Estudiante(
                nombre="Carlos López",
                codigo="20230278",
                email="carlos.lopez@uni.edu",
                password_hash=hash_password("estudiante123"),
                semestre=3
            ),
            Estudiante(
                nombre="María Rodríguez",
                codigo="20240012",
                email="maria.rodriguez@uni.edu",
                password_hash=hash_password("estudiante123"),
                semestre=1
            ),
            Estudiante(
                nombre="Juan Pérez",
                codigo="20240089",
                email="juan.perez@uni.edu",
                password_hash=hash_password("estudiante123"),
                semestre=2
            ),
            Estudiante(
                nombre="Laura Torres",
                codigo="20230301",
                email="laura.torres@uni.edu",
                password_hash=hash_password("estudiante123"),
                semestre=4
            ),
        ]
        db.add_all(estudiantes)
        print(f"✅ {len(estudiantes)} estudiantes insertados.")

        db.commit()
        print("\n🎉 Base de datos inicializada correctamente.")
        print("   Archivo: unigest.db")

    except Exception as e:
        db.rollback()
        print(f"❌ Error al insertar datos: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
