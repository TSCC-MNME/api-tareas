# API REST Básica de Tareas (FastAPI)

API mínima para gestionar tareas (`tasks`) con operaciones CRUD completas y un endpoint de salud (`/health`).  

La API:

- Sigue la especificación **OpenAPI 3.0.3** que se proporciona en el enunciado.
- Usa una **arquitectura en 3 capas**: `models`, `services`, `routers`.
- Almacena las tareas en **memoria** usando un **arreglo (lista)**, sin base de datos.
- Expone documentación interactiva con **Swagger UI** y **ReDoc**.

---

## Requisitos

- Python 3.10 o superior (recomendado 3.12, como en el entorno de ejemplo).
- `pip` para instalar dependencias.

---

## Instalación y ejecución

### 1. Clonar o descargar el proyecto

```bash
git clone <URL_DE_TU_REPO> api-tareas
cd api-tareas
```

(O simplemente coloca todos los archivos en una carpeta, por ejemplo `api-tareas/`).

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
```

Activar el entorno:

- En **Linux / macOS**:

  ```bash
  source venv/bin/activate
  ```

- En **Windows (PowerShell)**:

  ```bash
  .\venv\Scripts\Activate.ps1
  ```

### 3. Instalar dependencias

```bash
pip install fastapi uvicorn
```

*(FastAPI instalará Pydantic y Starlette automáticamente).*

Si quieres fijar versiones, puedes usar algo como:

```bash
pip install "fastapi[standard]" uvicorn
```

---

## Ejecución del servidor

Desde la raíz del proyecto (donde está `main.py`):

```bash
uvicorn main:app --reload --port 3000
```

- `--reload` recarga el servidor al modificar archivos (útil en desarrollo).
- `--port 3000` hace que el servidor escuche en `http://localhost:3000`, tal como indica el OpenAPI.

---

## Estructura del proyecto

Ejemplo de estructura esperada:

```bash
api-tareas/
├─ main.py
├─ models/
│  └─ task_model.py
├─ services/
│  └─ task_service.py
└─ routers/
   ├─ task_router.py
   └─ health_router.py
```

- `models/task_model.py`: Modelos Pydantic de la API (`Task`, `TaskCreate`, `TaskUpdate`, `TaskPatch`, `ErrorResponse`).
- `services/task_service.py`: Lógica de negocio y almacenamiento en memoria (lista de tareas).
- `routers/task_router.py`: Endpoints `/tasks` (CRUD completo).
- `routers/health_router.py`: Endpoint `/health`.
- `main.py`: Crea la instancia de FastAPI, registra los routers y personaliza el esquema OpenAPI (servidor `http://localhost:3000`).

---

## Endpoints disponibles

### Health

#### `GET /health`

Verifica el estado del servicio.

**Respuesta 200 OK**

```json
{
  "status": "ok",
  "uptime": 12.345,
  "timestamp": "2025-11-24T16:00:00.000000+00:00"
}
```

---

### Tasks

#### `GET /tasks`

Lista todas las tareas.

**Respuesta 200 OK**

```json
[
  {
    "id": 1,
    "title": "Estudiar REST",
    "done": false
  },
  {
    "id": 2,
    "title": "Hacer práctica",
    "done": true
  }
]
```

---

#### `POST /tasks`

Crea una nueva tarea.

**Body de ejemplo**

```json
{
  "title": "Repasar examen",
  "done": false
}
```

**Respuesta 201 Created**

```json
{
  "id": 3,
  "title": "Repasar examen",
  "done": false
}
```

---

#### `GET /tasks/{id}`

Obtiene una tarea por su `id`.

- **200 OK**: Tarea encontrada.
- **404 Not Found**:

  ```json
  {
    "error": "Not found"
  }
  ```

---

#### `PUT /tasks/{id}`

Actualiza **completamente** una tarea (reemplaza `title` y `done`).

**Body de ejemplo**

```json
{
  "title": "REST básico",
  "done": true
}
```

- **200 OK**: Tarea actualizada.
- **404 Not Found**: Si la tarea no existe.

---

#### `PATCH /tasks/{id}`

Actualiza **parcialmente** una tarea.  
Debe enviar **al menos uno** de estos campos:

- `title`
- `done`

**Body de ejemplo**

```json
{
  "done": false
}
```

- **200 OK**: Tarea actualizada.
- **404 Not Found**: Si la tarea no existe.

---

#### `DELETE /tasks/{id}`

Elimina una tarea.

- **204 No Content**: Eliminación exitosa (sin cuerpo).
- **404 Not Found**: Si la tarea no existe.

---

## Documentación interactiva

Con el servidor corriendo en `http://localhost:3000`:

- **Swagger UI** (documentación interactiva):  
  [http://localhost:3000/docs](http://localhost:3000/docs)

- **ReDoc**:  
  [http://localhost:3000/redoc](http://localhost:3000/redoc)

- **Esquema OpenAPI (JSON)**:  
  [http://localhost:3000/openapi.json](http://localhost:3000/openapi.json)

---

## Notas sobre el almacenamiento

- Las tareas se guardan en un **arreglo en memoria** (lista Python).
- Cuando el servidor se reinicia, la lista se **pierde** (no hay base de datos).
- El `id` de cada nueva tarea se calcula como `max(id existentes) + 1`.

---

## Ejemplos rápidos con `curl`

Crear una tarea:

```bash
curl -X POST "http://localhost:3000/tasks"   -H "Content-Type: application/json"   -d '{"title": "Repasar examen", "done": false}'
```

Listar tareas:

```bash
curl "http://localhost:3000/tasks"
```

Consultar una tarea:

```bash
curl "http://localhost:3000/tasks/1"
```

