from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.production import SFC, SFCState
import random


def perform_quality_check(db: Session, sfc_id: str, value: float, lower: float, upper: float):
    sfc = db.query(SFC).filter_by(sfc_id=sfc_id).first()

    if not sfc:
        raise HTTPException(404, "SFC not found")

    noise = random.uniform(-1, 1)
    adjusted_value = value + noise

    if lower <= adjusted_value <= upper:
        sfc.state = SFCState.DONE
        sfc.defect_code = None                    # Bug #6 fix — clear on pass
        result = "PASS"
        defect = None
    else:
        defect = "DIMENSION_FAIL"
        sfc.defect_code = defect                  # Bug #6 fix — persist to DB

        if sfc.rework_count < 1:
            sfc.state = SFCState.IN_REWORK
            sfc.rework_count += 1
            result = "REWORK"
        else:
            sfc.state = SFCState.SCRAPPED
            result = "SCRAP"

    db.commit()
    return {
        "sfc_id": str(sfc.sfc_id),
        "measured_value": round(adjusted_value, 2),
        "result": result,
        "defect": defect,
        "state": sfc.state,
    }
