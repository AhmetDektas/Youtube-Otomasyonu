# 💰 Apify Maliyet Analizi

## 📊 Apify Fiyatlandırma

### Free Plan (Ücretsiz):
- **$5 kredi/ay** (ücretsiz)
- Compute Unit (CU) başına: **$0.30**
- 2 concurrent run
- 8 GB RAM
- Community support

### Starter Plan:
- **$29/ay** + pay as you go
- CU başına: **$0.30**
- 5 concurrent run
- 32 GB RAM

---

## 🎯 TikTok Scraper Maliyeti

### Clockworks TikTok Scraper:
Kullandığımız actor: `clockworks/tiktok-scraper`

**Ortalama Maliyet:**
- 1 hashtag araması: ~0.02-0.05 CU
- 30 video scrape: ~0.1-0.2 CU
- Video metadata: Çok az (neredeyse bedava)

**Bizim Kullanım:**
- Her 3 saatte 1 video
- Günde 8 video
- Ayda 240 video

---

## 💵 Aylık Maliyet Hesabı

### Senaryo 1: Sadece Metadata (Video URL yok)
```
240 video/ay × 0.02 CU = 4.8 CU
4.8 CU × $0.30 = $1.44/ay
```
✅ **Free plan yeterli!** ($5 kredi var)

### Senaryo 2: Video URL ile (shouldDownloadVideos: true)
```
240 video/ay × 0.05 CU = 12 CU
12 CU × $0.30 = $3.60/ay
```
✅ **Free plan yeterli!** ($5 kredi var)

### Senaryo 3: Yoğun Kullanım (Günde 20 video)
```
600 video/ay × 0.05 CU = 30 CU
30 CU × $0.30 = $9/ay
```
⚠️ Free plan dolabilir, Starter plan gerekebilir

---

## 📈 Gerçek Kullanım Örneği

### Bizim Sistem:
- **Her 3 saatte 1 video** = 8 video/gün
- **Ayda 240 video**
- **Tahmini maliyet: $3-4/ay**

### Free Plan ile:
- $5 kredi/ay
- **Yeterli!** 🎉
- Hatta biraz kredi kalır

---

## 🔍 Detaylı Maliyet Kırılımı

### 1 Video İçin:
```
Hashtag araması:     0.01 CU
Video metadata:      0.01 CU
Video URL çıkarma:   0.01 CU
─────────────────────────────
Toplam:             ~0.03 CU
```

### Aylık (240 video):
```
240 × 0.03 CU = 7.2 CU
7.2 × $0.30 = $2.16/ay
```

### Yıllık:
```
$2.16 × 12 = $25.92/yıl
```

---

## 💡 Maliyet Optimizasyonu

### 1. Hashtag Sayısını Azalt
```yaml
tiktok:
  search_hashtags:
    - "komedi"  # Sadece 1 hashtag
```
Tasarruf: %30-40

### 2. resultsPerPage Ayarla
```python
"resultsPerPage": 10  # 20 yerine 10
```
Tasarruf: %20

### 3. Cache Kullan
Aynı hashtag'i tekrar aramak yerine cache'den al
Tasarruf: %50

---

## 📊 Alternatif Actor'lar

### 1. Clockworks TikTok Scraper (Kullandığımız)
- Maliyet: ~$0.03/video
- Hız: Orta
- Güvenilirlik: Yüksek
- ✅ **Önerilen**

### 2. Fast TikTok Scraper (Pay per video)
- Maliyet: ~$0.01/video
- Hız: Hızlı
- Güvenilirlik: Orta

### 3. TikTok API Scraper
- Maliyet: ~$0.05/video
- Hız: Çok hızlı
- Güvenilirlik: Çok yüksek

---

## 🎯 Öneriler

### Free Plan ile (Bizim Durum):
- ✅ Günde 8 video yükle
- ✅ Ayda 240 video
- ✅ Maliyet: $3-4/ay
- ✅ Free plan yeterli!

### Daha Fazla Video İçin:
- Günde 20 video → Starter plan ($29/ay)
- Günde 50 video → Scale plan ($199/ay)

---

## 💰 Toplam Sistem Maliyeti

### Aylık:
```
Apify (Free):        $0 (kredi dahil)
YouTube API:         $0 (ücretsiz)
Raspberry Pi:        ~$5 (elektrik)
─────────────────────────────
Toplam:             ~$5/ay
```

### Yıllık:
```
Apify:              $0 (free plan)
YouTube API:        $0
Raspberry Pi:       $60 (elektrik)
─────────────────────────────
Toplam:            ~$60/yıl
```

---

## 📈 Kullanım Takibi

### Apify Console'da:
1. **Usage** sekmesine git
2. **Compute units** grafiğini kontrol et
3. Aylık kullanımı gör

### Uyarı Ayarla:
1. Settings → Notifications
2. "Usage limit" ayarla
3. %80'e ulaşınca email al

---

## 🔔 Limit Dolduğunda Ne Olur?

### Free Plan Dolduğunda:
1. Actor çalışmayı durdurur
2. Email uyarısı gelir
3. Seçenekler:
   - Starter plan'e geç ($29/ay)
   - Sonraki ay bekle (kredi yenilenir)
   - Video sayısını azalt

---

## ✅ Sonuç

### Bizim Sistem İçin:
- **Free plan yeterli!** 🎉
- Ayda $5 kredi
- Kullanım: ~$3-4
- Kalan kredi: ~$1-2

### Önerilen Kullanım:
- Günde 8 video (her 3 saatte 1)
- Ayda 240 video
- Tamamen ücretsiz!

### Eğer Daha Fazla Video İstersen:
- Günde 15 video'ya kadar free plan yeterli
- Daha fazlası için Starter plan ($29/ay)

---

## 🎯 Özet

**Maliyet:** Neredeyse bedava! 🎉

Free plan ile ayda 240 video yükleyebilirsin. Tek maliyet Raspberry Pi'nin elektriği (~$5/ay).

Toplam sistem maliyeti: **~$5/ay** veya **~$60/yıl**

Çok ucuz! 🚀
