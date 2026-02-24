from unittest.mock import patch

import requests

from src.external_api import convert_to_rub


@patch("src.external_api.requests.get")
def test_convert_to_rub_usd(mock_get, mock_api_response):
    """Тест конвертации USD в RUB при успешном ответе API."""
    # Настраиваем mock так, чтобы он возвращал объект с методом json()
    mock_get.return_value.json.return_value = mock_api_response
    mock_get.return_value.status_code = 200

    result = convert_to_rub(100.0, "USD")

    assert result == 7550.0
    # Проверяем, что запрос был сделан по верному адресу
    mock_get.assert_called_once()
    assert "https://api.apilayer.com" in mock_get.call_args[0][0]


@patch("src.external_api.requests.get")
def test_convert_to_rub_server_error(mock_get):
    """Тест поведения функции при ошибке сервера """
    # Имитируем ошибку от библиотеки requests
    mock_get.return_value.raise_for_status.side_effect = requests.RequestException("Internal Server Error")

    result = convert_to_rub(100.0, "EUR")

    # Согласно логике функции, при ошибке возвращается 0.0
    assert result == 0.0


def test_convert_to_rub_already_rub():
    """Тест: если валюта уже RUB, API не должен вызываться."""
    with patch("src.external_api.requests.get") as mock_get:
        result = convert_to_rub(100.0, "RUB")

        assert result == 100.0
        # Проверяем, что запроса к API не было
        mock_get.assert_not_called()
