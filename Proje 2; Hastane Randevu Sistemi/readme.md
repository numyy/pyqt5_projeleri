# Hastane Randevu Sistemi

Bu proje, Python ve PyQt5 kütüphanesi kullanılarak geliştirilmiş bir Hastane Randevu Sistemi uygulamasıdır. Uygulama, hastaların doktor randevusu almasını, randevu geçmişini görüntülemesini ve randevu iptalini sağlar. Ayrıca, doktorların müsaitlik durumlarını gösterir.

## Kurulum

1. Bu depoyu klonlayın veya indirin.
2. Gerekli Python kütüphanelerini kurun:
pip install PyQt5

## Kullanım

1. Projenin ana dizinindeki `randevu.py` dosyasını çalıştırın.
2. Hasta bilgilerini (isim, soyisim, TC numarası) girin.
3. Doktor seçimi yapın.
4. Randevu tarihini ve saatini girin.
5. "Randevu Al" düğmesine tıklayın.
6. Randevu geçmişini görüntülemek için "Randevu Geçmişi" bölümüne bakın.
7. Randevu iptal etmek için, "Randevu İptal" düğmesine tıklayın ve iptal edilecek randevuyu seçin.

## Proje Yapısı

- `randevu.py`: Ana uygulama dosyası, kullanıcı arayüzünü ve randevu işlemlerini içerir.
- `musaitlik_takvimi.py`: Doktorların müsaitlik takvimini gösteren bir pencere oluşturur.

Proje, aşağıdaki sınıfları ve veri yapılarını kullanır:

- `Hasta`: İsim, soyisim, TC numarası ve randevu geçmişi bilgilerini tutar.
- `Doktor`: İsim, uzmanlık alanı, müsaitlik durumu ve müsaitlik takvimi bilgilerini tutar.
- `Randevu`: Randevu tarihi, doktor ve hasta bilgilerini tutar.

## Katkıda Bulunma

Bu proje, bir öğrenci projesidir ve katkıda bulunmak için açık değildir. Ancak, öneriler veya hataları bildirmek için lütfen bir Issue açın.

## Lisans

Bu proje, MIT Lisansı altında lisanslanmıştır.

## Uygulama görselleri

![image](https://github.com/flydedit/pyqt5_projeleri/assets/95934599/ff0a9b7e-4833-48f6-b5b9-2489d3114082)
![image](https://github.com/flydedit/pyqt5_projeleri/assets/95934599/e487bd70-846e-4b4b-a340-710057fc1070)

