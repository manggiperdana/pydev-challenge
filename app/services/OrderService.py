from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.OrderModel import Order
from app.schemas.order import OrderCreate, OrderUpdate
from app.respositories.OrderRepository import OrderRepository

class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repository = OrderRepository(self.db)

    def get_order(self, productId, customerId, limit, page, order_by) -> Optional[Order]:
        db_order = self.order_repository.get_order(productId=productId, customerId=customerId, limit=limit, page=page, order_by=order_by)
        if len(db_order) <= 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order
    
    def get_orders(self, q, limit, page, order_by, order) -> Optional[Order]:
        db_order = self.order_repository.get_orders(q=q, limit=limit, page=page, order_by=order_by, order=order)
        if len(db_order) <= 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order

    def create_order(self, order: OrderCreate) -> Order:
        return self.order_repository.create_order_and_order_detail(order=order)

    def update_order(self, order_id: int, order: OrderUpdate) -> Order:
        db_order = self.order_repository.update_order(order_id=order_id, order=order)
        if db_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order
    
    def mark_as_paid(self, order_id: int) -> Order:
        db_order = self.order_repository.mark_as_paid(order_id=order_id)
        if db_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order

    def delete_order(self, order_id: int):
        db_order = self.order_repository.delete_order(order_id=order_id)
        if db_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order
