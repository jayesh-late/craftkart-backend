from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    customizable = Column(String)
    seller_id = Column(Integer, ForeignKey("users.id"))
