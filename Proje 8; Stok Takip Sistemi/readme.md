# Stok Takip Sistemi

Bu proje, PyQt5 kütüphanesi kullanılarak oluşturulmuş bir stok takip sistemi uygulamasıdır. Uygulama, ürünlerin eklenmesi, siparişlerinin yönetilmesi ve stok güncellemelerinin yapılması gibi işlevleri yerine getirir.

## Kurulum

1. Bu depoyu yerel makinenize klonlayın:
git clone https://github.com/kullaniciadi/stok-takip-sistemi.git

2. Gerekli Python kütüphanelerini kurun:
pip install PyQt5

## Kullanım

1. Uygulamayı çalıştırın:
python deneme.py

2. Ana pencere açılacaktır. Buradan ürünleri ekleyebilir, çıkarabilir, siparişleri yönetebilir ve stok güncellemesi yapabilirsiniz.

3. Ürün eklemek için ilgili alanları doldurun ve "Ekle" butonuna basın.

4. Ürün çıkarmak için "Çıkar" butonuna basın, çıkarmak istediğiniz ürünleri seçin ve "Çıkar" butonuna basın.

5. Sipariş vermek için "Siparişleri Yönet" butonuna basın, bir ürün seçin, sipariş miktarını girin ve "Sipariş Ver" butonuna basın.

6. Stok güncellemesi yapmak için "Ürün Güncelleme" butonuna basın, değişiklikleri yapın ve "Kaydet" butonuna basın.

7. Arama kısmına metin girerek ürünleri filtreleyebilirsiniz.

8. Uygulama kapandığında veriler otomatik olarak kaydedilir ve bir sonraki açılışta yüklenir.

## Dosyalar

- `deneme.py`: Ana uygulama dosyası.
- `urun_guncelleme.py`: Ürün güncelleme penceresini içeren modül.
- `siparis_penceresi.py`: Sipariş yönetimi penceresini içeren modül.
- `urunler.pkl`: Ürün verilerinin saklandığı dosya.
- `siparisler.pkl`: Sipariş verilerinin saklandığı dosya.

## Lisans

Bu proje [MIT Lisansı](https://opensource.org/licenses/MIT) altında lisanslanmıştır.

## Uygulama görselleri

![image](https://github.com/Omercoskun77/PyQt5-Projeleri/assets/167522812/31020d08-83aa-4ec6-ac1b-8314b99d8780)
![image](https://github.com/Omercoskun77/PyQt5-Projeleri/assets/167522812/eecc2a99-abff-44ec-be5a-4a45517b1857)
![image](https://github.com/Omercoskun77/PyQt5-Projeleri/assets/167522812/22061c31-73ea-4346-896a-f21b0d660313)
