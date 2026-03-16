def futures_backtest(
    df,
    preds,
    initial_capital=1000,
    risk_per_trade=0.01,
    leverage=5,
    stop_loss=0.004,
    take_profit=0.008,
    fee=0.0008
):

    capital = initial_capital
    equity_curve = []

    position = None
    entry_price = 0
    entry_index = 0

    trades = []

    total_trades = 0
    winning_trades = 0

    for i in range(len(preds)):

        price = df.iloc[i]["close"]
        signal = preds[i]

        if position is None:

            if signal == 2:
                entry_price = price
                entry_index = i
                position = "long"

            elif signal == 0:
                entry_price = price
                entry_index = i
                position = "short"

        else:

            if position == "long":
                change = (price - entry_price) / entry_price
            else:
                change = (entry_price - price) / entry_price

            # Stop
            if change <= -stop_loss:
                capital -= capital * risk_per_trade
                capital -= capital * fee
                trades.append((entry_index, i, position, "SL"))
                total_trades += 1
                position = None

            # Take Profit
            elif change >= take_profit:
                capital += capital * risk_per_trade * 2
                capital -= capital * fee
                trades.append((entry_index, i, position, "TP"))
                total_trades += 1
                winning_trades += 1
                position = None

        equity_curve.append(capital)

    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    import numpy as np

    equity_array = np.array(equity_curve)
    peak = np.maximum.accumulate(equity_array)
    drawdown = (equity_array - peak) / peak
    max_drawdown = drawdown.min() * 100

    return {
        "final_capital": capital,
        "return_pct": (capital / initial_capital - 1) * 100,
        "equity_curve": equity_curve,
        "trades": trades,
        "win_rate": win_rate,
        "total_trades": total_trades,
        "max_drawdown": max_drawdown
    }