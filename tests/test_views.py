from io import StringIO

import pandas as pd
import pytest

from src.views import filter_data_by_date, load_operations_data


@pytest.fixture
def sample_excel():
    data = """Дата операции,Сумма операции,Категория
    2024-01-10,-500,Продукты
    2024-01-15,-200,Кафе
    """
    return StringIO(data)

def test_filter_data_by_date():
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2024-01-05", "2024-01-15", "2024-01-20"]),
        "Сумма операции": [-100, -200, -300]
    })
    result = filter_data_by_date(df, pd.Timestamp("2024-01-15"))
    assert len(result) == 2
