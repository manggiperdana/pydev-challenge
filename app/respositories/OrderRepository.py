from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import OrderModel as models
from app.schemas import order as schemas
from datetime import datetime
from app.services.InventoryService import InventoryService
import random
import string

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_orders(self, q, limit, page, order_by, order):
        try:
            offset = (page - 1) * limit
            query = self.db.query(models.Order).filter(models.Order.deleted_at == None)
            if q:
                query = query.filter(
                    (models.Order.customer.like(f"%{q}%")) |
                    (models.Order.description.like(f"%{q}%")) |
                    (models.Order.document_no.like(f"%{q}%"))
                )
            if order == "desc":
                query = query.order_by(getattr(models.Order, order_by).desc())
            else:
                query = query.order_by(getattr(models.Order, order_by).asc())

            return query.offset(offset).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_order(self, productId, customerId, limit, page, order_by):
        try:
            offset = (page - 1) * limit
            query = self.db.query(models.Order).filter(models.Order.deleted_at == None).join(models.OrderDetail)

            if productId:
                query = query.filter(
                    or_(
                        models.Order.customer.like(f"%{customerId}%"),
                        models.OrderDetail.product.like(f"%{productId}%")
                    ),
                    models.Order.deleted_at == None
                )

            if order_by == "desc":
                query = query.order_by(getattr(models.Order, order_by).desc())
            else:
                query = query.order_by(getattr(models.Order, order_by).asc())

            return  query.offset(offset).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create_order_and_order_detail(self, order: schemas.OrderCreate):
        try:
            db_order = self.create_order(order=order)
            self.create_order_detail(db_order=db_order, order=order)
            return db_order
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def create_order(self, order: schemas.OrderCreate):
        try:
            subtotal, discount, after_discount, tax, after_tax = self.calculate_total_in_order(order=order).values()
            db_order = models.Order(
                document_no= self.document_number(),
                customer=order.customer,
                status=order.status,
                subtotal=subtotal,
                discount=discount,
                after_discount=after_discount,
                tax=tax,
                after_tax=after_tax
            )
            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)
            return db_order
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    def create_order_detail(self, db_order, order: schemas.OrderCreate):
        try:
            inventoryService = InventoryService(db=self.db)
            for detail in order.details:
                db_detail = models.OrderDetail(
                    order_id=db_order.id,
                    product=detail.product,
                    qty=detail.qty,
                    qty_sent=detail.qty_sent,
                    price=detail.price,
                    subtotal=detail.subtotal,
                    discount_per_item=detail.discount_per_item,
                    after_discount=detail.after_discount,
                    tax=detail.tax,
                    after_tax=detail.after_tax
                )
                self.db.add(db_detail)
                self.db.commit()
                if(detail.qty_sent >= 0):
                    inventoryService.process_inventory(order_id=db_order.id, order_detail_id=db_detail.id, qty_out=detail.qty_sent, amount_out=detail.qty_sent)
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    def update_order(self, order_id: int, order: schemas.OrderUpdate):
        try:
            db_order = self.db.query(models.Order).filter(models.Order.id == order_id, models.Order.deleted_at == None).first()
            subtotal, discount, after_discount, tax, after_tax = self.calculate_total_in_order(order=order).values()
            qty, qty_sent = self.calculate_sent_order_detail(order=order).values()
            if db_order :
                if db_order.status != 'Paid':
                    db_order.subtotal = subtotal
                    db_order.discount = discount
                    db_order.after_discount = after_discount
                    db_order.tax = tax
                    db_order.after_tax = after_tax
                    db_order.status = "Sent" if qty == qty_sent else "Pending"

                    self.delete_order_detail_by_order_id(order_id=order_id)
                    self.create_order_detail(db_order=db_order,order=order)
                    for key, value in order.model_dump(exclude_unset=True).items():
                        if key != "details":
                            setattr(db_order, key, value)
                    self.db.commit()
                    self.db.refresh(db_order)
                else:
                    db_order.description = order.description
                    self.db.commit()
                    self.db.refresh(db_order)
            return db_order
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    def mark_as_paid(self, order_id: int):
        try:
            db_order = self.db.query(models.Order).filter(models.Order.id == order_id, models.Order.deleted_at == None).first()
            if  db_order:
                    db_order.status = "Paid"
                    self.db.commit()
                    self.db.refresh(db_order)
            return db_order
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))    

    def delete_order(self, order_id: int):
        try:
            db_order = self.db.query(models.Order).filter(models.Order.id == order_id, models.Order.deleted_at == None ).first()
            if db_order:
                db_order.deleted_at = datetime.now()
                self.db.commit()
            return db_order
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))    
        
    def delete_order_detail_by_order_id(self, order_id: int):
        try:
            db_order_detail = self.db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).all()
            if db_order_detail:
                for order in db_order_detail:
                    self.db.delete(order)
                    self.delete_inventory(order_id=order_id, order_detail_id=order.id)
                self.db.commit()
            return db_order_detail
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500,detail=str(e))
        
    def delete_inventory(self, order_id: int, order_detail_id):
        try:
            inventoryService = InventoryService(db=self.db)
            inventoryService.delete_inventory(order_id=order_id, order_detail_id=order_detail_id)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500,detail=str(e))
        
    def document_number(self):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join(random.choice(letters_and_digits) for _ in range(10))
        return result_str
    
    def calculate_total_in_order(self, order:schemas.OrderCreate):
        result = {
            "subtotal" : sum(detail.subtotal for detail in order.details),
            "discount" : sum(detail.discount_per_item for detail in order.details),
            "after_discount" : sum(detail.after_discount for detail in order.details),
            "tax" : sum(detail.tax for detail in order.details),
            "after_tax" : sum(detail.after_tax for detail in order.details)
        }
        return result
    def calculate_sent_order_detail(self, order:schemas.OrderCreate):
        result = {
            "qty" : sum(detail.qty for detail in order.details),
            "qty_sent" : sum(detail.qty_sent for detail in order.details)
        }
        return result
        
