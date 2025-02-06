import pandas as pd
from services import search_transactions
from views import load_operations_data

file_path = '../operations.xlsx'
df = load_operations_data(file_path)

query = "супермаркеты"
result = search_transactions(df, query)

print(result)