import logging

# Конфигурация логгера


def setup_logger():
    logger = logging.getLogger('financial_dashboard')
    logger.setLevel(logging.INFO)

    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Создаем форматтер
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавляем обработчик в логгер
    logger.addHandler(file_handler)

    return logger


# Получаем логгер
logger = setup_logger()
