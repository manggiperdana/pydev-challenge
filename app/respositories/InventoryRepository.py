from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import InventoryModel as inventoryModels, OrderModel as orderModel

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_inventories(self, limit:int, page:int, order_by:str, order:str, orderId:int, customerId:str):
        try:
            offset = (page - 1) * limit
            query = self.db.query(inventoryModels.Inventory).join(orderModel.Order)
            if customerId:
                query = query.filter(orderModel.Order.customer.ilike(f"%{customerId}%"))
            if orderId:
                query = query.filter(orderModel.Order.id == orderId)
            if order == "desc":
                query = query.order_by(getattr(inventoryModels.Inventory, order_by).desc())
            else:
                query = query.order_by(getattr(inventoryModels.Inventory, order_by).asc())

            return query.offset(offset).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_inventory_by_product(self, product_id: str, limit: int, page: int, order_by: str, order: str, customerId: str):
        try:
            offset = (page - 1) * limit
            query = self.db.query(inventoryModels.Inventory).join(orderModel.OrderDetail).join(orderModel.Order)
            if customerId:
                query = query.filter(orderModel.Order.customer.ilike(f"%{customerId}%"))
            if product_id:
                query = query.filter(orderModel.OrderDetail.product.ilike(f"%{product_id}%"))
            if order == "desc":
                query = query.order_by(getattr(inventoryModels.Inventory, order_by).desc())
            else:
                query = query.order_by(getattr(inventoryModels.Inventory, order_by).asc())

            return query.offset(offset).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def find_inventory(self, order_id: int, order_detail_id: int):
        try:
            return self.db.query(inventoryModels.Inventory).filter(inventoryModels.Inventory.order_id == order_id, inventoryModels.Inventory.order_detail_id == order_detail_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def create_inventory(self, order_id: int, order_detail_id: int, qty_out: int, amount_out: int):
        try:
            inventory = inventoryModels.Inventory(
                order_detail_id= order_detail_id,
                order_id= order_id,
                qty_out = qty_out,
                amount_out = amount_out
            )
            self.db.add(inventory)
            self.db.commit()
            return inventory
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_inventory(self, order_id: int, order_detail_id: int, qty_out: int, amount_out: int):
        try:
            inventory = self.find_inventory(order_id=order_id, order_detail_id=order_detail_id)
            inventory.qty_out = qty_out
            inventory.amount_out = amount_out
            self.db.commit()
            self.db.refresh(inventory)
            return inventory
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_inventory(self, order_id: int, order_detail_id: int):
        try:
            inventory = self.find_inventory(order_id=order_id,order_detail_id=order_detail_id)
            self.db.delete(inventory)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
