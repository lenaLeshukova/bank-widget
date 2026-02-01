from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """Определяет тип входных данных (карта или счет) и возвращает маскированную строку."""

    # Разбиваем строку на части по пробелам
    parts = data.split()

    # Извлекаем номер (последний элемент) и название (все элементы, кроме последнего)
    number = parts[-1]
    name = " ".join(parts[:-1])

    # Проверяем, является ли это счетом или картой
    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формате '2024-03-11T02:26:18.671407' и возвращает 'ДД.ММ.ГГГГ'."""
    if len(date_str) < 10:
        raise ValueError("Некорректный формат даты")
    # Извлекаем год, месяц и день по индексам
    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]

    # Проверка диапазона месяца
    if not (1 <= int(month) <= 12):
        raise ValueError("Месяц должен быть в диапазоне от 01 до 12")

    return f"{day}.{month}.{year}"

# Пример работы:
# Вход: "2024-03-11T02:26:18.671407"
# Выход: "11.03.2024"


# Примеры использования:
if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 73654108430135874305"))
