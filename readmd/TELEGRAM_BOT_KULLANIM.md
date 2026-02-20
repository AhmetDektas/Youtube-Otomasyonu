# 🤖 Telegram Bot Kullanımı

Telegram'dan YouTube videolarını yönet!

---

## 🚀 Kurulum

### 1️⃣ Sunucuda Güncelle

```bash
cd /root/Youtube-Otomasyonu
git pull
pip install -r requirements.txt
```

### 2️⃣ Telegram Bot Servisini Kur

```bash
nano /etc/systemd/system/telegram-bot.service
```

`telegram-bot-service.txt` içeriğini yapıştır, kaydet.

```bash
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot
systemctl status telegram-bot
```

### 3️⃣ YouTube Bot'u Yeniden Başlat

```bash
systemctl restart youtube-bot
```

---

## 📱 Kullanım

### Video Başlığını Değiştir

```
/title Yeni Video Başlığı Buraya
```

**Örnek:**
```
/title En Komik TikTok Videoları 2024 😂
```

### Video Açıklamasını Değiştir

```
/description Yeni açıklama buraya
```

**Örnek:**
```
/description Bu videoda en komik TikTok'ları derledik! Beğenmeyi unutmayın 👍
```

### Son Video Bilgisi

```
/info
```

### Yardım

```
/help
```

---

## 🎯 Nasıl Çalışır?

1. Bot video yükler (otomatik başlıkla)
2. Telegram'a bildirim gelir
3. Sen `/title Yeni Başlık` yazarsın
4. Bot YouTube'da başlığı günceller
5. Onay mesajı gelir

---

## 📊 Kontrol Komutları

```bash
# Bot durumu
systemctl status telegram-bot

# Log izle
journalctl -u telegram-bot -f

# Yeniden başlat
systemctl restart telegram-bot
```

---

## 💡 İpuçları

- Başlık max 100 karakter
- Açıklama max 5000 karakter
- Sadece son yüklenen video için çalışır
- Emoji kullanabilirsin 😊

---

## 🆘 Sorun Giderme

### Bot yanıt vermiyor

```bash
systemctl status telegram-bot
journalctl -u telegram-bot -n 50
```

### "Video bulunamadı" hatası

Video henüz yüklenmemiş, bekle.

### Başlık güncellenmiyor

YouTube API hatası olabilir, log'lara bak.

---

## 🎉 Örnek Kullanım

```
# Video yüklendi, Telegram'a mesaj geldi:
✅ Video Yüklendi!
📹 Başlık: komedi funnyvideos funny...
🎥 YouTube: https://youtube.com/watch?v=ABC123

# Sen yazarsın:
/title En Komik TikTok Anları 2024 😂🔥

# Bot cevap verir:
✅ Başlık güncellendi!
📹 Yeni Başlık: En Komik TikTok Anları 2024 😂🔥
🎥 Video: https://youtube.com/watch?v=ABC123
```

Artık videolarını Telegram'dan yönetebilirsin! 🚀
