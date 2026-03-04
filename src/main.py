import os
from src.utils import get_financial_transactions
from src.transactions import read_transactions_csv, read_transactions_excel
from src.processing import filter_by_state, sort_by_date, filter_by_query
from src.generators import filter_by_currency
from src.widget import mask_account_card, get_date


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("\nПользователь: ")

    # 1. Загрузка данных
    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        transactions = get_financial_transactions("data/operations.json")
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        transactions = read_transactions_csv("data/transactions.csv")
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        transactions = read_transactions_excel("data/transactions_excel.xlsx")
    else:
        print("Программа: Неверный выбор.")
        return

    # 2. Фильтрация по статусу
    while True:
        status = input("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.\n"
                       "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n\nПользователь: ")
        status_up = status.upper()
        if status_up in ["EXECUTED", "CANCELED", "PENDING"]:
            transactions = filter_by_state(transactions, status_up)
            print(f'Программа: Операции отфильтрованы по статусу "{status_up}"')
            break
        else:
            print(f'\nПрограмма: Статус операции "{status}" недоступен.')

    # 3. Сортировка по дате
    is_sort = input("\nПрограмма: Отсортировать операции по дате? Да/Нет\n\nПользователь: ").lower()
    if is_sort == "да":
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\n\nПользователь: ").lower()
        transactions = sort_by_date(transactions, descending=(order == "по убыванию"))

    # 4. Фильтрация по валюте (RUB)
    is_rub = input("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\n\nПользователь: ").lower()
    if is_rub == "да":
        # Используем генератор из модуля generators, приводим к списку
        transactions = list(filter_by_currency(transactions, "RUB"))

    # 5. Фильтрация по описанию
    is_descr = input(
        "\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n\nПользователь: ").lower()
    if is_descr == "да":
        query = input("Введите слово для поиска: ")
        transactions = filter_by_query(transactions, query)

    # 6. Вывод результата
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")
    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}\n")
        for t in transactions:
            # Дата через виджет
            date_fmt = get_date(t.get("date", "0000-00-00"))

            # Маскировка через виджет (с проверкой на наличие отправителя)
            from_info = mask_account_card(t.get("from")) if t.get("from") and str(t.get("from")) != "nan" else ""
            to_info = mask_account_card(t.get("to")) if t.get("to") else "Счет неизвестен"

            path = f"{from_info} -> {to_info}" if from_info else to_info

            # Сумма и валюта (универсальный доступ для JSON и CSV/XLSX)
            amount = t.get("amount") or t.get("operationAmount", {}).get("amount")
            curr = (t.get("currency_name") or
                    t.get("operationAmount", {}).get("currency", {}).get("name") or "руб.")

            print(f"{date_fmt} {t.get('description', 'Без описания')}")
            print(f"{path}")
            print(f"Сумма: {amount} {curr}\n")


if __name__ == "__main__":
    main()
