# 🚀 Raspberry Pi 4 - Hızlı Kurulum (5 Adım)

Raspberry Pi 4 (4GB) için süper basit kurulum. 30 dakikada bitir, 7/24 çalışsın.

---

## 📋 Adım 1: SD Kart Hazırla (Bilgisayarında)

1. **Raspberry Pi Imager indir:**
   - https://www.raspberrypi.com/software/
   - Kur ve aç

2. **SD Karta OS yaz:**
   - **CHOOSE OS** → Raspberry Pi OS (64-bit) - tam sürüm
   - **CHOOSE STORAGE** → SD kartını seç
   - **⚙️ Ayarlar** (sağ altta dişli ikonu):
     - ✅ Set hostname: `youtube-bot`
     - ✅ Enable SSH: Şifre ile
     - ✅ Set username: `pi`
     - ✅ Set password: `[güçlü bir şifre]`
     - ✅ Configure WiFi: 
       - SSID: `[WiFi adın]`
       - Password: `[WiFi şifren]`
       - Country: `TR`
   - **WRITE** butonuna bas
   - Bitince SD kartı Raspberry Pi'ye tak

3. **Raspberry Pi'yi başlat:**
   - SD kartı tak
   - Güç kablosunu tak
   - 2 dakika bekle (ilk açılış)

---

## 📋 Adım 2: Bağlan ve Kur (SSH)

**Bilgisayarında PowerShell aç:**

```powershell
# Bağlan
ssh pi@youtube-bot.local
# Şifre: [ayarladığın şifre]
```

**Raspberry Pi'de şunu çalıştır:**

```bash
# Kurulum scriptini indir ve çalıştır
curl -o install.sh https://raw.githubusercontent.com/[senin-repo]/install.sh
bash install.sh
```

**VEYA manuel yap:**

```bash
# Sistem güncelle
sudo apt update && sudo apt upgrade -y

# Python kur
sudo apt install -y python3 python3-pip python3-venv git

# Proje klasörü
mkdir -p ~/youtube-bot
cd ~/youtube-bot

# Virtual environment
python3 -m venv venv

# Paketleri kur
venv/bin/pip install --upgrade pip
venv/bin/pip install apify-client google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml requests python-dotenv schedule

# Klasörler
mkdir -p src config data/videos logs
```

**5-10 dakika sürer, bekle.**

---

## 📋 Adım 3: Dosyaları Kopyala

**Bilgisayarında (yeni PowerShell):**

```powershell
# Proje klasörüne git
cd C:\Users\[senin-kullanici-adin]\youtube-bot-projesi

# Tüm dosyaları kopyala
scp -r src scheduler.py .env config pi@youtube-bot.local:~/youtube-bot/
```

**Şifre sor, gir. Dosyalar kopyalanacak.**

---

## 📋 Adım 4: Test Et

**Raspberry Pi SSH'ında:**

```bash
cd ~/youtube-bot
venv/bin/python scheduler.py
```

**İlk video indirip yüklemeye başlarsa ✅ çalışıyor!**

`Ctrl+C` ile durdur.

---

## 📋 Adım 5: Otomatik Başlat (7/24 Çalışsın)

**Raspberry Pi SSH'ında:**

```bash
# Servis dosyası oluştur
sudo nano /etc/systemd/system/youtube-bot.service
```

**Şunu yapıştır (Ctrl+Shift+V):**

```ini
[Unit]
Description=YouTube TikTok Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/youtube-bot
Environment="PATH=/home/pi/youtube-bot/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/pi/youtube-bot/venv/bin/python /home/pi/youtube-bot/scheduler.py
Restart=always
RestartSec=300
StandardOutput=append:/home/pi/youtube-bot/logs/bot.log
StandardError=append:/home/pi/youtube-bot/logs/bot-error.log

[Install]
WantedBy=multi-user.target
```

**Kaydet: `Ctrl+X`, `Y`, `Enter`**

**Servisi başlat:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable youtube-bot
sudo systemctl start youtube-bot
sudo systemctl status youtube-bot
```

**Yeşil "active (running)" görürsen ✅ TAMAM!**

---

## 🎉 BITTI! Artık 7/24 Çalışıyor

Raspberry Pi artık:
- ✅ Her 3 saatte 1 video yükler
- ✅ Günde 8 video
- ✅ Ayda 240 video
- ✅ Tamamen otomatik
- ✅ Elektrik gitse bile yeniden başlar

---

## 📊 Kontrol Komutları

**Log'ları izle:**
```bash
ssh pi@youtube-bot.local
tail -f ~/youtube-bot/logs/bot.log
```

**Durumu kontrol et:**
```bash
ssh pi@youtube-bot.local
sudo systemctl status youtube-bot
```

**Durdur:**
```bash
ssh pi@youtube-bot.local
sudo systemctl stop youtube-bot
```

**Başlat:**
```bash
ssh pi@youtube-bot.local
sudo systemctl start youtube-bot
```

**Yeniden başlat:**
```bash
ssh pi@youtube-bot.local
sudo systemctl restart youtube-bot
```

---

## 🔧 Ayarları Değiştir

**Config dosyasını düzenle:**
```bash
ssh pi@youtube-bot.local
nano ~/youtube-bot/config/config.yaml
```

**Değişiklik yaptıktan sonra:**
```bash
sudo systemctl restart youtube-bot
```

---

## 📱 Uzaktan Erişim (Her Yerden)

**Telefondan veya başka yerden:**
```bash
ssh pi@youtube-bot.local
tail -f ~/youtube-bot/logs/bot.log
```

**Çıkmak için:** `Ctrl+C` sonra `exit`

---

## ⚠️ Sorun mu Var?

**Bağlanamıyorum:**
```bash
# IP adresini bul
ping youtube-bot.local

# IP ile bağlan
ssh pi@192.168.1.XXX
```

**Servis çalışmıyor:**
```bash
# Log'lara bak
sudo journalctl -u youtube-bot -n 50

# Manuel test
cd ~/youtube-bot
venv/bin/python scheduler.py
```

**Video yüklenmiyor:**
```bash
# Log'u kontrol et
tail -f ~/youtube-bot/logs/bot.log

# Config'i kontrol et
cat ~/youtube-bot/config/config.yaml

# .env'i kontrol et
cat ~/youtube-bot/.env
```

---

## 💡 Hızlı Özet

```bash
# 1. SD kart hazırla (Imager ile)
# 2. Raspberry Pi'yi başlat
# 3. SSH ile bağlan
ssh pi@youtube-bot.local

# 4. Kurulum yap
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
mkdir -p ~/youtube-bot && cd ~/youtube-bot
python3 -m venv venv
venv/bin/pip install apify-client google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml requests python-dotenv schedule
mkdir -p src config data/videos logs

# 5. Dosyaları kopyala (bilgisayarından)
scp -r src scheduler.py .env config pi@youtube-bot.local:~/youtube-bot/

# 6. Test et
cd ~/youtube-bot && venv/bin/python scheduler.py

# 7. Otomatik başlat
sudo nano /etc/systemd/system/youtube-bot.service
# (yukarıdaki içeriği yapıştır)
sudo systemctl daemon-reload
sudo systemctl enable youtube-bot
sudo systemctl start youtube-bot

# 8. Kontrol et
sudo systemctl status youtube-bot
tail -f ~/youtube-bot/logs/bot.log
```

---

## ✅ Checklist

- [ ] SD karta OS kurdum
- [ ] Raspberry Pi'yi başlattım
- [ ] SSH ile bağlandım
- [ ] Python ve paketleri kurdum
- [ ] Dosyaları kopyaladım
- [ ] Test ettim (çalışıyor)
- [ ] Systemd servisi kurdum
- [ ] Servis çalışıyor
- [ ] Log'ları kontrol ettim
- [ ] İlk video yüklendi

**Hepsi tamam mı? Raspberry Pi 4 hazır! 🎉**

---

## 🆘 Yardım Lazım?

1. **Log'lara bak:** `tail -f ~/youtube-bot/logs/bot.log`
2. **Manuel test:** `cd ~/youtube-bot && venv/bin/python scheduler.py`
3. **Servisi yeniden başlat:** `sudo systemctl restart youtube-bot`

Hala sorun varsa detaylı rehber: `RASPBERRY_PI_KURULUM.md`
