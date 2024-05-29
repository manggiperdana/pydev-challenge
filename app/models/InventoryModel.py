from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    order_detail_id = Column(Integer, ForeignKey('order_details.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    qty_out = Column(Integer)
    amount_out = Column(Float)

    order = relationship('Order', back_populates='inventory')
    order_detail = relationship('OrderDetail', back_populates='inventory')
