# backend/main.py
# Punto de entrada de FastAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth_router, materias, matricula, notas, kardex

# Crear tablas al iniciar (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UniGest API",
    description="Sistema de Gestión Universitaria",
    version="1.0.0"
)

# Permitir peticiones desde Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router.router)
app.include_router(materias.router)
app.include_router(matricula.router)
app.include_router(notas.router)
app.include_router(kardex.router)


@app.get("/")
def root():
    return {"mensaje": "Bienvenido a UniGest API", "docs": "/docs"}
