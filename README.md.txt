# JSE Golden Cross: Quantitative Analysis Suite

## Project Overview
This project is a quantitative trading suite designed to analyze trend-following strategies on the **Johannesburg Stock Exchange (JSE)**. 

It automates the detection of "Golden Cross" and "Death Cross" signals across major South African sectors (Banking, Mining, Tech, Retail) and includes a vectorized backtesting engine to validate the strategy's historical performance against a "Buy & Hold" benchmark.

**Core Tech Stack:** Python, Pandas (Vectorized), Matplotlib, yfinance API.

---

## The Strategy
The project implements a classic Momentum / Trend Following strategy:
* **Signal:** Crossover of Short-Term and Long-Term Simple Moving Averages (SMA).
* **Golden Cross (Buy):** When the 50-Day SMA crosses *above* the 200-Day SMA.
* **Death Cross (Sell):** When the 50-Day SMA crosses *below* the 200-Day SMA.
* **Hypothesis:** We aim to capture long-duration trends in the South African market while moving to cash during prolonged bear markets (e.g., 2018, 2020).

---

## Repository Structure

### 1. `01_jse_scanner.py` (The Automation)
* **Function:** Scans a watchlist of JSE stocks (e.g., FSR.JO, NPN.JO, SSW.JO) for signals occurring *today*.
* **Output:** If a signal is detected, it automatically generates and saves a technical chart to the `output/` folder for visual inspection.
* **Use Case:** Intended to be run as a daily Cron job/Task Scheduler script.

### 2. `02_backtester.py` (The Validation)
* **Function:** An interactive CLI tool that simulates the strategy over the last 10 years.
* **Key Feature:** Uses **Vectorized Operations** (NumPy/Pandas) for high-speed processing.
* **Risk Management:** Code specifically adjusts for **Look-Ahead Bias** by shifting signals (trading on $T+1$ Open rather than $T$ Close).

### 3. `03_optimizer.py` (The Research)
* **Function:** Runs a grid search over 500+ parameter combinations (e.g., 10/50, 20/100, 40/150) to find the optimal sensitivity for specific assets.
* **Goal:** To determine if the standard "50/200" convention fits the volatility profile of emerging market stocks like Sasol (SOL) or Sibanye (SSW).

---

## 🇿🇦 South African Market Insights
During the development of this project, several market-specific observations were made:

1.  **Sector Variance:** The strategy performs well on banking stocks (FirstRand, Standard Bank) which tend to have smoother trends linked to interest rate cycles.
2.  **Volatility Drag:** On high-beta mining stocks (Sibanye Stillwater), the standard 50/200 parameters often result in "Whipsaws" (false signals), leading to underperformance against Buy & Hold.
3.  **Naspers (NPN) Case Study:** Backtesting revealed that despite NPN's massive growth, the moving average strategy lagged the benchmark due to the stock's sharp "V-shaped" recoveries, which lagging indicators fail to catch in time.

---

## How to Run

**1. Prerequisites**
Install the required libraries:
```bash
pip install -r requirements.txt