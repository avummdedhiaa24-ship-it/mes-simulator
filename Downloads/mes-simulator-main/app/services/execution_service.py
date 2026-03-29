from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.production import WorkOrder, SFC, SFCState
from datetime import datetime


def start_work_order(db: Session, wo_id: str):
    wo = db.query(WorkOrder).filter_by(wo_id=wo_id).first()

    if not wo:
        raise HTTPException(404, "Work order not found")
    if wo.status == "IN_PROGRESS":
        raise HTTPException(400, "Work order already started")

    wo.status = "IN_PROGRESS"
    wo.actual_start = datetime.utcnow()           # Bug #2 fix

    sfcs = db.query(SFC).filter_by(wo_id=wo_id).all()
    for sfc in sfcs:
        if sfc.state == SFCState.NEW:
            sfc.state = SFCState.IN_QUEUE

    db.commit()
    return {"wo_id": wo_id, "status": "STARTED", "sfcs_moved": len(sfcs)}


def complete_work_order(db: Session, wo_id: str):
    wo = db.query(WorkOrder).filter_by(wo_id=wo_id).first()

    if not wo:
        raise HTTPException(404, "Work order not found")
    if wo.status != "IN_PROGRESS":
        raise HTTPException(400, "Work order not in progress")

    wo.status = "COMPLETED"
    wo.actual_end = datetime.utcnow()             # Bug #2 fix

    sfcs = db.query(SFC).filter_by(wo_id=wo_id).all()
    completed = 0
    for sfc in sfcs:
        if sfc.state in [SFCState.IN_QUEUE, SFCState.ACTIVE]:
            sfc.state = SFCState.DONE
            completed += 1

    # Bug #5 fix — advance SFCs to the next operation
    next_wo = (
        db.query(WorkOrder)
        .filter(
            WorkOrder.order_id == wo.order_id,
            WorkOrder.operation_seq == wo.operation_seq + 1,
        )
        .first()
    )

    if next_wo:
        done_sfcs = db.query(SFC).filter_by(wo_id=wo_id).all()
        for sfc in done_sfcs:
            new_sfc = SFC(
                wo_id=next_wo.wo_id,
                serial_number=sfc.serial_number,
                state=SFCState.IN_QUEUE,
            )
            db.add(new_sfc)

    db.commit()
    return {
        "wo_id": wo_id,
        "completed_sfcs": completed,
        "advanced_to_next_op": next_wo.operation_name if next_wo else None,
    }
