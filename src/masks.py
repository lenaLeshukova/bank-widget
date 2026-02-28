import logging
import os

# Настройка пути к файлу лога
# Создаем папку logs в корне, если она не существует
# Получаем путь к директории, где лежит файл masks.py (это src)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на один уровень вверх — в корень проекта
project_root = os.path.dirname(current_dir)

# Формируем путь к папке logs в корне проекта
log_directory = os.path.join(project_root, "logs")

# Создаем папку, если её нет
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Итоговый путь к файлу
log_file = os.path.join(log_directory, "masks.log")

# Настройка Логера
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# FileHandler с режимом 'w' для перезаписи при каждом запуске
file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты и возвращает его маску в формате XXXX XX** **** XXXX"""
    logger.info(f"Начало маскирования номера карты: {card_number}")
    card_str = str(card_number)
    if not card_str.isdigit():
        error_msg = "Номер карты должен содержать только цифры"
        logger.error(f"Ошибка: номер карты содержит не только цифры: {card_number}")
        raise ValueError(error_msg)

    if len(card_str) != 16:
        error_msg = "Номер карты должен содержать 16 цифр"
        logger.error(f"Ошибка: неверная длина номера карты ({len(card_str)} вместо 16)")
        raise ValueError(error_msg)

    first_6 = card_str[:6]
    last_4 = card_str[-4:]

    masked_raw = f"{first_6}******{last_4}"
    formatted_mask = f"{masked_raw[:4]} {masked_raw[4:8]} {masked_raw[8:12]} {masked_raw[12:]}"
    logger.info("Маскирование номера карты успешно завершено")
    return formatted_mask


def get_mask_account(account_number: str) -> str:
    """Принимает номер счета и возвращает его маску в формате **XXXX"""
    logger.info(f"Начало маскирования номера счета: {account_number}")

    account_str = str(account_number)
    if not account_str.isdigit():
        error_msg = "Номер счета должен содержать только цифры"
        logger.error(f"Ошибка: номер счета содержит не только цифры: {account_number}")
        raise ValueError(error_msg)
    if len(account_str) < 4:
        error_msg = "Номер счета слишком короткий"
        logger.error(f"Ошибка валидации: {error_msg}")
        raise ValueError(error_msg)

    last_4_digits = account_str[-4:]
    result = f"**{last_4_digits}"
    logger.info("Маскирование номера счета успешно завершено")
    return result


if __name__ == "__main__":
    # Тест
    try:
        print(get_mask_account("73654108430135874305"))
        print(get_mask_card_number("7000792289606361"))
        # Пример ошибки
        # print(get_mask_card_number("123"))
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        get_mask_card_number("1234ABC") # Буквы вместо цифр
    except ValueError:
        pass # Ошибка уже улетела в лог
