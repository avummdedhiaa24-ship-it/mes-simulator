from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.order import OrderStatus


class OrderCreate(BaseModel):
    erp_ref: str = Field(..., min_length=1)
    product_code: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None


class OrderResponse(BaseModel):
    order_id: UUID
    erp_ref: str
    product_code: str
    quantity: int
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True
