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

![image](https://github.com/Omercoskun77/PyQt-Projeleri/assets/167522812/6208508b-46d0-431e-8469-649b090ee38b)
![image](https://github.com/Omercoskun77/PyQt-Projeleri/assets/167522812/c89e93ae-8f6e-4f0c-b0a0-e69346dc5a33)
![image](https://github.com/Omercoskun77/PyQt-Projeleri/assets/167522812/80b0e20a-1758-4296-b582-12194d65f437)
![image](https://github.com/Omercoskun77/PyQt-Projeleri/assets/167522812/8a7d0956-d74e-477b-bade-f8855a92b382)
![image](https://github.com/Omercoskun77/PyQt-Projeleri/assets/167522812/0372853b-5bf7-49dc-b724-2e994a1fb17f)




