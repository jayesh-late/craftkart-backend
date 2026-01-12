from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.order import Order
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def place_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can place orders")

    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    order = Order(
        product_id=data.product_id,
        customer_id=current_user["user_id"]
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "message": "Order placed successfully",
        "order_id": order.id
    }
from app.models.product import Product

@router.get("/seller")
def get_seller_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Only sellers allowed
    if current_user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can view seller orders")

    # Join orders with products
    orders = (
        db.query(Order)
        .join(Product, Order.product_id == Product.id)
        .filter(Product.seller_id == current_user["user_id"])
        .all()
    )

    return orders

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can update order status")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product.seller_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not your order")

    allowed_status = ["accepted", "shipped", "delivered"]
    if data.status not in allowed_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    order.status = data.status
    db.commit()

    return {
        "message": "Order status updated",
        "order_id": order.id,
        "new_status": order.status
    }
