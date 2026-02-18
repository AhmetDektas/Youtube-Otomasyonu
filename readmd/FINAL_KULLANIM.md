# 🚀 TAM OTOMATİK TikTok → YouTube Sistemi

## ✅ Hazır! Şimdi Çalıştır

### 🎯 Sistem Özellikleri

- ✅ Apify ile TikTok'tan otomatik video bulma
- ✅ Her 3 saatte bir çalışır
- ✅ Her döngüde 1 video yükler
- ✅ Günde 8 video = Ayda 240 video
- ✅ Duplicate kontrolü (aynı video tekrar yüklenmez)
- ✅ Otomatik eski video temizleme
- ✅ Raspberry Pi'da 7/24 çalışabilir

---

## 🚀 Hemen Başla

### 1. Apify Token'ı Ekle

`.env` dosyasını aç ve token'ı yapıştır:

```env
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. YouTube Credentials Ekle

`YOUTUBE_API_SETUP.md` dosyasındaki adımları takip et ve `config/credentials.json` dosyasını oluştur.

### 3. Scheduler'ı Başlat

```bash
python scheduler.py
```

İşte bu kadar! Sistem otomatik çalışmaya başladı.

---

## ⏰ Nasıl Çalışır?

### İlk Çalıştırma:
- Hemen 1 video bulur ve yükler

### Sonraki Çalıştırmalar:
- Her 3 saatte bir otomatik çalışır
- TikTok'tan 1 video bulur
- İndirir
- YouTube'a yükler

### Günlük Sonuç:
- 8 video/gün
- 56 video/hafta
- 240 video/ay

---

## 📊 İstatistikler

Scheduler çalışırken göreceksin:

```
🤖 Otomasyon Başladı - 2026-02-15 22:00:00
============================================================
📊 Toplam yüklenen: 15
📊 Toplam başarısız: 2

🔍 Apify ile TikTok'tan 1 video aranıyor...
   ✅ Komik video başlığı... (👁️ 1,234,567)

✅ 1 video bulundu

--- Video 1/1 ---
⬇️ İndiriliyor: video.mp4
✅ İndirildi: data/videos/video.mp4
📤 YouTube'a yükleniyor...
✅ Yükleme başarılı: https://www.youtube.com/watch?v=xxxxx
🎉 Başarılı! YouTube: https://www.youtube.com/watch?v=xxxxx

🧹 Eski videolar temizleniyor...
✅ Döngü tamamlandı! 1 video yüklendi.

⏰ Scheduler aktif! Sonraki çalışma: 2026-02-16 01:00:00
```

---

## ⚙️ Ayarlar

### Video Sayısını Değiştir

`scheduler.py` dosyasında:

```python
max_videos = 1  # Her 3 saatte 1 video
```

Değiştir:

```python
max_videos = 2  # Her 3 saatte 2 video = günde 16 video
```

### Çalışma Aralığını Değiştir

```python
schedule.every(3).hours.do(run_automation)  # Her 3 saat
```

Değiştir:

```python
schedule.every(2).hours.do(run_automation)  # Her 2 saat
schedule.every(6).hours.do(run_automation)  # Her 6 saat
schedule.every().day.at("20:00").do(run_automation)  # Her gün 20:00
```

### Hashtag'leri Değiştir

`config/config.yaml` dosyasında:

```yaml
tiktok:
  search_hashtags:
    - "komedi"
    - "mizah"
    - "eğlence"
```

---

## 🍓 Raspberry Pi'da Çalıştırma

### 1. Projeyi Kur

```bash
cd ~
git clone <repo-url>
cd tiktok-youtube-automation
sudo bash raspberry-pi-setup.sh
```

### 2. Credentials Kopyala

Bilgisayarından Raspberry Pi'ya:

```bash
scp .env pi@raspberrypi:~/tiktok-youtube-automation/
scp config/credentials.json pi@raspberrypi:~/tiktok-youtube-automation/config/
scp config/token.pickle pi@raspberrypi:~/tiktok-youtube-automation/config/
```

### 3. Systemd Servisi Oluştur

```bash
sudo nano /etc/systemd/system/tiktok-scheduler.service
```

İçeriği:

```ini
[Unit]
Description=TikTok YouTube Scheduler
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/tiktok-youtube-automation
Environment="PATH=/home/pi/tiktok-youtube-automation/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/pi/tiktok-youtube-automation/venv/bin/python /home/pi/tiktok-youtube-automation/scheduler.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

### 4. Servisi Başlat

```bash
sudo systemctl daemon-reload
sudo systemctl enable tiktok-scheduler
sudo systemctl start tiktok-scheduler
```

### 5. Durumu Kontrol Et

```bash
sudo systemctl status tiktok-scheduler
journalctl -u tiktok-scheduler -f  # Log'ları izle
```

---

## 💰 Apify Maliyeti

### Free Plan:
- Ayda $5 kredi (ücretsiz)
- Her video ~$0.02
- 250 video/ay ücretsiz
- Bizim sistem: 240 video/ay
- **Yeterli!** 🎉

### Paid Plan:
- Daha fazla video için
- $49/ay başlangıç

---

## 🔧 Sorun Giderme

### "APIFY_API_TOKEN bulunamadı"
- `.env` dosyasını kontrol et
- Token'ı doğru yapıştırdın mı?

### "credentials.json bulunamadı"
- `YOUTUBE_API_SETUP.md` dosyasını oku
- Google Cloud Console'dan credentials al

### "YouTube API kotası doldu"
- Günlük limit: 10,000 birim
- Her yükleme: ~1,600 birim
- Max 6 video/gün
- Yarın tekrar dene

### Scheduler durdu
- Raspberry Pi'da: `sudo systemctl restart tiktok-scheduler`
- Manuel: `python scheduler.py`

---

## 📈 Başarı İpuçları

### İlk Hafta:
- Sistemi izle
- Log'ları kontrol et
- Ayarları optimize et

### İkinci Hafta:
- Hashtag'leri güncelle
- Başlık formatını özelleştir
- Analytics'i takip et

### Üçüncü Hafta:
- Tam otomatik bırak
- Sadece haftalık kontrol yap
- Yeni hashtag'ler ekle

---

## 🎉 Sonuç

Artık tamamen otomatik bir TikTok → YouTube sisteminiz var!

- ✅ Sıfır manuel iş
- ✅ Her 3 saatte otomatik çalışır
- ✅ Ayda 240 video
- ✅ Raspberry Pi'da 7/24

**Tek yapman gereken:** Scheduler'ı başlat ve unut! 🚀

---

## 📞 Komutlar

```bash
# Scheduler'ı başlat
python scheduler.py

# Test et (tek video)
python src/tiktok_apify_scraper.py

# Raspberry Pi servisi
sudo systemctl start tiktok-scheduler
sudo systemctl stop tiktok-scheduler
sudo systemctl status tiktok-scheduler
journalctl -u tiktok-scheduler -f

# Log'ları temizle
sudo journalctl --vacuum-time=7d
```

---

## ✅ Checklist

- [ ] Apify token ekledim (`.env`)
- [ ] YouTube credentials ekledim (`config/credentials.json`)
- [ ] İlk test yaptım (`python src/tiktok_apify_scraper.py`)
- [ ] Scheduler'ı başlattım (`python scheduler.py`)
- [ ] Raspberry Pi'ya kurdum (opsiyonel)
- [ ] Systemd servisi aktif (opsiyonel)

Hepsi tamam mı? O zaman hazırsın! 🎉
