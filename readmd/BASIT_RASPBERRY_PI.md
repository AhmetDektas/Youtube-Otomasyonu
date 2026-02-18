# 🍓 Raspberry Pi - Basit Kurulum Rehberi

## 📦 Alışveriş

**Raspberry Pi 4 (2GB RAM)** - ~$35-45
- MicroSD Kart (32GB) - ~$10
- Güç Adaptörü (USB-C) - ~$10
- **Toplam: ~$65**

---

## 🚀 Adım Adım Kurulum

### 1️⃣ Raspberry Pi OS Kur (Bilgisayarında)

1. **Raspberry Pi Imager indir:**
   - https://www.raspberrypi.com/software/
   - Bilgisayarına kur

2. **SD Karta OS yaz:**
   - Imager'ı aç
   - **OS:** Raspberry Pi OS Lite (64-bit)
   - **SD Kart:** Seç
   - **Ayarlar (⚙️):**
     - Hostname: `tiktok-bot`
     - SSH: ✅ Aktif
     - Kullanıcı: `pi`
     - Şifre: `[güçlü şifre]`
     - WiFi: SSID ve şifre gir
   - **YAZ** butonuna tıkla

3. **SD kartı Raspberry Pi'ye tak ve güç ver**

---

### 2️⃣ SSH ile Bağlan

Bilgisayarından:

```bash
# Windows (PowerShell)
ssh pi@tiktok-bot.local

# Mac/Linux (Terminal)
ssh pi@tiktok-bot.local

# Şifre: [ayarladığın şifre]
```

İlk bağlantıda "Are you sure?" sorarsa `yes` yaz.

---

### 3️⃣ Otomatik Kurulum

Raspberry Pi'da (SSH'da):

```bash
# Kurulum scriptini oluştur
nano install.sh
```

Aşağıdaki içeriği yapıştır (Ctrl+Shift+V):

```bash
#!/bin/bash
echo "🍓 Kurulum başlıyor..."

# Sistem güncelle
sudo apt update
sudo apt upgrade -y

# Python kur
sudo apt install -y python3 python3-pip python3-venv git

# Proje klasörü
mkdir -p ~/tiktok-bot
cd ~/tiktok-bot

# Virtual environment
python3 -m venv venv

# Paketleri kur
venv/bin/pip install --upgrade pip
venv/bin/pip install \
    apify-client==2.4.1 \
    google-auth-oauthlib==1.2.0 \
    google-auth-httplib2==0.2.0 \
    google-api-python-client==2.108.0 \
    pyyaml==6.0.1 \
    requests==2.31.0 \
    python-dotenv==1.0.0 \
    schedule==1.2.0

# Klasörler
mkdir -p src config data/videos logs

echo "✅ Kurulum tamamlandı!"
```

Kaydet: `Ctrl+X`, `Y`, `Enter`

Çalıştır:

```bash
chmod +x install.sh
bash install.sh
```

5-10 dakika sürer. Bekle...

---

### 4️⃣ Proje Dosyalarını Kopyala

**Bilgisayarından** (yeni terminal/PowerShell):

```bash
# Tüm projeyi kopyala
scp -r src scheduler.py .env config pi@tiktok-bot.local:~/tiktok-bot/

# Tek tek de kopyalayabilirsin:
scp -r src pi@tiktok-bot.local:~/tiktok-bot/
scp scheduler.py pi@tiktok-bot.local:~/tiktok-bot/
scp .env pi@tiktok-bot.local:~/tiktok-bot/
scp -r config pi@tiktok-bot.local:~/tiktok-bot/
```

---

### 5️⃣ Test Et

Raspberry Pi'da (SSH):

```bash
cd ~/tiktok-bot

# Test çalıştır
venv/bin/python scheduler.py
```

İlk video yüklenirse ✅ çalışıyor!

`Ctrl+C` ile durdur.

---

### 6️⃣ Otomatik Başlatma (Systemd)

Raspberry Pi'da:

```bash
# Servis dosyası oluştur
sudo nano /etc/systemd/system/tiktok-bot.service
```

İçeriği yapıştır:

```ini
[Unit]
Description=TikTok YouTube Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/tiktok-bot
Environment="PATH=/home/pi/tiktok-bot/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/pi/tiktok-bot/venv/bin/python /home/pi/tiktok-bot/scheduler.py
Restart=always
RestartSec=300
StandardOutput=append:/home/pi/tiktok-bot/logs/bot.log
StandardError=append:/home/pi/tiktok-bot/logs/bot-error.log

[Install]
WantedBy=multi-user.target
```

Kaydet: `Ctrl+X`, `Y`, `Enter`

Servisi başlat:

```bash
# Servisi aktif et
sudo systemctl daemon-reload
sudo systemctl enable tiktok-bot
sudo systemctl start tiktok-bot

# Durumu kontrol et
sudo systemctl status tiktok-bot
```

Yeşil "active (running)" görürsen ✅ çalışıyor!

---

## 🎯 Kullanım

### Log'ları İzle

```bash
# Canlı log
tail -f ~/tiktok-bot/logs/bot.log

# Son 50 satır
tail -n 50 ~/tiktok-bot/logs/bot.log

# Çıkmak için: Ctrl+C
```

### Servisi Yönet

```bash
# Başlat
sudo systemctl start tiktok-bot

# Durdur
sudo systemctl stop tiktok-bot

# Yeniden başlat
sudo systemctl restart tiktok-bot

# Durum
sudo systemctl status tiktok-bot
```

### İstatistikler

```bash
# Yüklenen videoları gör
cat ~/tiktok-bot/data/uploaded.json

# Disk kullanımı
du -sh ~/tiktok-bot/data/videos/
```

---

## 🔧 Sorun Giderme

### Servis başlamıyor

```bash
# Log'ları kontrol et
sudo journalctl -u tiktok-bot -n 50

# Manuel test
cd ~/tiktok-bot
venv/bin/python scheduler.py
```

### WiFi bağlantısı kopuyor

```bash
# Güç tasarrufunu kapat
sudo iwconfig wlan0 power off

# Kalıcı yap
sudo nano /etc/rc.local
# En alta ekle (exit 0'dan önce):
iwconfig wlan0 power off 2>/dev/null || true
```

### Dosya kopyalama hatası

```bash
# IP adresini bul
ping tiktok-bot.local

# IP ile dene
scp -r src pi@192.168.1.XXX:~/tiktok-bot/
```

---

## 📊 Kontrol Paneli

### Sistem Bilgisi

```bash
# CPU sıcaklığı
vcgencmd measure_temp

# RAM kullanımı
free -h

# Disk kullanımı
df -h

# Çalışma süresi
uptime
```

### Bot İstatistikleri

```bash
# Kaç video yüklendi?
cat ~/tiktok-bot/data/uploaded.json | grep "tiktok_url" | wc -l

# Son yüklenen video
cat ~/tiktok-bot/data/uploaded.json | tail -20
```

---

## 🎉 Tamamlandı!

Artık Raspberry Pi'n 7/24 çalışıyor:
- ✅ Her 3 saatte 1 video
- ✅ Günde 8 video
- ✅ Ayda 240 video
- ✅ Tamamen otomatik!

### Uzaktan Erişim

```bash
# Her yerden SSH ile bağlan
ssh pi@tiktok-bot.local

# Log'ları kontrol et
tail -f ~/tiktok-bot/logs/bot.log

# Çık
exit
```

---

## 💡 İpuçları

1. **İlk hafta:** Log'ları sık kontrol et
2. **Ayarları değiştir:** `nano ~/tiktok-bot/config/config.yaml`
3. **Yeniden başlat:** `sudo systemctl restart tiktok-bot`
4. **Güncelle:** Bilgisayardan yeni dosyaları kopyala, servisi yeniden başlat

---

## 📞 Hızlı Komutlar

```bash
# Bağlan
ssh pi@tiktok-bot.local

# Log izle
tail -f ~/tiktok-bot/logs/bot.log

# Durdur
sudo systemctl stop tiktok-bot

# Başlat
sudo systemctl start tiktok-bot

# Durum
sudo systemctl status tiktok-bot

# Çık
exit
```

---

## ✅ Checklist

- [ ] Raspberry Pi 4 aldım
- [ ] SD karta OS kurdum
- [ ] SSH ile bağlandım
- [ ] Kurulum scriptini çalıştırdım
- [ ] Proje dosyalarını kopyaladım
- [ ] Test ettim (çalışıyor)
- [ ] Systemd servisi kurdum
- [ ] Servis çalışıyor
- [ ] Log'ları kontrol ettim
- [ ] İlk video yüklendi

Hepsi tamam mı? Raspberry Pi hazır! 🎉

---

## 🆘 Yardım

Sorun mu var?

1. Log'ları kontrol et: `tail -f ~/tiktok-bot/logs/bot.log`
2. Manuel test: `cd ~/tiktok-bot && venv/bin/python scheduler.py`
3. Servisi yeniden başlat: `sudo systemctl restart tiktok-bot`

Hala sorun varsa detaylı rehber: `RASPBERRY_PI_KURULUM.md`
