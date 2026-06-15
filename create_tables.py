from database import Base, engine
from models import Category, Supplier, Product, Stock_movement

Base.metadata.create_all(engine)
print("Таблицы созданы!")