# ScribbleSense AI - Dil Öğrenme Koçu & Masaüstü Asistanı

<div align="center">

`Local AI + TTS + Deep Learning = Akıllı Dil Öğrenme Deneyimi`

[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111827?style=for-the-badge)](https://docs.ollama.com/quickstart)
[![Fork Info](https://img.shields.io/badge/Forked%20From-Ufuk%20As%C4%B1l-orange?style=for-the-badge)](https://github.com/u-asil)

</div>

---

## 📖 Proje Hakkında
Bu proje, **Ufuk Asıl** tarafından geliştirilen "AI Asistan Kampüsü" projesi temel alınarak fork edilmiş ve üzerinde kapsamlı geliştirmeler yapılarak bir **"Dil Öğrenme Koçu"** haline getirilmiştir. 

ScribbleSense AI, bilgisayarınızda (PDF, Word, Tarayıcı vb.) seçtiğiniz herhangi bir metni tek bir kısayol tuşuyla (**F8**) analiz eder, sesli telaffuz eder ve size o metnin gramer yapısını öğreten bir asistan vazifesi görür.

---

## ✨ Yeni ve Gelişmiş Özellikler

### 🎓 1. Dil Öğrenme Koçu (Gelişmiş Analiz)
Yalnızca çeviri yapmakla kalmaz; seçili İngilizce metni parçalarına ayırır:
- **Derin Gramer Analizi:** "Neden Öyle?" bölümüyle zaman kiplerini ve yapıları açıklar.
- **3 Seviyeli Örnekler:** Aynı yapıyı Gündelik, Akademik ve Sokak Ağzı formatlarında örnekler.
- **Kelime Analizi:** Zor kelimelerin kökenini (etimoloji) ve eş anlamlılarını sunar.

### 🔊 2. Akıllı Seslendirme (TTS)
- **Doğal Telaffuz:** Dil Koçu modunda metni İngilizce aksanıyla otomatik olarak seslendirir.
- **Tekrar Dinleme:** Sonuç ekranındaki buton ile telaffuzu istediğiniz kadar tekrar dinleyebilirsiniz.

---

## 🚀 Kurulum ve Başlatma

Programın çalışması için gerekli kütüphaneler bir sanal ortamda (`.venv`) tutulmaktadır. Doğrudan `python3 main.pyw` komutu hata verecektir.

### 🐧 Linux İşlemleri
1. **Bağımlılıkları Kurun:**
   ```bash
   bash kurulum.sh
   ```
2. **Programı Başlatın:**
   Sanal ortamı aktif ederek çalıştırmanız gerekir:
   ```bash
   source .venv/bin/activate
   python main.pyw
   ```
   *Veya alternatif olarak:* `./.venv/bin/python main.pyw`

### 🪟 Windows İşlemleri
1. `kurulum.bat` dosyasını çalıştırın.
2. `BASLAT.bat` dosyasını çalıştırarak uygulamayı açın (Bu dosya sanal ortamı otomatik kullanır).

---

## 🔧 Kullanım Rehberi

1. Herhangi bir doküman (PDF, Kitap, Web Sayfası vb.) açın.
2. Öğrenmek istediğiniz metni seçin.
3. Klavyeden **Shift + Alt + G** tuş kombinasyonuna basın.
4. Açılan menüden **"🎓 Dil Öğrenme Koçu"** veya diğer AI modlarını seçin.

---

## 🆘 Sorun Giderme

### `ModuleNotFoundError: No module named 'pyperclip'`
Bu hata, sanal ortamı (`.venv`) aktif etmediğinizde oluşur. Lütfen yukarıdaki "Başlatma" adımlarını takip edin: `source .venv/bin/activate`

### `sudo: apt-get: command not found`
Eğer `kurulum.sh` çalışırken bu hatayı alıyorsanız, sisteminiz Ubuntu/Debian tabanlı değildir. Kendi paket yöneticinizle şu paketleri kurun:
- **Fedora:** `sudo dnf install python3-tkinter espeak`
- **Arch:** `sudo pacman -S tk espeak-ng`

---

## 🛠️ Teknoloji Yığını
- **Shortkey:** Shift + Alt + G (Global)
- **Intelligence:** Ollama (Local LLM) / Google Gemini
- **Voice:** `pyttsx3` (Offline TTS)
- **GUI:** `Tkinter`

---

## 🤝 Teşekkür
Bu projenin temellerini atan ve fikir babası olan **Ufuk Asıl**'a katkılarından dolayı teşekkür ederiz. Orijinal projeye [buradan](https://github.com/ufukasia/Introduction-to-Data-Visualization-Project-Assignment) ulaşabilirsiniz.
