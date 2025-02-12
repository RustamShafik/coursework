import datetime
import json
import os
from src.utils import load_operations_data, filter_data_by_date, get_greeting, calculate_card_data, top_five_transact
import requests
from dotenv import load_dotenv

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
    # file_path = '../operations.xlsx'
    file_path = os.path.join(os.path.dirname(__file__), '../operations.xlsx')
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
