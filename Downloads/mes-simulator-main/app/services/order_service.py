from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.order import Order, AuditLog, OrderStatus
from app.schemas.order import OrderCreate
from app.services.production_service import create_work_orders_and_sfcs


# -------------------------
# AUDIT LOG FUNCTION
# -------------------------
def write_audit(db: Session, entity_id, action, old_val, new_val):
    log = AuditLog(
        entity_type="order",
        entity_id=entity_id,
        action=action,
        old_value=old_val,
        new_value=new_val,
        performed_by="system"
    )
    db.add(log)


# -------------------------
# CREATE ORDER (FR-01)
# -------------------------
def create_order(db: Session, payload: OrderCreate):
    order = Order(
        erp_ref=payload.erp_ref,
        product_code=payload.product_code,
        quantity=payload.quantity,
        planned_start=payload.planned_start,
        planned_end=payload.planned_end,
        status=OrderStatus.DRAFT
    )

    db.add(order)

    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Order with erp_ref '{payload.erp_ref}' already exists"
        )

    write_audit(
        db,
        order.order_id,
        "ORDER_CREATED",
        None,
        {
            "status": "DRAFT",
            "erp_ref": payload.erp_ref,
            "quantity": payload.quantity
        }
    )

    db.commit()
    db.refresh(order)
    return order


# -------------------------
# MATERIAL CHECK
# -------------------------
def simulate_material_check(product_code: str) -> bool:
    return not product_code.upper().endswith("X")


# -------------------------
# RELEASE ORDER (MES CORE)
# -------------------------
def release_order(db: Session, order_id: str):
    order = db.query(Order).filter(Order.order_id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatus.DRAFT:
        raise HTTPException(
            status_code=422,
            detail=f"Cannot release order in '{order.status}' state"
        )

    old_status = order.status.value

    material_ok = simulate_material_check(order.product_code)

    if material_ok:
        # 🔥 PRODUCTION START
        order.status = OrderStatus.RELEASED
        action = "ORDER_RELEASED"

        # 🔥 CREATE WORK ORDERS + SFCs
        create_work_orders_and_sfcs(db, order)

    else:
        order.status = OrderStatus.ON_HOLD
        action = "ORDER_ON_HOLD"

    write_audit(
        db,
        order.order_id,
        action,
        {"status": old_status},
        {
            "status": order.status.value,
            "material_check": material_ok
        }
    )

    db.commit()
    db.refresh(order)

    return order
