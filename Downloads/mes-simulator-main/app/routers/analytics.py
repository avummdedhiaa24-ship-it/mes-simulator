from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.analytics_service import get_production_insights

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/")
def analytics(db: Session = Depends(get_db)):
    return get_production_insights(db)
