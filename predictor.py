import requests
import numpy as np
import pandas as pd

def fetch_historical_data(ticker, period="1mo"):
    try:
        symbol = ticker if ticker.endswith('.JK') else f"{ticker}.JK"
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range={period}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        result = data['chart']['result'][0]
        closes = result['indicators']['quote'][0]['close']
        timestamps = result['timestamp']
        
        df = pd.DataFrame({'Close': closes}, index=pd.to_datetime(timestamps, unit='s'))
        df = df.dropna()
        return df
    except Exception as e:
        print(f"Error fetching historical data for {ticker}:", e)
        return None

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def predict_next_week(ticker):
    print(f"Analisis & Prediksi untuk {ticker}...")
    df = fetch_historical_data(ticker, period="3mo")
    if df is None or len(df) < 20:
        print("Data historis tidak cukup.")
        return
        
    closes = df['Close']
    current_price = closes.iloc[-1]
    
    # Hitung indikator teknik
    sma20 = closes.rolling(window=20).mean().iloc[-1]
    rsi_series = calculate_rsi(closes)
    current_rsi = rsi_series.iloc[-1]
    
    print(f"Harga Terakhir: Rp {current_price:,.2f}")
    print(f"SMA 20: Rp {sma20:,.2f}")
    print(f"RSI (14): {current_rsi:.2f}")
    
    # Simulasi Monte Carlo / Proyeksi Sederhana 5 Hari ke Depan
    returns = np.log(closes / closes.shift(1)).dropna()
    mu = returns.mean()
    sigma = returns.std()
    
    np.random.seed(42)
    simulated_prices = [current_price]
    for i in range(5):
        shock = np.random.normal(mu, sigma)
        next_price = simulated_prices[-1] * np.exp(shock)
        simulated_prices.append(round(next_price, 2))
        
    print("\nProyeksi Simulasi Harga 5 Hari ke Depan:")
    for day, p in enumerate(simulated_prices[1:], 1):
        print(f"Hari ke-{day}: Rp {p:,.2f}")
        
    return simulated_prices

if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "TLKM"
    predict_next_week(ticker)
