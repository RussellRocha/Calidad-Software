import numpy as np

def simulate_trading(df, signals, capital=100):

    balance = capital
    position = 0

    history = []

    for price, signal in zip(df["close"], signals):

        if signal == 1 and balance > 0:
            position = balance / price
            balance = 0

        elif signal == 0 and position > 0:
            balance = position * price
            position = 0

        total = balance + position * price
        history.append(total)

    return history
