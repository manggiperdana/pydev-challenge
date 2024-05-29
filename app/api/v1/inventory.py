from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.InventoryService import InventoryService
from app.schemas import inventory as schemas
from app.api import deps
from app.core.utils import handle_exceptions

router = APIRouter()

@router.get("/", response_model=List[schemas.Inventory])
@handle_exceptions
async def read_inventory(limit: int = 10, page: int = 1, order_by: str = "id", order: str = "asc", orderId: Optional[int] = None, customerId: Optional[str] = None, db: Session = Depends(deps.get_db)):
    inventoryService = InventoryService(db=db)
    return inventoryService.get_inventories(limit=limit, page=page, order_by=order_by, order=order, orderId=orderId, customerId=customerId)

@router.get("/{product_id}", response_model=List[schemas.Inventory])
@handle_exceptions
async def read_inventory_by_product(product_id: Optional[str] = None, limit: int = 10, page: int = 1, order_by: str = "id", order: str = "asc", customerId: Optional[str] = None, db: Session = Depends(deps.get_db)):
    inventoryService = InventoryService(db=db)
    return inventoryService.get_inventories_by_product(product_id=product_id, limit=limit, page=page, order_by=order_by, order=order, customerId=customerId)
