# main.py
from fastapi import FastAPI
from routers.tasks_router import router as tasks_router
from routers.health_router import router as health_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API REST  - Tareas")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Permitir todos los encabezados
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(tasks_router)
app.include_router(health_router)

# Prueba de funcionamiento:
@app.get("/")
def root():
    return {"message": "API de tareas funcionando"}
