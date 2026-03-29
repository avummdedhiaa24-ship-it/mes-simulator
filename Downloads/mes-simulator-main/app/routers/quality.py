from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.quality_service import perform_quality_check

router = APIRouter(prefix="/api/quality", tags=["Quality"])


@router.post("/{sfc_id}")
def quality_check(
    sfc_id: str,
    value: float,
    lower: float,
    upper: float,
    db: Session = Depends(get_db)
):
    return perform_quality_check(db, sfc_id, value, lower, upper)
