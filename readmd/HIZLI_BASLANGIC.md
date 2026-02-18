# ⚡ Hızlı Başlangıç - 5 Dakika

## 🎯 Raspberry Pi'da Çalıştırma

### 1. Raspberry Pi OS Kur
- Raspberry Pi Imager indir
- SD karta yaz (SSH aktif, WiFi ayarla)
- Raspberry Pi'ye tak, güç ver

### 2. Bağlan
```bash
ssh pi@tiktok-bot.local
```

### 3. Kur
```bash
# Tek komut kurulum
curl -sSL https://raw.githubusercontent.com/[repo]/install.sh | bash

# Veya manuel:
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
mkdir ~/tiktok-bot && cd ~/tiktok-bot
python3 -m venv venv
venv/bin/pip install apify-client google-auth-oauthlib google-api-python-client pyyaml requests python-dotenv schedule
```

### 4. Dosyaları Kopyala
```bash
# Bilgisayarından
scp -r src scheduler.py .env config pi@tiktok-bot.local:~/tiktok-bot/
```

### 5. Çalıştır
```bash
# Raspberry Pi'da
cd ~/tiktok-bot
venv/bin/python scheduler.py
```

Çalışıyor mu? ✅ Devam et!

### 6. Otomatik Başlat
```bash
# Servis kur
sudo nano /etc/systemd/system/tiktok-bot.service
# İçeriği yapıştır (BASIT_RASPBERRY_PI.md'de)

# Başlat
sudo systemctl enable tiktok-bot
sudo systemctl start tiktok-bot
```

## ✅ Hazır!

Log'ları izle:
```bash
tail -f ~/tiktok-bot/logs/bot.log
```

---

## 📚 Detaylı Rehberler

- **Basit:** `BASIT_RASPBERRY_PI.md` (adım adım)
- **Detaylı:** `RASPBERRY_PI_KURULUM.md` (her şey)
- **Sorun:** `VIDEO_YONETIMI.md`, `APIFY_MALIYET.md`

---

## 🎯 Özet

1. Raspberry Pi OS kur
2. SSH ile bağlan
3. Python kur
4. Dosyaları kopyala
5. Servisi başlat
6. Bitti! 🎉

Her 3 saatte 1 video, günde 8 video, ayda 240 video - tamamen otomatik!
