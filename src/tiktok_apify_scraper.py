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
                
                # Actor'ı çalıştır
                run = self.client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
                
                # Sonuçları al
                videos = []
                all_items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
                
                # Rastgele karıştır (her seferinde farklı videolar)
                import random
                random.shuffle(all_items)
                
                for item in all_items:
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
                        'title': (item.get('text') or item.get('desc') or 'TikTok Video')[:100],
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
    
    def download_video(self, video_info):
        """Videoyu indir"""
        try:
            if not video_info.get('video_url'):
                print("❌ Video URL bulunamadı")
                return None
            
            # Dosya adı
            safe_title = "".join(c for c in video_info['title'] if c.isalnum() or c in (' ', '-', '_'))[:50]
            filename = f"{safe_title}_{int(time.time())}.mp4"
            filepath = self.download_path / filename
            
            print(f"⬇️ İndiriliyor: {filename}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.tiktok.com/'
            }
            
            response = requests.get(video_info['video_url'], headers=headers, stream=True, timeout=60)
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
            
        except Exception as e:
            print(f"\n❌ İndirme hatası: {str(e)}")
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
