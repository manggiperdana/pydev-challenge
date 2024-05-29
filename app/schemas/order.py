from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class OrderDetailBase(BaseModel):
    product: str
    qty: int
    qty_sent: Optional[int] = 0
    price: float
    subtotal: float
    discount_per_item: float
    after_discount: float
    tax: float
    after_tax: float

    model_config = ConfigDict(from_attributes=True)

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetail(OrderDetailBase):
    id: int
    order_id: int

class OrderBase(BaseModel):
    # document_no: Optional[str] = ""
    customer: str
    status: Optional[str] = "Pending"
    subtotal: Optional[float] = 0.0
    discount: Optional[float] = 0.0
    after_discount: Optional[float] = 0.0
    tax: Optional[float] = 0.0
    after_tax: Optional[float] = 0.0
    last_modified_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    description: Optional[str] = ""

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderBase):
    details: List[OrderDetailCreate]

class OrderUpdate(OrderBase):
    details: List[OrderDetailCreate]

class Order(OrderBase):
    id: int
    document_no: str
    details: List[OrderDetail] = []

    model_config = ConfigDict(from_attributes=True)
