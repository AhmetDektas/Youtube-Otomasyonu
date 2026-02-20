#!/usr/bin/env python3
"""
Telegram Bildirim Sistemi
YouTube bot durumu hakkında Telegram'dan bildirim gönderir
"""

import requests
import os
from datetime import datetime

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        self.enabled = bool(self.bot_token and self.chat_id)
        
        if not self.enabled:
            print("⚠️  Telegram bildirimleri devre dışı (token veya chat_id yok)")
    
    def send_message(self, message, parse_mode='HTML'):
        """Telegram'a mesaj gönder"""
        if not self.enabled:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Telegram mesaj gönderilemedi: {e}")
            return False
    
    def notify_video_downloaded(self, video_title, tiktok_url):
        """Video indirildiğinde bildir"""
        message = f"""
🎬 <b>Video İndirildi</b>

📹 <b>Başlık:</b> {video_title}
🔗 <b>TikTok:</b> {tiktok_url}
⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⏳ YouTube'a yükleniyor...
"""
        return self.send_message(message)
    
    def notify_video_uploaded(self, video_title, youtube_url):
        """Video yüklendiğinde bildir"""
        message = f"""
✅ <b>Video Yüklendi!</b>

📹 <b>Başlık:</b> {video_title}
🎥 <b>YouTube:</b> {youtube_url}
⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎉 Başarıyla yayında!
"""
        return self.send_message(message)
    
    def notify_error(self, error_type, error_message):
        """Hata oluştuğunda bildir"""
        message = f"""
❌ <b>Hata Oluştu</b>

🔴 <b>Tip:</b> {error_type}
📝 <b>Mesaj:</b> {error_message}
⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️ Kontrol gerekebilir!
"""
        return self.send_message(message)
    
    def notify_bot_started(self):
        """Bot başladığında bildir"""
        message = f"""
🚀 <b>Bot Başlatıldı</b>

✅ YouTube TikTok Otomasyon çalışıyor
⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 Her 3 saatte 1 video yüklenecek
"""
        return self.send_message(message)
    
    def notify_bot_stopped(self):
        """Bot durduğunda bildir"""
        message = f"""
🛑 <b>Bot Durduruldu</b>

⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ℹ️ Bot manuel olarak durduruldu
"""
        return self.send_message(message)
    
    def notify_internet_lost(self):
        """İnternet kesildiğinde bildir"""
        message = f"""
📡 <b>İnternet Bağlantısı Kesildi</b>

⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔄 GSB WiFi otomatik giriş yapılıyor...
"""
        return self.send_message(message)
    
    def notify_internet_restored(self):
        """İnternet geri geldiğinde bildir"""
        message = f"""
✅ <b>İnternet Bağlantısı Geri Geldi</b>

⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎉 Bot çalışmaya devam ediyor
"""
        return self.send_message(message)
    
    def notify_daily_summary(self, videos_uploaded, videos_failed):
        """Günlük özet bildir"""
        message = f"""
📊 <b>Günlük Özet</b>

✅ <b>Yüklenen:</b> {videos_uploaded} video
❌ <b>Başarısız:</b> {videos_failed} video
⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 Toplam: {videos_uploaded + videos_failed} işlem
"""
        return self.send_message(message)
    
    def test_connection(self):
        """Telegram bağlantısını test et"""
        if not self.enabled:
            return False
        
        message = "🧪 <b>Test Mesajı</b>\n\n✅ Telegram bildirimleri çalışıyor!"
        return self.send_message(message)


# Test için
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    
    notifier = TelegramNotifier()
    
    if notifier.enabled:
        print("📱 Telegram test mesajı gönderiliyor...")
        if notifier.test_connection():
            print("✅ Test başarılı!")
        else:
            print("❌ Test başarısız!")
    else:
        print("❌ Telegram ayarları eksik (.env dosyasını kontrol et)")
