# 🤖 TikTok → YouTube Otomasyonu

Tam otomatik TikTok video bulma ve YouTube'a yükleme sistemi.

## ✨ Özellikler

- ✅ Apify ile otomatik TikTok video bulma
- ✅ Her 3 saatte bir çalışır (günde 8 video)
- ✅ Optimize edilmiş başlık ve açıklama
- ✅ Duplicate kontrolü (aynı video tekrar yüklenmez)
- ✅ Otomatik video temizleme (3 gün sonra)
- ✅ Raspberry Pi'da 7/24 çalışabilir

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
pip install -r requirements.txt
```

### 2. Apify Token Ekle

`.env` dosyasını düzenle:
```env
APIFY_API_TOKEN=apify_api_xxxxxxxxxx
```

### 3. YouTube Credentials Ekle

`YOUTUBE_API_SETUP.md` dosyasındaki adımları takip et.

### 4. Çalıştır

```bash
python scheduler.py
```

## 📁 Proje Yapısı

```
tiktok-youtube-bot/
├── scheduler.py              # Ana program (her 3 saatte çalışır)
├── src/
│   ├── tiktok_apify_scraper.py   # Apify ile TikTok scraping
│   ├── youtube_uploader.py       # YouTube yükleme
│   ├── content_manager.py        # Video yönetimi
│   └── title_generator.py        # Başlık optimizasyonu
├── config/
│   ├── config.yaml               # Ayarlar
│   └── credentials.json          # YouTube API (sen ekle)
├── data/
│   ├── videos/                   # İndirilen videolar (3 gün sonra silinir)
│   └── uploaded.json             # Yükleme kayıtları
└── .env                          # Apify token (sen ekle)
```

## ⚙️ Ayarlar

`config/config.yaml` dosyasını düzenle:

```yaml
tiktok:
  search_hashtags:
    - "komedi"
    - "mizah"
  max_videos_per_run: 5

youtube:
  title_style: "optimized"
  privacy_status: "public"

general:
  video_retention_days: 3  # Videoları 3 gün sonra sil
```

## 🍓 Raspberry Pi Kurulumu

Detaylı kurulum: `RASPBERRY_PI_KURULUM.md`

```bash
# Otomatik kurulum
sudo bash raspberry-pi-install.sh

# Servisi başlat
sudo systemctl start tiktok-bot
```

## 💰 Maliyet

- **Apify:** $0/ay (free plan, 240 video/ay)
- **YouTube API:** $0/ay (ücretsiz)
- **Raspberry Pi:** ~$1/ay (elektrik)
- **Toplam:** ~$1/ay

Detaylı analiz: `APIFY_MALIYET.md`

## 📊 Performans

- Her 3 saatte 1 video
- Günde 8 video
- Ayda 240 video
- Tamamen otomatik!

## 📝 Dokümantasyon

- `FINAL_KULLANIM.md` - Detaylı kullanım rehberi
- `YOUTUBE_API_SETUP.md` - YouTube API kurulumu
- `RASPBERRY_PI_KURULUM.md` - Raspberry Pi kurulumu
- `APIFY_KURULUM.md` - Apify kurulumu
- `BASLIK_OZELLESTIRME.md` - Başlık optimizasyonu
- `APIFY_MALIYET.md` - Maliyet analizi

## 🛠️ Komutlar

```bash
# Scheduler'ı başlat
python scheduler.py

# Başlık testi
python src/title_generator.py

# Raspberry Pi servisi
sudo systemctl start tiktok-bot
sudo systemctl status tiktok-bot
tail -f ~/tiktok-youtube-bot/logs/bot.log
```

## 🔧 Sorun Giderme

### Video temizleme ayarı

Videolar varsayılan olarak 3 gün sonra silinir. Değiştirmek için:

```yaml
# config/config.yaml
general:
  video_retention_days: 7  # 7 gün sonra sil
```

### Aynı video tekrar yükleniyor

Sistem otomatik duplicate kontrolü yapıyor. Eğer aynı video geliyorsa:
- Daha fazla hashtag ekle
- `max_videos_per_run` artır (daha fazla seçenek)

### Apify limiti doldu

Free plan: $5/ay kredi
- Günde 8 video: ~$3-4/ay kullanım
- Yeterli olmalı!

## 📈 İstatistikler

```bash
# Yüklenen videoları gör
cat data/uploaded.json | python -m json.tool

# Log'ları kontrol et
tail -f logs/bot.log
```

## ✅ Lisans

MIT License

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

---

**Not:** Bu sistem eğitim amaçlıdır. TikTok ve YouTube'un kullanım şartlarına uygun kullanın.
