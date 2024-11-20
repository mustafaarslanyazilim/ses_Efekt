import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import simpleaudio as sa


class AudioEffectApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Koro Efekt Uygulaması")
        self.audio = None
        self.processed_audio = None

        # Ana çerçeve
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill="both", expand=True)

        # Sol kısım: Ses efektleri ve kontroller
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", padx=10, pady=10, fill="y")

        # Sağ kısım: Efekt açıklamaları
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", padx=10, pady=10, fill="y")

        # Ses yükleme butonu
        self.load_button = tk.Button(left_frame, text="Ses Yükle", command=self.load_audio)
        self.load_button.pack(pady=10)

        # Oynatma butonu
        self.play_button = tk.Button(left_frame, text="Sesi Oynat", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(pady=5)

        # Chorus derinlik slider'ı
        self.chorus_depth_slider = self.create_effect_slider(left_frame, "Chorus Derinliği", self.update_effects, -1.0, 1.0)

        # Chorus hız slider'ı
        self.chorus_rate_slider = self.create_effect_slider(left_frame, "Chorus Hızı", self.update_effects, 0.1, 5.0)

        # İşlenmiş sesi oynat butonu
        self.play_processed_button = tk.Button(left_frame, text="İşlenmiş Sesi Oynat", command=self.play_processed_audio, state=tk.DISABLED)
        self.play_processed_button.pack(pady=5)

        # Efekt sıfırlama butonu
        self.reset_button = tk.Button(left_frame, text="Efektleri Sıfırla", command=self.reset_effects)
        self.reset_button.pack(pady=10)

        # Sağ kısma açıklama alanı ekle
        self.description_label = tk.Label(right_frame, text="Efekt Açıklamaları", font=("Arial", 12, "bold"))
        self.description_label.pack(pady=10)

        self.description_text = tk.Text(right_frame, height=20, width=30, wrap="word",font=(15))
        self.description_text.pack(pady=5)
        self.description_text.insert(tk.END, """Chorus Derinliği
    Barı sola doğru çekerseniz soldan ses derinliği gelecek
    Barı sağa doğru çekerseniz sağdan ses derinliği gelecek

    Chorus hızı: gelecek olan ikinci sesin geliş zamanı""")

        self.description_text.config(state=tk.DISABLED)  # Düzenlemeyi devre dışı bırak

    def create_effect_slider(self, parent, name, command, min_value=0, max_value=10):
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        label = tk.Label(frame, text=name)
        label.pack(side="left")
        slider = tk.Scale(frame, from_=min_value, to=max_value, orient="horizontal", resolution=0.1, command=lambda _: command())
        slider.pack(side="right")
        return slider

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", ".wav;.mp3")])
        if file_path:
            self.audio = AudioSegment.from_file(file_path)
            self.processed_audio = self.audio
            self.update_controls()

    def update_controls(self):
        self.play_button.config(state=tk.NORMAL)
        self.play_processed_button.config(state=tk.NORMAL)

    def play_audio(self):
        if self.audio:
            self.play_audio_segment(self.audio)

    def play_processed_audio(self):
        if self.processed_audio:
            self.play_audio_segment(self.processed_audio)

    def play_audio_segment(self, audio_segment):
        # Pydub sesini simpleaudio ile çalmak için WAV formatına çevir
        wave_data = audio_segment.export(format="wav")
        wave_obj = sa.WaveObject.from_wave_file(wave_data)
        wave_obj.play()

    def update_effects(self):
        if self.audio is None:
            return

        # Chorus efekt parametrelerini slider'lardan al
        depth = self.chorus_depth_slider.get()
        rate = self.chorus_rate_slider.get()

        # Chorus efekti uygula
        self.processed_audio = self.chorus_effect(self.audio, depth, rate)

    def chorus_effect(self, sound, depth, rate):
        # Overlay efektini uygulayın
        return sound.overlay(sound.pan(depth), position=int(rate * 1000))

    def reset_effects(self):
        if self.audio:
            self.processed_audio = self.audio
            self.chorus_depth_slider.set(0)
            self.chorus_rate_slider.set(0)


# Ana uygulama
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioEffectApp(root)
    root.geometry("500x600")
    root.mainloop()
