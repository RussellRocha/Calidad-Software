from src.data.download_binance import download_btc
from src.features.technical_indicators import add_indicators
from src.ai.train_model import train_lstm

df = download_btc(interval="1h", total_limit=10000)
df = add_indicators(df)

train_lstm(df)