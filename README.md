# UniGest — Sistema de Gestión Universitaria

Plataforma web de gestión académica universitaria construida 100% en Python.

## Stack Tecnológico

- **Backend:** FastAPI + SQLAlchemy 2.0 + SQLite
- **Frontend:** Streamlit
- **Auth:** JWT (python-jose) + passlib

## Instalación

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
cd backend
python seed.py

# Ejecutar backend (desde la raíz)
uvicorn backend.main:app --reload --port 8000

# Ejecutar frontend (otra terminal)
streamlit run frontend/app.py
```

## Credenciales de prueba

| Rol        | Email                  | Contraseña     |
|------------|------------------------|----------------|
| Estudiante | ana.garcia@uni.edu     | estudiante123  |
| Estudiante | carlos.lopez@uni.edu   | estudiante123  |
| Profesor   | prof.martinez@uni.edu  | profesor123    |
| Profesor   | prof.ramos@uni.edu     | profesor123    |
