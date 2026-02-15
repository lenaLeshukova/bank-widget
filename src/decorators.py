from functools import wraps


def log(filename=None):
    """
        Декоратор, который логирует начало и окончание выполнения функции.

        Записывает имя функции при старте, а по завершении — статус "ok"
        или текст ошибки с типами исключений и входными данными.

        Args:
            filename (str, optional): Путь к файлу для записи логов.
                Если не указан, логи выводятся в консоль. По умолчанию None.

        Returns:
            Callable: Декоратор, оборачивающий функцию.
        """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # ЛОГИРУЕМ НАЧАЛО
            start_msg = f"start {func.__name__}"
            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(start_msg + "\n")
            else:
                print(start_msg)

            log_message = ""
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                return result
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                raise
            finally:
                # ЛОГИРУЕМ КОНЕЦ (результат или ошибку)
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

        return wrapper

    return decorator


# Примеры использования
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


@log()
def div(x, y):
    return x / y


my_function(1, 2)

try:
    div(1, 0)
except ZeroDivisionError:
    pass
