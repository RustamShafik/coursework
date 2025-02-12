import pandas as pd

from src.reports import spending_by_category
from src.services import search_transactions
from src.utils import load_operations_data

file_path = 'operations.xlsx'
df = load_operations_data(file_path)

query = "супермаркеты"
result = search_transactions(df, query)

print(result)

# Указываем дату для фильтрации
query_date = '2021-12-31'  # Пример даты

# Запрос суммы всех трат по категории 'Фастфуд'
category_spending = spending_by_category(df, 'Каршеринг', query_date)

# Выводим результат
print(category_spending)