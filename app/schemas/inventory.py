from pydantic import BaseModel, ConfigDict
from app.schemas.order import OrderBase, OrderDetailBase
    
class InventoryBase(BaseModel):
    order_detail_id: int
    order_id: int
    qty_out: int
    amount_out: float

    model_config = ConfigDict(from_attributes=True)

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    order: OrderBase
    order_detail: OrderDetailBase
    model_config = ConfigDict(from_attributes=True)
