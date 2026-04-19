import pyperclip
from pynput import keyboard
import pyautogui
import tkinter as tk
from tkinter import messagebox
import time
import threading
import queue
import re
import matplotlib.pyplot as plt


KISAYOL_METIN = keyboard.Key.f8

root = None
gui_queue = queue.Queue()
kisayol_basildi = False


ISLEMLER = [
    "🏥 Egzersiz Öner",
    "📋 Klinik Özet Oluştur",
    "📊 Egzersizleri Sınıflandır",
    "⚠️ Uyarılar ve Dikkat Noktaları",
]


def secili_metni_kopyala(max_deneme=4):
    sentinel = f"__AI_ASISTAN__{time.time_ns()}__"
    try:
        pyperclip.copy(sentinel)
    except Exception:
        pass

    for _ in range(max_deneme):
        pyautogui.hotkey("command", "c")
        time.sleep(0.2)
        metin = pyperclip.paste()
        if metin and metin.strip() and metin != sentinel:
            return metin
    return ""


def bolge_bul(metin):
    m = metin.lower()

    if "boyun" in m and "omuz" in m:
        return "Boyun ve Omuz"
    if "boyun" in m:
        return "Boyun"
    if "omuz" in m:
        return "Omuz"
    if "bel" in m:
        return "Bel"
    if "diz" in m:
        return "Diz"
    if "sırt" in m or "sirt" in m:
        return "Sırt"
    return "Genel Kas-İskelet Sistemi"


def yakinmalari_bul(metin):
    m = metin.lower()
    sonuc = []

    if "ağrı" in m or "agri" in m:
        sonuc.append("ağrı")
    if "tutuk" in m:
        sonuc.append("tutukluk")
    if "zorlan" in m:
        sonuc.append("hareket sırasında zorlanma")
    if "otur" in m:
        sonuc.append("uzun süreli oturmada artış")
    if "kaldır" in m or "kaldir" in m:
        sonuc.append("kol kaldırmada zorlanma")

    if not sonuc:
        sonuc.append("genel kas-iskelet sistemi yakınması")

    return sonuc


def egzersiz_oner(metin):
    bolge = bolge_bul(metin)
    yakinmalar = yakinmalari_bul(metin)

    if bolge == "Boyun ve Omuz":
        egzersizler = [
            ("Boyun esnetme", "Boynu sağa ve sola yavaşça eğerek kasları gevşetme.", "10 tekrar"),
            ("Omuz dairesel çevirme", "Omuz eklem hareketliliğini artırmak için kontrollü omuz çevirme.", "10 tekrar"),
            ("Scapula sıkıştırma", "Kürek kemiklerini arkaya doğru yaklaştırarak postürü destekleme.", "12 tekrar"),
            ("Göğüs açma esnetmesi", "Masa başı duruşuna bağlı gerginliği azaltmaya yardımcı olur.", "20 saniye x 3 set"),
            ("Duvar destekli omuz kaldırma", "Omuz hareket açıklığını destekleyen kontrollü kaldırma egzersizi.", "10 tekrar"),
        ]
    elif bolge == "Bel":
        egzersizler = [
            ("Pelvik tilt", "Bel çevresindeki kas kontrolünü artırmaya yardımcı olur.", "10 tekrar"),
            ("Diz göğse çekme", "Bel ve kalça çevresi gerginliğini azaltmaya yardımcı olur.", "10 tekrar"),
            ("Kedi-deve egzersizi", "Omurga hareketliliğini artırmaya yardımcı olur.", "10 tekrar"),
            ("Köprü egzersizi", "Kalça ve gövde kaslarını destekler.", "10 tekrar"),
            ("Bel rotasyon esnetmesi", "Bel bölgesi esnekliğini destekler.", "10 tekrar"),
        ]
    elif bolge == "Diz":
        egzersizler = [
            ("Düz bacak kaldırma", "Diz çevresi kaslarını güçlendirmeye yardımcı olur.", "10 tekrar"),
            ("Topuk kaydırma", "Diz hareket açıklığını artırır.", "10 tekrar"),
            ("Quadriceps sıkma", "Ön uyluk kaslarını aktive eder.", "12 tekrar"),
            ("Mini squat", "Diz çevresi kas kontrolünü destekler.", "8 tekrar"),
            ("Oturur pozisyonda diz açma", "Diz eklem hareketini destekler.", "10 tekrar"),
        ]
    elif bolge == "Boyun":
        egzersizler = [
            ("Boyun yan esnetme", "Boyun kaslarını gevşetmeye yardımcı kontrollü yan eğme.", "10 tekrar"),
            ("Boyun rotasyon", "Başı sağa ve sola çevirerek hareket açıklığını artırma.", "10 tekrar"),
            ("Çene geriye çekme", "Postürü destekleyen derin boyun fleksör aktivasyonu.", "10 tekrar"),
            ("Omuz yükseltme-bırakma", "Boyun-omuz hattındaki gerginliği azaltma.", "10 tekrar"),
            ("Üst trapez esnetme", "Boyun yan hattındaki kasların gevşemesini destekleme.", "20 saniye x 3 set"),
        ]
    else:
        egzersizler = [
            ("Genel esneme", "Kas gerginliğini azaltmaya yardımcı olur.", "10 tekrar"),
            ("Postür düzeltme", "Duruş farkındalığını artırmaya yardımcı olur.", "10 tekrar"),
            ("Eklem hareket açıklığı egzersizi", "Hareket kısıtlılığını azaltmaya yardımcı olur.", "10 tekrar"),
            ("Hafif güçlendirme", "Kas dayanıklılığını destekler.", "10 tekrar"),
            ("Nefes ve gevşeme", "Gevşemeyi destekler.", "5 tekrar"),
        ]

    satirlar = [
        f"Ağrı Bölgesi: {bolge}",
        "",
        f"Şikayet Özeti: Hastada {', '.join(yakinmalar)} bulunmaktadır.",
        "",
        f"Önerilen Egzersiz Sayısı: {len(egzersizler)}",
        "",
        "Egzersizler:"
    ]

    for i, (ad, aciklama, tekrar) in enumerate(egzersizler, start=1):
        satirlar.append(f"{i}. {ad}")
        satirlar.append(f"   Açıklama: {aciklama}")
        satirlar.append(f"   Tekrar: {tekrar}")
        satirlar.append("")

    satirlar.append(
        "Dikkat Edilmesi Gerekenler: Egzersizler ağrı sınırı içinde, yavaş ve kontrollü şekilde yapılmalıdır. "
        "Şikayet artarsa uzman görüşü alınmalıdır."
    )

    return "\n".join(satirlar)


def klinik_ozet_olustur(metin):
    bolge = bolge_bul(metin)
    yakinmalar = yakinmalari_bul(metin)

    return (
        f"Şikayet Bölgesi: {bolge}\n"
        f"Temel Yakınmalar: {', '.join(yakinmalar)}.\n"
        f"Fonksiyonel Etki: Uzun süreli oturma ve ilgili bölge hareketlerinde rahatsızlık artışı gözlenmektedir.\n"
        f"Kısa Değerlendirme: Bulgular kas gerginliği, postüral yüklenme ve hareket kısıtlılığı ile uyumlu görünmektedir."
    )


def egzersizleri_siniflandir(metin):
    bolge = bolge_bul(metin)

    if bolge == "Boyun ve Omuz":
        esneme, guc, mob, postur, denge = 2, 1, 1, 1, 0
    elif bolge == "Bel":
        esneme, guc, mob, postur, denge = 2, 2, 1, 0, 0
    elif bolge == "Diz":
        esneme, guc, mob, postur, denge = 1, 3, 1, 0, 0
    elif bolge == "Boyun":
        esneme, guc, mob, postur, denge = 2, 1, 1, 1, 0
    else:
        esneme, guc, mob, postur, denge = 2, 1, 1, 1, 0

    toplam = esneme + guc + mob + postur + denge

    return (
        f"Ağrı Bölgesi: {bolge}\n"
        f"Toplam Egzersiz Sayısı: {toplam}\n"
        f"Esneme: {esneme}\n"
        f"Güçlendirme: {guc}\n"
        f"Mobilizasyon: {mob}\n"
        f"Postür: {postur}\n"
        f"Denge: {denge}\n"
        f"Kısa Not: Egzersiz dağılımı mevcut şikayet bölgesine uygun temel fizik tedavi yaklaşımına göre oluşturulmuştur."
    )


def uyarilar_olustur(metin):
    bolge = bolge_bul(metin)

    maddeler = [
        "Egzersizler ağrı sınırı içinde yapılmalıdır.",
        "Ani ve zorlayıcı hareketlerden kaçınılmalıdır.",
        "Egzersiz sırasında uyuşma, baş dönmesi veya keskin ağrı olursa uygulama durdurulmalıdır.",
        "Hareketler kontrollü ve düzenli yapılmalıdır.",
        "Belirgin yakınma artışı varsa uzman değerlendirmesi alınmalıdır.",
    ]

    if bolge in ["Boyun", "Boyun ve Omuz"]:
        maddeler.append("Boyun hareketlerinde ani ve sert geriye atma tarzı hareketlerden kaçınılmalıdır.")
    elif bolge == "Bel":
        maddeler.append("Bel bölgesinde ani öne eğilme ve ağır yük kaldırma sırasında dikkatli olunmalıdır.")
    elif bolge == "Diz":
        maddeler.append("Diz bölgesinde çömelme ve merdiven gibi yük bindiren hareketler kontrollü yapılmalıdır.")

    return "\n".join([f"{i+1}. {madde}" for i, madde in enumerate(maddeler)])


def sayi_cek(pattern, text):
    eslesme = re.search(pattern, text, re.IGNORECASE)
    if eslesme:
        try:
            return int(eslesme.group(1))
        except Exception:
            return 0
    return 0


def grafik_olustur(metin):
    esneme = sayi_cek(r"Esneme:\s*(\d+)", metin)
    guclendirme = sayi_cek(r"Güçlendirme:\s*(\d+)", metin)
    mobilizasyon = sayi_cek(r"Mobilizasyon:\s*(\d+)", metin)
    postur = sayi_cek(r"Postür:\s*(\d+)", metin)
    denge = sayi_cek(r"Denge:\s*(\d+)", metin)

    if all(x == 0 for x in [esneme, guclendirme, mobilizasyon, postur, denge]):
        gui_queue.put((
            messagebox.showinfo,
            ("Grafik Bilgisi", "Bu sonuç için sayısal egzersiz verisi bulunamadı.")
        ))
        return

    etiketler = ["Esneme", "Güçlendirme", "Mobilizasyon", "Postür", "Denge"]
    degerler = [esneme, guclendirme, mobilizasyon, postur, denge]

    plt.figure(figsize=(8, 5))
    plt.bar(etiketler, degerler)
    plt.title("Önerilen Egzersiz Türleri")
    plt.xlabel("Egzersiz Türü")
    plt.ylabel("Sayı")
    plt.tight_layout()
    plt.show()


def sonuc_penceresi_goster(baslik, icerik):
    pencere = tk.Toplevel(root)
    pencere.title(baslik)
    pencere.geometry("950x620")
    pencere.minsize(520, 320)
    pencere.attributes("-topmost", True)

    frame = tk.Frame(pencere, bg="#1f1f1f")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    text_alani = tk.Text(
        frame,
        wrap="word",
        bg="#2b2b2b",
        fg="white",
        insertbackground="white",
        font=("Arial", 13),
        padx=12,
        pady=12,
    )
    kaydirma = tk.Scrollbar(frame, command=text_alani.yview)
    text_alani.configure(yscrollcommand=kaydirma.set)

    text_alani.pack(side="left", fill="both", expand=True)
    kaydirma.pack(side="right", fill="y")

    text_alani.insert("1.0", icerik)
    text_alani.config(state="disabled")

    alt_frame = tk.Frame(pencere, bg="#1f1f1f")
    alt_frame.pack(fill="x", padx=10, pady=(0, 10))

    def panoya_kopyala():
        pyperclip.copy(icerik)

    tk.Button(
        alt_frame,
        text="Panoya Kopyala",
        command=panoya_kopyala,
        bg="#3d3d3d",
        fg="white",
        relief="flat",
        padx=12,
        pady=6,
    ).pack(side="left")

    tk.Button(
        alt_frame,
        text="Grafik Göster",
        command=lambda: grafik_olustur(icerik),
        bg="#3d3d3d",
        fg="white",
        relief="flat",
        padx=12,
        pady=6,
    ).pack(side="left", padx=10)

    tk.Button(
        alt_frame,
        text="Kapat",
        command=pencere.destroy,
        bg="#3d3d3d",
        fg="white",
        relief="flat",
        padx=12,
        pady=6,
    ).pack(side="right")

    pencere.focus_force()
    pencere.lift()


def islemi_yap(komut_adi, secili_metin):
    try:
        if komut_adi == "🏥 Egzersiz Öner":
            sonuc = egzersiz_oner(secili_metin)
        elif komut_adi == "📋 Klinik Özet Oluştur":
            sonuc = klinik_ozet_olustur(secili_metin)
        elif komut_adi == "📊 Egzersizleri Sınıflandır":
            sonuc = egzersizleri_siniflandir(secili_metin)
        elif komut_adi == "⚠️ Uyarılar ve Dikkat Noktaları":
            sonuc = uyarilar_olustur(secili_metin)
        else:
            sonuc = "Geçersiz işlem seçildi."

        gui_queue.put((sonuc_penceresi_goster, (komut_adi, sonuc)))
    except Exception as e:
        gui_queue.put((messagebox.showerror, ("Hata", f"İşlem sırasında hata oluştu:\n{e}")))


def process_queue():
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
    secili_metin = secili_metni_kopyala()

    if not secili_metin.strip():
        gui_queue.put(
            (
                messagebox.showwarning,
                (
                    "Seçim Bulunamadı",
                    "Lütfen önce hasta şikayet metnini seçin, sonra F8'e basın.",
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
        font=("Arial", 11),
    )

    def komut_olustur(k_adi, s_metin):
        def komut_calistir():
            threading.Thread(target=islemi_yap, args=(k_adi, s_metin), daemon=True).start()
        return komut_calistir

    for baslik in ISLEMLER:
        menu.add_command(label=baslik, command=komut_olustur(baslik, secili_metin))

    menu.add_separator()
    menu.add_command(label="❌ İptal", command=lambda: None)

    try:
        x, y = pyautogui.position()
        menu.tk_popup(x, y)
    finally:
        menu.grab_release()


def on_press(key):
    global kisayol_basildi
    try:
        if key == KISAYOL_METIN and not kisayol_basildi:
            kisayol_basildi = True
            gui_queue.put((menu_goster, ()))
    except AttributeError:
        pass


def on_release(key):
    global kisayol_basildi
    try:
        if key == KISAYOL_METIN:
            kisayol_basildi = False
    except AttributeError:
        pass


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Fizik Tedavi AI Asistanı")
    print("=" * 60)
    print("🔧 Kullanım:")
    print("   1. Hasta şikayet metnini seç")
    print("   2. F8'e bas")
    print("   3. Menüden işlem seç")
    print("=" * 60)

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    root = tk.Tk()
    root.withdraw()
    root.after(100, process_queue)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Kapatılıyor...")