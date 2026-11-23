import requests
import json
import os
import datetime

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '217707756')
WATCHLIST_FILE = os.path.join(os.path.dirname(__file__), 'watchlist.json')
PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), 'portfolio.json')

def send_telegram(message):
    if TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN':
        print("[Simulasi Morning Briefing Telegram]:\n", message)
        return
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Failed to send morning briefing:", e)

def fetch_price(ticker):
    try:
        symbol = ticker if ticker.endswith('.JK') else f"{ticker}.JK"
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=2d'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        return float(r.json()['chart']['result'][0]['meta']['regularMarketPrice'])
    except Exception:
        return None

def generate_morning_briefing():
    today = datetime.date.today().strftime('%d %B %Y')
    
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as f:
            watchlist = json.load(f)
    else:
        watchlist = {}
        
    msg = f"🌅 *MORNING BRIEFING IHSG & PORTOFOLIO* 🌅\n📅 Tanggal: {today}\n\n📊 *Pantauan Market Hari Ini:*\n"
    
    for ticker in watchlist.keys():
        p = fetch_price(ticker)
        if p:
            msg += f"• *{ticker}*: Rp {p:,.0f}\n"
            
    msg += "\n💡 *Tips Pagi:* Selalu patuhi manajemen risiko (Half-Kelly) dan jangan FOMO! Semangat cuan hari ini!"
    
    send_telegram(msg)
    print("Morning briefing generated and sent successfully!")

if __name__ == '__main__':
    generate_morning_briefing()
