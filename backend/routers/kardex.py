# backend/routers/kardex.py
# GET /kardex

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas

router = APIRouter(tags=["Kardex"])


@router.get("/kardex", response_model=schemas.KardexResponse)
def obtener_kardex(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Retorna el resumen académico completo del estudiante autenticado."""

    if current_user.rol != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden consultar su kardex")

    matriculas = db.query(models.Matricula).filter(
        models.Matricula.estudiante_id == current_user.id
    ).all()

    materias_kardex = []
    creditos_aprobados = 0
    creditos_matriculados = 0
    notas_con_valor = []

    for m in matriculas:
        materia = m.materia

        # Determinar estado
        if m.nota_definitiva is not None:
            estado = "Aprobada" if m.aprobada else "Reprobada"
            notas_con_valor.append(m.nota_definitiva)
            if m.aprobada:
                creditos_aprobados += materia.creditos
        else:
            estado = "En curso"

        creditos_matriculados += materia.creditos

        materias_kardex.append(schemas.KardexMateriaResponse(
            nombre=materia.nombre,
            codigo=materia.codigo,
            creditos=materia.creditos,
            nota=m.nota_definitiva,
            estado=estado
        ))

    # Calcular promedio
    promedio = round(sum(notas_con_valor) / len(notas_con_valor), 2) if notas_con_valor else None

    return schemas.KardexResponse(
        estudiante=current_user.nombre,
        codigo=current_user.codigo,
        semestre=current_user.semestre,
        materias=materias_kardex,
        promedio_acumulado=promedio,
        creditos_aprobados=creditos_aprobados,
        creditos_matriculados=creditos_matriculados
    )
