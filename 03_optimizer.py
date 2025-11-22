import yfinance as yf
import pandas as pd
import numpy as np

print("--- STRATEGY PARAMETER OPTIMIZER ---")

# 1. SETUP
ticker = input("Enter JSE Stock to Optimize (e.g. NPN): ").strip().upper()
if not ticker.endswith(".JO"): ticker += ".JO"

print("Downloading data... this may take a moment.")
df_raw = yf.download(ticker, start="2015-01-01", progress=False).dropna()

results = []

# 2. DEFINE SEARCH SPACE
# We will test Short MA from 10 to 60
# We will test Long MA from 100 to 260
short_range = range(10, 70, 10)
long_range = range(100, 270, 10)

total_tests = len(short_range) * len(long_range)
print(f"Running {total_tests} simulations...")

# 3. OPTIMIZATION LOOP
for short_ma in short_range:
    for long_ma in long_range:
        
        # Create a fresh copy for this test
        df = df_raw.copy()
        
        # Logic
        df['Short'] = df['Close'].rolling(window=short_ma).mean()
        df['Long'] = df['Close'].rolling(window=long_ma).mean()
        
        df['Signal'] = np.where(df['Short'] > df['Long'], 1, 0)
        df['Position'] = df['Signal'].shift(1)
        
        # Returns
        df['Strat_Ret'] = df['Position'] * np.log(df['Close'] / df['Close'].shift(1))
        
        # Calculate Final Cumulative Return
        total_return = np.exp(df['Strat_Ret'].cumsum().iloc[-1]) - 1
        
        results.append({
            'Short': short_ma,
            'Long': long_ma,
            'Return': total_return
        })

# 4. ANALYSIS
results_df = pd.DataFrame(results)
best_run = results_df.loc[results_df['Return'].idxmax()]

buy_hold_return = np.exp(np.log(df_raw['Close'] / df_raw['Close'].shift(1)).cumsum().iloc[-1]) - 1

print("\n" + "="*40)
print(f"OPTIMAL PARAMETERS FOR {ticker}")
print("="*40)
print(f"Best Combination: {int(best_run['Short'])} (Short) / {int(best_run['Long'])} (Long)")
print(f"Strategy Return:  {best_run['Return']*100:.2f}%")
print(f"Buy & Hold:       {buy_hold_return*100:.2f}%")

if best_run['Return'] > buy_hold_return:
    print("The Optimizer found a winning strategy!")
else:
    print("Even the best parameters could not beat Buy & Hold.")

print("\nNOTE: Past performance (Overfitting) does not guarantee future results.")