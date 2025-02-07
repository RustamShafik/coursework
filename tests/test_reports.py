import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def transactions_data():
    return pd.DataFrame({
        "Дата операции": pd.to_datetime(["2024-01-01", "2024-02-01"]),
        "Категория": ["Фастфуд", "Фастфуд"],
        "Сумма операции": [-500, -200]
    })


def test_spending_by_category(transactions_data):
    result = spending_by_category(transactions_data, "Фастфуд", "2024-02-01")
    assert result["total_spending"] == -700
