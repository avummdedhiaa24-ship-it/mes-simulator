from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.production import SFC, SFCState


def get_production_insights(db: Session):
    total = db.query(SFC).count()

    rows = (
        db.query(SFC.state, func.count(SFC.sfc_id))
        .group_by(SFC.state)
        .all()
    )

    states = {state.value: 0 for state in SFCState}
    for state, count in rows:
        states[state.value] = count

    bottleneck = max(states, key=states.get) if total else None

    return {
        "total_units": total,
        "state_distribution": states,
        "bottleneck_stage": bottleneck,
    }
