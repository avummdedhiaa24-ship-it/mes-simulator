from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.execution_service import start_work_order, complete_work_order

router = APIRouter(
    prefix="/api/execution",
    tags=["Execution"]
)


@router.post("/workorders/{wo_id}/start")
def start_work_order_api(wo_id: str, db: Session = Depends(get_db)):
    return start_work_order(db, wo_id)


@router.post("/workorders/{wo_id}/complete")
def complete_work_order_api(wo_id: str, db: Session = Depends(get_db)):
    return complete_work_order(db, wo_id)
