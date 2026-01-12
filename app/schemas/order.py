from pydantic import BaseModel

class OrderCreate(BaseModel):
    product_id: int

class OrderStatusUpdate(BaseModel):
    status: str  # accepted | shipped | delivered


