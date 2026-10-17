from fastapi import FastAPI, HTTPException

from app.data import orders
from app.models import Order

app = FastAPI()


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str) -> Order:
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
