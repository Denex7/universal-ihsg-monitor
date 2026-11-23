import requests
import numpy as np
import pandas as pd
import sys

def fetch_historical_data(ticker, period="3mo"):
    try:
        symbol = ticker.upper() if ticker.upper().endswith('.JK') else f"{ticker.upper()}.JK"
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range={period}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        
        if 'chart' not in data or data['chart']['result'] is None:
            print(f"❌ Data untuk emiten '{symbol}' tidak ditemukan atau salah.")
            return None
            
        result = data['chart']['result'][0]
        closes = result['indicators']['quote'][0]['close']
        timestamps = result['timestamp']
        
        df = pd.DataFrame({'Close': closes}, index=pd.to_datetime(timestamps, unit='s'))
        df = df.dropna()
        return df
    except Exception as e:
        print(f"❌ Error mengambil data untuk {ticker}:", e)
        return None

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_and_predict(ticker):
    print(f"\n🔍 Menganalisis emiten: {ticker.upper()}...")
    df = fetch_historical_data(ticker, period="3mo")
    if df is None or len(df) < 20:
        print("⚠️ Data historis tidak mencukupi untuk analisis.")
        return
        
    closes = df['Close']
    current_price = closes.iloc[-1]
    
    sma20 = closes.rolling(window=20).mean().iloc[-1]
    rsi_series = calculate_rsi(closes)
    current_rsi = rsi_series.iloc[-1]
    
    print("=" * 45)
    print(f"📊 LAPORAN ANALISIS TEKNIKAL: {ticker.upper()}")
    print("=" * 45)
    print(f"• Harga Terakhir : Rp {current_price:,.2f}")
    print(f"• SMA 20 (Tren)  : Rp {sma20:,.2f}")
    print(f"• RSI (14)       : {current_rsi:.2f} ({'Overbought 🔴' if current_rsi > 70 else 'Oversold 🟢' if current_rsi < 30 else 'Normal 🟡'})")
    
    returns = np.log(closes / closes.shift(1)).dropna()
    mu = returns.mean()
    sigma = returns.std()
    
    np.random.seed(42)
    simulated_prices = [current_price]
    for i in range(5):
        shock = np.random.normal(mu, sigma)
        next_price = simulated_prices[-1] * np.exp(shock)
        simulated_prices.append(round(next_price, 2))
        
    print("\n🔮 Proyeksi Simulasi Harga 5 Hari ke Depan:")
    for day, p in enumerate(simulated_prices[1:], 1):
        print(f"  Hari ke-{day}: Rp {p:,.2f}")
    print("=" * 45 + "\n")

def main():
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
        analyze_and_predict(ticker)
        return

    print("=" * 50)
    print("📈 UNIVERSAL IHSG STOCK PREDICTOR & ANALYZER")
    print("=" * 50)
    print("Pilihan Emiten Populer:")
    print(" 1. BBRI (Bank Rakyat Indonesia)")
    print(" 2. TLKM (Telkom Indonesia)")
    print(" 3. BBCA (Bank Central Asia)")
    print(" 4. ASII (Astra International)")
    print(" 5. GOTO (GoTo Gojek Tokopedia)")
    print(" 6. Masukkan Kode Saham Sendiri (Custom)")
    print(" 0. Keluar")
    
    choice = input("\nPilih menu (0-6): ").strip()
    
    if choice == '1':
        analyze_and_predict('BBRI')
    elif choice == '2':
        analyze_and_predict('TLKM')
    elif choice == '3':
        analyze_and_predict('BBCA')
    elif choice == '4':
        analyze_and_predict('ASII')
    elif choice == '5':
        analyze_and_predict('GOTO')
    elif choice == '6':
        custom_ticker = input("Masukkan kode emiten (contoh: UNVR, ADRO, BMRI): ").strip()
        if custom_ticker:
            analyze_and_predict(custom_ticker)
    elif choice == '0':
        print("Sampai jumpa, Master! (o˘◡˘o)✨")
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
