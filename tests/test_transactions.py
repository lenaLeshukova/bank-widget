from unittest.mock import patch, mock_open

import pandas as pd

from src.transactions import read_transactions_csv, read_transactions_excel


# Тесты для CSV

def test_read_transactions_csv_success():
    """Тест успешного чтения CSV через мок файла."""
    csv_content = "id;state;amount\n1;EXECUTED;100.5"

    with patch("builtins.open", mock_open(read_data=csv_content)) as mock_file:
        result = read_transactions_csv("data/transactions.csv")

        expected = [{"id": "1", "state": "EXECUTED", "amount": "100.5"}]
        assert result == expected
        mock_file.assert_called_once_with("data/transactions.csv", mode='r', encoding='utf-8')


def test_read_transactions_csv_not_found():
    """Тест обработки отсутствующего CSV файла."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_transactions_csv("missing.csv")
        assert result == []


# Тесты для Excel

@patch("pandas.read_excel")
def test_read_transactions_excel_success(mock_read_excel):
    """Тест успешного чтения Excel через мок pandas."""
    # Подменяем возвращаемое значение pandas.read_excel на тестовый DataFrame
    mock_read_excel.return_value = pd.DataFrame([{"id": 1, "state": "EXECUTED", "amount": 100.5}])

    result = read_transactions_excel("data/transactions_excel.xlsx")

    expected = [{"id": 1, "state": "EXECUTED", "amount": 100.5}]
    assert result == expected
    mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")


def test_read_transactions_excel_not_found():
    """Тест обработки отсутствующего Excel файла."""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = read_transactions_excel("missing.xlsx")
        assert result == []


def test_read_transactions_excel_error():
    """Тест обработки любой другой ошибки при чтении Excel."""
    with patch("pandas.read_excel", side_effect=Exception("Ошибка")):
        result = read_transactions_excel("bad_file.xlsx")
        assert result == []
