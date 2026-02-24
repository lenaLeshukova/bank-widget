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


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными транзакций."""
    return [
        {"id": 1, "state": "EXECUTED", "amount": "100.00"},
        {"id": 2, "state": "CANCELED", "amount": "200.00"}
    ]


@pytest.fixture
def sample_transactions():
    """Фикстура с корректными данными."""
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"}
    ]


@pytest.fixture
def empty_file_content():
    """Фикстура для имитации абсолютно пустого файла."""
    return ""


@pytest.fixture
def not_list_content():
    """Фикстура для имитации JSON, который не является списком."""
    return '{"error": "this is a dict, not a list"}'


@pytest.fixture
def mock_api_response():
    """Фикстура для создания типичного успешного ответа от API."""
    return {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 100},
        "info": {"timestamp": 1678900000, "rate": 75.5},
        "date": "2023-03-15",
        "result": 7550.0  # Ожидаемый результат конвертации
    }
