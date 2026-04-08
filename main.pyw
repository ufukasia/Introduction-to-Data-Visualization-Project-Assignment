import pyperclip
from pynput import keyboard
import pyautogui
import tkinter as tk
from tkinter import messagebox
import time
import threading
import requests
import queue
import pyttsx3
import platform
from gtts import gTTS
import os
import pygame


# --- AYARLAR ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_ADI = "gemma3:1b"  # Hızlı ve hafif zeka
TEXT_MODEL_CANDIDATES = [
    MODEL_ADI,
    "gemma4:e2b",
    "gemini-3-flash-preview:cloud",
]

KISAYOL_METIN = 'g'  # Metin seçimi için tetikleyici harf
ALT_BASILI = False    # Alt tuşunun durumu
SHIFT_BASILI = False  # Shift tuşunun durumu


# Global değişkenler
root = None
gui_queue = queue.Queue()
kisayol_basildi = False

# --- YÜKSEK KALİTELİ SES (gTTS) AYARLARI ---
def setup_tts():
    try:
        pygame.mixer.init()
        print("✅ Yüksek kaliteli ses motoru (Neural) hazır.")
    except Exception as e:
        print(f"⚠️ Ses Kartı Başlatma Hatası: {e}")

setup_tts()

def speak_text(text):
    """Metni gTTS ile yüksek kalitede seslendirir. Pygame veya sistem oynatıcı kullanır."""
    def run_speech():
        temp_file = "voice_temp.mp3"
        try:
            # Markdown işaretlerini temizle
            cleaned_text = text.replace("**", "").replace("#", "").replace("*", "").replace("- ", ", ")
            
            # Metni Google TTS ile oluştur
            tts = gTTS(text=cleaned_text, lang='en', tld='com')
            tts.save(temp_file)
            
            # --- YÖNTEM 1: Pygame (Öncelikli) ---
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                pygame.mixer.music.unload()
                return # Başarılı ise çık
            except Exception as e:
                print(f"ℹ️ Pygame ile ses çalınamadı, yedek yönteme geçiliyor... ({e})")

            # --- YÖNTEM 2: Sistem Oynatıcıları (Yedek) ---
            # Fedora/Ubuntu'da bulunabilecek yaygın oynatıcılar
            players = ["mpg123", "play", "vlc --play-and-exit", "paplay", "aplay"]
            for player in players:
                # vlc dışındakiler genelde sessiz çalışır, vlc için extra flag gerekebilir
                cmd = f"{player} {temp_file} > /dev/null 2>&1"
                if os.system(cmd) == 0:
                    return # Başarılı ise çık

        except Exception as e:
            print(f"⚠️ Seslendirme hatası: {e}")
        finally:
            if os.path.exists(temp_file):
                try:
                    # Bir saniye bekle (dosya kilitli kalmış olabilir)
                    time.sleep(0.5)
                    os.remove(temp_file)
                except:
                    pass

    threading.Thread(target=run_speech, daemon=True).start()


# --- MENÜ SEÇENEKLERİ VE PROMPT'LAR ---
ISLEMLER = {
    "📝 Gramer Düzelt": "Bu metni Türkçe yazım ve dil bilgisi kurallarına göre düzelt, resmi ve akıcı olsun. Sadece sonucu ver.",
    "🇬🇧 İngilizceye Çevir": "Bu metni İngilizceye çevir. Sadece çeviriyi ver.",
    "🇹🇷 Türkçeye Çevir": "Bu metni Türkçeye çevir. Sadece çeviriyi ver.",
    "📑 Özetle (Madde Madde)": "Bu metni analiz et ve en önemli noktaları madde madde özetle.",
    "💼 Daha Resmi Yap": "Bu metni kurumsal bir e-posta diline çevir, çok resmi olsun.",
    "🐍 Python Koduna Çevir": "Bu metindeki isteği yerine getiren bir Python kodu yaz. Sadece kodu ver.",
    "📧 Cevap Yaz (Mail)": "Bu gelen bir e-posta, buna kibar ve profesyonel bir cevap metni taslağı yaz.",
    "🎓 Dil Öğrenme Koçu": (
        "SADECE aşağıdaki şablona göre cevap ver. Başka hiçbir şey yazma.\n\n"
        "ŞABLON:\n"
        "📝 **ORİJİNAL METİN**\n[İngilizce Metin]\n\n"
        "🇹🇷 **ANLAMI**\n[Doğal Türkçe Çeviri]\n\n"
        "🔊 **TÜRKÇE OKUNUŞ (Yaklaşık)**\n[Örn: Ay woz ap örli in dı mornink]\n\n"
        "🧠 **PARÇALAYARAK ANLAM**\n[Kelime -> Anlam]\n\n"
        "⚡ **DOĞAL CÜMLE**\n[Akıcı Türkçe Çeviri]\n\n"
        "💡 **KISA NOT**\n[Gramer veya kelime notu]\n\n"
        "Analiz edilecek metin: "
    ),
    "🎮 PS5 Oyun Skor + Acımasız Yorum": (
        "Seçili metni bir PS5 oyunu adı olarak ele al. Aşağıdaki formatta Türkçe cevap ver:\n"
        "1) Oyun: <ad>\n"
        "2) Topluluk Beğeni Skorları:\n"
        "- Metacritic User Score: <değer veya 'bilgi yok'>\n"
        "- OpenCritic / benzer eleştirmen ortalaması: <değer veya 'bilgi yok'>\n"
        "- Oyuncu yorumu ortalaması (PS Store vb.): <değer veya 'bilgi yok'>\n"
        "3) Hüküm: sadece 'IYI' veya 'KOTU'\n"
        "4) Acımasız Yorum: 2-4 cümle, net ve sert.\n"
        "Kurallar: Kesin bilmediğin puanı uydurma, onun yerine 'bilgi yok' yaz. "
        "Yorumu skorlarla tutarlı kur."
    ),
}


def get_available_text_model():
    """Metin işlemede kullanılabilir modeli seçer."""
    preferred_models = []
    for model in TEXT_MODEL_CANDIDATES:
        if model and model not in preferred_models:
            preferred_models.append(model)

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            return MODEL_ADI

        models = response.json().get("models", [])
        installed_lower = {m.get("name", "").lower(): m.get("name", "") for m in models}

        for candidate in preferred_models:
            candidate_lower = candidate.lower()
            if candidate_lower in installed_lower:
                return installed_lower[candidate_lower]

            candidate_base = candidate_lower.split(":")[0]
            for installed_name_lower, installed_name in installed_lower.items():
                if installed_name_lower.startswith(candidate_base + ":"):
                    return installed_name
    except Exception as e:
        print(f"⚠️ Model listesi alınırken hata: {e}")
        pass

    print(f"ℹ️ Model bulunamadı veya liste alınamadı, varsayılan kullanılıyor: {MODEL_ADI}")
    return MODEL_ADI


def ollama_cevap_al(prompt):
    """Ollama API'den cevap al."""
    try:
        aktif_model = get_available_text_model()
        payload = {
            "model": aktif_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            },
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()

        err_msg = (
            f"Ollama API Hatası: {response.status_code}\n"
            f"Model: {aktif_model}\n"
            f"Cevap: {response.text}"
        )
        print(f"❌ {err_msg}")
        gui_queue.put((messagebox.showerror, ("API Hatası", err_msg)))
        return None

    except requests.exceptions.ConnectionError:
        err_msg = (
            "Ollama'ya bağlanılamadı.\n"
            "Programın çalıştığından emin olun!\n"
            "(http://localhost:11434)"
        )
        print(f"❌ {err_msg}")
        gui_queue.put((messagebox.showerror, ("Bağlantı Hatası", err_msg)))
        return None
    except Exception as e:
        err_msg = f"Beklenmeyen Hata: {e}"
        print(f"❌ {err_msg}")
        gui_queue.put((messagebox.showerror, ("Hata", err_msg)))
        return None


def strip_code_fence(text):
    if not text:
        return text
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        lines = lines[1:] if lines else []
        while lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def secili_metni_kopyala(max_deneme=4):
    sentinel = f"__AI_ASISTAN__{time.time_ns()}__"
    try:
        pyperclip.copy(sentinel)
    except Exception:
        pass

    for _ in range(max_deneme):
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.2)
        metin = pyperclip.paste()
        if metin and metin.strip() and metin != sentinel:
            return metin
    return ""


def pencere_modunda_gosterilsin_mi(komut_adi):
    return "PS5 Oyun Skor" in komut_adi or "Dil Öğrenme Koçu" in komut_adi


def sonuc_penceresi_goster(baslik, icerik, orijinal_metin=None):
    pencere = tk.Toplevel(root)
    pencere.title(f"ScribbleSense AI - {baslik}")
    pencere.geometry("820x600")
    pencere.minsize(600, 400)
    pencere.configure(bg="#121212")
    pencere.attributes("-topmost", True)

    # Başlık Alanı
    baslik_label = tk.Label(
        pencere,
        text=baslik.upper(),
        bg="#121212",
        fg="#00d1b2",
        font=("Segoe UI", 14, "bold"),
        pady=10
    )
    baslik_label.pack(fill="x")

    frame = tk.Frame(pencere, bg="#121212")
    frame.pack(fill="both", expand=True, padx=20, pady=5)

    text_alani = tk.Text(
        frame,
        wrap="word",
        bg="#1e1e1e",
        fg="#e0e0e0",
        insertbackground="white",
        font=("Consolas" if "Kod" in baslik else "Segoe UI", 11),
        padx=15,
        pady=15,
        relief="flat",
        borderwidth=0
    )
    kaydirma = tk.Scrollbar(frame, command=text_alani.yview)
    text_alani.configure(yscrollcommand=kaydirma.set)

    text_alani.pack(side="left", fill="both", expand=True)
    kaydirma.pack(side="right", fill="y")

    # İçeriği biçimlendirerek ekle (Başlıkları kalın yapabiliriz aslında ama basit tutalım)
    text_alani.insert("1.0", icerik)
    text_alani.config(state="disabled")

    alt_frame = tk.Frame(pencere, bg="#121212")
    alt_frame.pack(fill="x", padx=20, pady=15)

    def panoya_kopyala():
        pyperclip.copy(icerik)
        messagebox.showinfo("Başarılı", "İçerik panoya kopyalandı!")

    def tekrar_seslendir():
        if orijinal_metin:
            speak_text(orijinal_metin)

    # Butonlar
    btn_style = {
        "bg": "#333333",
        "fg": "white",
        "activebackground": "#444444",
        "activeforeground": "white",
        "relief": "flat",
        "padx": 15,
        "pady": 8,
        "font": ("Segoe UI", 9, "bold")
    }

    tk.Button(
        alt_frame,
        text="📋 Panoya Kopyala",
        command=panoya_kopyala,
        **btn_style
    ).pack(side="left", padx=(0, 10))

    if orijinal_metin and "Dil Öğrenme Koçu" in baslik:
        tk.Button(
            alt_frame,
            text="🔊 Tekrar Seslendir",
            command=tekrar_seslendir,
            **btn_style
        ).pack(side="left")

    tk.Button(
        alt_frame,
        text="Kapat",
        command=pencere.destroy,
        bg="#d9534f",
        fg="white",
        activebackground="#c9302c",
        activeforeground="white",
        relief="flat",
        padx=15,
        pady=8,
        font=("Segoe UI", 9, "bold")
    ).pack(side="right")

    pencere.focus_force()
    pencere.lift()


def islemi_yap(komut_adi, secili_metin):
    prompt_emri = ISLEMLER[komut_adi]
    full_prompt = f"{prompt_emri}:\n\n'{secili_metin}'"

    print(f"🤖 İşlem: {komut_adi}")
    print("⏳ Ollama ile işleniyor...")

    sonuc = ollama_cevap_al(full_prompt)
    if not sonuc:
        print("❌ Sonuç alınamadı.")
        return

    sonuc = strip_code_fence(sonuc)
    if sonuc.startswith("'") and sonuc.endswith("'"):
        sonuc = sonuc[1:-1]

    if pencere_modunda_gosterilsin_mi(komut_adi):
        gui_queue.put((sonuc_penceresi_goster, (komut_adi, sonuc, secili_metin)))
        
        # Dil Koçu ise ve orijinal metin varsa seslendir
        if "Dil Öğrenme Koçu" in komut_adi:
            speak_text(secili_metin)
            
        print("✅ Sonuç ayrı pencerede gösterildi.")
        return

    time.sleep(0.2)
    pyperclip.copy(sonuc)
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "v")
    print("✅ İşlem tamamlandı!")


def process_queue():
    """Kuyruktaki GUI işlemlerini ana thread'de çalıştırır."""
    try:
        while True:
            try:
                task = gui_queue.get_nowait()
            except queue.Empty:
                break
            func, args = task
            func(*args)
    finally:
        if root:
            root.after(100, process_queue)


def menu_goster():
    """Metni kopyalar ve menüyü gösterir (ana thread)."""
    secili_metin = secili_metni_kopyala()
    if not secili_metin.strip():
        gui_queue.put(
            (
                messagebox.showwarning,
                (
                    "Secim Bulunamadi",
                    "Lutfen once metin secin, sonra butona basin veya Shift + Alt + G yapin.",
                ),
            )
        )
        return

    menu = tk.Menu(
        root,
        tearoff=0,
        bg="#2b2b2b",
        fg="white",
        activebackground="#4a4a4a",
        activeforeground="white",
        font=("Segoe UI", 10),
    )

    def komut_olustur(k_adi, s_metin):
        def komut_calistir():
            threading.Thread(
                target=islemi_yap, args=(k_adi, s_metin), daemon=True
            ).start()

        return komut_calistir

    for baslik in ISLEMLER.keys():
        menu.add_command(label=baslik, command=komut_olustur(baslik, secili_metin))

    menu.add_separator()
    menu.add_command(label="❌ İptal", command=lambda: None)

    try:
        x, y = pyautogui.position()
        menu.tk_popup(x, y)
    finally:
        menu.grab_release()


def on_press(key):
    global kisayol_basildi, ALT_BASILI, SHIFT_BASILI
    try:
        # Alt ve Shift tuşlarını takip et
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_gr]:
            ALT_BASILI = True
        if key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
            SHIFT_BASILI = True
        
        # Harf kontrolü (char özelliği)
        k = ""
        try:
            k = key.char.lower()
        except:
            pass

        # Shift + Alt + G kontrolü
        if k == KISAYOL_METIN and ALT_BASILI and SHIFT_BASILI and not kisayol_basildi:
            print(f"🔥 Kısayol algılandı! İşlem başlatılıyor... (Model: {get_available_text_model()})")
            kisayol_basildi = True
            gui_queue.put((menu_goster, ()))
    except Exception:
        pass


def on_release(key):
    global kisayol_basildi, ALT_BASILI, SHIFT_BASILI
    try:
        # Alt tuşu bırakıldı mı?
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_gr]:
            ALT_BASILI = False
        # Shift tuşu bırakıldı mı?
        if key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
            SHIFT_BASILI = False
            
        # Harf bırakıldı mı?
        k = ""
        try:
            k = key.char.lower()
        except:
            pass
            
        if k == KISAYOL_METIN:
            kisayol_basildi = False
    except Exception:
        pass


class FloatingButton:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("ScribbleSense AI Trigger")
        
        # Pencere ayarları: Başlık çubuğunu kaldır ve her zaman üstte tut
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        
        # Linux Wayland/X11 uyumluluğu için alfa (şeffaflık)
        try:
            self.window.attributes("-alpha", 0.85)
        except:
            pass

        # Boyut ve Konum (Sağ alt köşe varsayılan)
        self.width = 60
        self.height = 60
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = screen_width - self.width - 50
        y = screen_height - self.height - 100
        self.window.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Görsel Tasarım
        self.canvas = tk.Canvas(
            self.window, 
            width=self.width, 
            height=self.height, 
            bg="#121212", 
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack()

        # Yuvarlak Buton Çizimi
        padding = 5
        self.button_circle = self.canvas.create_oval(
            padding, padding, self.width-padding, self.height-padding,
            fill="#00d1b2", outline="#008f7a", width=2
        )
        
        # Buton Üzerindeki Metin/Emoji
        self.canvas.create_text(
            self.width//2, self.height//2,
            text="🤖", font=("Segoe UI", 18), fill="white"
        )

        # Olay Bağlamaları (Events)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        
        # Sürükleme değişkenleri
        self.drag_data = {"x": 0, "y": 0}
        self.moved = False

    def on_click(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.moved = False

    def on_drag(self, event):
        self.moved = True
        deltax = event.x - self.drag_data["x"]
        deltay = event.y - self.drag_data["y"]
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        if not self.moved:
            # Tıklama gerçekleşti, menüyü göster
            gui_queue.put((menu_goster, ()))
        self.moved = False

    def show(self):
        self.window.deiconify()
        self.window.lift()


if __name__ == "__main__":
    print("\n" + "!" * 60)
    print("⚠️  SÜRÜM: 2.0 (GELISMIS DIL KOCU)")
    print("!" * 60 + "\n")
    print("=" * 60)
    print("🤖 AI Asistan - Metin İşleme")
    print("=" * 60)
    aktif_text_model = get_available_text_model()
    print(f"📦 Metin İşleme (Shift+Alt+G): {aktif_text_model}")
    print()
    print("🔧 Kullanım:")
    print("   Shift + Alt + G - Metin sec ve AI islemleri yap")
    print()
    print("⚠️ Programı kapatmak için bu pencereyi kapatın veya Ctrl+C yapın.")
    print("=" * 60)

    try:
        test_response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if test_response.status_code == 200:
            print("✅ Ollama bağlantısı başarılı!")
        else:
            print("⚠️ Ollama'ya bağlanılamadı, servisi kontrol edin!")
    except Exception:
        print("⚠️ Ollama çalışmıyor olabilir! 'ollama serve' ile başlatın.")

    print()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    root = tk.Tk()
    root.withdraw()
    
    # Yüzen Butonu Başlat
    floating_btn = FloatingButton(root)
    
    root.after(100, process_queue)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Kapatılıyor...")
