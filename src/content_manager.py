import json
import os
from pathlib import Path
from datetime import datetime


class ContentManager:
    def __init__(self, db_path='data/uploaded.json'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load_db()
    
    def _load_db(self):
        """Veritabanını yükle"""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'uploaded': [], 'failed': []}
    
    def _save_db(self):
        """Veritabanını kaydet"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def is_uploaded(self, tiktok_url):
        """Video daha önce yüklendi mi?"""
        return any(item['tiktok_url'] == tiktok_url for item in self.data['uploaded'])
    
    def mark_uploaded(self, tiktok_url, youtube_data, video_path):
        """Videoyu yüklenmiş olarak işaretle"""
        self.data['uploaded'].append({
            'tiktok_url': tiktok_url,
            'youtube_url': youtube_data['url'],
            'youtube_id': youtube_data['video_id'],
            'title': youtube_data['title'],
            'uploaded_at': datetime.now().isoformat(),
            'local_path': video_path
        })
        self._save_db()
    
    def mark_failed(self, tiktok_url, error):
        """Başarısız yüklemeyi kaydet"""
        self.data['failed'].append({
            'tiktok_url': tiktok_url,
            'error': str(error),
            'failed_at': datetime.now().isoformat()
        })
        self._save_db()
    
    def cleanup_old_videos(self, max_age_days=7):
        """Eski videoları temizle"""
        video_dir = Path('data/videos')
        if not video_dir.exists():
            return
        
        deleted_count = 0
        total_size_mb = 0
        
        for video_file in video_dir.glob('*.mp4'):
            age_days = (datetime.now().timestamp() - video_file.stat().st_mtime) / 86400
            if age_days > max_age_days:
                size_mb = video_file.stat().st_size / (1024 * 1024)
                total_size_mb += size_mb
                video_file.unlink()
                deleted_count += 1
                print(f"🗑️ Silindi: {video_file.name} ({size_mb:.1f} MB)")
        
        if deleted_count > 0:
            print(f"✅ {deleted_count} video temizlendi ({total_size_mb:.1f} MB boşaltıldı)")
        else:
            print(f"ℹ️ Silinecek eski video yok")
    
    def get_disk_usage(self):
        """Disk kullanımını hesapla"""
        video_dir = Path('data/videos')
        if not video_dir.exists():
            return {'count': 0, 'size_mb': 0}
        
        total_size = 0
        count = 0
        for video_file in video_dir.glob('*.mp4'):
            total_size += video_file.stat().st_size
            count += 1
        
        return {
            'count': count,
            'size_mb': total_size / (1024 * 1024)
        }
    
    def get_stats(self):
        """İstatistikleri getir"""
        return {
            'total_uploaded': len(self.data['uploaded']),
            'total_failed': len(self.data['failed']),
            'last_upload': self.data['uploaded'][-1] if self.data['uploaded'] else None
        }
