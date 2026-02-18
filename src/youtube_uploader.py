import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class YouTubeUploader:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, config, credentials_file='config/credentials.json'):
        self.config = config
        self.credentials_file = credentials_file
        self.youtube = self._authenticate()
    
    def _authenticate(self):
        """YouTube API ile kimlik doğrulama"""
        creds = None
        token_file = 'config/token.pickle'
        
        # Token varsa yükle
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Token yoksa veya geçersizse yenile
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"❌ {self.credentials_file} bulunamadı!\n"
                        "Google Cloud Console'dan OAuth 2.0 credentials oluşturun."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Token'ı kaydet
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        return build('youtube', 'v3', credentials=creds)
    
    def upload_video(self, video_path, title, description=None, tags=None):
        """YouTube'a video yükle"""
        try:
            if not os.path.exists(video_path):
                print(f"❌ Video bulunamadı: {video_path}")
                return None
            
            # Başlık ve açıklama hazırla
            full_title = f"{self.config['youtube']['title_prefix']}{title}{self.config['youtube']['title_suffix']}"
            full_title = full_title[:100]  # YouTube limiti
            
            if not description:
                description = self.config['youtube']['description_template']
            
            if not tags:
                tags = self.config['youtube']['tags']
            
            # Video metadata
            body = {
                'snippet': {
                    'title': full_title,
                    'description': description,
                    'tags': tags,
                    'categoryId': self.config['youtube']['category_id']
                },
                'status': {
                    'privacyStatus': self.config['youtube']['privacy_status'],
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Video yükle
            print(f"📤 YouTube'a yükleniyor: {full_title}")
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"⏳ Yüklendi: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"✅ Yükleme başarılı: {video_url}")
            
            return {
                'video_id': video_id,
                'url': video_url,
                'title': full_title
            }
            
        except Exception as e:
            print(f"❌ YouTube yükleme hatası: {str(e)}")
            return None
