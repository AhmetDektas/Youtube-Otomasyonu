# 🍓 Raspberry Pi Kurulum Rehberi

## 🛒 Alışveriş Listesi

### Önerilen: Raspberry Pi 4 (2GB)
- **Raspberry Pi 4 Model B (2GB RAM)** - ~$35-45
- **MicroSD Kart (32GB, Class 10)** - ~$10
- **Güç Adaptörü (5V 3A USB-C)** - ~$10
- **Kasa (opsiyonel, soğutmalı)** - ~$10
- **Toplam: ~$65-75**

### Minimum: Raspberry Pi Zero 2 W
- **Raspberry Pi Zero 2 W** - ~$15
- **MicroSD Kart (16GB)** - ~$8
- **Güç Adaptörü (5V 2.5A Micro USB)** - ~$8
- **Toplam: ~$31**
- ⚠️ **Yavaş olabilir, önerilmez**

---

## 📋 Kurulum Adımları

### 1️⃣ Raspberry Pi OS Kurulumu

#### A. Raspberry Pi Imager İndir
- [rpi-imager](https://www.raspberrypi.com/software/) indir
- Bilgisayarına kur

#### B. OS Yaz
1. Imager'ı aç
2. **OS Seç:** Raspberry Pi OS Lite (64-bit)
3. **SD Kart Seç:** MicroSD kartını tak
4. **Ayarlar (⚙️):**
   - Hostname: `tiktok-bot`
   - SSH aktif et
   - Kullanıcı: `pi` / Şifre: `[güçlü şifre]`
   - WiFi ayarla (SSID ve şifre)
   - Locale: `Europe/Istanbul`
5. **YAZ** butonuna tıkla

#### C. İlk Açılış
1. SD kartı Raspberry Pi'ye tak
2. Güç ver
3. 2-3 dakika bekle (ilk açılış)

---

### 2️⃣ SSH ile Bağlan

```bash
# IP adresini bul (router'dan veya)
ping tiktok-bot.local

# SSH ile bağlan
ssh pi@tiktok-bot.local
# Şifre: [ayarladığın şifre]
```

---

### 3️⃣ Otomatik Kurulum

Raspberry Pi'da:

```bash
# Kurulum scriptini indir
curl -O https://raw.githubusercontent.com/[repo]/raspberry-pi-install.sh

# Veya manuel oluştur
nano raspberry-pi-install.sh
# İçeriği yapıştır

# Çalıştırılabilir yap
chmod +x raspberry-pi-install.sh

# Kur
sudo bash raspberry-pi-install.sh
```

Script otomatik olarak:
- ✅ Sistem güncellemesi
- ✅ Python ve bağımlılıklar
- ✅ Virtual environment
- ✅ Klasör yapısı
- ✅ Systemd servisi
- ✅ Log rotation
- ✅ Swap ayarı (düşük RAM için)

---

### 4️⃣ Proje Dosyalarını Kopyala

Bilgisayarından Raspberry Pi'ya:

```bash
# Tüm projeyi kopyala
scp -r src config scheduler.py .env pi@tiktok-bot.local:~/tiktok-youtube-bot/

# Veya tek tek
scp -r src pi@tiktok-bot.local:~/tiktok-youtube-bot/
scp -r config pi@tiktok-bot.local:~/tiktok-youtube-bot/
scp scheduler.py pi@tiktok-bot.local:~/tiktok-youtube-bot/
scp .env pi@tiktok-bot.local:~/tiktok-youtube-bot/
```

---

### 5️⃣ Credentials Ekle

```bash
# .env dosyasını düzenle
ssh pi@tiktok-bot.local
nano ~/tiktok-youtube-bot/.env

# APIFY_API_TOKEN ekle
# Kaydet: Ctrl+X, Y, Enter

# credentials.json kopyala
exit
scp config/credentials.json pi@tiktok-bot.local:~/tiktok-youtube-bot/config/
scp config/token.pickle pi@tiktok-bot.local:~/tiktok-youtube-bot/config/
```

---

### 6️⃣ Servisi Başlat

```bash
# SSH ile bağlan
ssh pi@tiktok-bot.local

# Servisi başlat
sudo systemctl start tiktok-bot

# Durumu kontrol et
sudo systemctl status tiktok-bot

# Log'ları izle
tail -f ~/tiktok-youtube-bot/logs/bot.log
```

---

## 🔧 Sorun Giderme

### Servis başlamıyor

```bash
# Log'ları kontrol et
sudo journalctl -u tiktok-bot -n 50

# Manuel test
cd ~/tiktok-youtube-bot
venv/bin/python scheduler.py
```

### RAM doldu

```bash
# RAM kullanımı
free -h

# Swap ekle (script otomatik ekler)
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### WiFi bağlantısı kopuyor

```bash
# Güç tasarrufunu kapat
sudo iwconfig wlan0 power off

# Kalıcı yap
sudo nano /etc/rc.local
# Ekle: iwconfig wlan0 power off
```

### Disk doldu

```bash
# Disk kullanımı
df -h

# Eski videoları temizle
rm ~/tiktok-youtube-bot/data/videos/*.mp4

# Log'ları temizle
sudo journalctl --vacuum-time=7d
```

---

## 📊 Performans Optimizasyonu

### Raspberry Pi 4 (2GB+)
```yaml
# config/config.yaml
tiktok:
  max_videos_per_run: 5  # Rahat çalışır
```

### Raspberry Pi Zero 2 W
```yaml
# config/config.yaml
tiktok:
  max_videos_per_run: 2  # Daha az yük
```

---

## 🛠️ Yararlı Komutlar

### Servis Yönetimi
```bash
sudo systemctl start tiktok-bot      # Başlat
sudo systemctl stop tiktok-bot       # Durdur
sudo systemctl restart tiktok-bot    # Yeniden başlat
sudo systemctl status tiktok-bot     # Durum
sudo systemctl enable tiktok-bot     # Otomatik başlat
sudo systemctl disable tiktok-bot    # Otomatik başlatma
```

### Log İzleme
```bash
# Canlı log
tail -f ~/tiktok-youtube-bot/logs/bot.log

# Son 100 satır
tail -n 100 ~/tiktok-youtube-bot/logs/bot.log

# Hata log'ları
tail -f ~/tiktok-youtube-bot/logs/bot-error.log

# Systemd log'ları
sudo journalctl -u tiktok-bot -f
```

### Sistem Bilgisi
```bash
# CPU sıcaklığı
vcgencmd measure_temp

# RAM kullanımı
free -h

# Disk kullanımı
df -h

# CPU kullanımı
top
```

### Güncelleme
```bash
# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Python paketleri
cd ~/tiktok-youtube-bot
venv/bin/pip install --upgrade -r requirements.txt

# Servisi yeniden başlat
sudo systemctl restart tiktok-bot
```

---

## 🔐 Güvenlik

### SSH Güvenliği
```bash
# SSH key ile giriş (şifresiz)
ssh-keygen -t ed25519
ssh-copy-id pi@tiktok-bot.local

# Şifre ile girişi kapat
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no
sudo systemctl restart ssh
```

### Firewall
```bash
# UFW kur
sudo apt install ufw

# SSH'ye izin ver
sudo ufw allow ssh

# Aktif et
sudo ufw enable
```

---

## 💰 Maliyet

### Elektrik Tüketimi

**Raspberry Pi 4 (2GB):**
- Güç: ~3W (idle), ~6W (yük altında)
- Aylık: ~2-4 kWh
- Maliyet: ~$0.50-1/ay (elektrik fiyatına göre)

**Raspberry Pi Zero 2 W:**
- Güç: ~1W (idle), ~2W (yük altında)
- Aylık: ~1-2 kWh
- Maliyet: ~$0.25-0.50/ay

### Toplam Aylık Maliyet
```
Raspberry Pi 4:
├── Elektrik: ~$1/ay
├── Apify: $0 (free plan)
└── YouTube API: $0
─────────────────────
Toplam: ~$1/ay
```

---

## ✅ Checklist

- [ ] Raspberry Pi 4 (2GB) aldım
- [ ] MicroSD kart (32GB) aldım
- [ ] Raspberry Pi OS kurdum
- [ ] SSH ile bağlandım
- [ ] Kurulum scriptini çalıştırdım
- [ ] Proje dosyalarını kopyaladım
- [ ] .env dosyasını düzenledim
- [ ] credentials.json ekledim
- [ ] Servisi başlattım
- [ ] Log'ları kontrol ettim
- [ ] İlk video yüklendi

Hepsi tamam mı? Raspberry Pi hazır! 🎉

---

## 🎯 Sonuç

Raspberry Pi 4 (2GB) ile:
- ✅ 7/24 çalışır
- ✅ Sessiz ve soğuk
- ✅ Düşük elektrik (~$1/ay)
- ✅ Güvenilir
- ✅ Uzaktan yönetim

Raspberry Pi Zero 2 W ile:
- ⚠️ Çalışır ama yavaş
- ⚠️ RAM sınırlı (512MB)
- ✅ Çok ucuz (~$15)
- ✅ Çok düşük elektrik

**Önerim: Raspberry Pi 4 (2GB) al, değer!** 🚀
