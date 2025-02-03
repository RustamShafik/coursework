import pandas as pd
import datetime

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



file_path = '../operations.xlsx'

# Получаем и выводим приветствие
greeting = get_greeting()
print(greeting)

# Загружаем данные из файла и выводим их
operations_data = load_operations_data(file_path)
target_date = pd.to_datetime('2021-12-15')

# Фильтруем данные по дате
filtered_data = filter_data_by_date(operations_data, target_date)

# Выводим отфильтрованные данные
print(filtered_data)

