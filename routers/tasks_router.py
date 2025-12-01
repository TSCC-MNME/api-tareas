from fastapi import APIRouter, HTTPException, status
from typing import List
from services.tasks_service import (
    service_list_tasks,
    service_get_task,
    service_create_task,
    service_update_task,
    service_patch_task,
    service_delete_task
)
from models.tasks_model import Task, TaskCreate, TaskUpdate, TaskPatch, Error

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[Task])
def list_tasks():
    return service_list_tasks()


@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED
)
def create_task(data: TaskCreate):
    return service_create_task(data)


@router.get(
    "/{id}",
    response_model=Task,
    responses={404: {"model": Error}}
)
def get_task_by_id(id: int):
    task = service_get_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Not found")
    return task


@router.put(
    "/{id}",
    response_model=Task,
    responses={404: {"model": Error}}
)
def update_task(id: int, data: TaskUpdate):
    task = service_update_task(id, data)
    if task is None:
        raise HTTPException(status_code=404, detail="Not found")
    return task


@router.patch(
    "/{id}",
    response_model=Task,
    responses={404: {"model": Error}}
)
def patch_task(id: int, data: TaskPatch):
    task = service_patch_task(id, data)
    if task is None:
        raise HTTPException(status_code=404, detail="Not found")
    return task


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": Error}}
)
def delete_task(id: int):
    ok = service_delete_task(id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return None
