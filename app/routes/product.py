from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.utils.security import get_current_user
router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can create products")

    product = Product(
        **data.model_dump(),
        seller_id=current_user["user_id"]
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
