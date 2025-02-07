import json
import logging
from datetime import datetime, timedelta

import pandas as pd

# Конфигурируем logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Декоратор для записи отчета в файл
def report_decorator(file_name=None):
    if file_name is None:
        file_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Записываем результат в файл, без экранирования символов в Unicode
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            logging.info(f"Отчет записан в файл {file_name}")
            return result

        return wrapper

    return decorator


# Функция для получения суммы трат по категории за указанный период
@report_decorator()
def spending_by_category(transactions, category, date=None):
    # Если дата не передана, берем текущую
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    # Преобразуем строку в дату
    end_date = datetime.strptime(date, '%Y-%m-%d')

    # Определяем дату три месяца назад
    start_date = end_date - timedelta(days=90)

    # Убедимся, что 'Дата операции' в формате datetime
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], errors='coerce')

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ]

    # Суммируем только значения по столбцу "Сумма операции"
    total_spending = int(filtered_transactions['Сумма операции'].sum())

    # Выводим информацию о фильтрации
    logging.info(
        f"Общая сумма расходов по категории '{category}' за период с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')}: {total_spending}")

    # Возвращаем сумму трат по категории
    return {'category': category, 'total_spending': total_spending}
