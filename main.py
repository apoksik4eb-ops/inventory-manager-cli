from decimal import Decimal
from database import Base, engine
from crud import (
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category_name,
    delete_category,
    create_supplier,
    get_all_suppliers,
    get_supplier_by_id,
    update_supplier_contacts,
    deactivate_supplier,
    delete_supplier,
    create_product,
    get_all_products,
    get_product_by_id,
    get_products_by_category,
    get_products_by_supplier,
    update_product_prices,
    update_product_min_quantity,
    deactivate_product,
    delete_product,
    create_stock_movement,
    get_all_stock_movements,
    get_stock_movements_by_product,
    delete_stock_movement
)

from reports import (
    get_products_with_category_and_supplier,
    get_stock_movements_with_product,
    get_products_count_by_category,
    get_products_count_by_supplier,
    get_current_stock_by_product,
    get_low_stock_products,
    get_total_purchase_value,
    get_total_selling_value,
    get_potential_profit
)

def show_menu():
    print("Inventory Manager CLI")
    print()
    print("1. Создать категорию")
    print("2. Показать все категории")
    print()
    print("3. Создать поставщика")
    print("4. Показать всех поставщиков")
    print("5. Деактивировать поставщика")
    print()
    print("6. Создать товар")
    print("7. Показать все товары")
    print("8. Показать товар по id")
    print("9. Обновить цену товара")
    print("10. Деактивировать товар")
    print()
    print("11. Добавить поступление товара")
    print("12. Добавить списание товара")
    print("13. Добавить корректировку остатка")
    print()
    print("14. Показать историю операций")
    print("15. Показать операции по товару")
    print()
    print("16. Показать текущие остатки")
    print("17. Показать товары, которые заканчиваются")
    print("18. Показать общую стоимость склада")
    print("19. Показать товары по категориям")
    print("20. Показать товары по поставщикам")
    print()
    print("0. Выход")

def main():
    Base.metadata.create_all(engine)

    while True:
        show_menu()

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            name = input("Введите название категории: ")
            category = create_category(name)
            print(f"Категория '{category.name}' успешно добавлена.")

        elif choice == "2":
            categories = get_all_categories()

            print ("ID | Название")

            for category in categories:
                print(f"{category.id} | {category.name}")

        elif choice == "3":
            name = input("Введите название поставщика: ")
            phone = input("Введите телефон поставщика: ")
            email = input("Введите email поставщика: ")

            supplier = create_supplier(
                name=name,
                phone=phone if phone else None,
                email=email if email else None
            )

            print(f"Поставщик '{supplier.name}' успешно добавлен.")

        elif choice == "4":
            suppliers = get_all_suppliers()

            print("ID | Название | Телефон | Email | Активен")

            for supplier in suppliers:
                print(f"{supplier.id} | {supplier.name} | {supplier.phone} | {supplier.email} | {supplier.is_active}")

        elif choice == "5":
            supplier_id = int(input("Введите ID поставщика: "))

            supplier = deactivate_supplier(supplier_id)

            if supplier:
                print(f"Поставщик '{supplier.name}' деактивирован.")
            else:
                print(f"Поставщик не найден.")

        elif choice == "6":
            name = input("Введите название товара: ")
            sku = input("Введите уникальный артикул товара: ")
            category_id = input("Введите ID категории: ")
            supplier_id = input("Введите ID поставщика: ")
            purchase_price = Decimal(input("Введите закупочную цену: "))
            selling_price = Decimal(input("Введите продажная цену: "))
            min_quantity = Decimal(input("Введите минимальный остаток: "))

            product = create_product(
                name=name,
                sku=sku,
                category_id=int(category_id) if category_id else None,
                supplier_id=int(supplier_id) if supplier_id else None,
                purchase_price=purchase_price,
                selling_price=selling_price,
                min_quantity=min_quantity
            )

            print(f"Продукт '{product.name}' успешно добавлен.")

        elif choice == "7":
            products = get_all_products()

            print("ID | Товар | SKU")

            for product in products:
                print(f"{product.id} | {product.name} | {product.sku}")
                
        elif choice == "8":
            product_id = int(input("Введите ID товара: "))
            
            product = get_product_by_id(product_id)

            if product:
                print(product.id, product.name, product.sku)
            else:
                print("Товар не найден.")

        elif choice == "9":
            product_id = int(input("Введите ID товара: "))

            new_purchase = input("Новая закупочная цена: ")
            new_selling = input("Новая продажная цена: ")

            purchase = Decimal(new_purchase) if new_purchase else None
            selling = Decimal(new_selling) if new_selling else None

            update_product_prices(product_id, purchase, selling)

        elif choice == "10":
            product_id = int(input("Введите ID товара: "))

            product = deactivate_product(product_id)

            if product:
                print(f"Товар '{product.name}' деактивирован.")
            else:
                print(f"Товар не найден.")

        elif choice == "11":
            product_id = int(input("Введите ID товара: "))
            quantity = Decimal(input("Введите количество: "))
            create_stock_movement(product_id, "IN", quantity)

            product = get_product_by_id(product_id)

            print(f"Товар '{product.name}' в количестве {quantity} успешно добавлен.")

        elif choice == "12":
            product_id = int(input("ID товара: "))
            quantity = Decimal(input("Количество: "))
            create_stock_movement(product_id, "OUT", quantity)

            product = get_product_by_id(product_id)

            print(f"Товар '{product.name}' в количестве {quantity} успешно списан.")

        elif choice == "13":
            product_id = int(input("ID товара: "))
            quantity = Decimal(input("Количество: "))
            create_stock_movement(product_id, "ADJUST", quantity)

            product = get_product_by_id(product_id)

            print(f"Товар '{product.name}' в количестве {quantity} успешно скорректирован.")
        
        elif choice == "14":
            rows = get_stock_movements_with_product()

            print("Дата | Товар | SKU | Тип операции | Количество")

            for row in rows:
                print(f"{row.created_at} | {row.product_name} | {row.sku} | {row.movement_type} | {row.quantity}")

        elif choice == "15":
            product_id = int(input("ID товара: "))

            movements = get_stock_movements_by_product(product_id)

            for movement in movements:
                print(movement.created_at, movement.movement_type, movement.quantity)

        elif choice == "16":
            product_id = int(input("ID товара: "))

            stock = get_current_stock_by_product(product_id)
            product = get_product_by_id(product_id)    
            print(f"Текущий остаток '{product.name}': {stock}")

        elif choice == "17":
            products = get_low_stock_products()

            for product in products:
                print(product.id, product.name)

        elif choice == "18":
            print("Стоимость закупки:", get_total_purchase_value())
            print("Стоимость продажи:", get_total_selling_value())
            print("Потенциальная прибыль:", get_potential_profit())

        elif choice == "19":
            category_id = int(input("Введите ID категории: "))

            products = get_products_by_category(category_id)

            for product in products:
                print(product.id, product.name, product.sku)

        elif choice == "20":
            supplier_id = int(input("Введите ID поставщика: "))

            products = get_products_by_supplier(supplier_id)

            for product in products:
                print(product.id, product.name, product.sku)

        elif choice == "0":
            break

main()