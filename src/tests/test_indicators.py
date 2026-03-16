import pandas as pd
from src.features.technical_indicators import add_indicators


def test_indicators_added():
    df = pd.read_csv("data/btc_data.csv")

    df_ind = add_indicators(df)

    assert len(df_ind.columns) > len(df.columns)


def test_no_nan_after_indicators():
    df = pd.read_csv("data/btc_data.csv")

    df_ind = add_indicators(df)

    assert df_ind.isnull().sum().sum() == 0