import pytest


# Фикстура для примера номера карты
@pytest.fixture
def sample_card_number():
    return "7000792289606361"


# Фикстура для примера номера счета
@pytest.fixture
def sample_account_number():
    return "73654108430135874305"


# Фикстура с набором тестовых транзакций
@pytest.fixture
def transactions_data():
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации"
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Перевод со счета на счет"
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Оплата услуг"
        }
    ]

