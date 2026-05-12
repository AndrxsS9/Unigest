# 🎓 UniGest — Sistema de Gestión Universitaria

UniGest es una plataforma integral de gestión académica diseñada para modernizar y simplificar los procesos universitarios. Construida completamente en **Python**, esta aplicación ofrece un ecosistema robusto tanto para estudiantes como para docentes.

---

## 🚀 Características Principales

### 👨‍🎓 Para Estudiantes
- **Autenticación Segura:** Acceso mediante JWT.
- **Catálogo de Materias:** Visualización de oferta académica en tiempo real.
- **Gestión de Matrículas:** Inscripción y retiro de asignaturas con control de cupos.
- **Historial Académico (Kardex):** Consulta de notas definitivas y estado de aprobación.

### 👨‍🏫 Para Profesores
- **Gestión de Cursos:** Control total sobre las materias asignadas.
- **Listado de Estudiantes:** Consulta de alumnos inscritos por asignatura.
- **Calificaciones:** Sistema centralizado para el registro de notas definitivas.

### ⚙️ Administrativas
- **Base de Datos Relacional:** Gestión eficiente de datos con SQLAlchemy.
- **Seguridad:** Hash de contraseñas y validación de tokens Bearer.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **Base de Datos** | SQLite (SQLAlchemy 2.0) |
| **Seguridad** | JWT (JOSE) + Passlib (Bcrypt) |
| **Lenguaje** | Python 3.10+ |

---

## 📁 Estructura del Proyecto

```text
UniGest/
├── backend/            # Lógica del servidor y API REST
│   ├── routers/        # Endpoints organizados por módulos
│   ├── models.py       # Definición de tablas de la BD
│   ├── schemas.py      # Esquemas de validación Pydantic
│   ├── database.py     # Configuración de conexión SQLite
│   ├── auth.py         # Lógica de seguridad y JWT
│   ├── main.py         # Punto de entrada de la API
│   └── seed.py         # Script de inicialización de datos
├── frontend/           # Interfaz de usuario
│   ├── views/          # Pantallas de la aplicación
│   └── app.py          # Punto de entrada de Streamlit
├── .env                # Variables de entorno (Configuraciones)
└── requirements.txt    # Dependencias del proyecto
```

---

## 🔧 Instalación y Configuración

Siga estos pasos para poner en marcha el proyecto en su entorno local:

### 1. Clonar y Preparar Entorno
```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd Unigest

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Inicializar Datos
Antes de ejecutar la aplicación, cree la base de datos y cargue los datos de prueba:
```bash
cd backend
python seed.py
cd ..
```

### 3. Ejecutar la Aplicación
Debe iniciar ambos servicios en terminales separadas:

**Terminal 1 (Backend):**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
streamlit run frontend/app.py
```

---

## 🔑 Credenciales de Acceso (Modo Prueba)

Utilice las siguientes cuentas para explorar las funcionalidades:

| Rol | Usuario (Email) | Contraseña |
| :--- | :--- | :--- |
| **Estudiante** | `ana.garcia@uni.edu` | `estudiante123` |
| **Estudiante** | `carlos.lopez@uni.edu` | `estudiante123` |
| **Profesor** | `prof.martinez@uni.edu` | `profesor123` |
| **Profesor** | `prof.ramos@uni.edu` | `profesor123` |

---

## 🛡️ Seguridad y API
La documentación interactiva de la API está disponible en:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📄 Licencia
Este proyecto es de uso académico para la gestión universitaria.
