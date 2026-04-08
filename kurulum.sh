#!/bin/bash

# Renkli mesajlar için
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/4] Bağımlılıklar kontrol ediliyor...${NC}"

# Python kontrolü
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}[HATA] python3 bulunamadı. Lütfen yükleyin.${NC}"
    exit 1
fi

# Linux sistem paketleri (pynput, pyautogui ve pyttsx3 için)
echo -e "${BLUE}Sistem kütüphaneleri kontrol ediliyor (sudo yetkisi gerekebilir)...${NC}"
sudo apt-get update
sudo apt-get install -y python3-tk python3-dev xclip espeak libespeak1

echo -e "${BLUE}[2/4] Sanal ortam oluşturuluyor...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo -e "${BLUE}[3/4] pip güncelleniyor ve paketler kuruluyor...${NC}"
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}[OK] Kurulum tamamlandı!${NC}"
echo -e "Uygulamayı başlatmak için: ${BLUE}python3 main.pyw${NC}"
