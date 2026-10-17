from app.models import Order


orders: dict[str, Order] = {
    "ORD-1001": Order(
        order_id="ORD-1001",
        status="PENDING",
        reason="INVENTORY_NOT_AVAILABLE",
    ),
    "ORD-1002": Order(
        order_id="ORD-1002",
        status="SUBMITTED",
        reason=None,
    ),
    "ORD-1003": Order(
        order_id="ORD-1003",
        status="CANCELLED",
        reason="CUSTOMER_REQUEST",
    ),
}
