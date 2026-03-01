import numpy as np
import sounddevice as sd
from scipy.io import wavfile

# --- PARAMETRELER ---
FS = 44100  # Örnekleme hızı
DURATION = 0.05  # Her harf süresi: 50 ms
ALFABE = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ " # 29 Harf + Boşluk

# Her karakter için benzersiz frekans çiftleri (f_low, f_high)
char_to_freq = {char: (400 + i*20, 1000 + i*20) for i, char in enumerate(ALFABE)}

def encode_text(text):
    full_signal = np.array([], dtype=np.float32)
    t = np.linspace(0, DURATION, int(FS * DURATION), endpoint=False)
    
    for char in text.upper():
        if char in char_to_freq:
            f1, f2 = char_to_freq[char]
            # Formül: s(t) = sin(2πf1t) + sin(2πf2t)
            signal = (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)) / 2
            full_signal = np.concatenate((full_signal, signal))
    return full_signal

# UYGULAMA
metin = input("Kodlanacak metni girin: ")
ses_verisi = encode_text(metin)

# .wav dosyasına kaydet
wavfile.write("ODEV_2_SINYAL.wav", FS, (ses_verisi * 32767).astype(np.int16))

# Sesi duy (Eğer hata alırsanız bu kısmı yorum satırı yapın)
print("Ses çalınıyor...")
sd.play(ses_verisi, FS)
sd.wait()
print("Kayıt tamamlandı: ODEV_2_SINYAL.wav")