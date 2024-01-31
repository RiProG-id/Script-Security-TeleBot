# Script Security TeleBot

Sebuah bot Telegram untuk memindai dan mendeteksi kode berbahaya dalam dokumen, khususnya berfokus pada file ZIP dan skrip shell.

## Memulai

### Prasyarat

- Python 3.x
- Instal paket Python yang diperlukan dengan perintah:
  ```bash
  pip install python-telegram-bot==13.15
  ```

### Instalasi

1. Klon repositori:
   ```bash
   git clone https://github.com/RiProG-id/Script-Security-TeleBot.git
   ```

2. Masuk ke direktori proyek:
   ```bash
   cd Script-Security-TeleBot
   ```

3. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```

4. Gantilah `'YOUR_BOT_TOKEN'` di `x.py` dengan token bot Telegram yang sesuai.

5. Jalankan bot:
   ```bash
   python main.py
   ```

## Perintah Bot

- `/start`: Memulai bot dan menerima pesan selamat datang beserta tautan kode sumber.
- Mengirim dokumen (ZIP atau skrip shell) memicu bot untuk memindai kode berbahaya.

## Cara Kerja

- Bot memindai file ZIP untuk menemukan kode berbahaya dalam file-file di dalamnya.
- Bot memeriksa skrip shell untuk perintah dan pola yang dianggap berisiko.

## Kode Berbahaya yang Dideteksi

Bot mendeteksi pola berbahaya berikut dalam dokumen:

- `rm -rf`: Perintah hapus paksa secara rekursif.
- `if=/dev/null`: Redireksi input ke perangkat null.
- `cmd erase`: Perintah Windows untuk menghapus file.
- `apparmor`: Kerangka keamanan untuk Linux.
- `setenforce`: Perintah Linux untuk mengatur mode penegakan.
- `shred -f`: Menghapus dan mengganti isi file dengan aman.
- `ufw disable`: Menonaktifkan Uncomplicated Firewall di Linux.
- `iptables -F`: Menghapus semua aturan iptables di Linux.
- `setfacl`: Mengatur daftar kontrol akses file di Linux.
- `:(){ :|:& };:`: Bom fork, sebuah fungsi shell berbahaya.
