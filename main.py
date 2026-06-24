from decimal import Decimal
from database import Base, engine
from crud import (
    create_category,
    get_all_categories,
    create_supplier,
    get_all_suppliers,
    deactivate_supplier,
    create_product,
    get_all_products,
    get_product_by_id,
    update_product_prices,
    deactivate_product,
    create_stock_movement,
    get_stock_movements_by_product,
)

from reports import (
    get_stock_movements_with_product,
    get_products_count_by_category,
    get_products_count_by_supplier,
    get_current_stock_by_product,
    get_low_stock_products,
    get_current_stock_for_all_products,
    get_purchase_value_report
)

def show_menu():
    print()
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
            if not name:
                print("Название категории не может быть пустым.")
                continue

            category = create_category(name)
            
            if isinstance(category, str):
                print(category)
            else:
                print(f"Категория '{category.name}' успешно добавлена.")

        elif choice == "2":
            categories = get_all_categories()

            print ("ID | Название")

            for category in categories:
                print(f"{category.id} | {category.name}")

        elif choice == "3":
            name = input("Введите название поставщика: ")

            if not name:
                print("Название поставщика не может быть пустым.")
                continue

            phone = input("Введите телефон поставщика: ")
            email = input("Введите email поставщика: ")

            supplier = create_supplier(
                name=name,
                phone=phone if phone else None,
                email=email if email else None
            )

            if isinstance(supplier, str):
                print(supplier)
            else:
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
            if not name:
                print("Название товара не может быть пустым.")
                continue

            sku = input("Введите уникальный артикул товара: ")
            if not sku:
                print("SKU не может быть пустым.")
                continue

            try:
                category_id = int(input("Введите ID категории: "))
            except ValueError:
                print("ID категории должен быть числом.")
                continue

            try:
                supplier_id = int(input("Введите ID поставщика: "))
            except ValueError:
                print("ID поставщика должен быть числом.")
                continue

            purchase_price = Decimal(input("Введите закупочную цену: "))
            selling_price = Decimal(input("Введите продажная цену: "))
            min_quantity = Decimal(input("Введите минимальный остаток: "))

            product = create_product(
                name=name,
                sku=sku,
                category_id=category_id,
                supplier_id=supplier_id,
                purchase_price=purchase_price,
                selling_price=selling_price,
                min_quantity=min_quantity
            )

            if isinstance(product, str):
                print(product)
            else:
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

            product = update_product_prices(product_id, purchase, selling)

            if product:
                print("Цены успешно обновлены.")
            else:
                print("Товар не найден.")

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
            stock_movement = create_stock_movement(product_id, "IN", quantity)

            if isinstance(stock_movement, str):
                print(stock_movement)
            else:
                product = get_product_by_id(product_id)
                print(f"Товар '{product.name}' в количестве {quantity} успешно добавлен.")

        elif choice == "12":
            product_id = int(input("ID товара: "))
            quantity = Decimal(input("Количество: "))
            stock_movement = create_stock_movement(product_id, "OUT", quantity)

            if isinstance(stock_movement, str):
                print(stock_movement)
            else:
                product = get_product_by_id(product_id)
                print(f"Товар '{product.name}' в количестве {quantity} успешно списан.")

        elif choice == "13":
            product_id = int(input("ID товара: "))
            quantity = Decimal(input("Количество: "))
            stock_movement = create_stock_movement(product_id, "ADJUST", quantity)

            if isinstance(stock_movement, str):
                print(stock_movement)
            else:
                product = get_product_by_id(product_id)
                print(f"Товар '{product.name}' в количестве {quantity} успешно скорректирован.")
        
        elif choice == "14":
            rows = get_stock_movements_with_product()

            print("Дата | Товар | SKU | Тип операции | Количество")

            for row in rows:
                print(f"{row.created_at} | {row.product_name} | {row.sku} | {row.movement_type} | {row.quantity}")

        elif choice == "15":
            product_id = int(input("ID товара: "))

            product = get_product_by_id(product_id)

            if product is None:
                print("Товар не найден.")
                continue

            movements = get_stock_movements_by_product(product_id)
            
            print(f"{product.name}:")
            for movement in movements:
                print(movement.created_at, movement.movement_type, movement.quantity)

        elif choice == "16":
            stocks = get_current_stock_for_all_products()

            for product, stock in stocks:
                print(f"{product}: {stock}")

        elif choice == "17":
            products = get_low_stock_products()

            if not products:
                print("Нет товаров, которые заканчиваются.")
            else:
                for product in products:
                    current_stock = get_current_stock_by_product(product.id)

                    print(product.name)
                    print(f"Остаток: {current_stock}")
                    print(f"Минимальный остаток: {product.min_quantity}")
                    print()

        elif choice == "18":
            report, total_value = get_purchase_value_report()

            for name, stock, purchase_price, value in report:
                print(f"{name}:")
                print(f"Остаток: {stock}")
                print(f"Закупочная цена: {purchase_price}")
                print(f"Стоимость остатка: {value:.2f}")
                print()

            print(f"Итого по складу: {total_value:.2f}")

        elif choice == "19":
            products = get_products_count_by_category()

            for category, count in products:
                print(f"{category}: {count}")

        elif choice == "20":
            products = get_products_count_by_supplier()

            for supplier, count in products:
                print(f"{supplier}: {count}")

        elif choice == "0":
            break

main()