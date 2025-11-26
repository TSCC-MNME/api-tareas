from fastapi import APIRouter
import time
from datetime import datetime

router = APIRouter(tags=["Health"])

_start_time = time.time()


@router.get("/health")
def get_health():
    return {
        "status": "ok",
        "uptime": time.time() - _start_time,
        "timestamp": datetime.utcnow().isoformat()
    }


