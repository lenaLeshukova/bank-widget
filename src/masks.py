def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты и возвращает его маску в формате XXXX XX** **** XXXX"""

    card_str = str(card_number)
    if not card_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    first_6 = card_str[:6]
    last_4 = card_str[-4:]

    masked_raw = f"{first_6}******{last_4}"
    formatted_mask = f"{masked_raw[:4]} {masked_raw[4:8]} {masked_raw[8:12]} {masked_raw[12:]}"

    return formatted_mask



def get_mask_account(account_number: str) -> str:
    """Принимает номер счета и возвращает его маску в формате **XXXX"""

    account_str = str(account_number)
    if not account_str.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")
    if len(account_str) < 4:
        raise ValueError("Номер счета слишком короткий")

    last_4_digits = account_str[-4:]

    return f"**{last_4_digits}"


if __name__ == "__main__":

   print(get_mask_account("73654108430135874305"))  # Вывод: **4305

   print(get_mask_card_number("7000792289606361"))   # Вывод: 7000 79** **** 6361
