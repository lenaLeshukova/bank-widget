import pytest


# Фикстура для примера номера карты
@pytest.fixture
def sample_card_number():
    return "7000792289606361"


# Фикстура для примера номера счета
@pytest.fixture
def sample_account_number():
    return "73654108430135874305"
