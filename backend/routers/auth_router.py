# backend/routers/auth_router.py
# POST /login

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import verify_password, create_access_token
from .. import models, schemas

router = APIRouter(tags=["Autenticación"])


@router.post("/login", response_model=schemas.LoginResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Autentica al usuario y retorna un token JWT."""

    # Buscar primero en estudiantes
    estudiante = db.query(models.Estudiante).filter(
        models.Estudiante.email == data.email
    ).first()

    if estudiante and verify_password(data.password, estudiante.password_hash):
        token = create_access_token({
            "sub": estudiante.email,
            "rol": "estudiante",
            "id": estudiante.id
        })
        return schemas.LoginResponse(
            access_token=token,
            rol="estudiante",
            nombre=estudiante.nombre,
            id=estudiante.id
        )

    # Buscar en profesores
    profesor = db.query(models.Profesor).filter(
        models.Profesor.email == data.email
    ).first()

    if profesor and verify_password(data.password, profesor.password_hash):
        token = create_access_token({
            "sub": profesor.email,
            "rol": "profesor",
            "id": profesor.id
        })
        return schemas.LoginResponse(
            access_token=token,
            rol="profesor",
            nombre=profesor.nombre,
            id=profesor.id
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email o contraseña incorrectos"
    )
