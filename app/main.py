from fastapi import FastAPI
from app.api.v1 import order, inventory

from app.db.session import engine
from app.db.base import Base
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(order.router, prefix=f"{settings.API_V1_STR}/order", tags=["order"])
app.include_router(inventory.router, prefix=f"{settings.API_V1_STR}/inventory", tags=["inventory"])
