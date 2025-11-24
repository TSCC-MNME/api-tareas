# routers/health_router.py

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel, Field, ConfigDict


# Momento en que se inició el proceso (para calcular uptime)
START_TIME = datetime.now(timezone.utc)


class HealthResponse(BaseModel):
    """
    Respuesta del endpoint /health.

    Coincide con el esquema inline del OpenAPI:
      - status: string
      - uptime: number (float)
      - timestamp: string (date-time)
      - additionalProperties: false
    """
    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"] = Field(
        ...,
        example="ok",
        description="Estado del servicio",
    )
    uptime: float = Field(
        ...,
        description="Segundos desde que inició el proceso",
    )
    timestamp: datetime = Field(
        ...,
        description="Marca de tiempo del servidor (UTC)",
    )


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Verifica el estado del servicio",
    operation_id="getHealth",
)
async def get_health() -> HealthResponse:
    """
    Devuelve el estado del servicio, el uptime en segundos y la marca de tiempo actual.
    """
    now = datetime.now(timezone.utc)
    uptime_seconds = (now - START_TIME).total_seconds()

    return HealthResponse(
        status="ok",
        uptime=uptime_seconds,
        timestamp=now,
    )
