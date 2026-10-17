from pydantic import BaseModel


class Order(BaseModel):
    order_id: str
    status: str
    reason: str | None = None