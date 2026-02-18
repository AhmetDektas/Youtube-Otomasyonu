#!/bin/bash
# YouTube TikTok Otomasyon - Systemd Servis Kurulumu
# 7/24 otomatik çalışma için

echo "🔧 Systemd servisi kuruluyor..."
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Mevcut kullanıcı ve dizin
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

# Servis dosyası oluştur
echo -e "${YELLOW}📝 Servis dosyası oluşturuluyor...${NC}"

sudo tee /etc/systemd/system/youtube-bot.service > /dev/null << EOF
[Unit]
Description=YouTube TikTok Otomasyon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
Environment="PATH=$CURRENT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/scheduler.py
Restart=always
RestartSec=300
StandardOutput=append:$CURRENT_DIR/logs/bot.log
StandardError=append:$CURRENT_DIR/logs/bot-error.log

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ Servis dosyası oluşturuldu${NC}"
echo ""

# Systemd'yi yeniden yükle
echo -e "${YELLOW}🔄 Systemd yeniden yükleniyor...${NC}"
sudo systemctl daemon-reload
echo -e "${GREEN}✅ Systemd yenilendi${NC}"
echo ""

# Servisi etkinleştir
echo -e "${YELLOW}⚙️  Servis etkinleştiriliyor...${NC}"
sudo systemctl enable youtube-bot
echo -e "${GREEN}✅ Servis etkinleştirildi (otomatik başlayacak)${NC}"
echo ""

# Servisi başlat
echo -e "${YELLOW}🚀 Servis başlatılıyor...${NC}"
sudo systemctl start youtube-bot
echo ""

# Durum kontrolü
sleep 2
echo -e "${YELLOW}📊 Servis durumu:${NC}"
sudo systemctl status youtube-bot --no-pager
echo ""

# Başarı mesajı
if sudo systemctl is-active --quiet youtube-bot; then
    echo "================================================"
    echo -e "${GREEN}🎉 SERVİS BAŞARIYLA BAŞLATILDI!${NC}"
    echo "================================================"
    echo ""
    echo "📊 Kontrol Komutları:"
    echo ""
    echo "   Durum:          sudo systemctl status youtube-bot"
    echo "   Durdur:         sudo systemctl stop youtube-bot"
    echo "   Başlat:         sudo systemctl start youtube-bot"
    echo "   Yeniden başlat: sudo systemctl restart youtube-bot"
    echo "   Log izle:       tail -f logs/bot.log"
    echo ""
    echo "✅ Bot artık 7/24 çalışıyor!"
    echo ""
else
    echo "================================================"
    echo -e "${RED}❌ SERVİS BAŞLATILAMADI!${NC}"
    echo "================================================"
    echo ""
    echo "🔍 Hata kontrolü:"
    echo "   sudo journalctl -u youtube-bot -n 50"
    echo ""
    echo "🧪 Manuel test:"
    echo "   venv/bin/python scheduler.py"
    echo ""
fi
