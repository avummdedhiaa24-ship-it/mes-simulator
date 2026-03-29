from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from datetime import datetime
import uuid
import enum


class SFCState(str, enum.Enum):
    NEW = "NEW"
    IN_QUEUE = "IN_QUEUE"
    ACTIVE = "ACTIVE"
    DONE = "DONE"
    IN_REWORK = "IN_REWORK"
    SCRAPPED = "SCRAPPED"


class WorkOrder(Base):
    __tablename__ = "work_orders"

    wo_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.order_id"))
    operation_seq = Column(Integer, nullable=False)
    operation_name = Column(String(100))          # e.g. "Assembly", "Testing"

    machine_id = Column(String(50))
    operator_id = Column(String(50))

    status = Column(String(20), default="PENDING")
    actual_start = Column(DateTime)               # set when WO starts
    actual_end = Column(DateTime)                 # set when WO completes
    created_at = Column(DateTime, default=datetime.utcnow)


class SFC(Base):
    __tablename__ = "sfcs"

    sfc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wo_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.wo_id"))

    serial_number = Column(String(100))
    state = Column(SAEnum(SFCState), default=SFCState.NEW)

    rework_count = Column(Integer, default=0)
    # persisted from quality check
    defect_code = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
