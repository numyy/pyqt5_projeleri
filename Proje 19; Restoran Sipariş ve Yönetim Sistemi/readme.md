# Restoran Sipariş ve Yönetim Sistemi

Bu proje, Python ve PyQt5 kütüphanesi kullanılarak geliştirilmiş bir Restoran Sipariş ve Yönetim Sistemidir. Sistem, müşterilerin menüden sipariş vermelerini, çalışanların siparişleri yönetmelerini ve sipariş geçmişini takip etmelerini sağlar.

## Özellikler

- Müşteri ve Çalışan giriş arayüzleri
- Menü gösterimi ve ürün stok bilgisi
- Sipariş verme ve müşteri bilgilerinin girilmesi
- Sipariş onayı ve sipariş geçmişi takibi
- SQLite veritabanı ile çalışan kimlik doğrulama

## Kurulum

1. Öncelikle Python'un en son sürümünü [buradan](https://www.python.org/downloads/) indirin ve sisteminize kurun.
2. Projeyi indirmek veya klonlamak için aşağıdaki komutu kullanın:
git clone https://github.com/kullaniciadi/restaurant-system.git

3. Proje dizinine gidin:
cd restaurant-system

4. Gerekli Python paketlerini kurun:
pip install -r requirements.txt

5. SQLite veritabanını oluşturun:
python database.py

## Kullanım

1. Uygulamayı başlatmak için aşağıdaki komutu çalıştırın:
python main.py
2. Giriş arayüzünde "Müşteri Olarak Giriş Yap" veya "Çalışan Olarak Giriş Yap" butonlarından birini seçin.
3. Müşteri olarak giriş yaptıysanız, menüden sipariş verebilir ve müşteri bilgilerini girebilirsiniz.
4. Çalışan olarak giriş yaptıysanız, yalnızca mevcut siparişleri ve sipariş geçmişini görüntüleyebilirsiniz.

## Katkıda Bulunma

Eğer bu projeye katkıda bulunmak isterseniz, lütfen bir "pull request" oluşturun veya Issues bölümüne bir konu açın. Tüm katkılar dikkate alınacaktır.

## Lisans

Bu proje MIT Lisansı kapsamındadır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
