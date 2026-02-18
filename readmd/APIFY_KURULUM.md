# 🚀 Apify Kurulum Rehberi

## 1️⃣ Apify API Token Al

### Adımlar:
1. ✅ Zaten Apify Console'dasın
2. Ekranda "API token" dropdown'ı var
3. Yanındaki **📋 kopyala** butonuna tıkla
4. Token kopyalandı!

## 2️⃣ Token'ı Projeye Ekle

### .env Dosyasını Düzenle:

```bash
# .env dosyasını aç
notepad .env
```

Token'ı yapıştır:

```env
# Apify API Token
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxxxx

# YouTube API (Opsiyonel)
# YOUTUBE_CLIENT_ID=your_client_id
# YOUTUBE_CLIENT_SECRET=your_client_secret

# Genel
DEBUG=False
```

Kaydet ve kapat.

## 3️⃣ Test Et

```bash
python src/tiktok_apify_scraper.py
```

Çalışırsa:
```
🤖 Apify TikTok Scraper Test
============================================================
🔍 Apify ile TikTok videoları toplanıyor...

🔍 #komedi araştırılıyor...
   ⏳ Apify actor çalışıyor...
   ✅ 3 video bulundu

📊 3 video bulundu

📋 Bulunan videolar:
1. Komik video başlığı... (👁️ 1,234,567)
2. Başka komik video... (👁️ 987,654)
3. Daha fazla komedi... (👁️ 543,210)

⬇️ İlk videoyu indiriyorum...
✅ TEST BAŞARILI: data/videos/video.mp4
```

## 4️⃣ Tam Otomatik Çalıştır

```bash
python src/main.py --mode once
```

Veya sürekli mod:

```bash
python src/main.py --mode continuous
```

## 🎯 Apify Avantajları

✅ Bot tespiti yok
✅ IP bloğu yok
✅ Hızlı ve güvenilir
✅ Metadata dahil (beğeni, izlenme sayısı)
✅ Rate limiting yok

## 💰 Apify Fiyatlandırma

### Free Plan:
- Ayda $5 kredi (ücretsiz)
- ~500 video scrape edebilirsin
- Günde 16 video = ayda 480 video
- Yeterli! 🎉

### Paid Plan:
- Daha fazla video için
- $49/ay başlangıç

## 📊 Kullanım Takibi

Apify Console'da:
- Usage → API calls
- Kaç kredi kullandığını gör
- Limit dolmadan uyarı al

## ⚙️ Ayarlar

`config/config.yaml` dosyasında:

```yaml
tiktok:
  search_hashtags:
    - "komedi"
    - "mizah"
    - "eğlence"
  max_videos_per_run: 5  # Günde 5 video = ayda 150 video
```

## 🔧 Sorun Giderme

### "APIFY_API_TOKEN bulunamadı"
- `.env` dosyasını kontrol et
- Token'ı doğru yapıştırdın mı?
- Dosyayı kaydettinmi?

### "Actor not found"
- Apify hesabın aktif mi?
- Free plan limiti doldu mu?

### "Rate limit exceeded"
- Çok fazla istek attın
- Biraz bekle (1-2 saat)
- Veya paid plan'e geç

## ✅ Hazır!

Artık sistem tam otomatik çalışıyor:
1. Apify TikTok'tan video topluyor
2. Videoları indiriyor
3. YouTube'a yüklüyor

Hepsi otomatik! 🚀
