import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(amount: float, currency: str) -> float:
    """Конвертирует сумму из USD или EUR в RUB через API."""
    if currency == "RUB":
        return float(amount)

    headers = {"apikey": API_KEY}
    params = {"to": "RUB", "from": currency, "amount": amount}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        response.raise_for_status()  # Проверка на ошибки запроса
        data = response.json()
        return float(data["result"])
    except (requests.RequestException, KeyError):
        print("Ошибка при обращении к API конвертации.")
        return 0.0
