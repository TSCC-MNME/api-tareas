# services/tasks_service.py

from typing import List, Optional
from models.tasks_model import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskPatch,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    patch_task,
    delete_task,
)


# ---------------------------------------------------------
# Servicios de alto nivel para tareas
# ---------------------------------------------------------

def service_list_tasks() -> List[Task]:
    return get_all_tasks()


def service_get_task(task_id: int) -> Optional[Task]:
    return get_task_by_id(task_id)


def service_create_task(data: TaskCreate) -> Task:
    return create_task(data)


def service_update_task(task_id: int, data: TaskUpdate) -> Optional[Task]:
    return update_task(task_id, data)


def service_patch_task(task_id: int, data: TaskPatch) -> Optional[Task]:
    return patch_task(task_id, data)


def service_delete_task(task_id: int) -> bool:
    return delete_task(task_id)

if __name__ == "__main__":
    print("== Prueba de capa de servicios ==")

    # Crear tareas
    print("\n== Crear tareas ==")
    t1 = service_create_task(TaskCreate(title="Leer documentación"))
    t2 = service_create_task(TaskCreate(title="Escribir API", done=True))
    print(service_list_tasks())

    # Obtener por ID
    print("\n== Obtener tarea por ID ==")
    print(service_get_task(t1.id))

    # Actualización completa (PUT)
    print("\n== Actualización completa (PUT) ==")
    service_update_task(t1.id, TaskUpdate(title="Leer documentación FastAPI", done=True))
    print(service_get_task(t1.id))

    # Actualización parcial (PATCH)
    print("\n== Actualización parcial (PATCH) ==")
    service_patch_task(t2.id, TaskPatch(done=False))
    print(service_get_task(t2.id))

    # Eliminar
    print("\n== Eliminar tarea ==")
    service_delete_task(t1.id)
    print(service_list_tasks())

