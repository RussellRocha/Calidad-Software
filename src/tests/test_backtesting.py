import pandas as pd
import numpy as np
from src.trading.backtesting import futures_backtest


def test_backtest_runs():

    df = pd.DataFrame({
        "close": np.random.rand(100)*100
    })

    preds = np.random.rand(100)

    result = futures_backtest(df, preds)

    assert result is not None