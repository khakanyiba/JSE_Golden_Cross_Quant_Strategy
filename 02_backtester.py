import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("--- JSE INTERACTIVE BACKTESTER ---")

# 1. USER INPUTS
ticker = input("Enter JSE Stock Code (e.g. FSR, SOL): ").strip().upper()
if not ticker.endswith(".JO"): ticker += ".JO"

try:
    short_window = int(input("Short MA (Default 50): ") or 50)
    long_window = int(input("Long MA (Default 200): ") or 200)
except ValueError:
    short_window, long_window = 50, 200

print(f"\nDownloading data for {ticker}...")

# 2. GET DATA
# We download 10 years to get a good sample size
df = yf.download(ticker, start="2014-01-01", progress=False)

if len(df) == 0:
    print("Error: No data found. Check ticker symbol.")
    exit()

df = df.dropna()

# 3. STRATEGY LOGIC
df['Short_MA'] = df['Close'].rolling(window=short_window).mean()
df['Long_MA'] = df['Close'].rolling(window=long_window).mean()

# Signal: 1 = Buy, 0 = Sell (Cash)
df['Signal'] = np.where(df['Short_MA'] > df['Long_MA'], 1, 0)

# SHIFT THE SIGNAL: We trade the DAY AFTER the signal (Avoid Look-Ahead Bias)
df['Position'] = df['Signal'].shift(1)

# 4. CALCULATE RETURNS
# Log returns are additive and safer for math
df['Market_Log_Ret'] = np.log(df['Close'] / df['Close'].shift(1))
df['Strategy_Log_Ret'] = df['Position'] * df['Market_Log_Ret']

# Convert back to cumulative percentage growth
df['Market_Cum'] = df['Market_Log_Ret'].cumsum().apply(np.exp)
df['Strategy_Cum'] = df['Strategy_Log_Ret'].cumsum().apply(np.exp)

# 5. RESULTS
final_strat = (df['Strategy_Cum'].iloc[-1] - 1) * 100
final_market = (df['Market_Cum'].iloc[-1] - 1) * 100

print("\n" + "="*30)
print(f"RESULTS FOR {ticker}")
print("="*30)
print(f"Strategy Return: {final_strat:.2f}%")
print(f"Buy & Hold:      {final_market:.2f}%")

if final_strat > final_market:
    print("OUTPERFORMANCE: Strategy won.")
else:
    print("UNDERPERFORMANCE: Buy & Hold won.")

# 6. PLOT
plt.figure(figsize=(12, 6))
plt.plot(df['Market_Cum'], label='Buy & Hold', color='grey', alpha=0.5)
plt.plot(df['Strategy_Cum'], label=f'Strategy ({short_window}/{long_window})', color='blue', linewidth=2)
plt.title(f"Backtest: {ticker} vs Moving Average Strategy")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()