"""
TAM OTOMATİK SCHEDULER
Her 3 saatte bir TikTok'tan video bulup YouTube'a yükler
"""
import yaml
import time
import schedule
from datetime import datetime
from src.tiktok_hybrid_scraper import TikTokHybridScraper
from src.youtube_uploader import YouTubeUploader
from src.content_manager import ContentManager
from src.title_generator import TitleGenerator
from src.telegram_notifier import TelegramNotifier


def run_automation():
    """Tek döngü - video bul, indir, yükle"""
    print(f"\n{'='*60}")
    print(f"🤖 Otomasyon Başladı - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)
    
    try:
        # Config yükle
        with open('config/config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Modüller
        scraper = TikTokHybridScraper(config)
        uploader = YouTubeUploader(config)
        content_manager = ContentManager()
        title_generator = TitleGenerator(config)
        telegram = TelegramNotifier()
        
        # İstatistikler
        stats = content_manager.get_stats()
        disk_usage = content_manager.get_disk_usage()
        
        print(f"📊 Toplam yüklenen: {stats['total_uploaded']}")
        print(f"📊 Toplam başarısız: {stats['total_failed']}")
        print(f"💾 Disk kullanımı: {disk_usage['count']} video, {disk_usage['size_mb']:.1f} MB\n")
        
        # TikTok'tan video topla (daha fazla al, rastgele seç)
        max_videos = 5  # Daha fazla video al, rastgele seçilecek
        
        print(f"🔍 Apify ile TikTok'tan {max_videos} video aranıyor...")
        videos = scraper.scrape_trending_videos(max_videos=max_videos)
        
        if not videos:
            print("⚠️ Video bulunamadı!")
            return
        
        print(f"\n✅ {len(videos)} video bulundu")
        
        # Yeni videoları filtrele
        new_videos = [v for v in videos if not content_manager.is_uploaded(v['url'])]
        
        if not new_videos:
            print("⚠️ Tüm videolar daha önce yüklendi!")
            print("💡 Sonraki döngüde farklı videolar bulunacak")
            return
        
        print(f"🆕 {len(new_videos)} yeni video var")
        
        # Sadece 1 tanesini yükle (rastgele seçilmiş)
        videos = new_videos[:1]
        print(f"📤 {len(videos)} video yüklenecek\n")
        
        # Her videoyu işle
        uploaded_count = 0
        skipped_count = 0
        
        for i, video_info in enumerate(videos, 1):
            print(f"\n--- Video {i}/{len(videos)} ---")
            
            # Daha önce yüklendi mi?
            if content_manager.is_uploaded(video_info['url']):
                print(f"⏭️ Atlandı (daha önce yüklendi): {video_info['title'][:50]}")
                skipped_count += 1
                
                # Eğer tüm videolar yüklendiyse, daha fazla ara
                if skipped_count >= len(videos):
                    print("\n⚠️ Tüm videolar daha önce yüklendi!")
                    print("💡 Daha fazla hashtag ekle veya farklı hashtag'ler dene")
                
                continue
            
            try:
                # Videoyu indir
                video_path = scraper.download_video(video_info)
                if not video_path:
                    content_manager.mark_failed(video_info['url'], "İndirme başarısız")
                    telegram.notify_error("Video İndirme", f"Video indirilemedi: {video_info['title'][:50]}")
                    continue
                
                # Telegram bildirimi - video indirildi
                telegram.notify_video_downloaded(video_info['title'][:100], video_info['url'])
                
                # YouTube'a yükle
                optimized_title = title_generator.generate_title(
                    video_info['title'],
                    views=video_info.get('views', 0),
                    likes=video_info.get('likes', 0)
                )
                
                optimized_description = title_generator.generate_description(
                    video_info['title'],
                    author=video_info.get('author', ''),
                    views=video_info.get('views', 0),
                    likes=video_info.get('likes', 0)
                )
                
                optimized_tags = title_generator.get_optimized_tags(video_info['title'])
                
                print(f"📝 Optimize Edilmiş Başlık: {optimized_title}")
                
                youtube_result = uploader.upload_video(
                    video_path=video_path,
                    title=optimized_title,
                    description=optimized_description,
                    tags=optimized_tags
                )
                
                if youtube_result:
                    content_manager.mark_uploaded(
                        video_info['url'],
                        youtube_result,
                        video_path
                    )
                    uploaded_count += 1
                    print(f"🎉 Başarılı! YouTube: {youtube_result['url']}")
                    
                    # Son video ID'sini kaydet (Telegram bot için)
                    try:
                        import json
                        with open('data/last_video.json', 'w') as f:
                            json.dump({'video_id': youtube_result['video_id']}, f)
                    except:
                        pass
                    
                    # Telegram bildirimi - video yüklendi
                    telegram.notify_video_uploaded(optimized_title, youtube_result['url'])
                else:
                    content_manager.mark_failed(video_info['url'], "YouTube yükleme başarısız")
                    telegram.notify_error("YouTube Yükleme", f"Video yüklenemedi: {optimized_title[:50]}")
                
                # Rate limiting
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Hata: {str(e)}")
                content_manager.mark_failed(video_info['url'], str(e))
        
        # Eski videoları temizle
        print("\n🧹 Eski videolar temizleniyor...")
        retention_days = config['general'].get('video_retention_days', 7)
        content_manager.cleanup_old_videos(max_age_days=retention_days)
        
        print(f"\n✅ Döngü tamamlandı! {uploaded_count} video yüklendi.")
        
    except Exception as e:
        print(f"\n❌ Kritik hata: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    print("🤖 TAM OTOMATİK TikTok → YouTube Scheduler")
    print("="*60)
    print("⏰ Her 3 saatte bir çalışacak")
    print("📹 Her döngüde 1 video yüklenecek")
    print("📊 Günde 8 video = Ayda 240 video")
    print("="*60)
    
    # Telegram bildirimi - bot başladı
    telegram = TelegramNotifier()
    telegram.notify_bot_started()
    
    # İlk çalıştırma
    print("\n🚀 İlk döngü başlıyor...")
    run_automation()
    
    # Schedule ayarla - her 3 saatte bir
    schedule.every(3).hours.do(run_automation)
    
    print(f"\n⏰ Scheduler aktif! Sonraki çalışma: {schedule.next_run()}")
    print("💡 Durdurmak için Ctrl+C bas\n")
    
    # Sürekli çalış
    while True:
        schedule.run_pending()
        time.sleep(60)  # Her dakika kontrol et


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler durduruldu!")
