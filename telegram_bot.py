#!/usr/bin/env python3
"""
Telegram Bot - Interaktif Komutlar
Video başlıklarını ve açıklamalarını güncelle
"""

import os
import json
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from src.youtube_uploader import YouTubeUploader
import yaml

# .env yükle
load_dotenv()

# Config yükle
with open('config/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# YouTube uploader
uploader = YouTubeUploader(config)

# Son yüklenen video ID'sini sakla
LAST_VIDEO_FILE = 'data/last_video.json'

def get_last_video_id():
    """Son yüklenen video ID'sini al"""
    try:
        if os.path.exists(LAST_VIDEO_FILE):
            with open(LAST_VIDEO_FILE, 'r') as f:
                data = json.load(f)
                return data.get('video_id')
    except:
        pass
    return None

def save_last_video_id(video_id):
    """Son yüklenen video ID'sini kaydet"""
    try:
        with open(LAST_VIDEO_FILE, 'w') as f:
            json.dump({'video_id': video_id}, f)
    except Exception as e:
        print(f"❌ Video ID kaydedilemedi: {e}")

async def title_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    video_id = get_last_video_id()
    if not video_id:
        await update.message.reply_text(
            "❌ Henüz yüklenmiş video yok!\n"
            "Video yüklendikten sonra başlığı değiştirebilirsin."
        )
        return
    
    try:
        # YouTube'da başlığı güncelle
        await update.message.reply_text(f"⏳ Başlık güncelleniyor...")
        
        success = uploader.update_video_title(video_id, new_title)
        
        if success:
            await update.message.reply_text(
                f"✅ Başlık güncellendi!\n\n"
                f"📹 Yeni Başlık: {new_title}\n"
                f"🎥 Video: https://youtube.com/watch?v={video_id}"
            )
        else:
            await update.message.reply_text(
                "❌ Başlık güncellenemedi!\n"
                "YouTube API hatası olabilir."
            )
    
    except Exception as e:
        await update.message.reply_text(f"❌ Hata: {str(e)}")

async def description_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    video_id = get_last_video_id()
    if not video_id:
        await update.message.reply_text("❌ Henüz yüklenmiş video yok!")
        return
    
    try:
        await update.message.reply_text(f"⏳ Açıklama güncelleniyor...")
        
        success = uploader.update_video_description(video_id, new_description)
        
        if success:
            await update.message.reply_text(
                f"✅ Açıklama güncellendi!\n\n"
                f"📝 Yeni Açıklama: {new_description[:100]}...\n"
                f"🎥 Video: https://youtube.com/watch?v={video_id}"
            )
        else:
            await update.message.reply_text("❌ Açıklama güncellenemedi!")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Hata: {str(e)}")

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Son yüklenen video bilgisi"""
    video_id = get_last_video_id()
    if not video_id:
        await update.message.reply_text("❌ Henüz yüklenmiş video yok!")
        return
    
    await update.message.reply_text(
        f"ℹ️ Son Yüklenen Video\n\n"
        f"🎥 Video ID: {video_id}\n"
        f"🔗 Link: https://youtube.com/watch?v={video_id}\n\n"
        f"💡 Başlığı değiştirmek için:\n"
        f"/title Yeni Başlık"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yardım komutu"""
    help_text = """
🤖 <b>YouTube Bot Komutları</b>

📝 <b>/title</b> Yeni Başlık
   Video başlığını değiştir
   Örnek: /title En İyi TikTok Videoları

📄 <b>/description</b> Yeni Açıklama
   Video açıklamasını değiştir
   Örnek: /description Komik videolar!

ℹ️ <b>/info</b>
   Son yüklenen video bilgisi

❓ <b>/help</b>
   Bu yardım mesajını göster

💡 <b>Not:</b> Komutlar sadece son yüklenen video için çalışır.
"""
    await update.message.reply_text(help_text, parse_mode='HTML')

def main():
    """Bot'u başlat"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN bulunamadı!")
        return
    
    print("🤖 Telegram Bot başlatılıyor...")
    print("💡 Komutlar: /title, /description, /info, /help")
    
    # Application oluştur
    application = Application.builder().token(bot_token).build()
    
    # Komutları ekle
    application.add_handler(CommandHandler("title", title_command))
    application.add_handler(CommandHandler("description", description_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", help_command))
    
    # Bot'u başlat
    print("✅ Bot çalışıyor! Ctrl+C ile durdurun.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot durduruldu!")
