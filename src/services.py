import json

def search_transactions(df, query):
    """
    Ищет транзакции, содержащие запрос в описании или категории.

    Аргументы:
    df (pandas.DataFrame): Данные о транзакциях.
    query (str): Поисковый запрос.

    Возвращает:
    str: JSON-ответ со списком найденных транзакций.
    """
    query = query.lower()  # Приводим запрос к нижнему регистру

    # Приводим столбцы "Описание" и "Категория" к строковому типу и удаляем лишние пробелы
    df['Описание'] = df['Описание'].astype(str).str.strip()
    df['Категория'] = df['Категория'].astype(str).str.strip()

    # Преобразуем все столбцы с типом Timestamp в строку
    for column in df.select_dtypes(include=['datetime64']).columns:
        df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Фильтруем транзакции с помощью filter и lambda
    filtered_transactions = filter(
        lambda row: query in str(row['Описание']).lower() or query in str(row['Категория']).lower(),
        df.to_dict(orient="records")
    )

    # Преобразуем результат в JSON
    return json.dumps(list(filtered_transactions), ensure_ascii=False, indent=4)
