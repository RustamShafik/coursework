import datetime
from io import StringIO
import pandas as pd
import pytest
from unittest.mock import patch
from src.views import (
    load_operations_data,
    top_five_transact,
    filter_data_by_date,
    calculate_card_data,
    get_currency_rates,
    get_stock_prices,
    get_dashboard_data,
    get_greeting
)


# Тестирование функции load_operations_data с Mock
@pytest.fixture
def mock_excel_data():
    # Мокируем данные из Excel
    return pd.DataFrame({
        "Дата операции": pd.to_datetime(["2024-01-01", "2024-01-05"]),
        "Сумма операции": [-100, -200],
        "Категория": ["Продукты", "Кафе"]
    })

# Тестирование функции filter_data_by_date с пустым DataFrame
def test_filter_data_by_date_empty():
    df = pd.DataFrame(columns=["Дата операции", "Сумма операции"])
    result = filter_data_by_date(df, pd.Timestamp("2024-01-15"))
    assert result.empty

# Тестирование функции calculate_card_data с пустыми данными
def test_calculate_card_data_empty():
    df = pd.DataFrame(columns=["Номер карты", "Сумма операции", "Статус"])
    result = calculate_card_data(df)
    assert result == []  # Ожидаем пустой список

# Тестирование функции filter_data_by_date
def test_filter_data_by_date():
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2024-01-05", "2024-01-15", "2024-01-20"]),
        "Сумма операции": [-100, -200, -300]
    })
    result = filter_data_by_date(df, pd.Timestamp("2024-01-15"))
    assert len(result) == 2


# Тестирование функции calculate_card_data с параметризацией
@pytest.mark.parametrize(
    "input_data, expected_result",
    [
        (
                pd.DataFrame({
                    "Номер карты": ["1234567890123456", "1234567890123456"],
                    "Сумма операции": [-100, -200],
                    "Статус": ["OK", "OK"]
                }),
                [{"last_digits": "3456", "total_spent": 300.0, "cashback": 3.0}]
        ),
        (
                pd.DataFrame({
                    "Номер карты": ["1234567890123456", "1234567890123456"],
                    "Сумма операции": [100, 200],
                    "Статус": ["OK", "OK"]
                }),
                [{"last_digits": "3456", "total_spent": 0.0, "cashback": 0.0}]
        )
    ]
)
def test_calculate_card_data(input_data, expected_result):
    result = calculate_card_data(input_data)
    assert result == expected_result


# Тестирование функции get_currency_rates с Mock для внешнего API-запроса
@pytest.fixture
def mock_currency_data():
    return {
        "rates": {
            "RUB": 75.0
        }
    }


@patch("requests.get")
def test_get_currency_rates(mock_get, mock_currency_data):
    mock_get.return_value.json.return_value = mock_currency_data

    result = get_currency_rates()
    assert "currency_rates" in result
    assert result["currency_rates"][0]["currency"] == "USD"
    assert result["currency_rates"][0]["rate"] == 75.0


# Тестирование функции get_stock_prices с Mock для внешнего API-запроса
@pytest.fixture
def mock_stock_data():
    return {
        "data": [
            {"symbol": "AAPL", "close": 150.0},
            {"symbol": "GOOGL", "close": 2700.0}
        ]
    }


@patch("requests.get")
def test_get_stock_prices(mock_get, mock_stock_data):
    mock_get.return_value.json.return_value = mock_stock_data

    result = get_stock_prices()
    assert "stock_prices" in result
    assert len(result["stock_prices"]) == 5
    assert result["stock_prices"][0]["stock"] == "AAPL"
    assert result["stock_prices"][0]["price"] == 150.0


# Тестирование функции get_dashboard_data с Mock
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
@patch("src.views.calculate_card_data")
@patch("src.views.top_five_transact")
@patch("src.views.get_greeting")
def test_get_dashboard_data(mock_greeting, mock_top_transact, mock_card_data, mock_stock_prices, mock_currency_rates):
    # Мокируем возвращаемые значения для зависимых функций
    mock_greeting.return_value = "Доброе утро"
    mock_top_transact.return_value = [
        {"date": "01.01.2024", "amount": -100, "category": "Продукты", "description": "Продуктовый магазин"}]
    mock_card_data.return_value = [{"last_digits": "3456", "total_spent": 300.0, "cashback": 3.0}]
    mock_currency_rates.return_value = {"currency_rates": [{"currency": "USD", "rate": 75.0}]}
    mock_stock_prices.return_value = {"stock_prices": [{"stock": "AAPL", "price": 150.0}]}

    target_date = "2024-01-10 10:00:00"
    result = get_dashboard_data(target_date)

    # Проверяем, что результат не пустой и содержит необходимые данные
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result

    # Проверяем, что возвращенные данные соответствуют ожидаемым
    assert result["greeting"] == "Доброе утро"
    assert result["cards"][0]["total_spent"] == 300.0
    assert result["currency_rates"][0]["rate"] == 75.0
    assert result["stock_prices"][0]["price"] == 150.0

# Тестирование функции get_currency_rates с пустым ответом от API
@patch("requests.get")
def test_get_currency_rates_empty(mock_get):
    mock_get.return_value.json.return_value = {"rates": {}}

    result = get_currency_rates()
    assert "currency_rates" in result
    assert len(result["currency_rates"]) == 0  # Ожидаем пустой список


# Тестирование функции get_stock_prices с пустым ответом от API
@patch("requests.get")
def test_get_stock_prices_empty(mock_get):
    mock_get.return_value.json.return_value = {"data": []}

    result = get_stock_prices()
    assert "stock_prices" in result
    assert len(result["stock_prices"]) == 0  # Ожидаем пустой список


from io import StringIO
import pandas as pd
import pytest
from unittest.mock import patch
from src.views import (
    load_operations_data,
    filter_data_by_date,
    calculate_card_data,
    get_currency_rates,
    get_stock_prices,
    get_dashboard_data,
    get_greeting
)

def test_top_five_transact_less_than_five():
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2024-01-01", "2024-01-05"]),
        "Сумма операции": [-100, -200],
        "Категория": ["Продукты", "Кафе"],
        "Описание": ["Продуктовый магазин", "Кафе"]
    })
    result = top_five_transact(df)
    assert len(result) == 2  # Ожидаем 2 транзакции, так как их меньше 5





