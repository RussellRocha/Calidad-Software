import numpy as np
import pandas as pd

def realistic_futures_backtest(
    df,
    preds,
    initial_capital=1000,
    risk_per_trade=0.01,
    sl_pct=0.01,
    tp_pct=0.02,
    commission=0.00075,
    slippage=0.0005
):

    capital = initial_capital
    equity_curve = []
    trades = []
    position = None

    for i in range(len(preds)):

        price = df.iloc[i]["close"]
        signal = preds[i]  # 0 short | 1 long

        # ================= ENTRY =================
        if position is None:

            side = "long" if signal == 1 else "short"

            entry_price = price * (
                1 + slippage if side == "long"
                else 1 - slippage
            )

            position = {
                "side": side,
                "entry_price": entry_price,
                "entry_index": i
            }

        # ================= MANAGE =================
        else:

            side = position["side"]
            entry_price = position["entry_price"]

            if side == "long":
                change = (price - entry_price) / entry_price
            else:
                change = (entry_price - price) / entry_price

            exit_trade = False

            # SL
            if change <= -sl_pct:
                exit_trade = True

            # TP
            elif change >= tp_pct:
                exit_trade = True

            # Señal contraria
            elif (side == "long" and signal == 0) or \
                 (side == "short" and signal == 1):
                exit_trade = True

            if exit_trade:

                exit_price = price * (
                    1 - slippage if side == "long"
                    else 1 + slippage
                )

                raw_pnl = (
                    exit_price - entry_price
                    if side == "long"
                    else entry_price - exit_price
                )

                raw_pnl_pct = raw_pnl / entry_price
                raw_pnl_pct -= commission * 2

                trade_risk_amount = capital * risk_per_trade
                profit = trade_risk_amount * raw_pnl_pct

                capital += profit

                trades.append({
                    "side": side,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "pnl_usd": profit,
                    "capital_after": capital
                })

                position = None

        equity_curve.append(capital)

    return {
        "final_capital": capital,
        "return_pct": (capital / initial_capital - 1) * 100,
        "equity_curve": equity_curve,
        "trades": trades
    }