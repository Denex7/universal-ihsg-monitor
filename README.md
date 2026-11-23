# 📈 Universal IHSG Stock & 24/7 Telegram Alert Monitor

Sistem pemantauan harga saham universal untuk Bursa Efek Indonesia (IHSG / IDX) yang dirancang agar dapat berjalan secara mandiri dan 24/7 di perangkat hemat daya seperti **Android STB (Termux)**, dilengkapi dengan push notifikasi instan via **Telegram Bot**.

---

## 🏗️ Skema Alur Kerja (Workflow Architecture)

```text
  [ Yahoo Finance API ] (Sumber Data Real-time IHSG 800+ Emiten)
         │
         ▼ (Fetch via Python / requests setiap 15 menit)
  [ Android STB Server ] (Menyala 24/7 di Rumah / Tailscale IP)
         │
         ├──> monitor.py (Cek Kondisi Harga vs Target -> Push Telegram Alert)
         └──> predictor.py (Analisis Teknikal: RSI, SMA20, & Simulasi Proyeksi 5 Hari)
         │
         ├──> [Kondisi Tercapai?] ──( Ya )──> [ Telegram Bot API ]
         │                                         │
         └──> [Belum Tercapai] ──( Lanjut )──> [ Tunggu 15 Menit ]
                                                   │
                                                   ▼
                                           [ Handphone Koko ]
                                      (Notifikasi Alarm Masuk 📱)
```

---

## 🚀 Fitur Utama
* **Universal 800+ Emiten IHSG:** Mendukung pemantauan seluruh emiten di Bursa Efek Indonesia berakhiran `.JK` (dapat dikustomisasi melalui file konfigurasi atau daftar emiten/CSV).
* **Modul Prediksi & Analisis Teknikal (`predictor.py`):** Menghitung indikator **RSI (14)**, **SMA 20**, serta simulasi proyeksi harga 5 hari ke depan berdasarkan volatilitas historis.
* **Mandiri & Anti Rate-Limit AI:** Berbasis Python murni tanpa bergantung pada LLM API Key (sehingga aman dari gangguan *rate limit* 429/503).
* **24/7 STB Ready (Termux):** Sangat ringan, berjalan di perangkat STB Android rumahan berdaya rendah yang menyala 24/7.
* **Push Alarm Telegram:** Langsung mengirimkan peringatan instan saat harga menyentuh area *Buy on Dip* atau *Take Profit*.

---

## 📱 Trik & Panduan Setup STB Android sebagai Bot 24/7

Ikuti langkah-langkah berikut untuk mendeploy sistem ini di STB Android (Termux):

1. **Akses STB via SSH:**
   ```bash
   ssh -p 8022 u0_a47@<IP_TAILSCALE_STB>
   ```
2. **Buat Folder Proyek:**
   ```bash
   mkdir -p ~/Projects/IHSG-Monitor && cd ~/Projects/IHSG-Monitor
   ```
3. **Simpan Script Monitor (`monitor.py`):**
   Salin file `monitor.py` ke dalam folder tersebut dan sesuaikan Token Bot serta Chat ID Telegrammu.
4. **Jalankan di Background (Daemon 24/7):**
   Agar terus berjalan meskipun terminal SSH ditutup, gunakan `nohup`:
   ```bash
   nohup python3 monitor.py > monitor.log 2>&1 </dev/null &
   ```
5. **Cek Log Berjalan:**
   ```bash
   tail -f monitor.log
   ```

---

## ⚙️ Kebutuhan Sistem
* Python 3.8+
* `requests`, `pandas`, `numpy` (`pip install requests pandas numpy`)
