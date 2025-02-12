import pandas as pd
import pytest

from src.services import search_transactions


@pytest.fixture
def sample_transactions():
    data = {
        "Описание": ["Супермаркеты", "Кафе", "Такси", "Каршеринг"],
        "Категория": ["Продукты", "Рестораны", "Транспорт", "Транспорт"],
        "Сумма операции": [-500, -300, -100, -200]
    }
    return pd.DataFrame(data)


def test_search_transactions_found(sample_transactions):
    result = search_transactions(sample_transactions, "супермаркеты")
    assert '"Описание": "Супермаркеты"' in result


def test_search_transactions_not_found(sample_transactions):
    result = search_transactions(sample_transactions, "аптека")
    assert "[]" in result
