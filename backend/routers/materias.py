# backend/routers/materias.py
# GET /materias

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas

router = APIRouter(tags=["Materias"])


@router.get("/materias", response_model=list[schemas.MateriaResponse])
def listar_materias(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Lista todas las materias con cupos disponibles."""
    materias = db.query(models.Materia).all()

    resultado = []
    for m in materias:
        resultado.append(schemas.MateriaResponse(
            id=m.id,
            nombre=m.nombre,
            codigo=m.codigo,
            creditos=m.creditos,
            cupos_disponibles=m.cupos_disponibles,
            horario=m.horario,
            salon=m.salon,
            profesor=m.profesor.nombre
        ))

    return resultado
