# 📹 Video Yönetimi ve Disk Kullanımı

## ⏰ Video Temizleme Ayarı

### Varsayılan: 1 Gün

```yaml
# config/config.yaml
general:
  video_retention_days: 1  # 24 saat sonra sil
```

## 📊 Disk Kullanımı Hesabı

### Günlük Kullanım:
```
8 video/gün × 7.5 MB = ~60 MB/gün
```

### Farklı Ayarlar:

| Süre | Video Sayısı | Disk Kullanımı | Önerim |
|------|-------------|----------------|--------|
| 6 saat | 2 video | ~15 MB | ⚠️ Çok az (riskli) |
| 12 saat | 4 video | ~30 MB | ⚠️ Az (sorun olursa yedek yok) |
| **1 gün** | **8 video** | **~60 MB** | ✅ **İdeal** |
| 2 gün | 16 video | ~120 MB | ⚠️ Gereksiz |
| 3 gün | 24 video | ~180 MB | ❌ Fazla |
| 7 gün | 56 video | ~420 MB | ❌ Çok fazla |

## ✅ Neden 1 Gün İdeal?

### Avantajlar:
1. **Yeterli Yedek:** 24 saat yedek kalır
2. **Az Yer:** ~60 MB (Raspberry Pi için çok az)
3. **Güvenli:** Sorun olursa video hala var
4. **Temiz:** Disk dolmaz

### Duplicate Kontrolü:
- Video silinse bile `uploaded.json` dosyasında kayıt var
- Aynı video tekrar yüklenmez ✅
- Video dosyası gereksiz, sadece kayıt önemli

## 🔧 Farklı Senaryolar

### Senaryo 1: Çok Agresif (6 saat)
```yaml
video_retention_days: 0.25  # 6 saat
```
- Disk: ~15 MB
- Risk: Yüksek (sorun olursa video yok)
- ❌ Önerilmez

### Senaryo 2: Dengeli (1 gün) ✅
```yaml
video_retention_days: 1  # 24 saat
```
- Disk: ~60 MB
- Risk: Düşük
- ✅ **Önerilen**

### Senaryo 3: Güvenli (2 gün)
```yaml
video_retention_days: 2  # 48 saat
```
- Disk: ~120 MB
- Risk: Çok düşük
- ⚠️ Gereksiz (1 gün yeterli)

## 💾 Raspberry Pi Disk Durumu

### Raspberry Pi 4 (32GB SD Kart):
```
OS + Sistem:        ~4 GB
Python + Paketler:  ~500 MB
Videolar (1 gün):   ~60 MB
Logs:               ~10 MB
─────────────────────────────
Toplam Kullanım:   ~4.5 GB
Boş Alan:          ~27.5 GB
```

**Sonuç:** 1 gün ayarı ile disk asla dolmaz! ✅

### Raspberry Pi Zero 2 W (16GB SD Kart):
```
OS + Sistem:        ~3 GB
Python + Paketler:  ~400 MB
Videolar (1 gün):   ~60 MB
Logs:               ~10 MB
─────────────────────────────
Toplam Kullanım:   ~3.5 GB
Boş Alan:          ~12.5 GB
```

**Sonuç:** Yine sorun yok! ✅

## 📈 Uzun Vadeli Kullanım

### 1 Yıl Sonra:
```
Videolar (1 gün):      ~60 MB (sabit)
uploaded.json:         ~5 MB (2,920 kayıt)
Logs (7 gün rotation): ~50 MB
─────────────────────────────────────
Toplam:               ~115 MB
```

**Sonuç:** 1 yıl sonra bile sadece ~115 MB! ✅

## 🔍 Disk Kullanımını İzleme

### Scheduler Çıktısı:
```
📊 Toplam yüklenen: 150
📊 Toplam başarısız: 2
💾 Disk kullanımı: 8 video, 62.3 MB
```

### Manuel Kontrol:
```bash
# Raspberry Pi'da
du -sh ~/tiktok-youtube-bot/data/videos/
# Çıktı: 62M

# Video sayısı
ls ~/tiktok-youtube-bot/data/videos/*.mp4 | wc -l
# Çıktı: 8
```

## ⚙️ Otomatik Temizleme

### Ne Zaman Çalışır?
Her döngü sonunda (her 3 saatte bir):
```python
content_manager.cleanup_old_videos(max_age_days=1)
```

### Çıktı:
```
🧹 Eski videolar temizleniyor...
🗑️ Silindi: video1.mp4 (7.2 MB)
🗑️ Silindi: video2.mp4 (8.1 MB)
✅ 2 video temizlendi (15.3 MB boşaltıldı)
```

Veya:
```
🧹 Eski videolar temizleniyor...
ℹ️ Silinecek eski video yok
```

## 🎯 Öneriler

### Raspberry Pi 4 (2GB+):
```yaml
video_retention_days: 1  # İdeal
```

### Raspberry Pi Zero 2 W:
```yaml
video_retention_days: 1  # Yine ideal
```

### Çok Düşük Disk (8GB SD Kart):
```yaml
video_retention_days: 0.5  # 12 saat (minimum)
```

## 🚨 Acil Durum

### Disk Doldu?
```bash
# Tüm videoları sil (uploaded.json korunur)
rm ~/tiktok-youtube-bot/data/videos/*.mp4

# Log'ları temizle
sudo journalctl --vacuum-time=1d
```

### Duplicate Kontrolü Bozuldu?
```bash
# uploaded.json yedekle
cp ~/tiktok-youtube-bot/data/uploaded.json ~/uploaded.json.backup

# Düzenle (son 100 kaydı tut)
# Manuel düzenleme gerekirse
```

## ✅ Sonuç

**1 gün ayarı mükemmel!**

- ✅ Yeterli yedek (24 saat)
- ✅ Az yer (~60 MB)
- ✅ Duplicate kontrolü çalışır
- ✅ Disk asla dolmaz
- ✅ Raspberry Pi için ideal

**Değiştirmeye gerek yok!** 🚀
