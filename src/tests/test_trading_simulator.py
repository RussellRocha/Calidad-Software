import pandas as pd
import numpy as np
from src.trading.trading_simulator import simulate_trading


def test_trade_execution():

    df = pd.DataFrame({
        "close": [100, 105, 110, 108, 112]
    })

    signals = [1, 1, 0, 0, 0]

    result = simulate_trading(df, signals, capital=100)

    assert isinstance(result, list)
    assert len(result) == len(df)


def test_balance_changes_after_trade():

    df = pd.DataFrame({
        "close": [100, 110]
    })

    signals = [1, 0]

    result = simulate_trading(df, signals, capital=100)

    assert result[-1] > result[0]