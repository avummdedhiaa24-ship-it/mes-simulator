from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order, release_order
from app.models.order import Order

router = APIRouter(prefix="/api/orders", tags=["Orders"])


# -------------------------
# CREATE ORDER
# -------------------------
@router.post("/", response_model=OrderResponse, status_code=201)
def create_new_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, payload)


# -------------------------
# GET ORDER STATUS
# -------------------------
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# -------------------------
# RELEASE ORDER
# -------------------------
@router.post("/{order_id}/release", response_model=OrderResponse)
def release_order_endpoint(order_id: str, db: Session = Depends(get_db)):
    return release_order(db, order_id)
