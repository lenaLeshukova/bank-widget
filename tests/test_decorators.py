import pytest

from src.decorators import log


# Фикстура capsys является встроенной в pytest. Это значит, что её не нужно определять вручную или импортировать.
# Достаточно поместить capsys в аргументы функции

def test_log_to_console(capsys):
    """Проверка логирования в консоль (вывод через print)."""

    @log()
    def add(a, b):
        result = a + b
        return result

    add(2, 3)

    captured = capsys.readouterr()
    assert "start add" in captured.out
    assert "add ok" in captured.out


def test_log_to_file(tmp_path):
    """Проверка записи логов в файл с использованием временной директории tmp_path."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    multiply(3, 4)

    content = log_file.read_text(encoding="utf-8")
    assert "start multiply" in content
    assert "multiply ok" in content


def test_log_exception_console(capsys):
    """Проверка логирования ошибки в консоль."""

    @log()
    def fail():
        return 1 / 0

    with pytest.raises(ZeroDivisionError):
        fail()

    captured = capsys.readouterr()
    assert "start fail" in captured.out
    assert "fail error: ZeroDivisionError" in captured.out
    assert "Inputs: ()," in captured.out


def test_log_exception_file(tmp_path):
    """Проверка записи ошибки в файл."""
    log_file = tmp_path / "error_log.txt"

    @log(filename=str(log_file))
    def fail_with_args(a, b=None):
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError):
        fail_with_args(10, b="test")

    content = log_file.read_text(encoding="utf-8")
    assert "start fail_with_args" in content
    assert "fail_with_args error: ValueError" in content
    # Проверка записи аргументов
    assert "Inputs: (10,)" in content
    assert "'b': 'test'" in content


def test_wraps_metadata():
    """Проверка, что wraps сохраняет имя и документацию функции."""

    @log()
    def documented_func():
        """Hello doc"""
        pass

    assert documented_func.__name__ == "documented_func"
    assert documented_func.__doc__ == "Hello doc"
