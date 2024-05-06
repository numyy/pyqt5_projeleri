# Etkinlik ve Bilet Satış Platformu

Bu proje, bir etkinlik yönetim sistemini Python ve PyQt5 kütüphanesi kullanarak geliştirmektedir. Kullanıcılar, yeni etkinlikler ekleyebilir, etkinliklere bilet satabilir ve etkinliklere katılım sağlayabilir.

## Sınıflar

### Etkinlik

Bu sınıf, etkinliklerin bilgilerini (ad, tarih, mekan) ve bilet işlemlerini (bilet satma, bilet alma) yönetir.

### Bilet

Bu sınıf, bir biletin numarasını ve ilişkili etkinliği tutar.

### Kullanici

Bu sınıf, bir kullanıcının adını ve sahip olduğu biletleri yönetir.

## Veri Yapıları

- `etkinlikler` listesi, tüm etkinlik nesnelerini tutar.
- `kullanicilar` listesi, tüm kullanıcı nesnelerini tutar.
- `biletler` listesi (Etkinlik sınıfında), bir etkinliğe ait tüm biletleri tutar.

## Arayüz

PyQt5 kütüphanesi kullanılarak bir grafik kullanıcı arayüzü oluşturulmuştur. Arayüz, aşağıdaki bileşenleri içerir:

- Etkinlik listesi: Mevcut etkinlikleri gösterir.
- Etkinlik ekleme alanları: Yeni bir etkinlik eklemek için ad, tarih ve mekan girişi yapılır.
- Bilet satış alanı: Bir etkinliğe bilet satmak için bilet numarası girilir.
- İlgili butonlar: Etkinlik ekleme ve bilet satış işlemlerini gerçekleştirmek için butonlar.

## Kullanım

1. Projeyi indirin veya klonlayın.
2. Terminalde proje dizinine gidin.
3. `python etkinlikplatform.py` komutunu çalıştırın.
4. Arayüzden yeni etkinlikler ekleyebilir, bilet satabilir ve etkinlikleri görüntüleyebilirsiniz.

## Uygulama görselleri

![image](https://github.com/numyy/Python-pyqt5-Projeleri/assets/148050750/91440049-b6ca-4cba-aa78-d65e0d8b56d5)

