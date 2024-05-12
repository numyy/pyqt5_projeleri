# Çevrimiçi Kitap Okuma ve Paylaşım Platformu

Bu proje, Python ve PyQt5 kütüphanesi kullanılarak geliştirilmiş bir Çevrimiçi Kitap Okuma ve Paylaşım Platformu uygulamasıdır. Uygulama, kullanıcıların kitapları PDF formatında ekleyebilmelerine, görüntüleyebilmelerine ve yorumları paylaşabilmelerine olanak tanır. Ayrıca, yönetici kullanıcılar kitap ekleyebilir ve sistemde değişiklikler yapabilir.

## Özellikler

- Kullanıcı girişi (admin ve normal kullanıcı)
- Kitap ekleme (yönetici için)
- Kitap görüntüleme
- PDF formatındaki kitapların okunması
- Kitap yorumu ekleme ve görüntüleme

## Dosyalar

- `main.py`: Uygulamanın ana giriş noktası.
- `giris_ekranı.py`: Giriş ekranını içeren dosya.
- `book_add_window.py`: Kitap ekleme penceresini içeren dosya.
- `kitap_okuma_penceresi.py`: Kitap okuma penceresini içeren dosya.
- `yorum_penceresi.py`: Yorum penceresini içeren dosya.
- `books.json`: Eklenen kitapların bilgilerini tutan JSON dosyası.
- `comments.json`: Kullanıcıların yazdığı yorumları tutan JSON dosyası.
- `book_files/`: Eklenen kitap dosyalarının depolandığı klasör.

## Kurulum

1. Projeyi indirin veya klonlayın.
2. Terminal veya komut isteminden proje dizinine gidin.
3. PyQt5 kütüphanesini kurun: `pip install PyQt5`
4. Uygulamayı çalıştırın: `python main.py`

## Kullanım

1. Giriş ekranında kullanıcı adı ve şifre bilgilerini girin.
  - Admin kullanıcı: `kullanıcı adı = admin`, `şifre = admin123`
  - Normal kullanıcı: `kullanıcı adı = kullanıcı1903`, `şifre = 12345`
2. Ana ekranda aşağıdaki seçenekler mevcuttur:
  - **Kitap Ekle (sadece admin için)**: Yeni bir kitap eklemek için bu düğmeye tıklayın.
  - **Kitap Oku**: Mevcut kitapları görüntülemek ve okumak için bu düğmeye tıklayın.
  - **Yorum Yap**: Kitaplar hakkında yorum yapmak için bu düğmeye tıklayın.
3. İlgili pencerelerde işlemlerinizi gerçekleştirin.

## Lisans

[MIT](https://choosealicense.com/licenses/mit/)

## Uygulama görselleri

![image](https://github.com/Omercoskun77/PyQt5-Projeleri/assets/167522812/dc5b8976-c7cf-43e3-9102-761c451610ba)
![image](https://github.com/Omercoskun77/PyQt5-Projeleri/assets/167522812/98923bdd-0c20-4004-afcd-a7d740c7107f)
![image](https://github.com/Omercoskun77/PyQt5-Projeleri/assets/167522812/1d818d00-f086-4bde-8029-0baaa32430f7)
![image](https://github.com/Omercoskun77/PyQt5-Projeleri/assets/167522812/d0be3565-cf50-4474-a3ea-0667afbf846b)
![image](https://github.com/Omercoskun77/PyQt5-Projeleri/assets/167522812/da1ca1d6-2f86-4185-8545-7b533484c6e8)
