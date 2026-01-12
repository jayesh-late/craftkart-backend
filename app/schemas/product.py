from pydantic import BaseModel

class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    customizable: str
