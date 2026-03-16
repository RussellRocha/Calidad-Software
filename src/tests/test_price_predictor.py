import pandas as pd
import numpy as np
from src.trading.price_predictor import expected_range


def test_expected_range_returns_dict():

    df = pd.DataFrame({
        "close": np.random.rand(100) * 100
    })

    result = expected_range(df)

    assert isinstance(result, dict)


def test_expected_range_keys():

    df = pd.DataFrame({
        "close": np.random.rand(100) * 100
    })

    result = expected_range(df)

    assert "min" in result
    assert "max" in result


def test_expected_range_values():

    df = pd.DataFrame({
        "close": np.random.rand(100) * 100
    })

    result = expected_range(df)

    assert result["min"] < result["max"]