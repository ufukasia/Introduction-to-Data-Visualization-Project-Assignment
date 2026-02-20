# AI Asistan Kampusu

<div align="center">

### Sekilli Sukullu Ogrenci Baslangic Rehberi

`Local AI + Cloud AI = Daha hizli ogrenme`

[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111827?style=for-the-badge)](https://docs.ollama.com/quickstart)
[![Gemini 3 Preview](https://img.shields.io/badge/Gemini%203-Preview-0f766e?style=for-the-badge)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/get-started-with-gemini-3)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-1a73e8?style=for-the-badge)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart)

</div>

```text
 ____  ____     _   _ _____ _   _ _  __      _    ____ ___ _
|  _ \|  _ \   | | | |  ___| | | | |/ /     / \  / ___|_ _| |
| | | | |_) |  | | | | |_  | | | | ' /     / _ \ \___ \| || |
| |_| |  _ <   | |_| |  _| | |_| | . \    / ___ \ ___) | || |___
|____/|_| \_\   \___/|_|    \___/|_|\_\  /_/   \_\____/___|_____|
K   K  L      U   U  BBBB   EEEEE         H   H   OOO    SSSS          GGG   EEEEE  L      DDDD   IIIII  N   N           !
K  K   L      U   U  B   B  E             H   H  O   O  S             G      E      L      D   D    I    NN  N           !
KKK    L      U   U  BBBB   EEE           HHHHH  O   O   SSS          G  GG  EEE    L      D   D    I    N N N           !
K  K   L      U   U  B   B  E             H   H  O   O      S         G   G  E      L      D   D    I    N  NN
K   K  LLLLL   UUU   BBBB   EEEEE         H   H   OOO   SSSS           GGG   EEEEE  LLLLL  DDDD   IIIII  N   N           !
```

> [!IMPORTANT]
> Gemini 3 preview "indirilen bir program" degil, Google Cloud Vertex AI uzerinden API ile kullanilan bir model ailesidir.

## 0) Ogrenci Icin Tek Adim

1. Ollama'yi bir kez kur: https://docs.ollama.com/windows
2. Bu klasorde sadece `BASLAT.bat` calistir.
3. Hepsi bu kadar.

> [!IMPORTANT]
> Ogrenci tarafinda ekstra komut gerekmez. `BASLAT.bat` gerekli durumda `kurulum.bat` dosyasini otomatik cagirir ve ortami kendi kurar.

## 1) BASLAT Calisinca Ne Oluyor?

1. `BASLAT.bat` önce `.venv` var mi kontrol eder.
2. Yoksa `kurulum.bat` otomatik calisir; Python 3 kontrolu, `.venv` olusturma, `pip` guncelleme ve `requirements.txt` paket kurulumu yapilir.
3. Sonra `main.pyw` arka planda acilir.
4. Uygulama varsayilan olarak `gemma3:1b` modeliyle Ollama'ya istek atar.

Ollama API varsayilan adresi: `http://localhost:11434`

## 2) Google Cloud Gemini 3 Preview (Vertex AI)

### Once gerekli olanlar
- Google Cloud projesi
- Billing acik olmali
- Vertex AI API aktif olmali
- `gcloud` CLI kurulu olmali

### gcloud giris ve kimlik

```powershell
gcloud init
gcloud auth application-default login
```

### Proje ve API ayari

```powershell
gcloud config set project YOUR_PROJECT_ID
gcloud services enable aiplatform.googleapis.com
```

### Python SDK kurulumu

```powershell
pip install --upgrade google-genai
```

### Ortam degiskenleri (PowerShell)

```powershell
$env:GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
$env:GOOGLE_CLOUD_LOCATION="global"
$env:GOOGLE_GENAI_USE_VERTEXAI="True"
```

### Ilk Gemini 3 Preview istegi

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Merhaba! Bana 3 maddede Python'da for dongusunu anlat.",
)

print(response.text)
```


## 3) Mini Ogrenci Challenge (Opsiyonel)
1. Terminalde su komutu yaz: `ollama run gemini-3-flash-preview`
2. Sonra Ollama'da gecerli bir modelle sor: `ollama run gemma3:1b`
3. Ayni soruyu Gemini 3 preview ile sor.
4. Cevaplari hiz, detay ve dogruluk acisindan karsilastir.

## 4) Hata Cozme Kisa Notlari
- `403` alirsan: Billing, Vertex AI API ve IAM rol (`roles/aiplatform.user`) kontrol et.
- `401` alirsan: `gcloud auth application-default login` komutunu yeniden calistir.
- `ollama model not found` alirsan once su komutu calistir: `ollama run gemma3:1b`
- `Model not found` alirsan: model ID'yi kontrol et (`gemini-3-flash-preview`, `gemini-3-pro-preview`, `gemini-3.1-pro-preview`).

## Kaynaklar (Resmi)
- Ollama Quickstart: https://docs.ollama.com/quickstart
- Ollama Windows: https://docs.ollama.com/windows
- Ollama Linux: https://docs.ollama.com/linux
- Vertex AI Quickstart: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart
- Gemini 3 Baslangic: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/get-started-with-gemini-3
- Gemini 3 Pro Model: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro
- Gemini 3 Flash Model: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-flash
