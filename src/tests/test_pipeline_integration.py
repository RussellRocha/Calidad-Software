import pandas as pd
import numpy as np

from src.data.download_binance import download_btc
from src.features.technical_indicators import add_indicators
from src.ai.lstm_model import build_model
from src.trading.price_predictor import expected_range
from src.trading.trading_simulator import simulate_trading


def test_full_pipeline():

    # 1️⃣ descargar datos
    df = download_btc()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

    # 2️⃣ generar indicadores
    df = add_indicators(df)

    assert "close" in df.columns

    # 3️⃣ construir modelo
    model = build_model((50, 10))

    assert model is not None

    # 4️⃣ calcular rango esperado
    price_range = expected_range(df)

    assert "min" in price_range
    assert "max" in price_range

    # 5️⃣ generar señales falsas (mock)
    signals = np.random.randint(0, 2, len(df))

    # 6️⃣ simular trading
    history = simulate_trading(df, signals)

    assert isinstance(history, list)
    assert len(history) == len(df)