"""
Apify TikTok Scraper - TAM OTOMATİK
Apify API kullanarak TikTok'tan video toplar
"""
import os
import time
import requests
from pathlib import Path
from apify_client import ApifyClient
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


class TikTokApifyScraper:
    def __init__(self, config):
        self.config = config
        self.download_path = Path(config['general']['download_path'])
        self.download_path.mkdir(parents=True, exist_ok=True)
        
        # Apify client
        api_token = os.getenv('APIFY_API_TOKEN')
        if not api_token:
            raise ValueError("❌ APIFY_API_TOKEN bulunamadı! .env dosyasını kontrol et.")
        
        self.client = ApifyClient(api_token)
    
    def is_turkish_content(self, text):
        """Videonun Türkçe olup olmadığını kontrol et"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Türkçe karakterler
        turkish_chars = ['ğ', 'ü', 'ş', 'ı', 'ö', 'ç']
        has_turkish_char = any(char in text_lower for char in turkish_chars)
        
        # Yaygın İngilizce kelimeler (TikTok'ta sık kullanılan)
        english_words = [
            'what', 'this', 'comedy', 'funny', 'video', 'look', 'watch',
            'like', 'follow', 'subscribe', 'viral', 'trending', 'challenge',
            'prank', 'reaction', 'part', 'episode', 'series', 'compilation',
            'best', 'top', 'amazing', 'crazy', 'insane', 'epic', 'fail',
            'win', 'moment', 'caught', 'camera', 'real', 'fake', 'gone',
            'wrong', 'right', 'never', 'always', 'when', 'how', 'why',
            'who', 'where', 'call', 'entered', 'chat', 'has', 'the'
        ]
        
        # İngilizce kelime sayısı
        english_count = sum(1 for word in english_words if f' {word} ' in f' {text_lower} ')
        
        # Türkçe karakter varsa kesinlikle Türkçe
        if has_turkish_char:
            return True
        
        # İngilizce kelime çoksa İngilizce
        if english_count >= 2:
            return False
        
        # Yaygın Türkçe kelimeler
        turkish_words = [
            'ben', 'sen', 'biz', 'siz', 'bu', 'şu', 'ne', 'nasıl', 'neden',
            'kim', 'nerede', 'var', 'yok', 'için', 'ile', 'gibi', 'kadar',
            'daha', 'çok', 'az', 'her', 'hiç', 'böyle', 'şöyle', 'öyle',
            'ama', 'fakat', 'veya', 'ya', 'da', 'de', 'mi', 'mı', 'mu', 'mü',
            'yaşında', 'akşam', 'sabah', 'gün', 'saat', 'dakika', 'saniye'
        ]
        
        turkish_count = sum(1 for word in turkish_words if f' {word} ' in f' {text_lower} ')
        
        # Türkçe kelime varsa Türkçe
        if turkish_count >= 1:
            return True
        
        # Belirsiz durumda kabul et (hashtag'ler Türkçe olduğu için)
        return True
    
    def scrape_trending_videos(self, max_videos=10):
        """Hashtag'lerden video topla"""
        print("🔍 Apify ile TikTok videoları toplanıyor...")
        
        hashtags = self.config['tiktok']['search_hashtags']
        all_videos = []
        
        for hashtag in hashtags:
            if len(all_videos) >= max_videos:
                break
            
            print(f"\n🔍 #{hashtag} araştırılıyor...")
            
            try:
                # Apify TikTok Scraper actor'ını çalıştır
                # Actor ID: clockworks/tiktok-scraper
                run_input = {
                    "hashtags": [hashtag],
                    "resultsPerPage": min(max_videos - len(all_videos) + 10, 30),  # Biraz fazla al
                    "shouldDownloadVideos": True,  # Video URL'lerini al
                    "shouldDownloadCovers": False,
                }
                
                print(f"   ⏳ Apify actor çalışıyor...")
                
                # Actor'ı çalıştır (15 dakika timeout)
                run = self.client.actor("clockworks/tiktok-scraper").call(
                    run_input=run_input,
                    timeout_secs=900  # 15 dakika timeout
                )
                
                # Sonuçları al
                videos = []
                all_items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
                
                # Rastgele karıştır (her seferinde farklı videolar)
                import random
                random.shuffle(all_items)
                
                for item in all_items:
                    # Video başlığını al
                    title = (item.get('text') or item.get('desc') or 'TikTok Video')[:100]
                    
                    # Türkçe kontrolü yap
                    if not self.is_turkish_content(title):
                        print(f"   ⏭️ Atlandı (Yabancı): {title[:40]}...")
                        continue
                    
                    # Video URL'sini bul
                    video_url = None
                    
                    # mediaUrls içinde video var mı?
                    if 'mediaUrls' in item and item['mediaUrls']:
                        media_urls = item['mediaUrls']
                        if isinstance(media_urls, list) and len(media_urls) > 0:
                            video_url = media_urls[0]
                        elif isinstance(media_urls, dict):
                            video_url = media_urls.get('videoUrl') or media_urls.get('downloadAddr')
                    
                    # videoMeta içinde var mı?
                    if not video_url and 'videoMeta' in item:
                        video_meta = item['videoMeta']
                        if isinstance(video_meta, dict):
                            video_url = (video_meta.get('downloadAddr') or 
                                       video_meta.get('playAddr') or 
                                       video_meta.get('url'))
                    
                    # Apify TikTok scraper'ın döndürdüğü format
                    video_info = {
                        'url': item.get('webVideoUrl', ''),
                        'video_url': video_url or '',
                        'title': title,
                        'author': item.get('authorMeta', {}).get('name', 'Unknown'),
                        'likes': item.get('diggCount', 0),
                        'views': item.get('playCount', 0),
                    }
                    
                    if video_info['video_url']:
                        videos.append(video_info)
                        all_videos.append(video_info)
                        print(f"   ✅ {video_info['title'][:40]}... (👁️ {video_info['views']:,})")
                        
                        if len(all_videos) >= max_videos:
                            break
                
                print(f"   ✅ {len(videos)} video bulundu")
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Hata: {str(e)}")
                continue
        
        return all_videos[:max_videos]
    
    def download_video(self, video_info, max_retries=2):
        """Videoyu indir (retry mekanizması ile)"""
        for attempt in range(max_retries):
            try:
                if not video_info.get('video_url'):
                    print("❌ Video URL bulunamadı")
                    return None
                
                # Dosya adı
                safe_title = "".join(c for c in video_info['title'] if c.isalnum() or c in (' ', '-', '_'))[:50]
                filename = f"{safe_title}_{int(time.time())}.mp4"
                filepath = self.download_path / filename
                
                print(f"⬇️ İndiriliyor: {filename} (Deneme {attempt + 1}/{max_retries})")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://www.tiktok.com/'
                }
                
                response = requests.get(
                    video_info['video_url'], 
                    headers=headers, 
                    stream=True, 
                    timeout=120  # 2 dakika timeout
                )
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r   İlerleme: {percent:.1f}%", end='', flush=True)
                
                print(f"\n✅ İndirildi: {filepath}")
                return str(filepath)
                
            except requests.exceptions.Timeout:
                print(f"\n⏱️ Timeout! Video indirme çok uzun sürdü.")
                if attempt < max_retries - 1:
                    print(f"   🔄 {attempt + 2}. deneme yapılıyor...")
                    time.sleep(5)
                    continue
                else:
                    print(f"   ❌ {max_retries} deneme başarısız, video atlanıyor.")
                    return None
                    
            except Exception as e:
                print(f"\n❌ İndirme hatası: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"   🔄 {attempt + 2}. deneme yapılıyor...")
                    time.sleep(5)
                    continue
                else:
                    print(f"   ❌ {max_retries} deneme başarısız, video atlanıyor.")
                    return None
        
        return None


# Test
if __name__ == '__main__':
    import yaml
    
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    scraper = TikTokApifyScraper(config)
    
    print("🤖 Apify TikTok Scraper Test")
    print("="*60)
    
    videos = scraper.scrape_trending_videos(max_videos=3)
    
    print(f"\n\n📊 {len(videos)} video bulundu")
    
    if videos:
        print("\n📋 Bulunan videolar:")
        for i, video in enumerate(videos, 1):
            print(f"{i}. {video['title'][:50]}... (👁️ {video['views']:,})")
        
        print("\n⬇️ İlk videoyu indiriyorum...")
        filepath = scraper.download_video(videos[0])
        
        if filepath:
            print(f"\n✅ TEST BAŞARILI: {filepath}")
