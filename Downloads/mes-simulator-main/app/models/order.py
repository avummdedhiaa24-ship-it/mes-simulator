from sqlalchemy import Column, String, Integer, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.database import Base
from datetime import datetime
import uuid
import enum


class OrderStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    RELEASED = "RELEASED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ON_HOLD = "ON_HOLD"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    erp_ref = Column(String(100), unique=True, nullable=False)
    product_code = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(SAEnum(OrderStatus),
                    default=OrderStatus.DRAFT, nullable=False)

    planned_start = Column(DateTime)
    planned_end = Column(DateTime)
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String(100), nullable=False)
    old_value = Column(JSONB)
    new_value = Column(JSONB)
    performed_by = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
