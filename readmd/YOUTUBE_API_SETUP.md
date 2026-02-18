# 📺 YouTube API Kurulum Rehberi

## Adım 1: Google Cloud Console

1. [console.cloud.google.com](https://console.cloud.google.com/) adresine git
2. Sağ üstten "Proje Seç" > "YENİ PROJE"
3. Proje adı: **TikTok Bot** (veya istediğin isim)
4. OLUŞTUR'a tıkla

## Adım 2: YouTube Data API v3 Aktif Et

1. Sol menüden **APIs & Services** > **Library**
2. Arama kutusuna **"YouTube Data API v3"** yaz
3. İlk sonuca tıkla
4. **ENABLE** (ETKİNLEŞTİR) butonuna tıkla

## Adım 3: OAuth Credentials Oluştur

1. Sol menüden **APIs & Services** > **Credentials**
2. Üstten **+ CREATE CREDENTIALS** > **OAuth client ID**

### OAuth Onay Ekranı (İlk Seferinde)

Eğer "OAuth consent screen" uyarısı gelirse:

1. **CONFIGURE CONSENT SCREEN** tıkla
2. **External** seç > **CREATE**
3. Bilgileri doldur:
   - App name: **TikTok Bot**
   - User support email: **kendi emailin**
   - Developer contact: **kendi emailin**
4. **SAVE AND CONTINUE**
5. Scopes ekranında **SAVE AND CONTINUE**
6. Test users ekranında **+ ADD USERS** > **kendi emailini ekle**
7. **SAVE AND CONTINUE**

### OAuth Client ID Oluştur

1. Application type: **Desktop app**
2. Name: **TikTok Bot Client**
3. **CREATE**
4. **DOWNLOAD JSON** butonuna tıkla
5. İndirilen dosyayı `config/credentials.json` olarak kaydet

## Adım 4: Dosyayı Yerleştir

İndirilen JSON dosyasını proje klasörüne kopyala:

```
tiktok-youtube-automation/
└── config/
    └── credentials.json  <-- Buraya kopyala
```

## Adım 5: İlk Çalıştırma

İlk kez çalıştırdığında tarayıcı açılacak:

```bash
python src/main.py --mode once
```

1. Google hesabınla giriş yap
2. "Google bu uygulamayı doğrulamadı" uyarısı gelirse:
   - **Gelişmiş** > **TikTok Bot'a git (güvensiz)** tıkla
3. İzinleri onayla
4. Token otomatik kaydedilecek (`config/token.pickle`)

## ✅ Hazır!

Artık bot YouTube'a video yükleyebilir.

## 🔒 Güvenlik

- `credentials.json` ve `token.pickle` dosyalarını kimseyle paylaşma
- `.gitignore` bu dosyaları zaten koruyor
- Test users listesine sadece kendi hesabını ekle

## 📊 Kotalar

- **Günlük limit**: 10,000 birim
- **Video yükleme**: ~1,600 birim
- **Günlük max video**: ~6 adet

Daha fazla kota için Google'a başvurabilirsin.

## ⚠️ Sorun Giderme

### "Access blocked: This app's request is invalid"

OAuth consent screen'i düzgün yapılandırmadın. Adım 3'ü tekrar kontrol et.

### "The user did not consent to the scopes required"

İzinleri vermedin. Tekrar çalıştır ve tüm izinleri onayla.

### "Daily Limit Exceeded"

Günlük kotayı doldurdun. Yarın tekrar dene veya başka bir Google hesabı kullan.
