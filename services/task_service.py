# services/task_service.py

from typing import List

from models.task_model import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskPatch,
)


class TaskNotFoundError(Exception):
    """
    Excepción específica para cuando una tarea no existe.
    La capa de routers la traducirá a un 404.
    """
    def __init__(self, task_id: int):
        super().__init__(f"Task with id={task_id} not found")
        self.task_id = task_id


class TaskService:
    """
    Servicio de dominio para gestionar tareas en memoria.
    El almacenamiento interno es un ARREGLO (lista) de tareas.
    """

    def __init__(self) -> None:
        # Almacenamiento en memoria: lista de Task
        self._tasks: List[Task] = []

    # ---------------------------------------------------------
    # Utilidad interna para buscar por id
    # ---------------------------------------------------------
    def _find_index_by_id(self, task_id: int) -> int:
        """
        Regresa el índice en la lista para el task_id dado
        o lanza TaskNotFoundError si no existe.
        """
        for idx, task in enumerate(self._tasks):
            if task.id == task_id:
                return idx
        raise TaskNotFoundError(task_id)

    # ---------------------------------------------------------
    # Métodos CRUD
    # ---------------------------------------------------------
    def list_tasks(self) -> List[Task]:
        """
        Devuelve todas las tareas.
        """
        # Devolvemos una copia para no exponer la lista interna directamente
        return list(self._tasks)

    def create_task(self, data: TaskCreate) -> Task:
        """
        Crea una nueva tarea.
        El id se genera en base al máximo id existente + 1.
        """
        if self._tasks:
            new_id = max(t.id for t in self._tasks) + 1
        else:
            new_id = 1

        task = Task(
            id=new_id,
            title=data.title,
            done=data.done,
        )
        self._tasks.append(task)
        return task

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Obtiene una tarea por id o lanza TaskNotFoundError.
        """
        idx = self._find_index_by_id(task_id)
        return self._tasks[idx]

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        """
        Actualiza completamente una tarea (operación tipo PUT).
        Ambos campos title y done deben venir en data.
        """
        idx = self._find_index_by_id(task_id)

        updated_task = Task(
            id=task_id,
            title=data.title,
            done=data.done,
        )
        self._tasks[idx] = updated_task
        return updated_task

    def patch_task(self, task_id: int, data: TaskPatch) -> Task:
        """
        Actualiza parcialmente una tarea (operación tipo PATCH).
        Solo se cambian los campos presentes en data.
        """
        idx = self._find_index_by_id(task_id)
        current = self._tasks[idx]

        # Pydantic v2: usamos model_dump para obtener un dict
        updated_values = current.model_dump()

        if data.title is not None:
            updated_values["title"] = data.title
        if data.done is not None:
            updated_values["done"] = data.done

        updated_task = Task(**updated_values)
        self._tasks[idx] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> None:
        """
        Elimina una tarea por id o lanza TaskNotFoundError.
        """
        idx = self._find_index_by_id(task_id)
        del self._tasks[idx]

    # ---------------------------------------------------------
    # Utilidad para pruebas
    # ---------------------------------------------------------
    def reset(self) -> None:
        """
        Limpia todas las tareas.
        Útil para pruebas.
        """
        self._tasks.clear()


# Instancia única del servicio a usar desde los routers
task_service = TaskService()

__all__ = [
    "TaskService",
    "task_service",
    "TaskNotFoundError",
]

