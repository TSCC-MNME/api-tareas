# Almacenamiento en memoria para tareas

from typing import List, Optional
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Modelos de datos (equivalentes a schemas)
# ---------------------------------------------------------

class Task(BaseModel):
    id: int
    title: str
    done: bool = Field(default=False)


class TaskCreate(BaseModel):
    title: str
    done: bool = Field(default=False)


class TaskUpdate(BaseModel):
    title: str
    done: bool


class TaskPatch(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

class Error(BaseModel):
    error: str

    class Config:
        extra = "forbid"


# ---------------------------------------------------------
# Almacenamiento en memoria (no persistente)
# ---------------------------------------------------------

tasks: List[Task] = []
current_id: int = 0


# ---------------------------------------------------------
# Funciones CRUD para manejar el arreglo
# ---------------------------------------------------------

def get_all_tasks() -> List[Task]:
    return tasks


def get_task_by_id(task_id: int) -> Optional[Task]:
    return next((t for t in tasks if t.id == task_id), None)


def create_task(data: TaskCreate) -> Task:
    global current_id
    current_id += 1

    new_task = Task(
        id=current_id,
        title=data.title,
        done=data.done,
    )
    tasks.append(new_task)
    return new_task


def update_task(task_id: int, data: TaskUpdate) -> Optional[Task]:
    task = get_task_by_id(task_id)
    if task is None:
        return None

    task.title = data.title
    task.done = data.done
    return task


def patch_task(task_id: int, data: TaskPatch) -> Optional[Task]:
    task = get_task_by_id(task_id)
    if task is None:
        return None

    if data.title is not None:
        task.title = data.title
    if data.done is not None:
        task.done = data.done

    return task


def delete_task(task_id: int) -> bool:
    global tasks
    task = get_task_by_id(task_id)
    if task is None:
        return False

    tasks = [t for t in tasks if t.id != task_id]
    return True

if __name__ == "__main__":
    # Pruebas básicas del módulo arreglo.py

    print("== Crear tareas ==")
    t1 = create_task(TaskCreate(title="Aprender FastAPI"))
    t2 = create_task(TaskCreate(title="Preparar presentación", done=True))
    print(get_all_tasks())

    print("\n== Obtener tarea por ID ==")
    print(get_task_by_id(t1.id))

    print("\n== Actualización completa (PUT) ==")
    update_task(t1.id, TaskUpdate(title="Aprender FastAPI a fondo", done=True))
    print(get_task_by_id(t1.id))

    print("\n== Actualización parcial (PATCH) ==")
    patch_task(t2.id, TaskPatch(done=False))
    print(get_task_by_id(t2.id))

    print("\n== Eliminar tarea ==")
    delete_task(t1.id)
    print(get_all_tasks())
