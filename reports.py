from sqlalchemy import select, func, case
from database import SessionLocal
from models import Category, Supplier, Product, StockMovement

from decimal import Decimal

def get_products_with_category_and_supplier():
    with SessionLocal() as session:
        stmt = (
            select(
                Product.id,
                Product.name.label("product_name"),
                Product.sku,
                Category.name.label("category_name"),
                Supplier.name.label("supplier_name"),
                Product.purchase_price,
                Product.selling_price,
                Product.is_active
            )
            .join(Category, Product.category_id == Category.id)
            .join(Supplier, Product.supplier_id == Supplier.id)
        )
        return session.execute(stmt).all()
    
def get_stock_movements_with_product():
    with SessionLocal() as session:
        stmt = (
            select(
                StockMovement.created_at,
                Product.name.label("product_name"),
                Product.sku,
                StockMovement.movement_type,
                StockMovement.quantity
            )
            .join(Product, StockMovement.product_id == Product.id)
        )
        return session.execute(stmt).all()
    
def get_products_count_by_category():
    with SessionLocal() as session:
        stmt = select(Category.name, func.count(Product.id)).join(Product, Product.category_id == Category.id).group_by(Category.name)
        return session.execute(stmt).all()

def get_products_count_by_supplier():
    with SessionLocal() as session:
        stmt = select(Supplier.name, func.count(Product.id)).join(Product, Product.supplier_id == Supplier.id).group_by(Supplier.name)
        return session.execute(stmt).all()
    
def get_current_stock_by_product(product_id: int):
    with SessionLocal() as session:
        stmt = select(func.sum(case(
            (StockMovement.movement_type == "IN", StockMovement.quantity),
            (StockMovement.movement_type == "ADJUST", StockMovement.quantity),
            (StockMovement.movement_type == "OUT", -StockMovement.quantity)
        ))).where(StockMovement.product_id == product_id)

        return session.scalar(stmt)

def get_low_stock_products():
    with SessionLocal() as session:
        products = session.scalars(select(Product)).all()

        low_stock = []

        for product in products:
            current_stock = get_current_stock_by_product(product.id)

            if product.min_quantity is not None and current_stock < product.min_quantity:
                low_stock.append(product)

        return low_stock
    
def get_total_purchase_value():
    with SessionLocal() as session:
        products = session.scalars(select(Product)).all()
        total_purchase = Decimal("0")

        for product in products:
            current_stock = get_current_stock_by_product(product.id)

            if product.purchase_price is not None:
                total_purchase += current_stock * product.purchase_price

        return total_purchase
    
def get_total_selling_value():
    with SessionLocal() as session:
        products = session.scalars(select(Product)).all()
        total_selling = Decimal("0")

        for product in products:
            current_stock = get_current_stock_by_product(product.id)

            if product.selling_price is not None:
                total_selling += current_stock * product.selling_price
        
        return total_selling
    
def get_potential_profit():
    with SessionLocal() as session:
        products = session.scalars(select(Product)).all()
        total_profit = Decimal("0")

        for product in products:
            current_stock = get_current_stock_by_product(product.id)

            if product.selling_price is not None and product.purchase_price is not None:
                total_profit += current_stock * (product.selling_price - product.purchase_price)
        
        return total_profit