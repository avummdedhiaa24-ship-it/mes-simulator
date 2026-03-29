from sqlalchemy.orm import Session
from app.models.production import SFC, SFCState


def get_dashboard_metrics(db: Session):
    total = db.query(SFC).count()

    done = db.query(SFC).filter(SFC.state == SFCState.DONE).count()
    rework = db.query(SFC).filter(SFC.state == SFCState.IN_REWORK).count()
    scrap = db.query(SFC).filter(SFC.state == SFCState.SCRAPPED).count()
    active = db.query(SFC).filter(SFC.state == SFCState.ACTIVE).count()

    yield_rate = (done / total * 100) if total else 0
    scrap_rate = (scrap / total * 100) if total else 0

    return {
        "total_units": total,
        "completed": done,
        "in_progress": active,
        "rework": rework,
        "scrap": scrap,
        "yield_percent": round(yield_rate, 2),
        "scrap_percent": round(scrap_rate, 2)
    }
