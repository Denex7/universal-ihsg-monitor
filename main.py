#!/usr/bin/env python3
import sys
import os

def print_banner():
    print("=" * 60)
    print("📈 UNIVERSAL IHSG STOCK MONITOR & QUANTITATIVE TOOLKIT")
    print("   Author: Dennis Sucipto (Koko) & Hermes Agent")
    print("=" * 60)

def main():
    while True:
        print_banner()
        print("Pilih Menu Utama:")
        print(" 1. 🔍 Analisis & Prediksi Saham (Predictor & Teknikal)")
        print(" 2. 💼 Cek Portofolio & PnL Terkini (Portfolio & Risk)")
        print(" 3. 🌅 Kirim Morning Briefing Manual ke Telegram")
        print(" 4. 🚀 Jalankan Daemon Monitor Harga 24/7 (Background Alert)")
        print(" 0. Keluar")
        
        choice = input("\nMasukkan pilihan (0-4): ").strip()
        
        if choice == '1':
            ticker = input("Masukkan kode emiten (contoh: BBRI, TLKM, BBCA): ").strip()
            if ticker:
                os.system(f"./venv/bin/python3 predictor.py {ticker}")
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '2':
            os.system("./venv/bin/python3 portfolio.py")
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '3':
            os.system("./venv/bin/python3 morning_briefing.py")
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '4':
            print("\n🚀 Memulai pemantauan harga universal (tekan Ctrl+C untuk berhenti)...")
            os.system("./venv/bin/python3 monitor.py")
        elif choice == '0':
            print("\nSampai jumpa, Master! Tetap semangat cuannya (o˘◡˘o)✨")
            break
        else:
            print("❌ Pilihan tidak valid, silakan coba lagi.")

if __name__ == '__main__':
    main()
