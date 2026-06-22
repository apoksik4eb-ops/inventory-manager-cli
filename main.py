from decimal import Decimal
from database import Base, engine
from crud import (
    create_category,
    create_supplier,
    create_product,
    create_stock_movement,
    get_all_categories,
    get_all_suppliers,
    get_all_products,
    get_product_by_id,
    get_product_by_category,
    get_product_by_supplier,
    get_all_stock_movement,
    get_stock_movement_by_product,
    update_category_name,
    update_supplier_contacts,
    update_product_prices,
    update_product_min_quantity,
    deactivate_product,
    deactivate_supplier,
    delete_category,
    delete_supplier,
    delete_product,
    delete_stock_movement
)