# AI Asistan — Seçili Metin İçin F8 Menüsü (Ollama)

Windows için hazırlanmış küçük bir masaüstü yardımcısı: herhangi bir programda bir metni seçip **F8** tuşuna bastığınızda fare imlecinin yanında bir menü açılır. Seçtiğiniz işlem, yerelde çalışan [Ollama](https://ollama.com) sunucusundaki dil modeline gönderilir ve sonuç seçili metnin yerine yapıştırılır.

## Menüdeki işlemler

- 📝 Gramer düzelt (Türkçe yazım ve dil bilgisi)
- 🇬🇧 İngilizceye çevir
- 🇹🇷 Türkçeye çevir
- 📑 Madde madde özetle
- 💼 Daha resmî yap (kurumsal e-posta dili)
- 🐍 Python koduna çevir
- 📧 E-postaya cevap taslağı yaz
- 🎮 PS5 oyun skoru + yorum (sonuç ayrı bir pencerede gösterilir, panoya kopyalanabilir)

Menüdeki işlemler ve istem (prompt) metinleri `main.pyw` içindeki `ISLEMLER` sözlüğünde tanımlıdır.

## Gereksinimler

- Windows ve Python 3 (kurulum betiği Python 3.13'ü önerir)
- Çalışan bir Ollama sunucusu (`http://localhost:11434`)
- Ollama'da kullanılabilir bir model. Uygulama sırasıyla `gemini-3-flash-preview:latest` ve `gemini-3-flash-preview:cloud` modellerini arar; farklı bir model kullanmak için `main.pyw` içindeki `MODEL_ADI` ve `TEXT_MODEL_CANDIDATES` değerlerini değiştirin.

## Kurulum ve çalıştırma

1. Ollama'yı kurun ve kullanmak istediğiniz modelin Ollama'da hazır olduğundan emin olun.
2. Bu klasörde `BASLAT.bat` dosyasını çalıştırın.

`BASLAT.bat` ilk çalıştırmada `.venv` sanal ortamını bulamazsa `kurulum.bat` dosyasını otomatik çağırır. Kurulum betiği Python 3'ü bulur, `.venv` oluşturur, `pip`'i günceller ve `requirements.txt` içindeki paketleri kurar. Ardından `main.pyw` arka planda (konsol penceresi olmadan) başlatılır.

## Kullanım

1. Herhangi bir uygulamada metni seçin.
2. **F8** tuşuna basın; açılan menüden işlemi seçin.
3. Sonuç seçili metnin yerine yapıştırılır.

Metin seçilmeden F8'e basılırsa uyarı gösterilir. Ollama'ya ulaşılamazsa bağlantı hatası penceresi açılır.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `main.pyw` | Uygulama (F8 dinleyicisi, menü, Ollama istekleri) |
| `BASLAT.bat` | Başlatıcı; gerekirse kurulumu çalıştırır |
| `kurulum.bat` | Sanal ortam ve paket kurulumu |
| `requirements.txt` | Python bağımlılıkları |

## İletişim

Dr. Öğr. Üyesi Ufuk Asil, Ostim Teknik Üniversitesi.
