from sklearn.preprocessing import MinMaxScaler
import joblib
import os
import numpy as np
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping
from .lstm_model import build_model
from ..trading.realistic_backtest import realistic_futures_backtest 

def train_lstm(df):

    # =====================================
    # BINARIO REAL
    # =====================================
    df = df[df["target"] != 1].copy()
    df["binary_target"] = (df["target"] == 2).astype(int)

    print("\n🔎 Distribución binaria:")
    print(df["binary_target"].value_counts(normalize=True))

    features = [c for c in df.columns if c not in ["time", "target", "future_return", "binary_target"]]

    scaler = MinMaxScaler()
    X = scaler.fit_transform(df[features])
    y = df["binary_target"].values

    os.makedirs("models", exist_ok=True)
    joblib.dump(scaler, "models/scaler.save")

    # =====================================
    # SECUENCIAS
    # =====================================
    window = 72
    X_seq, y_seq = [], []

    for i in range(window, len(X)):
        X_seq.append(X[i - window:i])
        y_seq.append(y[i])

    X_seq = np.array(X_seq)
    y_seq = np.array(y_seq)

    split = int(len(X_seq) * 0.8)

    X_train = X_seq[:split]
    X_val = X_seq[split:]

    y_train = y_seq[:split]
    y_val = y_seq[split:]

    print("\n📐 Shapes:")
    print("Shape X_train:", X_train.shape)
    print("Shape X_val:", X_val.shape)

    # =====================================
    # MODELO BINARIO
    # =====================================
    model = build_model((X_train.shape[1], X_train.shape[2]), binary=True)

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        callbacks=[early_stop]
    )

    model.save("models/lstm_trading_model.keras")
    print("\n✅ Modelo guardado")

    # =====================================
    # PREDICCIONES BINARIAS
    # =====================================
    probs = model.predict(X_val).reshape(-1)

    confidence_threshold = 0.60

    preds = np.where(probs > confidence_threshold, 1, 0)

    df_val = df.iloc[window + split : window + split + len(preds)].reset_index(drop=True)

    # =====================================
    # BACKTEST
    # =====================================
    results = realistic_futures_backtest(
        df_val,
        preds,
        initial_capital=1000,
        risk_per_trade=0.05,
        sl_pct=0.01,
        tp_pct=0.03,
        commission=0,
        slippage=0
    )

    print("\n===== BACKTEST RESULTS =====")
    print("Final Capital:", results["final_capital"])
    print("Return %:", results["return_pct"])
    print("Total Trades:", len(results["trades"]))