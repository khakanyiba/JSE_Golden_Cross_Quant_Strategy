import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- CONFIGURATION ---
# Create the output folder if it doesn't exist
folder_name = "output"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# List of JSE Tickers to Scan (Banks, Mining, Retail, Tech)
tickers = [
    'FSR.JO', 'SBK.JO', 'NED.JO', 'ABG.JO', 'CPI.JO', # Banks
    'NPN.JO', 'PRX.JO', 'MTN.JO', 'VOD.JO',           # Tech & Telco
    'SSW.JO', 'GFI.JO', 'ANG.JO', 'SOL.JO', 'IMP.JO', # Resources
    'SHP.JO', 'WHL.JO', 'PIK.JO', 'SPP.JO'            # Retail
]

print(f"--- STARTING JSE SCAN ({len(tickers)} Stocks) ---\n")

for ticker in tickers:
    try:
        # Download last 2 years of data (minimal data needed for 200MA)
        df = yf.download(ticker, start="2023-01-01", progress=False)
        
        if len(df) < 200:
            continue # Skip if stock is too new

        # Calculate Moving Averages
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()

        # Get values for Today (-1) and Yesterday (-2)
        curr_50 = df['MA50'].iloc[-1].item()
        curr_200 = df['MA200'].iloc[-1].item()
        prev_50 = df['MA50'].iloc[-2].item()
        prev_200 = df['MA200'].iloc[-2].item()

        signal_type = None

        # CHECK FOR GOLDEN CROSS (50 crosses ABOVE 200)
        if prev_50 < prev_200 and curr_50 > curr_200:
            signal_type = "GOLDEN_CROSS"
            print(f"ALERT: {ticker} just triggered a GOLDEN CROSS!")

        # CHECK FOR DEATH CROSS (50 crosses BELOW 200)
        elif prev_50 > prev_200 and curr_50 < curr_200:
            signal_type = "DEATH_CROSS"
            print(f"ALERT: {ticker} just triggered a DEATH CROSS!")

        # IF SIGNAL FOUND, PLOT AND SAVE
        if signal_type:
            plt.figure(figsize=(12, 6))
            plt.plot(df.index, df['Close'], label='Price', color='black', alpha=0.3)
            plt.plot(df.index, df['MA50'], label='50-Day MA', color='green', linewidth=2)
            plt.plot(df.index, df['MA200'], label='200-Day MA', color='red', linewidth=2)
            plt.title(f"{ticker} - {signal_type} Detected")
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Save to output folder
            filename = f"{folder_name}/{ticker}_{signal_type}.png"
            plt.savefig(filename)
            plt.close()
            print(f"   -> Chart saved to: {filename}")

    except Exception as e:
        print(f"Error processing {ticker}: {e}")

print("\n--- SCAN COMPLETE ---")