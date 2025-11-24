# models/task_model.py

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, model_validator


class Task(BaseModel):
    """
    Representa una tarea completa tal como se expone en la API.
    Corresponde al schema 'Task' del OpenAPI.
    """
    # extra = "forbid"  -> additionalProperties: false en OpenAPI
    model_config = ConfigDict(extra="forbid")

    id: int = Field(..., example=3)
    title: str = Field(..., example="Repasar examen")
    done: bool = Field(..., example=False)


class TaskCreate(BaseModel):
    """
    Datos necesarios para crear una tarea.
    Corresponde al schema 'TaskCreate':
      - title es requerido
      - done es opcional, por defecto False
    """
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., example="Repasar examen")
    done: bool = Field(False, example=False, description="Estado inicial de la tarea")


class TaskUpdate(BaseModel):
    """
    Datos para actualización completa de una tarea.
    Corresponde al schema 'TaskUpdate':
      - title y done son ambos requeridos (PUT).
    """
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., example="REST básico")
    done: bool = Field(..., example=True)


class TaskPatch(BaseModel):
    """
    Datos para actualización parcial de una tarea.
    Corresponde al schema 'TaskPatch':
      - title y done son opcionales,
      - pero al menos uno de los dos debe estar presente (anyOf en OpenAPI).
    """
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = Field(None, example="Nuevo título")
    done: Optional[bool] = Field(None, example=False)

    @model_validator(mode="after")
    def at_least_one_field(self) -> "TaskPatch":
        """
        Garantiza que al menos uno de los campos (title, done) venga en el body.
        Equivale al anyOf del schema TaskPatch.
        """
        if self.title is None and self.done is None:
            raise ValueError(
                "Debe especificarse al menos uno de los campos: 'title' o 'done'."
            )
        return self


class ErrorResponse(BaseModel):
    """
    Formato estándar de error.
    Corresponde al schema 'Error' del OpenAPI.
    """
    model_config = ConfigDict(extra="forbid")

    error: str = Field(..., example="Not found")


__all__ = [
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskPatch",
    "ErrorResponse",
]

