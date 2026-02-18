#!/bin/bash

echo "🍓 Raspberry Pi - TikTok YouTube Bot Kurulumu"
echo "=============================================="
echo ""

# Root kontrolü
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Bu script sudo ile çalıştırılmalı!"
    echo "Kullanım: sudo bash raspberry-pi-install.sh"
    exit 1
fi

# Kullanıcı adını al
ACTUAL_USER=${SUDO_USER:-$USER}
PROJECT_DIR="/home/$ACTUAL_USER/tiktok-youtube-bot"

echo "👤 Kullanıcı: $ACTUAL_USER"
echo "📁 Proje dizini: $PROJECT_DIR"
echo ""

# Sistem bilgisi
echo "📊 Sistem Bilgisi:"
echo "   Model: $(cat /proc/device-tree/model 2>/dev/null || echo 'Unknown')"
echo "   RAM: $(free -h | awk '/^Mem:/ {print $2}')"
echo "   CPU: $(nproc) core"
echo ""

# RAM kontrolü
TOTAL_RAM=$(free -m | awk '/^Mem:/ {print $2}')
if [ "$TOTAL_RAM" -lt 1024 ]; then
    echo "⚠️ UYARI: RAM düşük ($TOTAL_RAM MB)"
    echo "   Raspberry Pi 4 (2GB+) önerilir"
    echo "   Devam edilsin mi? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Sistem güncellemesi
echo ""
echo "📦 Sistem güncelleniyor..."
apt-get update
apt-get upgrade -y

# Gerekli paketler
echo ""
echo "📥 Gerekli paketler kuruluyor..."
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget

# Proje dizini oluştur
echo ""
echo "📁 Proje dizini oluşturuluyor..."
if [ ! -d "$PROJECT_DIR" ]; then
    sudo -u $ACTUAL_USER mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Virtual environment
echo ""
echo "🐍 Python virtual environment oluşturuluyor..."
sudo -u $ACTUAL_USER python3 -m venv venv

# Bağımlılıkları yükle
echo ""
echo "📦 Python paketleri yükleniyor..."
sudo -u $ACTUAL_USER venv/bin/pip install --upgrade pip
sudo -u $ACTUAL_USER venv/bin/pip install \
    apify-client==2.4.1 \
    google-auth-oauthlib==1.2.0 \
    google-auth-httplib2==0.2.0 \
    google-api-python-client==2.108.0 \
    pyyaml==6.0.1 \
    requests==2.31.0 \
    python-dotenv==1.0.0 \
    schedule==1.2.0

# Klasör yapısı
echo ""
echo "📂 Klasör yapısı oluşturuluyor..."
sudo -u $ACTUAL_USER mkdir -p "$PROJECT_DIR/src"
sudo -u $ACTUAL_USER mkdir -p "$PROJECT_DIR/config"
sudo -u $ACTUAL_USER mkdir -p "$PROJECT_DIR/data/videos"
sudo -u $ACTUAL_USER mkdir -p "$PROJECT_DIR/logs"

# Systemd servis dosyası
echo ""
echo "⚙️ Systemd servisi oluşturuluyor..."

cat > /etc/systemd/system/tiktok-bot.service << EOF
[Unit]
Description=TikTok YouTube Automation Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$ACTUAL_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/scheduler.py
Restart=always
RestartSec=300
StandardOutput=append:$PROJECT_DIR/logs/bot.log
StandardError=append:$PROJECT_DIR/logs/bot-error.log

# Kaynak limitleri (Raspberry Pi için optimize)
MemoryMax=1G
CPUQuota=80%

[Install]
WantedBy=multi-user.target
EOF

# Log rotation
echo ""
echo "📝 Log rotation ayarlanıyor..."

cat > /etc/logrotate.d/tiktok-bot << EOF
$PROJECT_DIR/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 $ACTUAL_USER $ACTUAL_USER
}
EOF

# Servisi etkinleştir
echo ""
echo "🚀 Servis etkinleştiriliyor..."
systemctl daemon-reload
systemctl enable tiktok-bot.service

# Swap ayarı (düşük RAM için)
if [ "$TOTAL_RAM" -lt 2048 ]; then
    echo ""
    echo "💾 Swap alanı ayarlanıyor (düşük RAM için)..."
    
    # Mevcut swap'ı kontrol et
    SWAP_SIZE=$(free -m | awk '/^Swap:/ {print $2}')
    
    if [ "$SWAP_SIZE" -lt 1024 ]; then
        echo "   1GB swap oluşturuluyor..."
        
        # Swap dosyası oluştur
        fallocate -l 1G /swapfile
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
        
        # Kalıcı yap
        if ! grep -q '/swapfile' /etc/fstab; then
            echo '/swapfile none swap sw 0 0' >> /etc/fstab
        fi
        
        echo "   ✅ Swap aktif"
    fi
fi

# Güç tasarrufu ayarları
echo ""
echo "⚡ Güç tasarrufu ayarları..."

# WiFi güç tasarrufunu kapat (bağlantı kopmasın)
if [ -f /etc/rc.local ]; then
    if ! grep -q 'iwconfig wlan0 power off' /etc/rc.local; then
        sed -i '/^exit 0/i iwconfig wlan0 power off 2>/dev/null || true' /etc/rc.local
    fi
fi

# Tamamlandı
echo ""
echo "=============================================="
echo "✅ Kurulum tamamlandı!"
echo "=============================================="
echo ""
echo "📋 Sonraki adımlar:"
echo ""
echo "1. Proje dosyalarını kopyala:"
echo "   scp -r src config scheduler.py $ACTUAL_USER@raspberrypi:$PROJECT_DIR/"
echo ""
echo "2. .env dosyasını düzenle:"
echo "   nano $PROJECT_DIR/.env"
echo "   # APIFY_API_TOKEN ekle"
echo ""
echo "3. credentials.json ekle:"
echo "   scp config/credentials.json $ACTUAL_USER@raspberrypi:$PROJECT_DIR/config/"
echo ""
echo "4. Servisi başlat:"
echo "   sudo systemctl start tiktok-bot"
echo ""
echo "5. Durumu kontrol et:"
echo "   sudo systemctl status tiktok-bot"
echo "   tail -f $PROJECT_DIR/logs/bot.log"
echo ""
echo "🛠️ Yararlı komutlar:"
echo "   sudo systemctl start tiktok-bot    # Başlat"
echo "   sudo systemctl stop tiktok-bot     # Durdur"
echo "   sudo systemctl restart tiktok-bot  # Yeniden başlat"
echo "   sudo systemctl status tiktok-bot   # Durum"
echo "   tail -f $PROJECT_DIR/logs/bot.log # Log'ları izle"
echo ""
echo "🍓 Raspberry Pi hazır! Dosyaları kopyala ve başlat."
echo ""
