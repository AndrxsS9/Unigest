# backend/routers/notas.py
# POST /notas, PUT /notas/{id}, GET /mis-estudiantes

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas

router = APIRouter(tags=["Notas"])


@router.post("/notas", response_model=schemas.NotaResponse)
def registrar_nota(
    data: schemas.NotaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Registra la nota definitiva de un estudiante en una materia."""

    # 1. Verificar que el usuario es profesor
    if current_user.rol != "profesor":
        raise HTTPException(status_code=403, detail="Solo profesores pueden registrar notas")

    # 2. Verificar que la matrícula existe
    matricula = db.query(models.Matricula).filter(
        models.Matricula.id == data.matricula_id
    ).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")

    # 3. Verificar que el profesor es dueño de la materia
    materia = db.query(models.Materia).filter(
        models.Materia.id == matricula.materia_id
    ).first()
    if materia.profesor_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para calificar esta materia")

    # 4. Validar rango de nota
    if data.nota < 0.0 or data.nota > 5.0:
        raise HTTPException(status_code=400, detail="La nota debe estar entre 0.0 y 5.0")

    # 5. Registrar nota
    matricula.nota_definitiva = data.nota
    matricula.aprobada = data.nota >= 3.0

    db.commit()

    estudiante = db.query(models.Estudiante).filter(
        models.Estudiante.id == matricula.estudiante_id
    ).first()

    return schemas.NotaResponse(
        mensaje="Nota registrada correctamente",
        estudiante=estudiante.nombre,
        nota=data.nota,
        aprobada=matricula.aprobada
    )


@router.put("/notas/{matricula_id}", response_model=schemas.NotaResponse)
def actualizar_nota(
    matricula_id: int,
    data: schemas.NotaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Actualiza la nota de un estudiante."""

    if current_user.rol != "profesor":
        raise HTTPException(status_code=403, detail="Solo profesores pueden actualizar notas")

    matricula = db.query(models.Matricula).filter(
        models.Matricula.id == matricula_id
    ).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")

    materia = db.query(models.Materia).filter(
        models.Materia.id == matricula.materia_id
    ).first()
    if materia.profesor_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para calificar esta materia")

    if data.nota < 0.0 or data.nota > 5.0:
        raise HTTPException(status_code=400, detail="La nota debe estar entre 0.0 y 5.0")

    matricula.nota_definitiva = data.nota
    matricula.aprobada = data.nota >= 3.0
    db.commit()

    estudiante = db.query(models.Estudiante).filter(
        models.Estudiante.id == matricula.estudiante_id
    ).first()

    return schemas.NotaResponse(
        mensaje="Nota actualizada correctamente",
        estudiante=estudiante.nombre,
        nota=data.nota,
        aprobada=matricula.aprobada
    )


@router.get("/mis-estudiantes", response_model=list[schemas.EstudianteMateriaResponse])
def mis_estudiantes(
    materia_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Retorna los estudiantes matriculados en una materia del profesor."""

    if current_user.rol != "profesor":
        raise HTTPException(status_code=403, detail="Solo profesores pueden consultar estudiantes")

    # Verificar que la materia pertenece al profesor
    materia = db.query(models.Materia).filter(
        models.Materia.id == materia_id,
        models.Materia.profesor_id == current_user.id
    ).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada o no te pertenece")

    matriculas = db.query(models.Matricula).filter(
        models.Matricula.materia_id == materia_id,
        models.Matricula.estado == "activa"
    ).all()

    resultado = []
    for m in matriculas:
        estudiante = m.estudiante
        resultado.append(schemas.EstudianteMateriaResponse(
            matricula_id=m.id,
            estudiante_id=estudiante.id,
            nombre=estudiante.nombre,
            codigo=estudiante.codigo,
            nota_definitiva=m.nota_definitiva,
            aprobada=m.aprobada
        ))

    return resultado
