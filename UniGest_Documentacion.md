# UniGest — Sistema de Gestión Universitaria
### Taller Python · Full Stack · 90 minutos

---

## Índice

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Arquitectura general](#2-arquitectura-general)
3. [Estructura de carpetas](#3-estructura-de-carpetas)
4. [Modelos de datos](#4-modelos-de-datos)
5. [Instalación y configuración](#5-instalación-y-configuración)
6. [Backend — Endpoints FastAPI](#6-backend--endpoints-fastapi)
7. [Frontend — Vistas Streamlit](#7-frontend--vistas-streamlit)
8. [Flujo completo del sistema](#8-flujo-completo-del-sistema)
9. [Distribución del taller](#9-distribución-del-taller)
10. [Convenciones del código](#10-convenciones-del-código)

---

## 1. Descripción del proyecto

**UniGest** es una plataforma web de gestión académica universitaria construida 100% en Python. Permite a estudiantes matricularse en materias y consultar su kardex, y a profesores registrar notas y visualizar el rendimiento del grupo.

### Roles del sistema

| Rol | Capacidades |
|---|---|
| **Estudiante** | Ver materias disponibles, matricularse, ver horario semanal, consultar kardex y promedio |
| **Profesor** | Ver estudiantes por materia, registrar y actualizar notas, ver gráfica de distribución |

### Stack tecnológico

| Capa | Tecnología | Propósito |
|---|---|---|
| Backend API | FastAPI | Endpoints REST, validación, autenticación |
| ORM | SQLAlchemy 2.0 | Modelos y queries a la base de datos |
| Base de datos | SQLite | Almacenamiento local (sin configuración) |
| Validación | Pydantic v2 | Schemas de entrada y salida |
| Auth | python-jose + passlib | JWT y hash de contraseñas |
| Frontend | Streamlit | Interfaz de usuario interactiva |
| HTTP client | httpx | Llamadas del frontend al backend |
| Gráficas | Plotly Express | Dashboard del profesor |

---

## 2. Arquitectura general

```
┌─────────────────────────────┐        ┌─────────────────────────────┐
│       FRONTEND              │        │         BACKEND              │
│       Streamlit             │──────▶ │         FastAPI              │
│   Puerto: 8501              │  HTTP  │     Puerto: 8000             │
│                             │◀────── │                              │
│  - Vista Estudiante         │  JSON  │  - Auth (JWT)                │
│  - Vista Profesor           │        │  - Materias                  │
└─────────────────────────────┘        │  - Matrícula                 │
                                       │  - Notas                     │
                                       │  - Kardex                    │
                                       └──────────┬──────────────────┘
                                                  │ SQLAlchemy ORM
                                       ┌──────────▼──────────────────┐
                                       │         SQLite              │
                                       │      unigest.db             │
                                       └─────────────────────────────┘
```

El frontend **nunca** accede directamente a la base de datos. Toda la lógica pasa por el backend.

---

## 3. Estructura de carpetas

```
unigest/
│
├── backend/
│   ├── main.py               # Punto de entrada de FastAPI
│   ├── database.py           # Conexión y sesión de SQLAlchemy
│   ├── models.py             # Modelos ORM (tablas)
│   ├── schemas.py            # Schemas Pydantic (request/response)
│   ├── auth.py               # JWT: crear y verificar tokens
│   ├── seed.py               # Datos iniciales de prueba
│   └── routers/
│       ├── auth_router.py    # POST /login
│       ├── materias.py       # GET /materias
│       ├── matricula.py      # POST /matricula, GET /mis-materias
│       ├── notas.py          # POST /notas, PUT /notas/{id}
│       └── kardex.py         # GET /kardex
│
├── frontend/
│   ├── app.py                # Entrada Streamlit, manejo de sesión
│   ├── views/
│   │   ├── login.py          # Pantalla de login
│   │   ├── estudiante.py     # Dashboard del estudiante
│   │   └── profesor.py       # Dashboard del profesor
│   └── utils/
│       └── api_client.py     # Funciones para llamar al backend
│
├── requirements.txt
├── .env                      # Variables de entorno (SECRET_KEY)
└── README.md
```

---

## 4. Modelos de datos

### Diagrama de relaciones

```
Estudiante ──────┐
                 │ many-to-many
Materia  ────────┴──▶ Matricula ──▶ Nota
                          │
                      (cupo, estado)

Profesor ────────────────▶ Materia (un profesor por materia)
```

### Tablas

#### `estudiantes`
| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| nombre | String | Nombre completo |
| codigo | String (único) | Código estudiantil |
| email | String (único) | Correo institucional |
| password_hash | String | Contraseña hasheada |
| semestre | Integer | Semestre actual |

#### `profesores`
| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| nombre | String | Nombre completo |
| email | String (único) | Correo institucional |
| password_hash | String | Contraseña hasheada |
| departamento | String | Departamento académico |

#### `materias`
| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| nombre | String | Nombre de la materia |
| codigo | String (único) | Código (ej: MAT101) |
| creditos | Integer | Número de créditos |
| cupos_totales | Integer | Cupos máximos |
| cupos_disponibles | Integer | Cupos restantes |
| horario | String | Ej: "Lun/Mie 8:00-10:00" |
| salon | String | Ej: "Edificio A - 301" |
| profesor_id | FK → profesores | Profesor asignado |

#### `matriculas` (tabla de asociación)
| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| estudiante_id | FK → estudiantes | Estudiante |
| materia_id | FK → materias | Materia |
| fecha_matricula | DateTime | Cuándo se matriculó |
| estado | String | "activa" / "retirada" |
| nota_definitiva | Float (nullable) | Nota final (0.0 – 5.0) |
| aprobada | Boolean (nullable) | True si nota >= 3.0 |

---

## 5. Instalación y configuración

### Requisitos previos

- Python 3.10 o superior
- pip

### Paso 1 — Clonar y crear entorno virtual

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/unigest.git
cd unigest

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Mac / Linux)
source venv/bin/activate
```

### Paso 2 — Instalar dependencias

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
fastapi==0.111.0
uvicorn==0.29.0
sqlalchemy==2.0.30
pydantic==2.7.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
httpx==0.27.0
streamlit==1.35.0
plotly==5.22.0
pandas==2.2.2
python-dotenv==1.0.1
```

### Paso 3 — Variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=unigest_clave_secreta_2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./unigest.db
```

### Paso 4 — Inicializar base de datos y datos de prueba

```bash
cd backend
python seed.py
```

Esto crea la base de datos y carga:
- 3 profesores de prueba
- 6 materias con horarios
- 5 estudiantes de prueba

### Paso 5 — Ejecutar el backend

```bash
# Desde la carpeta raíz
uvicorn backend.main:app --reload --port 8000
```

Documentación interactiva disponible en: `http://localhost:8000/docs`

### Paso 6 — Ejecutar el frontend

```bash
# En otra terminal
streamlit run frontend/app.py
```

Interfaz disponible en: `http://localhost:8501`

### Credenciales de prueba

| Rol | Email | Contraseña |
|---|---|---|
| Estudiante | ana.garcia@uni.edu | estudiante123 |
| Estudiante | carlos.lopez@uni.edu | estudiante123 |
| Profesor | prof.martinez@uni.edu | profesor123 |
| Profesor | prof.ramos@uni.edu | profesor123 |

---

## 6. Backend — Endpoints FastAPI

### Autenticación

#### `POST /login`
Genera un token JWT según el rol del usuario.

**Request body:**
```json
{
  "email": "ana.garcia@uni.edu",
  "password": "estudiante123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "rol": "estudiante",
  "nombre": "Ana García",
  "id": 1
}
```

El campo `rol` indica qué vistas mostrar en el frontend.

---

### Materias

#### `GET /materias`
Lista todas las materias con cupos disponibles.

**Headers requeridos:** `Authorization: Bearer <token>`

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Cálculo Diferencial",
    "codigo": "MAT101",
    "creditos": 4,
    "cupos_disponibles": 12,
    "horario": "Lun/Mie 8:00-10:00",
    "salon": "Edificio A - 301",
    "profesor": "Prof. Martínez"
  }
]
```

---

### Matrícula

#### `POST /matricula`
Matricula al estudiante autenticado en una materia.

**Headers:** `Authorization: Bearer <token>` (solo estudiantes)

**Request body:**
```json
{
  "materia_id": 3
}
```

**Validaciones que realiza el backend:**
- ¿Tiene cupos disponibles la materia?
- ¿El estudiante ya está matriculado en esa materia?
- ¿Hay choque de horario con otra materia inscrita?

**Response exitoso:**
```json
{
  "mensaje": "Matrícula exitosa",
  "materia": "Programación Orientada a Objetos",
  "horario": "Mar/Jue 10:00-12:00"
}
```

**Response con error:**
```json
{
  "detail": "No hay cupos disponibles para esta materia"
}
```

#### `GET /mis-materias`
Retorna las materias en las que está matriculado el estudiante, con notas si ya fueron registradas.

---

### Notas

#### `POST /notas`
El profesor registra la nota definitiva de un estudiante en su materia.

**Headers:** `Authorization: Bearer <token>` (solo profesores)

**Request body:**
```json
{
  "matricula_id": 7,
  "nota": 4.2
}
```

**Lógica automática en el backend:**
- Si `nota >= 3.0` → `aprobada = True`
- Si `nota < 3.0` → `aprobada = False`
- Solo el profesor de esa materia puede ingresar la nota

**Response:**
```json
{
  "mensaje": "Nota registrada correctamente",
  "estudiante": "Ana García",
  "nota": 4.2,
  "aprobada": true
}
```

#### `GET /mis-estudiantes`
Retorna todos los estudiantes matriculados en las materias del profesor autenticado, con sus notas.

---

### Kardex

#### `GET /kardex`
Retorna el resumen académico completo del estudiante autenticado.

**Headers:** `Authorization: Bearer <token>` (solo estudiantes)

**Response:**
```json
{
  "estudiante": "Ana García",
  "codigo": "20230145",
  "semestre": 3,
  "materias": [
    {
      "nombre": "Cálculo Diferencial",
      "codigo": "MAT101",
      "creditos": 4,
      "nota": 4.2,
      "estado": "Aprobada"
    },
    {
      "nombre": "Inglés I",
      "codigo": "ING101",
      "creditos": 2,
      "nota": null,
      "estado": "En curso"
    }
  ],
  "promedio_acumulado": 4.2,
  "creditos_aprobados": 4,
  "creditos_matriculados": 6
}
```

---

## 7. Frontend — Vistas Streamlit

### Manejo de sesión (`app.py`)

El estado de la sesión se guarda en `st.session_state` con las siguientes claves:

| Clave | Tipo | Descripción |
|---|---|---|
| `token` | str | JWT del usuario autenticado |
| `rol` | str | `"estudiante"` o `"profesor"` |
| `nombre` | str | Nombre del usuario |
| `user_id` | int | ID en la base de datos |

Si `st.session_state.token` es `None`, se muestra la vista de login. Según el rol, se redirige a la vista correspondiente.

### Vista del estudiante

**Panel izquierdo (sidebar):**
- Nombre y código del estudiante
- Botón de cerrar sesión

**Pestaña 1 — Mis materias y horario:**
- Tabla con materias matriculadas, horario, salón y nota (si existe)
- Vista de horario semanal generada con pandas

**Pestaña 2 — Matricularme:**
- Tabla de materias disponibles con cupos
- Botón "Matricularme" por cada materia
- Mensaje de éxito o error según la respuesta del backend

**Pestaña 3 — Mi kardex:**
- Métricas: promedio acumulado, créditos aprobados, materias en curso
- Tabla completa con estado por materia

### Vista del profesor

**Panel izquierdo (sidebar):**
- Nombre del profesor y departamento
- Selector de materia (si tiene varias)

**Panel principal:**
- Tabla de estudiantes de la materia seleccionada con notas
- Input de nota por estudiante con botón "Guardar"
- Gráfica de distribución de notas (histograma con Plotly)
- Métricas: promedio del grupo, porcentaje de aprobación

---

## 8. Flujo completo del sistema

```
1. ESTUDIANTE inicia sesión
         │
         ▼
2. Ve materias disponibles con cupos
         │
         ▼
3. Hace clic en "Matricularme" en una materia
         │
         ├── Backend valida cupos y choque de horario
         │
         ├── Si hay error → muestra mensaje en rojo
         │
         └── Si es exitoso → materia aparece en "Mis materias"
                   │
                   ▼
4. PROFESOR inicia sesión (en otra sesión/navegador)
         │
         ▼
5. Ve su lista de estudiantes matriculados
         │
         ▼
6. Ingresa nota definitiva para cada estudiante
         │
         ├── Backend calcula si aprobó o reprobó
         │
         └── Nota queda guardada en la BD
                   │
                   ▼
7. ESTUDIANTE actualiza su kardex
         │
         └── Ve nota, estado y promedio acumulado actualizado
```

---

## 9. Distribución del taller

| Tiempo | Actividad | Responsable |
|---|---|---|
| 0 – 10 min | Presentación del proyecto, recorrido de la estructura de carpetas y modelos | Presentador |
| 10 – 30 min | Implementar endpoint `POST /matricula` con validaciones de cupos y choque de horario | Todo el grupo |
| 30 – 50 min | Implementar `POST /notas` con cálculo automático de aprobación y `GET /kardex` | Todo el grupo |
| 50 – 75 min | Construir las dos vistas de Streamlit (estudiante y profesor) | Todo el grupo |
| 75 – 90 min | Demo completa del flujo y preguntas | Todo el grupo |

> **Nota:** Los modelos, la conexión a la base de datos, el seed y la estructura de carpetas se entregan ya construidos. El taller se enfoca en la lógica de negocio y el frontend.

---

## 10. Convenciones del código

### Nombres
- Archivos y carpetas: `snake_case`
- Clases (modelos, schemas): `PascalCase`
- Funciones y variables: `snake_case`
- Constantes: `UPPER_SNAKE_CASE`

### Estructura de un router

```python
# backend/routers/matricula.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/matricula", tags=["Matrícula"])

@router.post("/", response_model=schemas.MatriculaResponse)
def matricular(
    data: schemas.MatriculaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Verificar que el usuario es estudiante
    if current_user.rol != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden matricularse")

    # 2. Verificar cupos
    materia = db.query(models.Materia).filter(models.Materia.id == data.materia_id).first()
    if not materia or materia.cupos_disponibles <= 0:
        raise HTTPException(status_code=400, detail="No hay cupos disponibles")

    # 3. Verificar si ya está matriculado
    # ... lógica adicional

    # 4. Crear matrícula y descontar cupo
    # ... crear registro y guardar
```

### Llamadas al backend desde Streamlit

```python
# frontend/utils/api_client.py

import httpx
import streamlit as st

BASE_URL = "http://localhost:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def get_mis_materias():
    response = httpx.get(f"{BASE_URL}/mis-materias", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return []

def matricular(materia_id: int):
    response = httpx.post(
        f"{BASE_URL}/matricula",
        json={"materia_id": materia_id},
        headers=get_headers()
    )
    return response.json(), response.status_code
```

---

*Documentación preparada para el taller de Python Full Stack — UniGest v1.0*
