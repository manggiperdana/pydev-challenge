from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import order as schemas
from app.api import deps
from app.services.OrderService import OrderService
from app.core.utils import handle_exceptions

router = APIRouter()

@router.get("/", response_model=List[schemas.Order])
@handle_exceptions
async def read_orders(q: Optional[str] = None, limit: int = 10, page: int = 1, order_by: str = "id", order: str = "asc", db: Session = Depends(deps.get_db)):
    orderService = OrderService(db=db)
    return orderService.get_orders(q=q, limit=limit, page=page, order_by=order_by, order=order)

@router.post("/{order_id}/mark-as-paid", response_model=schemas.Order)
@handle_exceptions
async def mark_as_paid_order(order_id: int, db: Session = Depends(deps.get_db)):
    orderService = OrderService(db=db)
    return orderService.mark_as_paid(order_id=order_id)
    
@router.get("/details", response_model=List[schemas.Order])
@handle_exceptions
async def read_order_details(productId: Optional[str] = None, customerId: Optional[str] = None, limit: int = 10, page: int = 1, order_by: str = "id", order: str = "asc", db: Session = Depends(deps.get_db)):
    orderService = OrderService(db=db)
    return orderService.get_order(productId=productId, customerId=customerId, limit=limit, page=page, order_by=order_by)
    

@router.post("/", response_model=schemas.Order)
@handle_exceptions
async def create_order(order: schemas.OrderCreate, db: Session = Depends(deps.get_db)):
    orderService = OrderService(db=db)
    return orderService.create_order(order=order)

@router.put("/{order_id}", response_model=schemas.Order)
@handle_exceptions
async def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(deps.get_db)):
    orderService = OrderService(db=db)
    return orderService.update_order(order_id=order_id, order=order)

@router.delete("/{order_id}", response_model=schemas.Order)
@handle_exceptions
async def delete_order(order_id: int, db: Session = Depends(deps.get_db)):
    orderService = OrderService(db=db)
    return orderService.delete_order(order_id=order_id)
