from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.InventoryModel import Inventory
from app.schemas.inventory import InventoryCreate
from app.respositories.InventoryRepository import InventoryRepository

class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_repository = InventoryRepository(db)

    def get_inventories(self, limit: int, page: int, order_by:str, order:str, orderId:int, customerId:str) -> List[Inventory] :
        return self.inventory_repository.get_inventories(limit=limit, page=page, order_by=order_by, order=order, orderId=orderId, customerId=customerId)
    
    def get_inventories_by_product(self, product_id: str, limit: int, page: int, order_by: str, order: str, customerId: str)-> List[Inventory]:
        return self.inventory_repository.get_inventory_by_product(product_id=product_id, limit=limit, page=page, order_by=order_by,order=order, customerId=customerId)

    def create_inventory(self, order_id: int, order_detail_id: int, qty_out: int, amount_out: int) -> Inventory:
        
        return self.inventory_repository.create_inventory(order_id=order_id, order_detail_id=order_detail_id,qty_out=qty_out,amount_out=amount_out)
    
    def find_inventory(self, order_id: int, order_detail_id: int) -> Inventory:
        return self.inventory_repository.find_inventory(order_id=order_id, order_detail_id=order_detail_id)

    def update_inventory(self, order_id: int, order_detail_id: int, qty_out: int, amount_out: int) -> Optional[Inventory]:
        return self.inventory_repository.update_inventory(order_id=order_id, order_detail_id=order_detail_id,qty_out=qty_out,amount_out=amount_out)
    
    def process_inventory(self, order_id: int, order_detail_id: int, qty_out: int, amount_out: int) -> Optional[Inventory]:
        inventory = self.find_inventory(order_id=order_id, order_detail_id=order_detail_id)
        if inventory:
            self.update_inventory(order_id=order_id, order_detail_id=order_detail_id,qty_out=qty_out,amount_out=amount_out)
        else:
            self.create_inventory(order_id=order_id, order_detail_id=order_detail_id,qty_out=qty_out,amount_out=amount_out)
    
    def delete_inventory(self, order_id: int, order_detail_id: int):
        return self.inventory_repository.delete_inventory(order_id=order_id, order_detail_id=order_detail_id)
