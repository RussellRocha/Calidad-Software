import numpy as np
import pandas as pd
import joblib
import requests
import tensorflow as tf
from src.features.technical_indicators import add_indicators
import json
from datetime import datetime

SEQ_LENGTH = 72
SYMBOL = "BTCUSDT"
INTERVAL = "15m"
LIMIT = 500  # descargamos suficiente para generar features

def get_latest_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": LIMIT
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp","open","high","low","close","volume",
        "close_time","qav","num_trades",
        "taker_base_vol","taker_quote_vol","ignore"
    ])

    # convertir todo menos timestamp
    numeric_cols = df.columns.drop("timestamp")
    df[numeric_cols] = df[numeric_cols].astype(float)

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": LIMIT
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp","open","high","low","close","volume",
        "close_time","qav","num_trades",
        "taker_base_vol","taker_quote_vol","ignore"
    ])

    df = df[["timestamp","open","high","low","close","volume"]]
    df = df.astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df

def predict_live():
    print("Descargando datos actuales...")

    # 1️⃣ Descargar datos
    df = get_latest_data()
    df = add_indicators(df)

    # 2️⃣ Cargar scaler y modelo
    scaler = joblib.load("models/scaler.save")  # ojo con el nombre real
    model = tf.keras.models.load_model("models/lstm_trading_model.h5")

    # 3️⃣ Mantener exactamente las columnas usadas en entrenamiento
    df = df[scaler.feature_names_in_]

    # 4️⃣ Escalar
    features_scaled = scaler.transform(df)

    # 5️⃣ Crear secuencia
    X_live = features_scaled[-SEQ_LENGTH:]
    X_live = np.expand_dims(X_live, axis=0)

    # 6️⃣ Predecir
    prediction = model.predict(X_live)[0]
    predicted_class = np.argmax(prediction)

    signal_map = {
        0: "SHORT",
        1: "HOLD",
        2: "LONG"
    }

    print("\n===== SEÑAL ACTUAL =====")
    print("Señal:", signal_map[predicted_class])
    print("Probabilidades:")
    print(f"SHORT: {prediction[0]*100:.2f}%")
    print(f"HOLD : {prediction[1]*100:.2f}%")
    print(f"LONG : {prediction[2]*100:.2f}%")
    print("Descargando datos actuales...")

    df = get_latest_data()
    df = add_indicators(df)
    df = df[scaler.feature_names_in_]

    scaler = joblib.load("models/scaler.save")
    model = tf.keras.models.load_model("models/lstm_trading_model.h5")

    features_scaled = scaler.transform(df)

    X_live = features_scaled[-SEQ_LENGTH:]
    X_live = np.expand_dims(X_live, axis=0)

    prediction = model.predict(X_live)[0]
    predicted_class = np.argmax(prediction)

    signal_map = {
        0: "SHORT",
        1: "HOLD",
        2: "LONG"
    }

    print("\n===== SEÑAL ACTUAL =====")
    print("Señal:", signal_map[predicted_class])
    print("Probabilidades:")
    print(f"SHORT: {prediction[0]*100:.2f}%")
    print(f"HOLD : {prediction[1]*100:.2f}%")
    print(f"LONG : {prediction[2]*100:.2f}%")
    
    # Guardar señal en archivo
    signal_data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "signal": signal_map[predicted_class],
        "short_prob": float(prediction[0]),
        "hold_prob": float(prediction[1]),
        "long_prob": float(prediction[2])
    }

    with open("models/live_signal.json", "w") as f:
        json.dump(signal_data, f, indent=4)

    print("Señal guardada en models/live_signal.json")



if __name__ == "__main__":
    predict_live()

