from database import Base, engine, SessionLocal
from models import Category, Supplier, Product, StockMovement

from decimal import Decimal

Base.metadata.create_all(engine)

with SessionLocal() as session:
    
    electronics = Category(name="Electronics")
    furniture = Category(name="Furniture")
    office = Category(name="Office Supplies")
    tools = Category(name="Tools")

    session.add_all([electronics, furniture, office, tools])

    session.commit()

    techtrade = Supplier(name="TechTrade")
    officemarket = Supplier(name="OfficeMarket")
    woodfactory = Supplier(name="WoodFactory")
    globaltools = Supplier(name="GlobalTools")

    session.add_all([techtrade, officemarket, woodfactory, globaltools])

    session.commit()

    laptop = Product(
        name="Laptop Lenovo ThinkPad",
        sku="LP001",
        category_id=electronics.id,
        supplier_id=techtrade.id,
        purchase_price=Decimal("700"),
        selling_price=Decimal("950"),
        min_quantity=Decimal("3")
    )

    mouse = Product(
        name="Wireless Mouse",
        sku="MS001",
        category_id=electronics.id,
        supplier_id=techtrade.id,
        purchase_price=Decimal("15"),
        selling_price=Decimal("30"),
        min_quantity=Decimal("10")
    )

    chair = Product(
        name="Office Chair",
        sku="CH001",
        category_id=furniture.id,
        supplier_id=woodfactory.id,
        purchase_price=Decimal("80"),
        selling_price=Decimal("140"),
        min_quantity=Decimal("5")
    )

    paper = Product(
        name="A4 Paper Pack",
        sku="PP001",
        category_id=office.id,
        supplier_id=officemarket.id,
        purchase_price=Decimal("3"),
        selling_price=Decimal("6"),
        min_quantity=Decimal("50")
    )

    screwdriver = Product(
        name="Screwdriver Set",
        sku="SD001",
        category_id=tools.id,
        supplier_id=globaltools.id,
        purchase_price=Decimal("20"),
        selling_price=Decimal("40"),
        min_quantity=Decimal("5")
    )

    monitor = Product(
        name="Monitor 27 inch",
        sku="MN001",
        category_id=electronics.id,
        supplier_id=techtrade.id,
        purchase_price=Decimal("180"),
        selling_price=Decimal("260"),
        min_quantity=Decimal("2")
    )

    session.add_all([laptop, mouse, chair, paper, screwdriver, monitor])

    session.commit()

    session.add_all([
        StockMovement(product_id=laptop.id, movement_type="IN", quantity=Decimal("10")),
        StockMovement(product_id=mouse.id, movement_type="IN", quantity=Decimal("30")),
        StockMovement(product_id=chair.id, movement_type="IN", quantity=Decimal("15")),
        StockMovement(product_id=paper.id, movement_type="IN", quantity=Decimal("200")),
        StockMovement(product_id=screwdriver.id, movement_type="IN", quantity=Decimal("25")),
        StockMovement(product_id=laptop.id, movement_type="OUT", quantity=Decimal("2")),
        StockMovement(product_id=mouse.id, movement_type="OUT", quantity=Decimal("5")),
        StockMovement(product_id=paper.id, movement_type="OUT", quantity=Decimal("80")),
        StockMovement(product_id=chair.id, movement_type="ADJUST", quantity=Decimal("1"))
    ])

    session.commit()

print("Seed-данные успешно добавлены.")