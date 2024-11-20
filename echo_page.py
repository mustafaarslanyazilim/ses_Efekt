import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
from pydub.playback import play

# Tape Echo Efektini Uygulayan Fonksiyon
def apply_tape_echo(audio, sr, delay_time=0.3, feedback=0.5):
    delay_samples = int(sr * delay_time)
    output = np.zeros(len(audio) + delay_samples)
    for i in range(len(audio)):
        output[i] += audio[i]
        if i - delay_samples >= 0:
            output[i] += feedback * output[i - delay_samples]
    return np.clip(output[:len(audio)], -1.0, 1.0)

# Slider değerleri değişince işlenen sesi güncelleme
def update_processed_audio(event=None):
    global processed_audio
    if original_audio is None:
        return
    
    delay_time = delay_slider.get() / 1000  # Milisaniyeyi saniyeye çevir
    feedback = feedback_slider.get() / 100
    
    processed_audio = apply_tape_echo(original_audio, sample_rate, delay_time, feedback)
    sf.write("processed_audio.wav", processed_audio, sample_rate)
    status_label.config(text="İşlenmiş ses güncellendi.")

# Yüklenen sesi oynatma
def play_original_audio():
    if original_audio is not None:
        audio_segment = AudioSegment.from_file(file_path, format="wav")
        play(audio_segment)

# İşlenmiş sesi oynatma
def play_processed_audio():
    if processed_audio is not None:
        audio_segment = AudioSegment.from_file("processed_audio.wav", format="wav")
        play(audio_segment)

# Ses dosyası seçme
def select_file():
    global file_path, original_audio, sample_rate, processed_audio
    file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    if file_path:
        file_label.config(text=f"Seçilen dosya: {file_path.split('/')[-1]}")
        # Ses dosyasını yükle
        original_audio, sample_rate = sf.read(file_path)
        if len(original_audio.shape) == 2:  # Stereo ise mono'ya dönüştür
            original_audio = np.mean(original_audio, axis=1)
        # İlk işlenmiş sesi oluştur
        update_processed_audio()

# Arayüz oluşturma
root = tk.Tk()
root.title("Tape Echo Ses İşleyici")
root.geometry("600x400")

# Sol panel
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Dosya seçme butonu
file_button = tk.Button(left_frame, text="Ses Dosyası Seç", command=select_file)
file_button.pack(pady=10)

file_label = tk.Label(left_frame, text="Hiçbir dosya seçilmedi")
file_label.pack()

# Sliderlar
tk.Label(left_frame, text="Gecikme Süresi (ms):").pack()
delay_slider = tk.Scale(left_frame, from_=10, to=1000, orient="horizontal", command=update_processed_audio)
delay_slider.set(300)  # Varsayılan değer
delay_slider.pack()

tk.Label(left_frame, text="Geri Besleme (%):").pack()
feedback_slider = tk.Scale(left_frame, from_=0, to=100, orient="horizontal", command=update_processed_audio)
feedback_slider.set(50)  # Varsayılan değer
feedback_slider.pack()

# Ses oynatma butonları
play_original_button = tk.Button(left_frame, text="Orijinal Sesi Çal", command=play_original_audio)
play_original_button.pack(pady=5)

play_processed_button = tk.Button(left_frame, text="İşlenmiş Sesi Çal", command=play_processed_audio)
play_processed_button.pack(pady=5)

# Durum göstergesi
status_label = tk.Label(left_frame, text="")
status_label.pack()

# Sağ paneli oluştur
right_frame = tk.Frame(root, width=200)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Açıklama metni için bir Text widget
description_text = tk.Text(right_frame, height=20, width=30, wrap="word",font=(15))
description_text.pack(pady=5)
description_text.insert(
    tk.END,
    """Ses kaydına tape echo etkisi ekler. Tape echo, sesi tekrar eden bir yankı efekti oluşturur.

--- Gecikme Süresi: Ses kaydının ne kadar gecikerek tekrar edileceğini belirler.
--- Geri Besleme: Tekrarlanan sesin ne kadarının tekrar gecikmeye geri yollanacağını belirler.

# Gecikme Süresi: 0.0-2.0 saniye(0-2000 ms)
# Geri Besleme: 0.0-1.0 arası değer (%0 - %100)""",
)
description_text.config(state=tk.DISABLED)  # Düzenlemeyi devre dışı bırak

# Değişkenler
file_path = None
original_audio = None
sample_rate = None
processed_audio = None

root.mainloop()
