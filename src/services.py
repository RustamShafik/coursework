import json
import logging

# Настройка логгера для записи в файл app.search.log
logging.basicConfig(
    filename='app.search.log',  # Логи будут записываться в файл app.search.log
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат лог-сообщений
)


def search_transactions(df, query):
    """
    Ищет транзакции, содержащие запрос в описании или категории.

    Аргументы:
    df (pandas.DataFrame): Данные о транзакциях.
    query (str): Поисковый запрос.

    Возвращает:
    str: JSON-ответ со списком найденных транзакций.
    """
    # Логгируем начало поиска
    logging.info(f"Начинаем поиск транзакций по запросу: {query}")

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

    filtered_transactions_list = list(filtered_transactions)

    # Логгируем количество найденных транзакций
    logging.info(f"Найдено {len(filtered_transactions_list)} транзакций по запросу '{query}'.")

    # Если транзакции не найдены, записываем предупреждение
    if len(filtered_transactions_list) == 0:
        logging.warning(f"По запросу '{query}' не найдено ни одной транзакции.")

    # Преобразуем результат в JSON и возвращаем
    result = json.dumps(filtered_transactions_list, ensure_ascii=False,
                        indent=4) if filtered_transactions_list else '[]'

    # Логгируем результат, который возвращается
    logging.info(f"Результат поиска: {result}")

    return result
