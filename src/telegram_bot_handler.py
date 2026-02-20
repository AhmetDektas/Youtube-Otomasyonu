#!/usr/bin/env python3
"""
Telegram Bot Handler
Kullanıcıdan komut alır ve YouTube videolarını yönetir
"""

import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from src.youtube_uploader import YouTubeUploader
import yaml

class TelegramBotHandler:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        
        # Config yükle
        with open('config/config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.uploader = YouTubeUploader(self.config)
        self.last_video_id = None
    
    def set_last_video_id(self, video_id):
        """Son yüklenen video ID'sini kaydet"""
        self.last_video_id = video_id
    
    async def title_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /title komutu - Video başlığını güncelle
        Kullanım: /title Yeni Video Başlığı
        """
        if not context.args:
            await update.message.reply_text(
                "❌ Kullanım: /title Yeni Video Başlığı\n\n"
                "Örnek: /title En Komik TikTok Videoları 2024"
            )
            return
        
        # Yeni başlık
        new_title = ' '.join(context.args)
        
        if not self.last_video_id:
            await update.message.reply_text(
                "❌ Henüz yüklenmiş video yok!\n"
                "Video yüklendikten sonra başlığı değiştirebilirsin."
            )
            return
        
        try:
            # YouTube'da başlığı güncelle
            await update.message.reply_text(f"⏳ Başlık güncelleniyor...")
            
            success = self.uploader.update_video_title(self.last_video_id, new_title)
            
            if success:
                await update.message.reply_text(
                    f"✅ Başlık güncellendi!\n\n"
                    f"📹 Yeni Başlık: {new_title}\n"
                    f"🎥 Video: https://youtube.com/watch?v={self.last_video_id}"
                )
            else:
                await update.message.reply_text(
                    "❌ Başlık güncellenemedi!\n"
                    "YouTube API hatası olabilir."
                )
        
        except Exception as e:
            await update.message.reply_text(f"❌ Hata: {str(e)}")
    
    async def description_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /description komutu - Video açıklamasını güncelle
        Kullanım: /description Yeni açıklama
        """
        if not context.args:
            await update.message.reply_text(
                "❌ Kullanım: /description Yeni açıklama\n\n"
                "Örnek: /description Bu videoda en komik TikTok'ları derledik!"
            )
            return
        
        new_description = ' '.join(context.args)
        
        if not self.last_video_id:
            await update.message.reply_text("❌ Henüz yüklenmiş video yok!")
            return
        
        try:
            await update.message.reply_text(f"⏳ Açıklama güncelleniyor...")
            
            success = self.uploader.update_video_description(self.last_video_id, new_description)
            
            if success:
                await update.message.reply_text(
                    f"✅ Açıklama güncellendi!\n\n"
                    f"📝 Yeni Açıklama: {new_description[:100]}...\n"
                    f"🎥 Video: https://youtube.com/watch?v={self.last_video_id}"
                )
            else:
                await update.message.reply_text("❌ Açıklama güncellenemedi!")
        
        except Exception as e:
            await update.message.reply_text(f"❌ Hata: {str(e)}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Yardım komutu"""
        help_text = """
🤖 <b>YouTube Bot Komutları</b>

📝 <b>/title</b> Yeni Başlık
   Video başlığını değiştir
   Örnek: /title En İyi TikTok Videoları

📄 <b>/description</b> Yeni Açıklama
   Video açıklamasını değiştir
   Örnek: /description Komik videolar!

ℹ️ <b>/help</b>
   Bu yardım mesajını göster

💡 <b>Not:</b> Komutlar sadece son yüklenen video için çalışır.
"""
        await update.message.reply_text(help_text, parse_mode='HTML')
    
    def run(self):
        """Bot'u başlat (arka planda)"""
        if not self.bot_token:
            print("⚠️  Telegram bot token bulunamadı, bot çalışmayacak")
            return
        
        # Application oluştur
        application = Application.builder().token(self.bot_token).build()
        
        # Komutları ekle
        application.add_handler(CommandHandler("title", self.title_command))
        application.add_handler(CommandHandler("description", self.description_command))
        application.add_handler(CommandHandler("help", self.help_command))
        
        # Bot'u başlat (non-blocking)
        print("🤖 Telegram bot başlatılıyor...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


# Global instance
bot_handler = None

def get_bot_handler():
    """Bot handler instance'ını al"""
    global bot_handler
    if bot_handler is None:
        bot_handler = TelegramBotHandler()
    return bot_handler
