import datetime
import logging

import pandas as pd


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


def load_operations_data(file_path):
    """
    Загружает данные о транзакциях из Excel-файла.

    Аргументы:
    file_path (str): Путь к файлу Excel.

    Возвращает:
    pandas.DataFrame: Данные о транзакциях.
    """
    # Загрузка данных из Excel
    df = pd.read_excel(file_path)

    # Преобразуем колонку "Дата операции" в формат datetime
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], errors='coerce', dayfirst=True)

    # Преобразуем колонку "Дата платежа" в формат datetime
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], errors='coerce', dayfirst=True)

    # Преобразуем числовые колонки в нужные форматы
    df['Сумма операции'] = pd.to_numeric(df['Сумма операции'], errors='coerce')
    df['Сумма платежа'] = pd.to_numeric(df['Сумма платежа'], errors='coerce')
    df['Кэшбэк'] = pd.to_numeric(df['Кэшбэк'], errors='coerce')
    df['Бонусы (включая кэшбэк)'] = pd.to_numeric(df['Бонусы (включая кэшбэк)'], errors='coerce')
    df['Округление на инвесткопилку'] = pd.to_numeric(df['Округление на инвесткопилку'], errors='coerce')
    df['Сумма операции с округлением'] = pd.to_numeric(df['Сумма операции с округлением'], errors='coerce')
    logger.info(f"Данные из файла {file_path} успешно загружены.")
    # print (df.head())
    return df


def filter_data_by_date(df, target_date):
    """
        Фильтрует данные о транзакциях по диапазону дат:
        с 1-го числа месяца до целевой даты.

        Аргументы:
        df (pandas.DataFrame): Данные о транзакциях.
        target_date (datetime): Целевая дата для фильтрации.

        Возвращает:
        pandas.DataFrame: Отфильтрованные данные о транзакциях.
        """
    # Определяем первый день месяца
    first_of_month = target_date.replace(day=1)
    # Фильтруем данные, чтобы оставить только транзакции с 1-го числа месяца до целевой даты
    filtered_data = df[(df['Дата операции'] >= first_of_month) & (df['Дата операции'] <= target_date)]
    return filtered_data


def get_greeting():
    """
        Возвращает приветствие в зависимости от времени суток.

        Возвращает:
        str: Приветствие ("Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи").
        """
    current_time = datetime.datetime.now().hour

    if current_time < 12:
        return "Доброе утро"
    if current_time < 18:
        return "Добрый день"
    if current_time < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def calculate_card_data(df):
    """
    Рассчитывает данные по картам: общую сумму расходов (по "Сумма платежа") и кешбэк.

    Аргументы:
    df (pandas.DataFrame): Данные о транзакциях.

    Возвращает:
    list: Список словарей с данными по картам.
    """
    # Фильтруем строки, где есть номер карты и статус OK
    df_filtered = df[df['Номер карты'].notnull() & (df['Статус'] == 'OK')]

    card_data = []
    for card, group in df_filtered.groupby('Номер карты'):
        # Суммируем только отрицательные значения в "Сумма операции"
        total_spent = group[group['Сумма операции'] < 0]['Сумма операции'].sum()

        # Если total_spent отрицательный, делаем его положительным
        total_spent = abs(total_spent)

        # Рассчитываем кешбэк (по положительной сумме расходов)
        cashback = total_spent / 100
        cashback = max(cashback, 0)  # Если кешбэк отрицательный, устанавливаем его в 0

        card_data.append({
            'last_digits': card[-4:],  # Последние 4 цифры карты
            'total_spent': round(total_spent, 2),
            'cashback': round(cashback, 2),
        })

    return card_data


def top_five_transact(df):
    df_filtered = df[['Дата операции', 'Сумма операции', 'Категория', 'Описание']]
    df_filtered = df_filtered.sort_values(by='Сумма операции', key=abs, ascending=False).head(5)
    top_transact = []
    for _, row in df_filtered.iterrows():
        top_transact.append({
            "date": row['Дата операции'].strftime("%d.%m.%Y"),  # Форматируем дату
            "amount": round(row['Сумма операции'], 2),
            "category": row['Категория'],
            "description": row['Описание']
        })

    return top_transact
