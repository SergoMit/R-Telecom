import logging

def logger_func() -> None:

    # Создание логгирующего объекта
    logger = logging.basicConfig(level=logging.INFO)

    # Настройка обработчика и форматировщика для логгирующего объекта logger
    handler = logging.FileHandler('py_log.log', mode='w')
    formatter = logging.Formatter("s%(name)s %(asctime)s %(levelname)s %(message)s")

    # Добавление форматировщика к обработчику
    handler.setFormatter(formatter)

    # Добавление обработчика к объекту logger
    logger.addHandler(handler)
