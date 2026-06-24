from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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
    
def get_all_categories():
    with SessionLocal() as session:
        stmt = select(Category)
        categories = session.execute(stmt).scalars().all()
        return categories
    
def get_category_by_id(category_id: int):
    with SessionLocal() as session:
        category_by_id = session.get(Category, category_id)
        return category_by_id
    
def update_category_name(category_id: int, new_name: str):
    with SessionLocal() as session:
        category = session.get(Category, category_id)

        if category is None:
            return None
        
        category.name = new_name

        session.commit()
        session.refresh(category)
        return category

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
        
def get_all_suppliers():
    with SessionLocal() as session:
        stmt = select(Supplier)
        suppliers = session.execute(stmt).scalars().all()
        return suppliers

def get_supplier_by_id(supplier_id: int):
    with SessionLocal() as session:
        supplier_by_id = session.get(Supplier, supplier_id)
        return supplier_by_id
    
def update_supplier_contacts(supplier_id: int, new_phone: str | None, new_email: str | None):
    with SessionLocal() as session:
        supplier = session.get(Supplier, supplier_id)

        if supplier is None:
            return None
        
        if new_phone is not None:
            supplier.phone = new_phone
        if new_email is not None:
            supplier.email = new_email

        session.commit()
        session.refresh(supplier)
        return supplier

def deactivate_supplier(supplier_id: int):
    with SessionLocal() as session:
        supplier = session.get(Supplier, supplier_id)

        if supplier is None:
            return None
        
        supplier.is_active = False

        session.commit()
        session.refresh(supplier)
        return supplier
    
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

def create_product(
        name: str,
        sku: str,
        category_id: int | None = None,
        supplier_id: int | None = None,
        purchase_price: Decimal | None = None,
        selling_price: Decimal | None = None,
        min_quantity: Decimal | None = None
):
    if purchase_price is not None and purchase_price < 0:
        return "Закупочная цена не может быть отрицательной."

    if selling_price is not None and selling_price < 0:
        return "Продажная цена не может быть отрицательной."

    if min_quantity is not None and min_quantity < 0:
        return "Минимальный остаток не может быть отрицательным."
    
    with SessionLocal() as session:

        if category_id is not None:
            category = session.get(Category, category_id)

            if category is None:
                return "Категория не найдена."

        if supplier_id is not None:
            supplier = session.get(Supplier, supplier_id)

            if supplier is None:
                return "Поставщик не найден."
            
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
            return "Невозможно создать 2 товара с одинаковым уникальным артикулом."

def get_all_products():
    with SessionLocal() as session:
        stmt = select(Product)
        products = session.execute(stmt).scalars().all()
        return products
    
def get_product_by_id(product_id: int):
    with SessionLocal() as session:
        product_by_id = session.get(Product, product_id)
        return product_by_id
    
def get_products_by_category(category_id: int):
    with SessionLocal() as session:
        stmt = select(Product).where(Product.category_id == category_id)
        products = session.execute(stmt).scalars().all()
        return products
    
def get_products_by_supplier(supplier_id: int):
    with SessionLocal() as session:
        stmt = select(Product).where(Product.supplier_id == supplier_id)
        products = session.execute(stmt).scalars().all()
        return products
        
def update_product_prices(product_id: int, new_purchase_price: Decimal | None, new_selling_price: Decimal | None):
    
    if new_purchase_price is not None and new_purchase_price < 0:
        return "Закупочная цена не может быть отрицательной."

    if new_selling_price is not None and new_selling_price < 0:
        return "Продажная цена не может быть отрицательной."
    
    with SessionLocal() as session:
        product = session.get(Product, product_id)

        if product is None:
            return None
        
        if new_purchase_price is not None:
            product.purchase_price = new_purchase_price

        if new_selling_price is not None:    
            product.selling_price = new_selling_price

        session.commit()
        session.refresh(product)
        return product
    
def update_product_min_quantity(product_id: int, new_min_quantity: Decimal):
    with SessionLocal() as session:
        product = session.get(Product, product_id)

        if product is None:
            return None
        
        if new_min_quantity < 0:
            return "Минимальный остаток не может быть отрицательным."
        
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
    
def create_stock_movement(
        product_id: int,
        movement_type: str,
        quantity: Decimal       
):
    if quantity <= 0:
        return "Количество должно быть больше нуля."
    
    with SessionLocal() as session:
        product = session.get(Product, product_id)

        if product is None:
            return "Товар не найден."
        
        stock_movement = StockMovement(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity
        )

        try:
            session.add(stock_movement)
            session.commit()
            session.refresh(stock_movement)
            return stock_movement
        
        except IntegrityError:
            session.rollback()
            return "Не удалось создать складскую операцию."
   
def get_all_stock_movements():
    with SessionLocal() as session:
        stmt = select(StockMovement)
        stock_movement = session.execute(stmt).scalars().all()
        return stock_movement
    
def get_stock_movements_by_product(product_id: int):
    with SessionLocal() as session:
        stmt = select(StockMovement).where(StockMovement.product_id == product_id)
        stock_movement = session.execute(stmt).scalars().all()
        return stock_movement

def delete_stock_movement(stock_movement_id: int):
    with SessionLocal() as session:
        stock_movement = session.get(StockMovement, stock_movement_id)

        if stock_movement is None:
            return False
        
        session.delete(stock_movement)
        session.commit()

        return True