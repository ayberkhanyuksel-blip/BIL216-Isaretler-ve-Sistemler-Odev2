import numpy as np
from scipy.io import wavfile
from scipy.signal import get_window

# --- PARAMETRELER (Encode ile aynı olmalı) ---
DURATION = 0.05 
ALFABE = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ "
char_to_freq = {char: (400 + i*20, 1000 + i*20) for i, char in enumerate(ALFABE)}

def goertzel_filter(samples, target_freq, fs):
    """Goertzel Algoritması: Belirli frekansların varlığını kontrol eder """
    n = len(samples)
    k = int(0.5 + (n * target_freq) / fs)
    w = (2.0 * np.pi / n) * k
    coeff = 2.0 * np.cos(w)
    q1, q2 = 0.0, 0.0
    for x in samples:
        q0 = coeff * q1 - q2 + x
        q2, q1 = q1, q0
    return q1**2 + q2**2 - q1 * q2 * coeff

def decode_audio(file_path):
    fs, data = wavfile.read(file_path) # Dosyayı belleğe al [cite: 46]
    if data.dtype == np.int16:
        data = data / 32768.0 # Normalizasyon
    
    samples_per_char = int(fs * DURATION)
    decoded_str = ""
    
    for i in range(0, len(data), samples_per_char):
        segment = data[i : i + samples_per_char]
        if len(segment) < samples_per_char: break
        
        # Hamming penceresi kullanarak gürültüyü azaltma 
        windowed = segment * get_window('hamming', len(segment))
        
        best_char = ""
        max_pwr = -1
        # 30 frekans çiftini kontrol et 
        for char, (f1, f2) in char_to_freq.items():
            pwr = goertzel_filter(windowed, f1, fs) + goertzel_filter(windowed, f2, fs)
            if pwr > max_pwr:
                max_pwr = pwr
                best_char = char
        decoded_str += best_char
    return decoded_str

# UYGULAMA
try:
    cozumlenen_metin = decode_audio("ODEV_2_SINYAL.wav")
    print(f"Çözümlenen Orijinal Metin: {cozumlenen_metin}")
except FileNotFoundError:
    print("Hata: Önce encoding kodunu çalıştırıp dosyayı oluşturun.")