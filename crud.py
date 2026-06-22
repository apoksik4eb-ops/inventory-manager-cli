from sqlalchemy import select, update, delete, IntegrityError
from database import SessionLocal
from models import Category, Supplier, Product, StockMovement

from decimal import Decimal
from typing import Optional

def create_category(name:str):
    with SessionLocal() as session:
        category = Category(name=name)

        try:
            session.add(category)
            session.commit()
            session.refresh(category)
            return category
        
        except IntegrityError:
            session.rollback()
            return "Невозможно создать 2 категории с одинаковым названием."


def create_supplier(
    name: str,
    phone: Optional[str] = None,
    email: Optional[str] = None    
):
    with SessionLocal() as session:
        supplier = Supplier(
            name=name,
            phone=phone,
            email=email
        )

        try:
            session.add(supplier)
            session.commit()
            session.refresh(supplier)
            return supplier
        
        except IntegrityError:
            session.rollback()
            return "Невозможно создать 2 поставщиков с одинаковым названием."

def create_product(
        name: str,
        sku: str,
        category_id: int | None = None,
        supplier_id: int | None = None,
        purchase_price: Decimal | None = None,
        selling_price: Decimal | None = None,
        min_quantity: Decimal | None = None
):
    with SessionLocal() as session:
        product = Product(
            name=name,
            sku=sku,
            category_id=category_id,
            supplier_id=supplier_id,
            purchase_price=purchase_price,
            selling_price=selling_price,
            min_quantity=min_quantity
        )

        try:
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
        
        except IntegrityError:
            session.rollback()
            return "Невозможно создать 2 одинаковых товара с одинаковой единицей складского учета"
    
def create_stock_movement(
        product_id: int,
        movement_type: str,
        quantity: Decimal       
):
    with SessionLocal() as session:
        stock_movement = StockMovement(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity
        )

        session.add(stock_movement)
        session.commit()
        session.refresh(stock_movement)

        return stock_movement
    
def get_all_categories():
    with SessionLocal() as session:
        stmt = select(Category)
        categories = session.execute(stmt).scalars().all()
        return categories
    
def get_all_suppliers():
    with SessionLocal() as session:
        stmt = select(Supplier)
        suppliers = session.execute(stmt).scalars().all()
        return suppliers
    
def get_all_products():
    with SessionLocal() as session:
        stmt = select(Product)
        products = session.execute(stmt).scalars().all()
        return products
    
def get_product_by_id(product_id: int):
    with SessionLocal() as session:
        product_by_id = session.get(Product, product_id)
        return product_by_id
    
def get_product_by_category(category_name: str):
    with SessionLocal() as session:
        stmt = select(Product).where(Product.category == category_name)
        products = session.execute(stmt).scalars().all()
        return products
    
def get_product_by_supplier(supplier_name: str):
    with SessionLocal() as session:
        stmt = select(Product).where(Product.supplier == supplier_name)
        products = session.execute(stmt).scalars().all()
        return products
    
def get_all_stock_movement():
    with SessionLocal() as session:
        stmt = select(StockMovement)
        stock_movement = session.execute(stmt).scalars().all()
        return stock_movement
    
def get_stock_movement_by_product(stock_movement: str):
    with SessionLocal() as session:
        stmt = select(StockMovement).where(StockMovement.product == stock_movement)
        stock_movement = session.execute(stmt).scalars().all()
        return stock_movement
    
def update_category_name(category_id: int, new_name: str):
    with SessionLocal() as session:
        category = session.get(Category, category_id)

        if category is None:
            return None
        
        category.name = new_name

        session.commit()
        session.refresh(category)
        return category
    
def update_supplier_contacts(supplier_id: int, new_phone: str, new_email: str):
    with SessionLocal() as session:
        supplier = session.get(Supplier, supplier_id)

        if supplier is None:
            return None
        
        supplier.phone = new_phone
        supplier.email = new_email

        session.commit()
        session.refresh(supplier)
        return supplier

def update_product_prices(product_id: int, new_purchase_prices: Decimal, new_selling_prices: Decimal):
    with SessionLocal() as session:
        with SessionLocal() as session:
            product = session.get(Product, product_id)

        if product is None:
            return None
        
        product.purchase_prices = new_purchase_prices
        product.selling_prices = new_selling_prices

        session.commit()
        session.refresh(product)
        return product
    
def update_product_min_quantity(product_id: int, new_min_quantity: Decimal):
    with SessionLocal() as session:
        product = session.get(Product, product_id)

        if product is None:
            return None
        
        product.min_quantity = new_min_quantity

        session.commit()
        session.refresh(product)
        return product

def deactivate_product(product_id: int):
    with SessionLocal() as session:
        product = session.get(Product, product_id)

        if product is None:
            return None
        
        product.is_active = False

        session.commit()
        session.refresh(product)
        return product
    
def deactivate_supplier(supplier_id: int):
    with SessionLocal() as session:
        supplier = session.get(Supplier, supplier_id)

        if supplier is None:
            return None
        
        supplier.is_active = False

        session.commit()
        session.refresh(supplier)
        return supplier
    
def delete_category(category_id: int):
    with SessionLocal() as session:
        category = session.get(Category, category_id)

        if category is None:
            return False
        
        try:
            session.delete(category)
            session.commit()
            return True
        
        except IntegrityError:
            session.rollback()
            return "Нельзя удалить категорию, у которой есть товары."
    
def delete_supplier(supplier_id: int):
    with SessionLocal() as session:
        supplier = session.get(Supplier, supplier_id)

        if supplier is None:
            return False
        
        try:
            session.delete(supplier)
            session.commit()
            return True
        
        except IntegrityError:
            session.rollback()
            return "Нельзя удалить поставщика, у которого есть товары."
    
def delete_product(product_id: int):
    with SessionLocal() as session:
        product = session.get(Product, product_id)

        if product is None:
            return False
        
        try:
            session.delete(product)
            session.commit()
            return True
        
        except IntegrityError:
            session.rollback()
            return "Нельзя удалить товар, у которого есть складские операции."
    
def delete_stock_movement(stock_movement_id: int):
    with SessionLocal() as session:
        stock_movement = session.get(StockMovement, stock_movement_id)

        if stock_movement is None:
            return False
        
        session.delete(stock_movement)
        session.commit()

        return True