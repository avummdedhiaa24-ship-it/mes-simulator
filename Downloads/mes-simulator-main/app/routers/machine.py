from fastapi import APIRouter
from app.services.machine_service import simulate_machine_failure

router = APIRouter(prefix="/api/machine", tags=["Machine"])


@router.get("/status")
def machine_status():
    return simulate_machine_failure()
