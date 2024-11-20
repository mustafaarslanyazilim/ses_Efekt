import tkinter as tk  
from tkinter import filedialog  
from pydub import AudioSegment  
from pydub.playback import play  
import numpy as np  
import threading  
import librosa 
import subprocess 
from scipy.signal import butter, lfilter  

class AudioEffectApp:  
    def __init__(self, master):  
        self.master = master  
        self.master.title("Ses Efektleri Uygulaması")  
        self.audio = None  
        self.processed_audio = None  
        self.playing = False
        
        # Create a right frame for the explanation section
        self.right_frame = tk.Frame(self.master, width=300)
        self.right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Add a label and a text widget for displaying explanations
        self.description_label = tk.Label(self.right_frame, text="Efekt Açıklamaları", font=("Arial", 12, "bold"))
        self.description_label.pack(pady=10)

        self.description_text = tk.Text(self.right_frame, height=40, width=40, wrap="word", font=(15))
        self.description_text.insert(tk.END, """
                                     
        # Reverb: Ortamın akustik etkisini simüle eder; sesin daha geniş, derin ve yankılı duyulmasını sağlar.
                                     
        # Subtle Echo: Sesin hafif bir gecikmeyle tekrar edilmesini sağlar, mekân hissini güçlendirir.
                                     
        # Flanger: Sesin hafif zaman gecikmeleriyle üst üste binerek dalgalı bir efekt oluşturur.
                                     
        # Pitch Shift: Sesin frekansını değiştirerek notalarını yükseltir veya düşürür; sesin daha ince veya kalın duyulmasını sağlar.
                                     
                                     """)
        self.description_text.config(state=tk.DISABLED)
        self.description_text.pack(pady=5)

        #bass-tiz sayfasına yönlendirme
        # Tape echo sayfasına yönlendirme butonu
        self.new_page_button2 = tk.Button(self.master,text="BAS_TİZ effect", command=self.open_new_page3)
        self.new_page_button2.pack(pady=20)

        # Koro sayfasına yönlendirme butonu
        self.new_page_button = tk.Button(self.master, text="Koro effect", command=self.open_new_page)
        self.new_page_button.pack(pady=20)

        # Tape echo sayfasına yönlendirme butonu
        self.new_page_button2 = tk.Button(self.master,text="Echo effect", command=self.open_new_page2)
        self.new_page_button2.pack(pady=20)

        #frekans aralıkları ekleme butonu
        self.new_page_button2 = tk.Button(self.master,text="Frekans effect", command=self.open_new_page4)
        self.new_page_button2.pack(pady=20)

        # Ses yükleme butonu  
        self.load_button = tk.Button(self.master, text="Ses Yükle", command=self.load_audio)  
        self.load_button.pack(pady=10)  

        # Oynatma butonu  
        self.play_button = tk.Button(self.master, text="Sesi Oynat", command=self.play_audio, state=tk.DISABLED)  
        self.play_button.pack(pady=5)  

 
        # Efekt slider'ları    
        self.reverb_slider = self.create_effect_slider("Reverb Miktarı", self.apply_effects, 0, 10) 
        self.subtle_echo_slider = self.create_effect_slider("Subtle Echo Gecikmesi (ms)", self.apply_effects, 0, 500)  
        self.flanger_slider = self.create_effect_slider("Flanger Pozisyon (ms)", self.apply_effects, 0, 20)  
        self.pitch_shift_slider = self.create_effect_slider("Pitch Shift (Yarım Ton)", self.apply_effects, -5, 5)

        # İşlenmiş sesi oynat butonu  
        self.play_processed_button = tk.Button(self.master, text="İşlenmiş Sesi Oynat", command=self.play_processed_audio, state=tk.DISABLED)  
        self.play_processed_button.pack(pady=5)  

        # Sıfırlama butonu  
        self.reset_button = tk.Button(self.master, text="Efektleri Sıfırla", command=self.reset_effects)  
        self.reset_button.pack(pady=10)  

        
    def open_new_page(self):
            # yeni_sayfa.py dosyasını çalıştır
            subprocess.Popen(["python", "koro_page.py"])
    
    def open_new_page2(self):
            # yeni_sayfa.py dosyasını çalıştır
            subprocess.Popen(["python", "echo_page.py"])

    def open_new_page3(self):
            # yeni_sayfa.py dosyasını çalıştır
            subprocess.Popen(["python", "bass.py"])

    def open_new_page4(self):
            # yeni_sayfa.py dosyasını çalıştır
            subprocess.Popen(["python", "frekans.py"])

    def create_effect_slider(self, name, command, min_value=0, max_value=10):  
        frame = tk.Frame(self.master)  
        frame.pack(pady=5)  
        label = tk.Label(frame, text=name)  
        label.pack(side="left")  
        slider = tk.Scale(frame, from_=min_value, to=max_value, orient="horizontal", resolution=0.1, command=command)  
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
        if self.audio and not self.playing:  
            self.playing = True  
            self.thread = threading.Thread(target=self.update_playback)  
            self.thread.start()  
            self.play_button.config(state=tk.DISABLED)  

    def update_playback(self):  
        play(self.audio)  
        self.reset_controls()  

    def reset_controls(self):  
        self.playing = False  
        self.play_button.config(state=tk.NORMAL)  

    def play_processed_audio(self):  
        if self.processed_audio and not self.playing:  
            self.playing = True  
            self.thread = threading.Thread(target=self.update_processed_playback)  
            self.thread.start()  
            self.play_processed_button.config(state=tk.DISABLED)  

    def update_processed_playback(self):  
        play(self.processed_audio)  
        self.reset_processed_controls()  

    def reset_processed_controls(self):  
        self.playing = False  
        # GUI güncellemesini ana iş parçacığında yapmak için after kullan  
        self.play_processed_button.after(0, lambda: self.play_processed_button.config(state=tk.NORMAL))  

    def apply_effects(self, value=None):  
        if self.audio is None:  
            return  

        # Ses verisini numpy dizisine çevir  
        samples = np.array(self.audio.get_array_of_samples())  
        fs = self.audio.frame_rate  # Örnekleme frekansını al  

        # Normalize et (-1, 1 aralığına)  
        if self.audio.sample_width == 2:  # 16-bit ses
            samples = samples.astype(np.int16) / 32768.0
        else:
            raise ValueError("Sadece 16-bit ses destekleniyor.")  

        # Efekt parametrelerini al
        reverb_value = self.reverb_slider.get()
        subtle_echo_value = self.subtle_echo_slider.get()  
        flanger_value = self.flanger_slider.get()  
        pitch_shift_steps = self.pitch_shift_slider.get()

        # Reverb efekti uygula  
        if reverb_value > 0:  
            samples = self.apply_reverb(samples, reverb_value)  

        # Subtle Echo uygula  
        if subtle_echo_value > 0:  
            samples = self.subtle_echo_effect(samples, delay_ms=subtle_echo_value)  

        # Flanger uygula  
        if flanger_value > 0:  
            samples = self.flanger_effect(samples, depth=flanger_value, fs=fs)  

        # Pitch Shift uygula
        if pitch_shift_steps != 0:
            samples = librosa.effects.pitch_shift(samples, sr=fs, n_steps=pitch_shift_steps)  


        # Normalize et (yeniden -1, 1 aralığına)  
        samples = samples / np.max(np.abs(samples))  

        # 16-bit'e geri dönüştür  
        samples = (samples * 32767).astype(np.int16)  

        # AudioSegment'e geri dönüştür  
        self.processed_audio = AudioSegment(  
            samples.tobytes(),  
            frame_rate=fs,  
            sample_width=self.audio.sample_width,  
            channels=self.audio.channels  
        )  

        self.play_processed_button.config(state=tk.NORMAL)


    def apply_reverb(self, audio_data, reverb_amount):  
            num_samples = len(audio_data)  
            delayed_samples = int(44100 * (0.1 * reverb_amount))  
            reverb_signal = np.zeros(num_samples)  

            for i in range(num_samples):  
                reverb_signal[i] = audio_data[i]  
                if i - delayed_samples >= 0:  
                    reverb_signal[i] += audio_data[i - delayed_samples] * 0.5  

            return reverb_signal  

    def subtle_echo_effect(self, sound, delay_ms=150):  
        delay_samples = int(delay_ms * 44.1)  # Delay in samples  
        echoed_sound = np.zeros(len(sound))  
        for i in range(len(sound)):  
            echoed_sound[i] = sound[i]  
            if i - delay_samples >= 0:  
                echoed_sound[i] += sound[i - delay_samples] * 0.5  
        return echoed_sound  

    def flanger_effect(self, samples, depth, fs):  
        delay_samples = int(depth * fs / 1000.0)  # Derinliği ms'den örneğe çevir  
        flanged_samples = np.zeros_like(samples)  

        for i in range(len(samples)):  
            if i >= delay_samples:  
                flanged_samples[i] = samples[i] + samples[i - delay_samples] * 0.5  # %50 katkı  
            else:  
                flanged_samples[i] = samples[i]  # Gecikme süresinin dışında orijinal kalır  

        return flanged_samples.astype(samples.dtype)  # Uygun türde döndür 

    def apply_pitch_shift(self, audio, sr, n_steps):  
        return librosa.effects.pitch_shift(y=audio, sr=sr, n_steps=n_steps)  
    

    def yarim_pes_ver(self, audio):  
        return audio._spawn(audio.raw_data, overrides={  
            "frame_rate": int(audio.frame_rate * 0.94387)  # Yaklaşık yarım ton düşürme oranı  
        }).set_frame_rate(audio.frame_rate)  

    def yarim_tiz_ver(self, audio):  
        return audio._spawn(audio.raw_data, overrides={  
            "frame_rate": int(audio.frame_rate * 1.05946)  # Yaklaşık yarım ton artırma oranı  
        }).set_frame_rate(audio.frame_rate)


    def reset_effects(self):
        self.reverb_slider.set(0)
        self.flanger_slider.set(0)
        self.pitch_shift_slider.set(0)
        self.subtle_echo_slider.set(0)

# Ana uygulama  
if __name__ == "__main__":  
    root = tk.Tk()  
    app = AudioEffectApp(root)
    root.geometry("900x800")  
    root.mainloop()

    


