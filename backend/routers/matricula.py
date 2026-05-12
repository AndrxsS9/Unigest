# backend/routers/matricula.py
# POST /matricula, GET /mis-materias

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas

router = APIRouter(tags=["Matrícula"])


@router.post("/matricula", response_model=schemas.MatriculaResponse)
def matricular(
    data: schemas.MatriculaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Matricula al estudiante autenticado en una materia."""

    # 1. Verificar que el usuario es estudiante
    if current_user.rol != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden matricularse")

    # 2. Verificar que la materia existe y tiene cupos
    materia = db.query(models.Materia).filter(models.Materia.id == data.materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    if materia.cupos_disponibles <= 0:
        raise HTTPException(status_code=400, detail="No hay cupos disponibles para esta materia")

    # 3. Verificar si ya está matriculado
    matricula_existente = db.query(models.Matricula).filter(
        models.Matricula.estudiante_id == current_user.id,
        models.Matricula.materia_id == data.materia_id,
        models.Matricula.estado == "activa"
    ).first()
    if matricula_existente:
        raise HTTPException(status_code=400, detail="Ya estás matriculado en esta materia")

    # 4. Verificar choque de horario
    materias_inscritas = db.query(models.Matricula).filter(
        models.Matricula.estudiante_id == current_user.id,
        models.Matricula.estado == "activa"
    ).all()

    for mi in materias_inscritas:
        materia_inscrita = db.query(models.Materia).filter(
            models.Materia.id == mi.materia_id
        ).first()
        if materia_inscrita and materia_inscrita.horario == materia.horario:
            raise HTTPException(
                status_code=400,
                detail=f"Choque de horario con {materia_inscrita.nombre} ({materia_inscrita.horario})"
            )

    # 5. Crear matrícula y descontar cupo
    nueva_matricula = models.Matricula(
        estudiante_id=current_user.id,
        materia_id=data.materia_id,
        estado="activa"
    )
    materia.cupos_disponibles -= 1

    db.add(nueva_matricula)
    db.commit()

    return schemas.MatriculaResponse(
        mensaje="Matrícula exitosa",
        materia=materia.nombre,
        horario=materia.horario
    )


@router.get("/mis-materias", response_model=list[schemas.MiMateriaResponse])
def mis_materias(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Retorna las materias en las que está matriculado el estudiante."""

    if current_user.rol != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden consultar sus materias")

    matriculas = db.query(models.Matricula).filter(
        models.Matricula.estudiante_id == current_user.id,
        models.Matricula.estado == "activa"
    ).all()

    resultado = []
    for m in matriculas:
        materia = m.materia
        resultado.append(schemas.MiMateriaResponse(
            id=m.id,
            materia_id=materia.id,
            nombre=materia.nombre,
            codigo=materia.codigo,
            creditos=materia.creditos,
            horario=materia.horario,
            salon=materia.salon,
            nota_definitiva=m.nota_definitiva,
            estado=m.estado
        ))

    return resultado
