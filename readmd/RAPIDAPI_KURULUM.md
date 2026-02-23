# RapidAPI Ücretsiz TikTok Scraper Kurulumu

## Neden RapidAPI?
- ✅ **Tamamen ücretsiz**: Ayda 500 istek
- ✅ **Güvenilir**: TikTok engellemez
- ✅ **Kolay kurulum**: Sadece API key gerekli
- ✅ **Backup sistem**: Başarısız olursa Apify devreye girer

## Maliyet Karşılaştırması

| Yöntem | Aylık Maliyet | Video Sayısı |
|--------|---------------|--------------|
| Sadece Apify | ~$44 | 240 video |
| RapidAPI + Apify | **$0-5** | 240 video |
| Sadece RapidAPI | **$0** | 165 video (500 istek) |

## Kurulum Adımları

### 1. RapidAPI Hesabı Oluştur
1. https://rapidapi.com/ adresine git
2. "Sign Up" ile ücretsiz hesap aç
3. Email ile doğrula

### 2. TikTok Scraper API'ye Abone Ol
1. https://rapidapi.com/tikwm-tikwm-default/api/tiktok-scraper7 adresine git
2. "Subscribe to Test" butonuna tıkla
3. **Basic Plan** seç (Ücretsiz - 500 istek/ay)
4. Kredi kartı isterse **atla** (ücretsiz plan için gerekli değil)

### 3. API Key'i Al
1. API sayfasında **"Code Snippets"** bölümüne git
2. Sağ üstte **"X-RapidAPI-Key"** değerini kopyala
3. Örnek: `1234567890abcdefghijklmnopqrstuv`

### 4. .env Dosyasına Ekle
```bash
# .env dosyasını aç
nano .env

# RAPIDAPI_KEY satırını bul ve key'i yapıştır
RAPIDAPI_KEY=1234567890abcdefghijklmnopqrstuv

# Kaydet ve çık (Ctrl+X, Y, Enter)
```

### 5. Botu Yeniden Başlat
```bash
systemctl restart youtube-bot
journalctl -u youtube-bot -f
```

## Nasıl Çalışır?

Hybrid sistem 3 aşamalı:

1. **RapidAPI dener** (ücretsiz, 500 istek/ay)
   - Başarılı ✅ → Video indirilir
   - Başarısız ❌ → 2. aşamaya geç

2. **Apify dener** (ücretli, backup)
   - Başarılı ✅ → Video indirilir
   - Başarısız ❌ → Video atlanır

3. **Sonraki hashtag'e geç**

## Kullanım İstatistikleri

- Her döngü: 4 hashtag × 1 istek = **4 istek**
- Günde 8 döngü: 4 × 8 = **32 istek**
- Ayda: 32 × 30 = **960 istek**

**Sorun:** 500 istek/ay yeterli değil!

**Çözüm:** Hashtag sayısını azalt veya döngü süresini artır

### Seçenek 1: Hashtag Azalt (Önerilen)
```yaml
# config/config.yaml
tiktok:
  search_hashtags:
    - "komedi"  # Sadece 1 hashtag
```
- Aylık istek: 240 (500 limitin altında ✅)
- Maliyet: **$0**

### Seçenek 2: Döngü Süresini Artır
```yaml
# config/config.yaml
general:
  check_interval: 10800  # 3 saat (şu anki)
  # check_interval: 21600  # 6 saate çıkar
```
- Günde 4 döngü = Ayda 480 istek (500 limitin altında ✅)
- Maliyet: **$0**

## Sorun Giderme

### RapidAPI çalışmıyor
```bash
# Logları kontrol et
journalctl -u youtube-bot -n 50

# Şunu görmelisin:
# "💚 Ücretsiz RapidAPI deneniyor..."
# "✅ RapidAPI: X video bulundu"
```

### API Key geçersiz
```bash
# .env dosyasını kontrol et
cat .env | grep RAPIDAPI

# Key'in doğru olduğundan emin ol
# Boşluk veya özel karakter olmamalı
```

### 500 istek limiti doldu
```bash
# Apify backup devreye girer
# "🔵 Apify backup kullanılıyor..." mesajını görürsün

# Yeni ay başında limit sıfırlanır
# https://rapidapi.com/developer/billing
```

## Alternatif Ücretsiz API'ler

Eğer RapidAPI de çalışmazsa:

1. **TikAPI** - https://rapidapi.com/tikapi/api/tiktok-api
   - 100 istek/ay ücretsiz

2. **TikTok Downloader** - https://rapidapi.com/yi005/api/tiktok-download-without-watermark
   - 50 istek/ay ücretsiz

3. **Sadece Apify** - Aylık $5 ücretsiz kredi
   - ~27 video/ay

## Sonuç

✅ RapidAPI key ekle → Tamamen ücretsiz (hashtag azaltırsan)
❌ RapidAPI key yok → Apify backup kullanılır (~$44/ay)
