#!/bin/bash
# YouTube TikTok Otomasyon - Otomatik Kurulum Scripti
# Raspberry Pi 4 için optimize edilmiştir

echo "🚀 YouTube TikTok Otomasyon Kurulumu Başlıyor..."
echo "================================================"
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Hata kontrolü
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo -e "${RED}❌ Hata: \"${last_command}\" komutu başarısız oldu${NC}"' ERR

# 1. Sistem Güncelleme
echo -e "${YELLOW}📦 Sistem güncelleniyor...${NC}"
sudo apt update
echo -e "${GREEN}✅ Sistem güncellendi${NC}"
echo ""

# 2. Python ve Git Kurulumu
echo -e "${YELLOW}🐍 Python ve Git kuruluyor...${NC}"
sudo apt install -y python3 python3-pip python3-venv git
echo -e "${GREEN}✅ Python ve Git kuruldu${NC}"
echo ""

# 3. Proje Klasörü Kontrolü
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment zaten var, atlanıyor...${NC}"
else
    # 4. Virtual Environment Oluşturma
    echo -e "${YELLOW}📦 Virtual environment oluşturuluyor...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment oluşturuldu${NC}"
fi
echo ""

# 5. Pip Güncelleme
echo -e "${YELLOW}⬆️  Pip güncelleniyor...${NC}"
venv/bin/pip install --upgrade pip --quiet
echo -e "${GREEN}✅ Pip güncellendi${NC}"
echo ""

# 6. Python Paketlerini Kurma
echo -e "${YELLOW}📦 Python paketleri kuruluyor (5-10 dakika sürebilir)...${NC}"
venv/bin/pip install -r requirements.txt
echo -e "${GREEN}✅ Python paketleri kuruldu${NC}"
echo ""

# 7. Klasörleri Oluşturma
echo -e "${YELLOW}📁 Klasörler oluşturuluyor...${NC}"
mkdir -p data/videos logs
echo -e "${GREEN}✅ Klasörler oluşturuldu${NC}"
echo ""

# 8. .env Dosyası Kontrolü
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env dosyası bulunamadı!${NC}"
    echo -e "${YELLOW}📝 .env dosyası oluşturuluyor...${NC}"
    cat > .env << EOF
# Apify API Token
APIFY_API_TOKEN=your_apify_token_here

# YouTube API (config/credentials.json kullanılıyor)
EOF
    echo -e "${GREEN}✅ .env dosyası oluşturuldu${NC}"
    echo -e "${RED}⚠️  ÖNEMLI: .env dosyasını düzenle: nano .env${NC}"
else
    echo -e "${GREEN}✅ .env dosyası mevcut${NC}"
fi
echo ""

# 9. Config Dosyası Kontrolü
if [ ! -f "config/credentials.json" ]; then
    echo -e "${RED}⚠️  config/credentials.json bulunamadı!${NC}"
    echo -e "${YELLOW}📝 Bilgisayarından kopyala:${NC}"
    echo -e "   scp config/credentials.json pi@$(hostname):~/Youtube-Otomasyonu/config/"
else
    echo -e "${GREEN}✅ credentials.json mevcut${NC}"
fi
echo ""

# 10. Test
echo -e "${YELLOW}🧪 Kurulum testi yapılıyor...${NC}"
if venv/bin/python -c "import apify_client, google.oauth2, yaml, schedule" 2>/dev/null; then
    echo -e "${GREEN}✅ Tüm paketler başarıyla yüklendi${NC}"
else
    echo -e "${RED}❌ Bazı paketler eksik, tekrar dene${NC}"
    exit 1
fi
echo ""

# 11. Sistem Bilgileri
echo "================================================"
echo -e "${GREEN}🎉 KURULUM TAMAMLANDI!${NC}"
echo "================================================"
echo ""
echo "📊 Sistem Bilgileri:"
echo "   Python: $(python3 --version)"
echo "   Pip: $(venv/bin/pip --version | cut -d' ' -f2)"
echo "   RAM: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "   Disk: $(df -h ~ | tail -1 | awk '{print $3 "/" $2}')"
echo ""
echo "🎯 Sıradaki Adımlar:"
echo ""
echo "1️⃣  .env dosyasını düzenle:"
echo "   nano .env"
echo ""
echo "2️⃣  YouTube API dosyasını kopyala (bilgisayarından):"
echo "   scp config/credentials.json pi@$(hostname):~/Youtube-Otomasyonu/config/"
echo ""
echo "3️⃣  Test et:"
echo "   venv/bin/python scheduler.py"
echo ""
echo "4️⃣  Otomatik başlatma için:"
echo "   sudo bash setup-service.sh"
echo ""
echo "📚 Daha fazla bilgi: readmd/HIZLI_KURULUM_PI4.md"
echo ""
