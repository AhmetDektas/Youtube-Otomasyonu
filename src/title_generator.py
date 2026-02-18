"""
YouTube Başlık ve Açıklama Oluşturucu
Shorts için optimize edilmiş, çekici başlıklar
"""
import random
import re


class TitleGenerator:
    
    # Başlık şablonları
    TITLE_TEMPLATES = [
        "{emoji} {title} {hook}",
        "{hook} {emoji} {title}",
        "{title} {emoji} {cta}",
        "{emoji} {title} | {hook}",
    ]
    
    # Hook'lar (dikkat çekici başlangıçlar)
    HOOKS = [
        "😂 Gülmekten Öldüm",
        "🔥 Bu Efsane",
        "💀 Buna İnanamayacaksın",
        "😱 Şok Oldum",
        "🤣 Kahkaha Garantili",
        "⚡ Viral Oldu",
        "🎯 Mutlaka İzle",
        "💯 Mükemmel",
        "🚀 Rekor Kırdı",
        "⭐ Harika",
    ]
    
    # CTA (Call to Action)
    CTAS = [
        "#shorts",
        "Beğenmeyi Unutma 👍",
        "Abone Ol 🔔",
        "Paylaş 📤",
    ]
    
    # Emoji'ler
    EMOJIS = ["😂", "🤣", "😆", "😅", "🔥", "💀", "😱", "⚡", "💯", "🎯", "⭐", "🚀"]
    
    def __init__(self, config):
        self.config = config
    
    def generate_title(self, original_title, views=0, likes=0):
        """Çekici başlık oluştur"""
        # Orijinal başlığı temizle
        clean_title = self._clean_title(original_title)
        
        # Çok uzunsa kısalt
        if len(clean_title) > 60:
            clean_title = clean_title[:57] + "..."
        
        # Şablon seç
        template = random.choice(self.TITLE_TEMPLATES)
        
        # Değişkenleri doldur
        title = template.format(
            emoji=random.choice(self.EMOJIS),
            title=clean_title,
            hook=random.choice(self.HOOKS),
            cta=random.choice(self.CTAS)
        )
        
        # YouTube limiti: 100 karakter
        if len(title) > 100:
            title = title[:97] + "..."
        
        return title
    
    def generate_description(self, original_title, author="", views=0, likes=0):
        """Detaylı açıklama oluştur"""
        
        # Viral bilgisi
        viral_text = ""
        if views > 1000000:
            viral_text = f"🔥 {views:,} izlenme ile viral oldu!\n"
        elif views > 100000:
            viral_text = f"⚡ {views:,} izlenme!\n"
        
        # Açıklama şablonu
        description = f"""{viral_text}
📱 TikTok'tan en komik videolar burada!

{original_title}

━━━━━━━━━━━━━━━━━━━━
🎬 İçerik Hakkında:
Bu video TikTok'ta viral olan en eğlenceli içeriklerden biri. Gülmek garantili! 😂

━━━━━━━━━━━━━━━━━━━━
👍 Beğenmeyi unutma!
🔔 Abone ol, daha fazlası için!
📤 Arkadaşlarınla paylaş!
💬 Yorumlarda görüşelim!

━━━━━━━━━━━━━━━━━━━━
🏷️ Etiketler:
#shorts #tiktok #komedi #mizah #eğlence #viral #türkiye #funny #comedy #entertainment

━━━━━━━━━━━━━━━━━━━━
📊 Orijinal Video İstatistikleri:
👁️ İzlenme: {views:,}
❤️ Beğeni: {likes:,}
👤 Yazar: @{author}

━━━━━━━━━━━━━━━━━━━━
⚠️ Telif Hakkı:
Bu video TikTok'tan alınmıştır. Tüm hakları orijinal içerik üreticisine aittir.

━━━━━━━━━━━━━━━━━━━━
🔗 Daha Fazla İçerik:
Kanalımızda her gün yeni videolar! Kaçırma! 🚀
"""
        
        return description.strip()
    
    def _clean_title(self, title):
        """Başlığı temizle"""
        # Hashtag'leri kaldır
        title = re.sub(r'#\w+', '', title)
        
        # Mention'ları kaldır
        title = re.sub(r'@\w+', '', title)
        
        # Fazla boşlukları temizle
        title = ' '.join(title.split())
        
        # Emoji'leri koru ama fazla varsa azalt
        # (YouTube başlıkta emoji'yi sever)
        
        return title.strip()
    
    def get_optimized_tags(self, original_title):
        """Optimize edilmiş tag'ler"""
        base_tags = self.config['youtube']['tags'].copy()
        
        # Başlıktan keyword'ler çıkar
        words = original_title.lower().split()
        keywords = [w for w in words if len(w) > 3 and w.isalpha()][:5]
        
        # Trend tag'ler ekle
        trend_tags = [
            "viral",
            "trending",
            "funny",
            "comedy",
            "türkiye",
            "turkish",
            "2026",
        ]
        
        # Hepsini birleştir
        all_tags = base_tags + keywords + trend_tags
        
        # Duplicate'leri kaldır, max 15 tag
        unique_tags = []
        for tag in all_tags:
            if tag not in unique_tags:
                unique_tags.append(tag)
        
        return unique_tags[:15]


# Test
if __name__ == '__main__':
    import yaml
    
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    generator = TitleGenerator(config)
    
    # Test başlık
    original = "Arkadaşımla yaptığımız şaka çok komik oldu 😂 #komedi #mizah"
    
    print("🎬 Orijinal Başlık:")
    print(original)
    print()
    
    print("✨ Yeni Başlık:")
    new_title = generator.generate_title(original, views=1500000, likes=25000)
    print(new_title)
    print()
    
    print("📝 Açıklama:")
    description = generator.generate_description(original, author="kullanici123", views=1500000, likes=25000)
    print(description)
    print()
    
    print("🏷️ Tag'ler:")
    tags = generator.get_optimized_tags(original)
    print(", ".join(tags))
