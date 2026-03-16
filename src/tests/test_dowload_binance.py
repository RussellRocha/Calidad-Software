import pandas as pd
from src.data.download_binance import download_btc


def test_download_returns_dataframe():
    df = download_btc()

    assert isinstance(df, pd.DataFrame)


def test_dataframe_not_empty():
    df = download_btc()

    assert len(df) > 0