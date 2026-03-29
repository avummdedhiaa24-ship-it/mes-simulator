from sqlalchemy.orm import Session
from app.models.production import WorkOrder, SFC
from app.models.order import Order
import uuid


OPERATIONS = [
    {"seq": 1, "name": "ASSEMBLY"},
    {"seq": 2, "name": "TESTING"},
    {"seq": 3, "name": "PACKAGING"}
]


OPERATIONS = [
    (1, "Assembly"),
    (2, "Testing"),
    (3, "Packaging"),
]


def create_work_orders_and_sfcs(db: Session, order: Order):
    work_orders = []

    for seq, name in OPERATIONS:
        wo = WorkOrder(
            order_id=order.order_id,
            operation_seq=seq,
            operation_name=name,
            machine_id=f"M-{seq}",
            operator_id=f"OP-{seq}",
        )
        db.add(wo)
        db.flush()
        work_orders.append(wo)

    # SFCs start at the first operation only
    for i in range(order.quantity):
        sfc = SFC(
            wo_id=work_orders[0].wo_id,
            serial_number=f"{order.erp_ref}-{i+1}",
        )
        db.add(sfc)

    db.commit()
    return work_orders
