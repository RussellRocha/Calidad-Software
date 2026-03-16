# dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from streamlit_autorefresh import st_autorefresh 

# ========================================
# CONFIGURACIÓN GENERAL
# ========================================

st.set_page_config(layout="wide", page_title="AI Trading Stability Dashboard")
st_autorefresh(interval=900000, key="refresh")  # 15 minutos

st.markdown("""
<style>
.big-font { font-size:20px !important; font-weight:600; }
.metric-card { padding: 10px; border-radius: 10px; background-color: #111827; }
</style>
""", unsafe_allow_html=True)

st.title("📊 AI Trading Model - Stability Dashboard")
st.markdown("---")

# ========================================
# CARGA HISTÓRICA
# ========================================

try:
    df = pd.read_csv("models/backtest_runs.csv")
except:
    st.error("No se encontró models/backtest_runs.csv")
    st.stop()

# ========================================
# SECCIÓN 1 - PRECIO + TRADES
# ========================================

st.header("📈 Price Action & Trade Entries")

try:
    df_price = pd.read_csv("models/last_validation_prices.csv")
    df_trades = pd.read_csv("models/last_trades_detailed.csv")
except:
    st.warning("No hay datos de backtest recientes.")
    st.stop()

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=np.arange(len(df_price)),
    open=df_price["open"],
    high=df_price["high"],
    low=df_price["low"],
    close=df_price["close"],
    name="Price"
))

for _, t in df_trades.iterrows():
    color = "green" if t["side"] == "long" else "red"

    fig.add_scatter(
        x=[t["entry_index"]],
        y=[t["entry_price"]],
        mode="markers",
        marker=dict(color=color, size=9, symbol="circle"),
        showlegend=False
    )

fig.update_layout(
    height=600,
    template="plotly_dark",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ========================================
# SECCIÓN 2 - EQUITY
# ========================================

st.header("📈 Equity Curve")

try:
    df_equity = pd.read_csv("models/last_equity_curve.csv")
    fig_eq = px.line(df_equity, y="equity", template="plotly_dark")
    fig_eq.update_layout(height=400)
    st.plotly_chart(fig_eq, use_container_width=True)
except:
    st.info("No hay equity guardada.")

st.markdown("---")

# ========================================
# SECCIÓN 3 - MÉTRICAS GENERALES
# ========================================

st.header("📊 Global Metrics")

avg_return = df["return_pct"].mean()
best_return = df["return_pct"].max()
worst_return = df["return_pct"].min()
std_return = df["return_pct"].std()
avg_dd = df["max_drawdown"].mean()
avg_wr = df["win_rate"].mean()

initial_capital = 1000
avg_final_capital = df["final_capital"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Capital Inicial", f"${initial_capital:,.0f}")
col2.metric("Capital Final Promedio", f"${avg_final_capital:,.0f}")
col3.metric("Return Promedio", f"{avg_return:.2f}%")
col4.metric("Win Rate Promedio", f"{avg_wr:.2f}%")

col5, col6, col7 = st.columns(3)
col5.metric("Mejor Corrida", f"{best_return:.2f}%")
col6.metric("Peor Corrida", f"{worst_return:.2f}%")
col7.metric("Drawdown Promedio", f"{avg_dd:.2f}%")

st.markdown("---")

# ========================================
# SECCIÓN 4 - EVALUACIÓN
# ========================================

st.header("🧠 Model Evaluation")

if avg_return > 15 and worst_return > -10 and std_return < 15:
    verdict = "🟢 MODELO OPERABLE"
    color = "green"
elif avg_return > 5 and worst_return > -20:
    verdict = "🟡 MODELO EXPERIMENTAL"
    color = "orange"
else:
    verdict = "🔴 MODELO NO ESTABLE"
    color = "red"

st.markdown(f"<h2 style='color:{color};'>{verdict}</h2>", unsafe_allow_html=True)

st.markdown("---")

# ========================================
# SECCIÓN 5 - ESTABILIDAD
# ========================================

if len(df) > 1:

    st.header("📊 Stability Analysis")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("Distribución de Retornos")
        fig1 = px.histogram(df, x="return_pct", nbins=10, template="plotly_dark")
        fig1.update_layout(height=350)
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Drawdown por Corrida")
        fig3 = px.line(df, y="max_drawdown", markers=True, template="plotly_dark")
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)

    with colB:
        st.subheader("Capital Final por Corrida")
        fig2 = px.line(df, y="final_capital", markers=True, template="plotly_dark")
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("⚠ Ejecuta varias corridas para evaluar estabilidad.")

st.markdown("---")

# ========================================
# SECCIÓN 6 - TRADES DETALLADOS
# ========================================

st.header("📋 Detailed Trades")
st.dataframe(df_trades, use_container_width=True)

st.markdown("---")

# ========================================
# SECCIÓN 7 - SEÑAL EN TIEMPO REAL
# ========================================

st.header("📡 Live Signal")

signal_path = "models/live_signal.json"

if os.path.exists(signal_path):
    with open(signal_path, "r") as f:
        signal = json.load(f)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Señal Actual: {signal['signal']}")
        st.write(f"Última actualización: {signal['timestamp']}")

    with col2:
        st.subheader("Probabilidades")

        st.write("LONG")
        st.progress(signal["long_prob"])

        st.write("SHORT")
        st.progress(signal["short_prob"])

        st.write("HOLD")
        st.progress(signal["hold_prob"])

else:
    st.warning("Aún no hay señal generada.")

st.markdown("---")

# ========================================
# SECCIÓN 8 - RECOMENDACIÓN OPERATIVA
# ========================================

st.header("📌 Operational Recommendation")

if verdict == "🟢 MODELO OPERABLE":
    st.success("Operar con 1% de riesgo por trade.")
elif verdict == "🟡 MODELO EXPERIMENTAL":
    st.warning("Operar con 0.5% de riesgo por trade y monitoreo constante.")
else:
    st.error("No operar en real todavía.")