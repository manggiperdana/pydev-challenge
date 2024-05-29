from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    document_no = Column(String, unique=True, index=True)
    customer = Column(String)
    description = Column(String)
    status = Column(String, default="Pending")
    subtotal = Column(Float)
    discount = Column(Float)
    after_discount = Column(Float)
    tax = Column(Float)
    after_tax = Column(Float)
    last_modified_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    details = relationship("OrderDetail", back_populates="order")
    inventory = relationship('Inventory', back_populates='order')

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product = Column(String)
    qty = Column(Integer)
    qty_sent = Column(Integer, default=0)
    price = Column(Float)
    subtotal = Column(Float)
    discount_per_item = Column(Float)
    after_discount = Column(Float)
    tax = Column(Float)
    after_tax = Column(Float)

    order = relationship("Order", back_populates="details")
    inventory = relationship('Inventory', back_populates='order_detail')
