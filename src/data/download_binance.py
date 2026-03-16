import requests
import pandas as pd
import time

def download_btc(interval="1h", total_limit=10000):

    print(f"Descargando {total_limit} velas...")

    url = "https://api.binance.com/api/v3/klines"
    symbol = "BTCUSDT"

    all_data = []
    limit_per_request = 1000
    end_time = None

    while len(all_data) < total_limit:

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit_per_request
        }

        if end_time:
            params["endTime"] = end_time

        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            break

        # Insertamos al principio (vamos hacia atrás en el tiempo)
        all_data = data + all_data

        print(f"Descargadas: {len(all_data)}")

        # Próxima iteración termina antes de la primera vela recibida
        end_time = data[0][0] - 1

        time.sleep(0.5)

        if len(data) < limit_per_request:
            break

    all_data = all_data[-total_limit:]

    df = pd.DataFrame(all_data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "num_trades",
        "taker_base_vol", "taker_quote_vol", "ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.set_index("open_time", inplace=True)

    df = df.astype(float)

    print("Descarga completa.")
    print("Total velas:", len(df))

    return df