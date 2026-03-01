import csv

import pandas as pd


def read_transactions_csv(file_path: str) -> list:
    """
    Считывает финансовые операции из CSV-файла
    возвращает список словарей.
    """
    transactions = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            # DictReader превращает каждую строку в словарь {заголовок: значение}
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                transactions.append(row)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
        return []
    return transactions


def read_transactions_excel(file_path: str) -> list:
    """
    Считывает финансовые операции из файла Excel,
    возвращает список словарей.
    """
    try:
        # Читаем файл.
        df = pd.read_excel(file_path)

        # Заменяем пустые значения (NaN) на пустые строки или None
        df = df.fillna("")

        # Преобразуем таблицу в список словарей
        return df.to_dict(orient='records')
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return []


# Пример вызова:
if __name__ == "__main__":
    print("Начинаю чтение файлов...")

    # Для CSV
    csv_data = read_transactions_csv('../data/transactions.csv')
    print(f"Загружено {len(csv_data)} транзакций из CSV")

    # Для Excel
    excel_data = read_transactions_excel('../data/transactions_excel.xlsx')
    print(f"Загружено {len(excel_data)} транзакций из Excel")

    print(f"Первая транзакция из Excel: {excel_data[0] if excel_data else 'Данных нет'}")
