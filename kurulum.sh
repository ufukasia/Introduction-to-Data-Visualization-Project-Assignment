#!/bin/bash

# --- ScribbleSense AI Kurulum Betiği (Fedora/Ubuntu/Arch Uyumlu) ---

echo "============================================================"
echo "🚀 ScribbleSense AI Kurulumu Başlatılıyor..."
echo "============================================================"

# Dağıtım tespiti
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    OS=$(uname -s)
fi

echo "[1/4] Dağıtım Tespiti: $OS"

case $OS in
    fedora|centos|rhel)
        echo "📦 Fedora tabanlı sistem tespit edildi. Gerekli kütüphaneler kuruluyor..."
        sudo dnf install -y python3-devel SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel freetype-devel mesa-libGL-devel gcc-c++
        ;;
    ubuntu|debian|kali|linuxmint)
        echo "📦 Debian tabanlı sistem tespit edildi. Gerekli kütüphaneler kuruluyor..."
        sudo apt-get update
        sudo apt-get install -y python3-tk python3-venv python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev
        ;;
    arch|manjaro)
        echo "📦 Arch tabanlı sistem tespit edildi. Gerekli kütüphaneler kuruluyor..."
        sudo pacman -S --noconfirm tk sdl2 sdl2_image sdl2_mixer sdl2_ttf freetype2
        ;;
    *)
        echo "⚠️  Bilinmeyen dağıtım ($OS). Lütfen SDL2 ve Python-devel paketlerini manuel kurun."
        ;;
esac

echo -e "\n[2/4] Sanal ortam (.venv) oluşturuluyor..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ .venv oluşturuldu."
else
    echo "ℹ️ .venv zaten mevcut."
fi

echo -e "\n[3/4] pip güncelleniyor ve bağımlılıklar kuruluyor..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Pygame kurulum kontrolü
if python3 -c "import pygame" &> /dev/null; then
    echo "✅ Pygame başarıyla kuruldu."
else
    echo "⚠️  Pygame derlenemedi! Sistemdeki ses oynatıcısı otomatik yedek olarak kullanılacak."
fi

echo -e "\n============================================================"
echo "✅ Kurulum Tamamlandı!"
echo "============================================================"
echo "🚀 Uygulamayı başlatmak için:"
echo "   source .venv/bin/activate"
echo "   python main.pyw"
echo "============================================================"
