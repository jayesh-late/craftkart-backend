from fastapi import FastAPI
from app.database import Base, engine
from app.routes import order
from dotenv import load_dotenv
load_dotenv()

from app.routes import product, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gift Kart Backend")

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)