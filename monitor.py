import requests
import time
import datetime
import os
import json

# Universal IHSG Stock & Telegram Alert Monitor with Watchlist JSON
# Author: Developer & Hermes Agent

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '217707756')
WATCHLIST_FILE = os.path.join(os.path.dirname(__file__), 'watchlist.json')

def send_telegram(message):
    if TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN':
        print("[Simulasi Telegram Alert]:", message)
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

def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return {
            'BBRI': {'target_buy': 3000, 'target_sell': 3500, 'status': 'NEUTRAL'},
            'TLKM': {'target_buy': 2000, 'target_sell': 2204, 'status': 'NEUTRAL'}
        }
    with open(WATCHLIST_FILE, 'r') as f:
        return json.load(f)

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(watchlist, f, indent=2)

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
    print('Universal IHSG Stock Monitor started (Watchlist JSON mode)...')
    watchlist = load_watchlist()
    
    for ticker, config in watchlist.items():
        price = fetch_price(ticker)
        if price is not None:
            print(f'-> {ticker}: Rp {price:,.0f} (Target Buy: ≤ Rp {config["target_buy"]:,}, Target Sell: ≥ Rp {config["target_sell"]:,})')

if __name__ == '__main__':
    main()
