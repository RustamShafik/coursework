import datetime
import json
import os
from src.utils import logger
import pandas as pd
import requests
from dotenv import load_dotenv


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


# Загружаем переменные окружения из файла .env (если используете этот метод)
load_dotenv()

# Загружаем настройки пользователя
with open('user_settings.json') as f:
    user_settings = json.load(f)

# Получаем API-ключ из переменной окружения
api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("API-ключ не найден. Установите переменную среды API_KEY.")


def get_currency_rates():
    rates = []

    # Обрабатываем каждую валюту из списка user_currencies
    for currency in user_settings['user_currencies']:
        try:
            # Формируем URL для запроса к API
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"

            headers = {
                "apikey": api_key
            }

            # Делаем запрос к API
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимет исключение для HTTP ошибок

            # Если запрос успешен
            data = response.json()

            if 'rates' not in data:
                return {"error": "Курсы не обнаружены в данных ответа"}

            # Получаем курс для рубля относительно текущей базовой валюты
            rate = data['rates'].get('RUB')
            if rate:
                rates.append({
                    "currency": currency,
                    "rate": rate
                })
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except requests.exceptions.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An error occurred: {err}"}

    return {"currency_rates": rates}


def get_stock_prices():
    stock_prices = []
    api_key = os.getenv("MARKETSTACK_API_KEY")  # Получаем API-ключ из переменной окружения

    if not api_key:
        print("Ошибка: API-ключ не найден. Проверьте .env файл.")
        return {"error": "API key is missing"}

    for stock in user_settings['user_stocks']:
        try:
            # Формируем URL с тикером акции
            url = f"https://api.marketstack.com/v1/eod?access_key={api_key}&symbols={stock}"

            # Делаем запрос к API
            response = requests.get(url)
            response.raise_for_status()  # Проверяем ошибки HTTP

            # Получаем JSON-ответ
            data = response.json()

            # Проверяем, есть ли данные о цене
            if "data" not in data or not data["data"]:
                print(f"Ошибка: нет данных для {stock}")
                continue

            # Получаем последнюю цену закрытия акции
            price = data["data"][0]["close"]

            stock_prices.append({
                "stock": stock,
                "price": price
            })

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error for {stock}: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error for {stock}: {req_err}")
        except Exception as err:
            print(f"An error occurred for {stock}: {err}")

    return {"stock_prices": stock_prices}


def get_dashboard_data(target_date):
    if isinstance(target_date, str):
        try:
            target_date = datetime.datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте формат 'YYYY-MM-DD HH:MM:SS'.")

    # Загружаем данные
    file_path = '../operations.xlsx'
    df = load_operations_data(file_path)

    # Фильтруем по дате
    filtered_df = filter_data_by_date(df, target_date)

    # Формируем JSON
    dashboard_data = {
        "greeting": get_greeting(),
        "cards": calculate_card_data(filtered_df),
        "top_transactions": top_five_transact(filtered_df),
        "currency_rates": get_currency_rates().get("currency_rates", []),
        "stock_prices": get_stock_prices().get("stock_prices", [])
    }

    return dashboard_data


# import datetime
# target_date = datetime.datetime(2021, 12, 20)
# dashboard = get_dashboard_data(target_date)
# print(json.dumps(dashboard, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    # target_date = datetime.datetime(2021, 12, 20)
    target_date = ("2021-12-20 17:00:00")
    dashboard = get_dashboard_data(target_date)
    print(json.dumps(dashboard, ensure_ascii=False, indent=4))
