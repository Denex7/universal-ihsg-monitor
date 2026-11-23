import json
import os
import requests

PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), 'portfolio.json')

def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        return {"initial_capital": 700000, "cash": 700000, "holdings": {}}
    with open(PORTFOLIO_FILE, 'r') as f:
        return json.load(f)

def fetch_current_price(ticker):
    try:
        symbol = ticker.upper() if ticker.upper().endswith('.JK') else f"{ticker.upper()}.JK"
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=2d'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        data = r.json()
        return float(data['chart']['result'][0]['meta']['regularMarketPrice'])
    except Exception:
        return None

def show_portfolio_report():
    pf = load_portfolio()
    print("=" * 50)
    print("💼 LAPORAN PORTOFOLIO SAHAM & MANAJEMEN RISIKO")
    print("=" * 50)
    print(f"• Modal Awal    : Rp {pf['initial_capital']:,.0f}")
    print(f"• Sisa Kas      : Rp {pf['cash']:,.0f}")
    
    total_assets_value = pf['cash']
    print("\n📦 Daftar Kepemilikan (Holdings):")
    
    if not pf['holdings']:
        print("  (Belum ada saham yang dibeli)")
    else:
        for ticker, data in pf['holdings'].items():
            shares = data['shares']
            buy_price = data['avg_buy_price']
            current_price = fetch_current_price(ticker) or buy_price
            
            total_buy = shares * buy_price
            current_val = shares * current_price
            pnl = current_val - total_buy
            pnl_pct = (pnl / total_buy) * 100 if total_buy > 0 else 0
            
            total_assets_value += current_val
            
            print(f"  • {ticker}: {shares} lembar (1 Lot)")
            print(f"    - Harga Beli  : Rp {buy_price:,.0f}")
            print(f"    - Harga Kini  : Rp {current_price:,.0f}")
            print(f"    - Nilai Sekarang: Rp {current_val:,.0f}")
            print(f"    - PnL         : Rp {pnl:,.0f} ({pnl_pct:+.2f}%) {'🟢' if pnl >= 0 else '🔴'}")
            print(f"    - Target TP   : Rp {data['target_sell']:,.0f}")
            print(f"    - Stop Loss   : Rp {data['stop_loss']:,.0f}")
            
    total_return = total_assets_value - pf['initial_capital']
    total_return_pct = (total_return / pf['initial_capital']) * 100
    print("-" * 50)
    print(f"💰 Total Nilai Portofolio: Rp {total_assets_value:,.0f}")
    print(f"📈 Total Return          : Rp {total_return:,.0f} ({total_return_pct:+.2f}%)")
    print("=" * 50)

def calculate_position_sizing(ticker, price, risk_profile="conservative"):
    pf = load_portfolio()
    cash = pf['cash']
    
    # Manajemen Risiko: Max alokasi 25% (Half-Kelly rule) dari total kas/modal
    max_allocation = cash * 0.25
    max_lots = int(max_allocation / (price * 100))
    if max_lots < 1 and cash >= (price * 100):
        max_lots = 1
        
    print(f"\n📐 KALKULATOR POSISI & MANAJEMEN RISIKO ({ticker.upper()})")
    print(f"• Kas Tersedia       : Rp {cash:,.0f}")
    print(f"• Alokasi Maksimal   : Rp {max_allocation:,.0f} (25% dari kas)")
    print(f"• Harga Saham Saat Ini: Rp {price:,.0f} / lembar")
    print(f"• Rekomendasi Aman   : {max_lots} Lot ({max_lots * 100} lembar)")
    print(f"• Estimasi Kebutuhan : Rp {max_lots * price * 100:,.0f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'size':
        ticker = sys.argv[2] if len(sys.argv) > 2 else 'BBRI'
        price = float(sys.argv[3]) if len(sys.argv) > 3 else 3100
        calculate_position_sizing(ticker, price)
    else:
        show_portfolio_report()
