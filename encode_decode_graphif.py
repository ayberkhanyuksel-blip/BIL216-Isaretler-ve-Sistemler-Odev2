import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import get_window

# --- 1. PARAMETRELER (Encoding ile aynı olmalı) ---
FS = 44100
DURATION = 0.05
ALFABE = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ "
char_to_freq = {char: (400 + i*20, 1000 + i*20) for i, char in enumerate(ALFABE)}

def goertzel_filter(samples, target_freq, fs):
    n = len(samples)
    k = int(0.5 + (n * target_freq) / fs)
    w = (2.0 * np.pi / n) * k
    coeff = 2.0 * np.cos(w)
    q1, q2 = 0.0, 0.0
    for x in samples:
        q0 = coeff * q1 - q2 + x
        q2, q1 = q1, q0
    return q1**2 + q2**2 - q1 * q2 * coeff

def analyze_and_decode(file_path):
    # .wav dosyasını oku
    fs, data = wavfile.read(file_path)
    if data.dtype == np.int16:
        data = data / 32768.0
    
    samples_per_char = int(fs * DURATION)
    decoded_str = ""
    
    # --- GRAFİK 1: TÜM SİNYALİN SPEKTROGRAMI (Spektral Analiz) ---
    plt.figure(figsize=(12, 6))
    plt.specgram(data, Fs=fs, NFFT=1024, noverlap=512, cmap='viridis')
    plt.title("Tüm Sinyalin Spektrogram Analizi (Zaman-Frekans Düzlemi)")
    plt.xlabel("Zaman (s)")
    plt.ylabel("Frekans (Hz)")
    plt.ylim(0, 2000)
    plt.colorbar(label='Şiddet (dB)')
    plt.savefig("analiz_spektrogram.png")
    print("-> analiz_spektrogram.png oluşturuldu.")

    # Analiz ve Decoding İşlemi
    for i in range(0, len(data), samples_per_char):
        segment = data[i : i + samples_per_char]
        if len(segment) < samples_per_char: break
        
        # --- GRAFİK 2 & 3: Sadece ilk harf için Hamming ve FFT detaylarını çıkar ---
        if i == 0:
            # Hamming Uygulaması
            window = get_window('hamming', len(segment))
            windowed = segment * window
            
            # Hamming Grafiği
            plt.figure(figsize=(10, 5))
            plt.subplot(2, 1, 1)
            plt.plot(segment)
            plt.title("Orijinal Sinyal Segmenti (Penceresiz)")
            plt.subplot(2, 1, 2)
            plt.plot(windowed, color='orange')
            plt.title("Hamming Penceresi Uygulanmış Sinyal (Spektral Sızıntı Önlenmiş)")
            plt.tight_layout()
            plt.savefig("analiz_hamming_etkisi.png")
            print("-> analiz_hamming_etkisi.png oluşturuldu.")

            # FFT Spektral Analiz Grafiği
            fft_vals = np.abs(np.fft.rfft(windowed))
            fft_freqs = np.fft.rfftfreq(len(windowed), 1/fs)
            plt.figure(figsize=(10, 4))
            plt.plot(fft_freqs, fft_vals)
            plt.title("Tek Bir Harfin Frekans Spektrumu (FFT Peak Tespiti)")
            plt.xlabel("Frekans (Hz)")
            plt.ylabel("Genlik")
            plt.xlim(0, 2000)
            plt.grid(True)
            plt.savefig("analiz_tek_harf_fft.png")
            print("-> analiz_tek_harf_fft.png oluşturuldu.")

        # Goertzel ile Karar Verme
        window = get_window('hamming', len(segment))
        windowed = segment * window
        best_char, max_pwr = "?", -1
        for char, (f1, f2) in char_to_freq.items():
            pwr = goertzel_filter(windowed, f1, fs) + goertzel_filter(windowed, f2, fs)
            if pwr > max_pwr:
                max_pwr, best_char = pwr, char
        decoded_str += best_char

    return decoded_str

# Ana Çalıştırma
try:
    sonuc = analyze_and_decode("ODEV_2_SINYAL.wav")
    print("\n" + "="*30)
    print(f"ÇÖZÜLEN METİN: {sonuc}")
    print("="*30)
except FileNotFoundError:
    print("Hata: 'ODEV_2_SINYAL.wav' dosyası bulunamadı.")