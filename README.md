# PlanKey

PlanKey, arka planda çalışan ve sistem genelinde `F8` tuşunu dinleyen yerel yapay zeka (Ollama) tabanlı bir çalışma asistanıdır. Herhangi bir uygulamada metin seçip klavye kısayoluna basarak, seçili bağlam üzerinden hızlıca planlar oluşturabilirsiniz.

## Özellikler

- **Sınav Çalışma Takvimi:** Seçilen metne göre gün/saat bazlı çalışma programı.
- **Pomodoro Planı:** 25dk odak / 5dk mola döngülerine dayalı saatlik görev listesi.
- **Konu Analizi:** İçeriği önem sırasına göre ayırıp strateji oluşturma.
- **Tamamen Yerel:** API servisine ihtiyaç duymaz.

## Akış

```mermaid
flowchart LR
    A([Metin Seç]) --> B[F8]
    B --> C[Uygulama Menüsü]
    C --> D[Ollama API]
    D --> E([Sonuç Penceresi])
```

## Kurulum

Sisteminizde [Ollama](https://ollama.com) ve Python 3.8+ kurulu olmalıdır.

```bash
# 1. Ollama modelini indirin ve servisi başlatın
ollama pull gemma4:31b-cloud
ollama serve

# 2. Bağımlılıkları kurun
pip install -r requirements.txt
```
*(Not: `kurulum.bat` dosyasını çalıştırarak Python ortamını otomatik hazırlayabilirsiniz.)*

## Başlatma

Uygulamayı arka planda terminal penceresi olmadan başlatmak için:
```bash
pythonw main.pyw
```
*(Veya direkt olarak `BASLAT.bat` dosyasına tıklayın.)*

## 📁 Dosyalar

```
.
├── main.pyw          # Ana uygulama — arka planda sessiz çalışır
├── BASLAT.bat        # Tek tıkla başlatıcı
├── kurulum.bat       # İlk kurulum scripti
└── requirements.txt  # requests · pyperclip · pynput · pyautogui
```

## Lisans

MIT
