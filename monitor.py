import requests
import time
import datetime
import os

# Universal IHSG Stock & Telegram Alert Monitor for 24/7 STB (Termux)
# Author: Dennis Sucipto (Koko) & Hermes Agent

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID')

def send_telegram(message):
    if TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN':
        print("[Simulasi Telegram]:", message)
        return
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        print('Telegram response:', r.status_code)
    except Exception as e:
        print('Failed to send telegram:', e)

def fetch_price(ticker):
    try:
        symbol = ticker if ticker.endswith('.JK') else f"{ticker}.JK"
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d'
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except Exception as e:
        print(f'Error fetching {ticker}:', e)
        return None

def main():
    print('Universal IHSG Stock Monitor started...')
    # Watchlist universal (bisa diperluas ke 800+ emiten IHSG atau dibaca via CSV)
    watchlist = {
        'BBRI': {'target_buy': 3000, 'target_sell': 3500, 'status': None},
        'TLKM': {'target_buy': 2000, 'target_sell': 2204, 'status': None},
        'BBCA': {'target_buy': 9000, 'target_sell': 10500, 'status': None},
        'ASII': {'target_buy': 5000, 'target_sell': 6000, 'status': None},
    }
    
    while True:
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'--- [Cek Pasar: {timestamp}] ---')
        
        for ticker, config in watchlist.items():
            price = fetch_price(ticker)
            if price is not None:
                print(f'{ticker}: Rp {price:,.0f}')
                tb = config['target_buy']
                ts = config['target_sell']
                
                if price <= tb and config['status'] != 'BUY':
                    msg = f"🚨 *ALARM BELI ({ticker})* 🚨\n\nHarga saat ini: *Rp {price:,.0f}*\n🎯 Menyentuh target *Buy on Dip* (≤ Rp {tb:,}).\n✨ Waktunya eksekusi akumulasi!"
                    send_telegram(msg)
                    watchlist[ticker]['status'] = 'BUY'
                elif price >= ts and config['status'] != 'SELL':
                    msg = f"🚨 *ALARM JUAL / TP ({ticker})* 🚨\n\nHarga saat ini: *Rp {price:,.0f}*\n🎯 Menyentuh target *Take Profit* (≥ Rp {ts:,}).\n💰 Waktunya realisasi cuan!"
                    send_telegram(msg)
                    watchlist[ticker]['status'] = 'SELL'
                elif tb < price < ts:
                    watchlist[ticker]['status'] = 'NEUTRAL'
                    
        time.sleep(900)

if __name__ == '__main__':
    main()
