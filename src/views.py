import json
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
        # Суммируем только отрицательные значения в "Сумма платежа"
        total_spent = group[group['Сумма платежа'] < 0]['Сумма платежа'].sum()

        # Если total_spent отрицательный, делаем его положительным
        total_spent = abs(total_spent)

        # Рассчитываем кешбэк (по положительной сумме расходов)
        cashback = total_spent // 100
        cashback = max(cashback, 0)  # Если кешбэк отрицательный, устанавливаем его в 0

        # Составляем список расходов
        expenses = group[group['Сумма платежа'] < 0]['Сумма платежа'].apply(lambda x: f"Сумма платежа: {abs(x)} RUB").tolist()

        card_data.append({
            'last_digits': card[-4:],  # Последние 4 цифры карты
            'total_spent': round(total_spent, 2),
            'cashback': round(cashback, 2),
            'expenses': expenses  # Список расходов
        })

    return card_data


file_path = '../operations.xlsx'  # Путь к вашему файлу
df = load_operations_data(file_path)

# Установим целевую дату
target_date = datetime.datetime(2021, 12, 20)

# Отфильтруем данные по дате
filtered_df = filter_data_by_date(df, target_date)

filtered_df.to_excel('filtered_operations.xlsx', index=False)

card_data = calculate_card_data(filtered_df)
json_output = json.dumps(card_data, ensure_ascii=False, indent=4)

# Выводим результат
print(json_output)


