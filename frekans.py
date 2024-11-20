import numpy as np
from scipy.signal import butter, lfilter
import soundfile as sf
import simpleaudio as sa
import tkinter as tk
from tkinter import Label, Scale, Button, HORIZONTAL, filedialog

# Band-pass filter function
def apply_band_pass_filter(sound, lowcut, highcut, sr=44100):
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(4, [low, high], btype='band')
    return lfilter(b, a, sound)

# Initialize global variables for sound data
sound_data = None
sample_rate = 44100
filtered_data = None

# GUI for selecting frequency range
def create_gui():
    global sound_data, sample_rate, filtered_data  # Global değişkenler
    
    def load_audio():
        global sound_data, sample_rate
        file_path = filedialog.askopenfilename(
            title="Ses Dosyasını Seç",
            filetypes=(("WAV Dosyaları", "*.wav"), ("Tüm Dosyalar", "*.*"))
        )
        if file_path:
            sound_data, sample_rate = sf.read(file_path)
            status_label.config(text=f"Ses Yüklendi: {file_path}")

    def apply_filter():
        global filtered_data
        if sound_data is None:
            status_label.config(text="Lütfen önce bir ses dosyası yükleyin.")
            return
        
        lowcut = low_slider.get()
        highcut = high_slider.get()
        filtered_data = apply_band_pass_filter(sound_data, lowcut, highcut, sample_rate)
        status_label.config(text=f"Filtre Uygulandı: {lowcut} Hz - {highcut} Hz")

    def play_filtered_audio():
        global filtered_data
        if filtered_data is None:
            status_label.config(text="Lütfen önce filtre uygulayın.")
            return
        
        # Normalize and play filtered audio
        normalized_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
        audio = sa.play_buffer(normalized_data, num_channels=1 if len(normalized_data.shape) == 1 else normalized_data.shape[1], bytes_per_sample=2, sample_rate=sample_rate)
        audio.wait_done()
        status_label.config(text="İşlenmiş ses çalınıyor.")

    # Ana pencere oluşturma
    root = tk.Tk()
    root.title("Band-Pass Filtre ve Ses İşleme")

    # Başlık etiketi
    title_label = Label(root, text="Band-Pass Filtre Ayarları", font=("Arial", 16))
    title_label.pack(pady=10)

    # Ses yükleme butonu
    load_button = Button(root, text="Ses Yükle", command=load_audio)
    load_button.pack(pady=5)

    # Düşük kesim slider
    low_slider_label = Label(root, text="Düşük Kesim Frekansı (Hz):")
    low_slider_label.pack()
    low_slider = Scale(root, from_=20, to=2000, orient=HORIZONTAL, resolution=10)
    low_slider.pack()

    # Yüksek kesim slider
    high_slider_label = Label(root, text="Yüksek Kesim Frekansı (Hz):")
    high_slider_label.pack()
    high_slider = Scale(root, from_=500, to=8000, orient=HORIZONTAL, resolution=10)
    high_slider.pack()

    # Filtre uygula butonu
    apply_button = Button(root, text="Filtreyi Uygula", command=apply_filter)
    apply_button.pack(pady=10)

    # İşlenmiş ses çalma butonu
    play_button = Button(root, text="İşlenmiş Sesi Çal", command=play_filtered_audio)
    play_button.pack(pady=10)

    # Durum etiketi
    status_label = Label(root, text="Durum: Bekleniyor")
    status_label.pack(pady=10)

    # Pencere döngüsü
    root.mainloop()

# GUI'yi çalıştır
create_gui()
