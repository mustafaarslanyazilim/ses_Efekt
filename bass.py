import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import simpleaudio as sa

# Bas frekanslarını artırma
def bas_ekle(ses, db=5):
    bas_filter = ses.low_pass_filter(200)  # 200 Hz altındaki frekansları al
    return bas_filter.apply_gain(db)  # Kazanç ekle

# Tiz frekanslarını artırma
def tiz_ekle(ses, db=5):
    tiz_filter = ses.high_pass_filter(2000)  # 2000 Hz üstündeki frekansları al
    return tiz_filter.apply_gain(db)  # Kazanç ekle

# Equalizer fonksiyonu
def apply_equalizer(ses, bas_db=5, mid_db=0, tiz_db=5):
    # Bas frekanslarını artır
    bas = bas_ekle(ses, bas_db)
    # Orta frekansları artır (200-2000 Hz arası)
    low_mid = ses.high_pass_filter(200).low_pass_filter(2000).apply_gain(mid_db)
    # Tiz frekanslarını artır
    tiz = tiz_ekle(ses, tiz_db)
    # Üç bileşeni üst üste bindir
    return bas.overlay(low_mid).overlay(tiz)

# Ses çalma fonksiyonu
def ses_cal(ses):
    global play_obj
    if play_obj:
        play_obj.stop()
    play_obj = sa.play_buffer(ses.raw_data, num_channels=ses.channels, bytes_per_sample=ses.sample_width, sample_rate=ses.frame_rate)
    play_obj.wait_done()

# Slider değiştiğinde işlenmiş sesi güncelle
def guncelle_ve_cal(val):
    if ses_dosyasi:
        bas_db = bas_scale.get()
        mid_db = mid_scale.get()
        tiz_db = tiz_scale.get()
        # Equalizer'ı uygula ve işlenmiş sesi güncelle
        global islenmis_ses
        islenmis_ses = apply_equalizer(ses_dosyasi, bas_db, mid_db, tiz_db)

# Ses dosyası yükleme fonksiyonu
def ses_yukle():
    global ses_dosyasi, islenmis_ses
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Ses Dosyaları", "*.mp3 *.wav")])
    if dosya_yolu:
        ses_dosyasi = AudioSegment.from_file(dosya_yolu)
        islenmis_ses = ses_dosyasi  # İlk başta işlenmemiş sesi atayın
        durum_label.config(text=f"Yüklendi: {dosya_yolu.split('/')[-1]}")
        # Yükleme işleminden sonra otomatik çalmayı engellemek için ses hemen çalınmaz

# İlk yüklenen sesi çalma
def ilk_sesi_cal():
    if ses_dosyasi:
        ses_cal(ses_dosyasi)

# İşlenmiş sesi çalma
def islenmis_sesi_cal():
    if islenmis_ses:
        ses_cal(islenmis_ses)

# Efektleri sıfırlama fonksiyonu
def efektleri_sifirla():
    # Sliderları sıfırla
    bas_scale.set(0)
    mid_scale.set(0)
    tiz_scale.set(0)
    # Efektleri sıfırla
    global islenmis_ses
    islenmis_ses = ses_dosyasi  # İşlenmemiş sese geri dön

# GUI'yi başlat
root = tk.Tk()
root.title("Ses Equalizer")
root.geometry("600x600")

# Ses dosyası seçimi
ses_dosyasi = None
islenmis_ses = None
play_obj = None

# Sol panel
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Sağ panel (açıklamalar)
right_frame = tk.Frame(root, width=200)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Ses dosyasını yükle butonu
yukle_buton = tk.Button(left_frame, text="Ses Yükle", command=ses_yukle)
yukle_buton.pack(pady=10)

# Yüklenen sesi oynat butonu
ilk_ses_buton = tk.Button(left_frame, text="Yüklenen Sesi Oynat", command=ilk_sesi_cal)
ilk_ses_buton.pack(pady=10)

# Durum etiketini ekle
durum_label = tk.Label(left_frame, text="Ses dosyası seçilmedi")
durum_label.pack()

# Bas, Orta, Tiz slider barları
bas_label = tk.Label(left_frame, text="Bas")
bas_label.pack()
bas_scale = tk.Scale(left_frame, from_=-10, to=10, orient=tk.HORIZONTAL, command=guncelle_ve_cal)
bas_scale.set(0)
bas_scale.pack()

mid_label = tk.Label(left_frame, text="Orta")
mid_label.pack()
mid_scale = tk.Scale(left_frame, from_=-10, to=10, orient=tk.HORIZONTAL, command=guncelle_ve_cal)
mid_scale.set(0)
mid_scale.pack()

tiz_label = tk.Label(left_frame, text="Tiz")
tiz_label.pack()
tiz_scale = tk.Scale(left_frame, from_=-10, to=10, orient=tk.HORIZONTAL, command=guncelle_ve_cal)
tiz_scale.set(0)
tiz_scale.pack()

# İşlenmiş sesi oynat butonu
islenmis_ses_buton = tk.Button(left_frame, text="İşlenmiş Sesi Oynat", command=islenmis_sesi_cal)
islenmis_ses_buton.pack(pady=10)

# Efektleri sıfırlama butonu
efektleri_sifirla_buton = tk.Button(left_frame, text="Efektleri Sıfırla", command=efektleri_sifirla)
efektleri_sifirla_buton.pack(pady=10)

# Açıklama metnini ekleyelim
description_text = tk.Text(right_frame, height=20, width=20, wrap="word", font=(10))
description_text.insert(tk.END, """
        # Bas ekleme : 200 Hz altındaki frekansları artırır
        # Tiz ekleme : 2000 Hz üstündeki frekansları artırır
        # Orta frekansları artır (200-2000 Hz arası)
""")
description_text.config(state=tk.DISABLED)
description_text.pack(pady=5)

root.mainloop()
