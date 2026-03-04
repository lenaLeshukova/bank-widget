from unittest.mock import patch

from src.main import main


@patch("src.main.get_financial_transactions")
def test_main_full_scenario(mock_get_json, mock_transactions, capsys, monkeypatch):
    """Тест полного сценария: JSON -> EXECUTED -> Сортировка Да -> По убыванию -> Валюта Да -> Поиск Нет"""

    # Настраиваем мок для чтения файла
    mock_get_json.return_value = mock_transactions

    # Имитируем ввод пользователя (последовательно на каждый input)
    inputs = iter([
        "1",  # Выбор JSON
        "EXECUTED",  # Статус
        "да",  # Сортировать?
        "по убыванию",  # Порядок
        "да",  # Только рубли?
        "нет"  # Фильтр по слову?
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Запускаем main
    main()

    # Проверяем вывод в консоль
    captured = capsys.readouterr().out

    assert "Для обработки выбран JSON-файл" in captured
    assert "Операции отфильтрованы по статусу \"EXECUTED\"" in captured
    assert "Всего банковских операций в выборке: 2" in captured
    assert "08.12.2019 Открытие вклада" in captured
    assert "Счет **9454" in captured
    assert "8390.00 руб." in captured


def test_main_invalid_status_retry(capsys, monkeypatch):
    """Тест проверки на неверный статус и повторный ввод"""

    # Имитируем: сначала ввели некорректно, потом корректный статус, потом на все вопросы "нет"
    # Также нужно прервать выполнение после загрузки, чтобы не упасть на отсутствии моков
    inputs = iter([
        "1", "WRONG_STATUS", "EXECUTED", "нет", "нет", "нет"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Мокаем загрузку данных, чтобы вернула пустой список и программа завершилась
    with patch("src.main.get_financial_transactions", return_value=[]):
        main()

    captured = capsys.readouterr().out
    assert 'Статус операции "WRONG_STATUS" недоступен' in captured


@patch("src.main.get_financial_transactions")
def test_main_empty_result(mock_get_json, capsys, monkeypatch):
    """Тест случая, когда транзакции не найдены"""

    mock_get_json.return_value = []  # Пустой файл

    inputs = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr().out
    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in captured
