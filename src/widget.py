from masks import get_mask_card_number, get_mask_account


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


# Примеры использования (для проверки):
if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 73654108430135874305"))

