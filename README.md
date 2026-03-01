BIL216 İşaretler ve Sistemler
Görev 2: Metinden Sese ve Sesten Metine DTMF
Uygulaması

1. Sinyal Sentezleme (Encoding)Bu modül, kullanıcıdan alınan metni sese dönüştürür.
2. Karakter Seti: Türk alfabesindeki 29 harf ve "Boşluk" karakteri dahil olmak üzere toplam 30 karakter tanımlanmıştır.
3. Matematiksel Model: Ses üretimi, her karakter için belirlenen iki farklı frekans çifti (f_1 ve f_2) kullanılarak aşağıdaki formüle göre sentezlenir:
s(t) = \sin(2π.f_1.t) + \sin(2\π.f_2.t)
4.Süre ve Kayıt: Her karakter sesi 50 ms sürecek şekilde ayarlanmış ve elde edilen sinyal ODEV_2_SINYAL.wav dosyasına kaydedilmiştir.
5.Sinyal Çözümleme (Decoding) Bu modül, kaydedilen ses dosyasını analiz ederek metni geri elde eder. Yöntem: Dosya belleğe alınarak zaman pencerelerine bölünmüştür.
6.Goertzel Algoritması: FFT'ye göre daha hızlı ve verimli olduğu için önceden belirlenmiş frekansların varlığını kontrol eden bu algoritma tercih edilmiştir.5. 
7.Pencereleme: Spektral sızıntıyı önlemek ve gürültüyü azaltmak amacıyla Hamming Penceresi uygulanmıştır.
