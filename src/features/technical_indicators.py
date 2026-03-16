
import numpy as np
import pandas as pd

def compute_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs = gain.rolling(period).mean() / loss.rolling(period).mean()
    return 100 - (100 / (1 + rs))

def add_indicators(df):

    df["EMA9"] = df["close"].ewm(span=9).mean()
    df["EMA21"] = df["close"].ewm(span=21).mean()
    df["EMA50"] = df["close"].ewm(span=50).mean()

    df["RSI"] = compute_rsi(df["close"])

    df["MACD"] = df["close"].ewm(12).mean() - df["close"].ewm(26).mean()

    df["ATR"] = (df["high"] - df["low"]).rolling(14).mean()

    df["BB_UPPER"] = df["close"].rolling(20).mean() + 2*df["close"].rolling(20).std()
    df["BB_LOWER"] = df["close"].rolling(20).mean() - 2*df["close"].rolling(20).std()

    df["VOL_CHANGE"] = df["volume"].pct_change()

    df["future_return"] = df["close"].shift(-12) / df["close"] - 1

    threshold = 0.0075  # 0.2% para 15m (ajustable)

    # 0 = SHORT
    # 1 = HOLD
    # 2 = LONG

    df["target"] = 1  # default HOLD

    df.loc[df["future_return"] > threshold, "target"] = 2
    df.loc[df["future_return"] < -threshold, "target"] = 0

    df = df.dropna().reset_index(drop=True)
    
    # Bollinger
    ma20 = df['close'].rolling(20).mean()
    std20 = df['close'].rolling(20).std()
    df['bb_upper'] = ma20 + 2 * std20
    df['bb_lower'] = ma20 - 2 * std20

    # Volatilidad
    df['volatility'] = df['close'].pct_change().rolling(10).std()
    df.dropna(inplace=True)

    return df
