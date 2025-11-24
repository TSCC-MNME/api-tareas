# main.py

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from routers.task_router import router as tasks_router
from routers.health_router import router as health_router  # asumiendo que ya lo tendrás


app = FastAPI(
    title="API REST Básica de Tareas",
    version="1.0.0",
    description=(
        "API mínima para operaciones CRUD sobre el recurso 'tasks'.\n"
        "Incluye endpoint de salud y almacenamiento en memoria."
    ),
    openapi_tags=[
        {
            "name": "Health",
            "description": "Estado del servicio",
        },
        {
            "name": "Tasks",
            "description": "Gestión de tareas",
        },
    ],
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Permitir todos los encabezados
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Incluir routers
app.include_router(health_router)
app.include_router(tasks_router)


# Opcional: endpoint raíz solo informativo
@app.get("/", tags=["Health"])
async def root():
    return {"message": "API REST Básica de Tareas"}


# Personalizar el esquema OpenAPI para agregar 'servers'
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["servers"] = [
        {
            "url": "http://localhost:3000",
            "description": "Servidor local de desarrollo",
        }
    ]

    app.openapi_schema = openapi_schema
    return openapi_schema


app.openapi = custom_openapi



