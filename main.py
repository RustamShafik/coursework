import pandas as pd
import json
from src.reports import spending_by_category
from src.services import search_transactions
from src.views import load_operations_data, get_greeting, calculate_card_data, top_five_transact, get_currency_rates, get_stock_prices, get_dashboard_data

file_path = 'operations.xlsx'
df = load_operations_data(file_path)

# Пример поискового запроса по транзакциям
query = "супермаркеты"
result = search_transactions(df, query)

print(result)

# Указываем дату для фильтрации
query_date = '2021-12-31'  # Пример даты

# Запрос суммы всех трат по категории 'Каршеринг'
category_spending = spending_by_category(df, 'Каршеринг', query_date)

# Выводим результат по категории
print(category_spending)

# Получаем приветствие из функции get_greeting
greeting = get_greeting()
print(f"Приветствие: {greeting}")

# Рассчитываем данные по картам
card_data = calculate_card_data(df)
print(f"Данные по картам: {card_data}")

# Получаем топ-5 транзакций
top_transactions = top_five_transact(df)
print(f"Топ-5 транзакций: {top_transactions}")

# Получаем курсы валют
currency_rates = get_currency_rates()
print(f"Курсы валют: {currency_rates}")

# Получаем цены акций
stock_prices = get_stock_prices()
print(f"Цены акций: {stock_prices}")

# Запрашиваем сводные данные по дате
target_date = '2021-12-20 17:00:00'
dashboard_data = get_dashboard_data(target_date)
print(json.dumps(dashboard_data, ensure_ascii=False, indent=4))
