from sqlalchemy import select, update, delete, func
from database import SessionLocal
from models import Category, Supplier, Product, StockMovement

from decimal import Decimal
from typing import Optional

def create_category(name:str):
    with SessionLocal() as session:
        category = Category(name=name)

        session.add(category)
        session.commit()
        session.refresh(category)

        return category

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

        session.add(supplier)
        session.commit()
        session.refresh(supplier)

        return supplier

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

        session.add(product)
        session.commit()
        session.refresh(product)

        return product
    
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
    
def delete_supplier(supplier_id: int):
    with SessionLocal() as session:
        supplier = session.get(Supplier, supplier_id)

        if supplier is None:
            return False
        
        session.delete(supplier)
        session.commit()

        return True
    
# def get_employees_with_salary_gt(amount: Decimal):
#     with SessionLocal() as session:
#         stmt = select(Employee).where(Employee.salary > amount)
#         return session.execute(stmt).scalars().all()
    
# def get_employees_order_by_salary_desc():
#     with SessionLocal() as session:
#         stmt = select(Employee).order_by(Employee.salary.desc())
#         return session.execute(stmt).scalars().all()
    
# def get_employees_page(page: int, per_page: int):
#     with SessionLocal() as session:
#         stmt = select(Employee).offset((page - 1) * per_page).limit(per_page)
#         return session.execute(stmt).scalars().all()
    
# def update_employee_salary(employee_id: int, salary: int):
#     with SessionLocal() as session:
#         employee = session.get(Employee, employee_id)

#         if employee is None:
#             return None
        
#         employee.salary = salary

#         session.commit()
#         session.refresh(employee)
#         return employee

# def update_employee_salary_via_update(employee_id: int, salary: int):
#     with SessionLocal() as session:
#         stmt = update(Employee).where(Employee.id == employee_id).values(salary=salary)

#         session.execute(stmt)
#         session.commit()
    
# def delete_project_via_delete(project_id: int):
#     with SessionLocal() as session:
#         stmt = delete(Project).where(Project.id == project_id)

#         session.execute(stmt)
#         session.commit()

# def get_employees_with_department_names():
#     with SessionLocal() as session:
#         stmt = select(Employee.name, Department.name).join(Department, Employee.department_id == Department.id)
#         return session.execute(stmt).all()
    
# def get_employees_with_optional_departments():
#     with SessionLocal() as session:
#         stmt = select(Employee.name, Department.name).outerjoin(Department, Employee.department_id == Department.id)
#         return session.execute(stmt).all()
    
# def get_project_employees_departments():
#     with SessionLocal() as session:
#         stmt = select(
#             Project.name.label("project_name"),
#             Employee.name.label("employee_name"),
#             Department.name.label("department_name")).join(Employee, Project.employee_id == Employee.id).join(Department, Employee.department_id == Department.id)
#         return session.execute(stmt).all()
    
# def count_employees():
#     with SessionLocal() as session:
#         stmt = select(func.count(Employee.id))
#         return session.execute(stmt).scalar()
    
# def get_average_salary():
#     with SessionLocal() as session:
#         stmt = select(func.avg(Employee.salary))
#         return session.execute(stmt).scalar()
    
# def get_min_salary():
#     with SessionLocal() as session:
#         stmt = select(func.min(Employee.salary))
#         return session.execute(stmt).scalar()
    
# def get_max_salary():
#     with SessionLocal() as session:
#         stmt = select(func.max(Employee.salary))
#         return session.execute(stmt).scalar()
    
# def get_total_active_projects_budget():
#     with SessionLocal() as session:
#         stmt = select(func.sum(Project.budget)).where(Project.is_active._is(True))
#         return session.execute(stmt).scalar()
    
# def count_employees_by_department():
#     with SessionLocal() as session:
#         stmt = select(Department.name, func.count(Employee.id)).join(Employee, Employee.department_id == Department.id).group_by(Department.name)
#         return session.execute(stmt).all()
    
# def get_average_salary_by_department():
#     with SessionLocal() as session:
#         stmt = select(Department.name, func.avg(Employee.salary).label("avg_salary")).join(Employee, Employee.department_id == Department.id).group_by(Department.name)
#         return session.execute(stmt).all()
    
# def deactivate_project(project_id: int):
#     with SessionLocal() as session:
#         project = session.get(Project, project_id)

#         if project is None:
#             return None
        
#         project.is_active = False
#         session.commit()
#         session.refresh(project)

#         return project