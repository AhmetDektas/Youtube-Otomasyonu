# 🎬 Başlık ve Açıklama Özelleştirme

## ✨ Yeni Özellikler

Artık videolar için otomatik olarak:
- ✅ Çekici başlıklar oluşturulur
- ✅ Detaylı açıklamalar eklenir
- ✅ Optimize edilmiş tag'ler kullanılır
- ✅ Emoji'ler ve hook'lar eklenir

---

## 📝 Başlık Örnekleri

### Orijinal TikTok Başlığı:
```
Arkadaşımla yaptığımız şaka çok komik oldu 😂 #komedi #mizah
```

### Optimize Edilmiş YouTube Başlığı:
```
🎯 Arkadaşımla yaptığımız şaka çok komik oldu 😂 💯 Mükemmel
```

veya

```
😂 Gülmekten Öldüm 🔥 Arkadaşımla yaptığımız şaka çok komik oldu
```

veya

```
💀 Buna İnanamayacaksın | Arkadaşımla yaptığımız şaka çok komik oldu 😂
```

---

## 🎨 Başlık Şablonları

Sistem bu şablonlardan birini rastgele seçer:

1. `{emoji} {title} {hook}`
2. `{hook} {emoji} {title}`
3. `{title} {emoji} {cta}`
4. `{emoji} {title} | {hook}`

### Hook'lar (Dikkat Çekici):
- 😂 Gülmekten Öldüm
- 🔥 Bu Efsane
- 💀 Buna İnanamayacaksın
- 😱 Şok Oldum
- 🤣 Kahkaha Garantili
- ⚡ Viral Oldu
- 🎯 Mutlaka İzle
- 💯 Mükemmel
- 🚀 Rekor Kırdı
- ⭐ Harika

---

## 📄 Açıklama Formatı

```
🔥 1,500,000 izlenme ile viral oldu!

📱 TikTok'tan en komik videolar burada!

[Orijinal Başlık]

━━━━━━━━━━━━━━━━━━━━
🎬 İçerik Hakkında:
Bu video TikTok'ta viral olan en eğlenceli içeriklerden biri. Gülmek garantili! 😂

━━━━━━━━━━━━━━━━━━━━
👍 Beğenmeyi unutma!
🔔 Abone ol, daha fazlası için!
📤 Arkadaşlarınla paylaş!
💬 Yorumlarda görüşelim!

━━━━━━━━━━━━━━━━━━━━
🏷️ Etiketler:
#shorts #tiktok #komedi #mizah #eğlence #viral #türkiye

━━━━━━━━━━━━━━━━━━━━
📊 Orijinal Video İstatistikleri:
👁️ İzlenme: 1,500,000
❤️ Beğeni: 25,000
👤 Yazar: @kullanici123

━━━━━━━━━━━━━━━━━━━━
⚠️ Telif Hakkı:
Bu video TikTok'tan alınmıştır. Tüm hakları orijinal içerik üreticisine aittir.
```

---

## ⚙️ Özelleştirme

### Başlık Stilini Değiştir

`config/config.yaml` dosyasında:

```yaml
youtube:
  title_style: "optimized"  # veya "original"
```

- `optimized`: Otomatik çekici başlık
- `original`: TikTok'taki orijinal başlık

### Hook'ları Özelleştir

`src/title_generator.py` dosyasında `HOOKS` listesini düzenle:

```python
HOOKS = [
    "😂 Senin Hook'un",
    "🔥 Başka Hook",
    # Daha fazla ekle...
]
```

### Emoji'leri Değiştir

```python
EMOJIS = ["😂", "🤣", "🔥", "💀", "⚡"]  # İstediğin emoji'leri ekle
```

---

## 🏷️ Tag Optimizasyonu

Sistem otomatik olarak:
1. Config'teki base tag'leri alır
2. Başlıktan keyword'ler çıkarır
3. Trend tag'ler ekler
4. Duplicate'leri kaldırır
5. Max 15 tag kullanır

### Örnek Tag Listesi:
```
shorts, komedi, eğlence, tiktok, mizah, viral, trending, 
funny, comedy, türkiye, turkish, 2026, arkadaşımla, şaka
```

---

## 📊 YouTube Shorts İçin İpuçları

### Başlık:
- ✅ 60-80 karakter ideal
- ✅ Emoji kullan (dikkat çeker)
- ✅ Hook ile başla
- ✅ Merak uyandır
- ❌ Clickbait yapma

### Açıklama:
- ✅ İlk 2 satır önemli (önizlemede görünür)
- ✅ Hashtag'leri kullan
- ✅ CTA ekle (beğen, abone ol)
- ✅ İstatistikleri paylaş

### Tag'ler:
- ✅ "shorts" tag'i mutlaka olsun
- ✅ İlgili keyword'ler kullan
- ✅ Trend tag'leri ekle
- ✅ Max 15 tag

---

## 🎯 A/B Test Önerileri

Farklı başlık stilleri dene:

### Stil 1: Emoji + Hook
```
😂 Gülmekten Öldüm | Video Başlığı
```

### Stil 2: Hook + Emoji
```
💀 Buna İnanamayacaksın 🔥 Video Başlığı
```

### Stil 3: Basit + CTA
```
Video Başlığı 😂 #shorts
```

Hangisi daha fazla izlenme alıyor, onu kullan!

---

## 📈 Sonuçları İzle

YouTube Studio'da:
1. Analytics → Reach
2. "Impressions click-through rate" kontrol et
3. Hangi başlık stili daha iyi çalışıyor?
4. Config'i ona göre ayarla

---

## 💡 Pro İpuçları

1. **İlk 3 kelime çok önemli** - Dikkat çekici olsun
2. **Emoji'yi akıllıca kullan** - Fazla olmasın
3. **Merak uyandır** - Ama clickbait yapma
4. **Trend'leri takip et** - Güncel hashtag'ler kullan
5. **Test et** - Farklı stilleri dene

---

## ✅ Özet

Artık her video için:
- Otomatik çekici başlık
- Detaylı açıklama
- Optimize edilmiş tag'ler
- Viral potansiyeli yüksek format

Hepsi otomatik! 🚀
