# routers/task_router.py

from typing import List

from fastapi import APIRouter, HTTPException, Path, status, Response

from models.task_model import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskPatch,
    ErrorResponse,
)
from services.task_service import task_service, TaskNotFoundError

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


# ---------------------------------------------------------
# GET /tasks  - listTasks
# ---------------------------------------------------------
@router.get(
    "",
    response_model=List[Task],
    status_code=status.HTTP_200_OK,
    summary="Lista todas las tareas",
    operation_id="listTasks",
)
async def list_tasks() -> List[Task]:
    """
    Devuelve la lista completa de tareas.
    """
    return task_service.list_tasks()


# ---------------------------------------------------------
# POST /tasks  - createTask
# ---------------------------------------------------------
@router.post(
    "",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Crea una nueva tarea",
    operation_id="createTask",
    responses={
        400: {"model": ErrorResponse, "description": "Error de validación"},
    },
)
async def create_task(payload: TaskCreate) -> Task:
    """
    Crea una tarea nueva.
    Las validaciones de esquema las hace Pydantic (422 si el body es inválido).
    """
    task = task_service.create_task(payload)
    return task


# ---------------------------------------------------------
# GET /tasks/{id}  - getTaskById
# ---------------------------------------------------------
@router.get(
    "/{id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Obtiene una tarea por id",
    operation_id="getTaskById",
    responses={
        404: {"model": ErrorResponse, "description": "Tarea no encontrada"},
    },
)
async def get_task_by_id(
    id: int = Path(..., ge=1, description="Identificador de la tarea"),
) -> Task:
    """
    Devuelve una tarea por su ID.
    """
    try:
        return task_service.get_task_by_id(id)
    except TaskNotFoundError:
        # Cuerpo de error: {"error": "Not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Not found"},
        )


# ---------------------------------------------------------
# PUT /tasks/{id}  - updateTask
# ---------------------------------------------------------
@router.put(
    "/{id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Actualiza completamente una tarea",
    operation_id="updateTask",
    responses={
        400: {"model": ErrorResponse, "description": "Error de validación"},
        404: {"model": ErrorResponse, "description": "Tarea no encontrada"},
    },
)
async def update_task(
    payload: TaskUpdate,
    id: int = Path(..., ge=1, description="Identificador de la tarea"),
) -> Task:
    """
    Reemplaza completamente la tarea (PUT).
    """
    try:
        return task_service.update_task(id, payload)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Not found"},
        )


# ---------------------------------------------------------
# PATCH /tasks/{id}  - patchTask
# ---------------------------------------------------------
@router.patch(
    "/{id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Actualiza parcialmente una tarea",
    operation_id="patchTask",
    responses={
        400: {"model": ErrorResponse, "description": "Error de validación"},
        404: {"model": ErrorResponse, "description": "Tarea no encontrada"},
    },
)
async def patch_task(
    payload: TaskPatch,
    id: int = Path(..., ge=1, description="Identificador de la tarea"),
) -> Task:
    """
    Modifica parcialmente una tarea (PATCH).
    """
    try:
        return task_service.patch_task(id, payload)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Not found"},
        )


# ---------------------------------------------------------
# DELETE /tasks/{id}  - deleteTask
# ---------------------------------------------------------
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina una tarea",
    operation_id="deleteTask",
    responses={
        204: {"description": "Eliminación exitosa (sin contenido)"},
        404: {"model": ErrorResponse, "description": "Tarea no encontrada"},
    },
)
async def delete_task(
    id: int = Path(..., ge=1, description="Identificador de la tarea"),
) -> Response:
    """
    Elimina una tarea por su ID.
    """
    try:
        task_service.delete_task(id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Not found"},
        )

    # 204 -> sin cuerpo
    return Response(status_code=status.HTTP_204_NO_CONTENT)

