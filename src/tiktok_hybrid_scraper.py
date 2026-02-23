"""
Hybrid TikTok Scraper - ÜCRETSİZ + Backup
1. Önce ücretsiz TikTok API dener
2. Başarısız olursa Apify'a geçer
"""
import os
import time
import requests
import json
from pathlib import Path
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()


class TikTokHybridScraper:
    def __init__(self, config):
        self.config = config
        self.download_path = Path(config['general']['download_path'])
        self.download_path.mkdir(parents=True, exist_ok=True)
        
        # Apify client (backup için)
        self.apify_token = os.getenv('APIFY_API_TOKEN')
        if self.apify_token:
            self.apify_client = ApifyClient(self.apify_token)
        else:
            self.apify_client = None
            print("⚠️ Apify token yok, sadece ücretsiz API kullanılacak")
    
    def is_turkish_content(self, text):
        """Videonun Türkçe olup olmadığını kontrol et"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Türkçe karakterler
        turkish_chars = ['ğ', 'ü', 'ş', 'ı', 'ö', 'ç']
        has_turkish_char = any(char in text_lower for char in turkish_chars)
        
        # Yaygın İngilizce kelimeler
        english_words = [
            'what', 'this', 'comedy', 'funny', 'video', 'look', 'watch',
            'like', 'follow', 'subscribe', 'viral', 'trending', 'challenge',
            'prank', 'reaction', 'part', 'episode', 'series', 'compilation',
            'best', 'top', 'amazing', 'crazy', 'insane', 'epic', 'fail',
            'win', 'moment', 'caught', 'camera', 'real', 'fake', 'gone',
            'wrong', 'right', 'never', 'always', 'when', 'how', 'why',
            'who', 'where', 'call', 'entered', 'chat', 'has', 'the'
        ]
        
        english_count = sum(1 for word in english_words if f' {word} ' in f' {text_lower} ')
        
        if has_turkish_char:
            return True
        
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
        
        if turkish_count >= 1:
            return True
        
        return True
    
    def scrape_with_free_api(self, hashtag, max_videos=10):
        """Ücretsiz RapidAPI TikTok ile video topla"""
        print(f"   💚 Ücretsiz RapidAPI deneniyor...")
        
        try:
            # RapidAPI TikTok Scraper (500 istek/ay ücretsiz)
            url = "https://tiktok-scraper7.p.rapidapi.com/challenge/posts"
            
            headers = {
                "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY', ''),
                "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
            }
            
            # RapidAPI key yoksa atla
            if not headers["X-RapidAPI-Key"]:
                print(f"   ⚠️ RAPIDAPI_KEY bulunamadı, atlanıyor...")
                return None
            
            querystring = {
                "challenge_name": hashtag,
                "count": str(max_videos * 2)
            }
            
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            
            if response.status_code != 200:
                print(f"   ❌ RapidAPI başarısız (Status: {response.status_code})")
                return None
            
            data = response.json()
            
            if 'data' not in data or not data['data']:
                print(f"   ❌ RapidAPI veri döndürmedi")
                return None
            
            videos = []
            for item in data['data']:
                try:
                    title = item.get('desc', 'TikTok Video')[:100]
                    
                    # Türkçe kontrolü
                    if not self.is_turkish_content(title):
                        continue
                    
                    video_info = {
                        'url': item.get('video_url', ''),
                        'video_url': item.get('play', ''),
                        'title': title,
                        'author': item.get('author', {}).get('unique_id', 'Unknown'),
                        'likes': item.get('statistics', {}).get('digg_count', 0),
                        'views': item.get('statistics', {}).get('play_count', 0),
                    }
                    
                    if video_info['video_url']:
                        videos.append(video_info)
                    
                    if len(videos) >= max_videos:
                        break
                        
                except Exception as e:
                    continue
            
            if videos:
                print(f"   ✅ RapidAPI: {len(videos)} video bulundu")
                return videos
            else:
                print(f"   ❌ RapidAPI Türkçe video bulamadı")
                return None
                
        except Exception as e:
            print(f"   ❌ RapidAPI hatası: {str(e)}")
            return None

    
    def scrape_with_apify(self, hashtag, max_videos=10):
        """Apify ile video topla (backup)"""
        if not self.apify_client:
            return None
        
        print(f"   🔵 Apify backup kullanılıyor...")
        
        try:
            run_input = {
                "hashtags": [hashtag],
                "resultsPerPage": min(max_videos + 10, 30),
                "shouldDownloadVideos": True,
                "shouldDownloadCovers": False,
            }
            
            run = self.apify_client.actor("clockworks/tiktok-scraper").call(
                run_input=run_input,
                timeout_secs=900
            )
            
            videos = []
            all_items = list(self.apify_client.dataset(run["defaultDatasetId"]).iterate_items())
            
            import random
            random.shuffle(all_items)
            
            for item in all_items:
                title = (item.get('text') or item.get('desc') or 'TikTok Video')[:100]
                
                if not self.is_turkish_content(title):
                    continue
                
                video_url = None
                if 'mediaUrls' in item and item['mediaUrls']:
                    media_urls = item['mediaUrls']
                    if isinstance(media_urls, list) and len(media_urls) > 0:
                        video_url = media_urls[0]
                    elif isinstance(media_urls, dict):
                        video_url = media_urls.get('videoUrl') or media_urls.get('downloadAddr')
                
                if not video_url and 'videoMeta' in item:
                    video_meta = item['videoMeta']
                    if isinstance(video_meta, dict):
                        video_url = (video_meta.get('downloadAddr') or 
                                   video_meta.get('playAddr') or 
                                   video_meta.get('url'))
                
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
                    
                    if len(videos) >= max_videos:
                        break
            
            if videos:
                print(f"   ✅ Apify: {len(videos)} video bulundu")
                return videos
            else:
                return None
                
        except Exception as e:
            print(f"   ❌ Apify hatası: {str(e)}")
            return None
    
    def scrape_trending_videos(self, max_videos=10):
        """Hybrid: Önce ücretsiz RapidAPI, sonra Apify"""
        print("🔍 Hybrid TikTok Scraper başlatılıyor...")
        print("   💚 Önce ücretsiz RapidAPI denenecek (500 istek/ay)")
        print("   🔵 Başarısız olursa Apify backup devreye girecek")
        print("   ⚠️ RapidAPI için .env dosyasına RAPIDAPI_KEY ekleyin")
        print("   📝 https://rapidapi.com/tikwm-tikwm-default/api/tiktok-scraper7")
        
        hashtags = self.config['tiktok']['search_hashtags']
        all_videos = []
        
        for hashtag in hashtags:
            if len(all_videos) >= max_videos:
                break
            
            print(f"\n🔍 #{hashtag} araştırılıyor...")
            
            # 1. Önce ücretsiz API dene
            videos = self.scrape_with_free_api(hashtag, max_videos - len(all_videos))
            
            # 2. Başarısız olursa Apify
            if not videos:
                videos = self.scrape_with_apify(hashtag, max_videos - len(all_videos))
            
            # 3. Hiçbiri çalışmazsa devam et
            if not videos:
                print(f"   ⚠️ #{hashtag} için video bulunamadı")
                continue
            
            # Videoları ekle
            for video in videos:
                all_videos.append(video)
                print(f"   ✅ {video['title'][:40]}... (👁️ {video['views']:,})")
                
                if len(all_videos) >= max_videos:
                    break
            
            time.sleep(2)
        
        print(f"\n✅ Toplam {len(all_videos)} video bulundu")
        return all_videos[:max_videos]
    
    def download_video(self, video_info, max_retries=2):
        """Videoyu indir"""
        for attempt in range(max_retries):
            try:
                if not video_info.get('video_url'):
                    print("❌ Video URL bulunamadı")
                    return None
                
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
                    timeout=120
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
                print(f"\n⏱️ Timeout!")
                if attempt < max_retries - 1:
                    print(f"   🔄 {attempt + 2}. deneme...")
                    time.sleep(5)
                    continue
                else:
                    print(f"   ❌ Video atlanıyor")
                    return None
                    
            except Exception as e:
                print(f"\n❌ Hata: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"   🔄 {attempt + 2}. deneme...")
                    time.sleep(5)
                    continue
                else:
                    print(f"   ❌ Video atlanıyor")
                    return None
        
        return None


# Test
if __name__ == '__main__':
    import yaml
    
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    scraper = TikTokHybridScraper(config)
    
    print("🤖 Hybrid TikTok Scraper Test")
    print("="*60)
    
    videos = scraper.scrape_trending_videos(max_videos=3)
    
    print(f"\n📊 {len(videos)} video bulundu")
    
    if videos:
        print("\n📋 Bulunan videolar:")
        for i, video in enumerate(videos, 1):
            print(f"{i}. {video['title'][:50]}... (👁️ {video['views']:,})")
