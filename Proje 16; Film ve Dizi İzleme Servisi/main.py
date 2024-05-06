import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import Qt

class Icerik:
    def __init__(self, ad, sure, tur):
        self.ad = ad
        self.sure = sure
        self.tur = tur

class Film(Icerik):
    def __init__(self, ad, sure, tur, yonetmen):
        super().__init__(ad, sure, tur)
        self.yonetmen = yonetmen

    def film_ekle(self, kullanici):
        kullanici.film_listesi.append(self)
        print(f"{self.ad} filmi {kullanici.kullanici_adi} kullanıcısının izleme listesine eklendi.")

    def liste_olustur(self, kullanici, liste_adi):
        yeni_liste = Liste(liste_adi)
        kullanici.izleme_listeleri[liste_adi] = yeni_liste
        print(f"{liste_adi} isimli yeni bir izleme listesi oluşturuldu.")

    def icerik_izle(self, kullanici):
        kullanici.izleme_gecmisi.append(self)
        print(f"{self.ad} filmi {kullanici.kullanici_adi} kullanıcısı tarafından izlendi.")

class Dizi(Icerik):
    def __init__(self, ad, sure, tur, sezon, bolum_sayisi):
        super().__init__(ad, sure, tur)
        self.sezon = sezon
        self.bolum_sayisi = bolum_sayisi

    def dizi_ekle(self, kullanici):
        kullanici.dizi_listesi.append(self)
        print(f"{self.ad} dizisi {kullanici.kullanici_adi} kullanıcısının izleme listesine eklendi.")

    def liste_olustur(self, kullanici, liste_adi):
        yeni_liste = Liste(liste_adi)
        kullanici.izleme_listeleri[liste_adi] = yeni_liste
        print(f"{liste_adi} isimli yeni bir izleme listesi oluşturuldu.")

    def icerik_izle(self, kullanici):
        kullanici.izleme_gecmisi.append(self)
        print(f"{self.ad} dizisinin bir bölümü {kullanici.kullanici_adi} kullanıcısı tarafından izlendi.")

class Liste:
    def __init__(self, ad):
        self.ad = ad
        self.icerikler = []

    def icerik_ekle(self, icerik):
        self.icerikler.append(icerik)
        print(f"{icerik.ad} içeriği {self.ad} listesine eklendi.")

    def icerik_kaldir(self, icerik):
        self.icerikler.remove(icerik)
        print(f"{icerik.ad} içeriği {self.ad} listesinden kaldırıldı.")

class Kullanici:
    def __init__(self, kullanici_adi, sifre):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.film_listesi = []
        self.dizi_listesi = []
        self.izleme_listeleri = {}
        self.izleme_gecmisi = []

    def icerik_izle(self, icerik):
        icerik.icerik_izle(self)

    def liste_olustur(self, liste_adi):
        yeni_liste = Liste(liste_adi)
        self.izleme_listeleri[liste_adi] = yeni_liste
        print(f"{liste_adi} isimli yeni bir izleme listesi oluşturuldu.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("main_window.ui", self)

        # Örnek kullanıcı oluşturma
        self.kullanici = Kullanici("kullanici1", "sifre123")

        # Örnek içerikler oluşturma
        film1 = Film("Film 1", "120 dakika", "Aksiyon", "Yönetmen 1")
        film2 = Film("Film 2", "150 dakika", "Dram", "Yönetmen 2")
        dizi1 = Dizi("Dizi 1", "45 dakika", "Komedi", 1, 10)
        dizi2 = Dizi("Dizi 2", "60 dakika", "Bilim Kurgu", 2, 8)

        # Örnek içerikleri kullanıcıya ekleme
        film1.film_ekle(self.kullanici)
        dizi1.dizi_ekle(self.kullanici)

        # Film listesini doldurma
        self.film_listesi_doldur()

        # Sinyal bağlantıları
        self.ui.film_listesi.itemClicked.connect(self.film_secildi)

    def film_listesi_doldur(self):
        self.ui.film_listesi.clear()
        for film in self.kullanici.film_listesi:
            item = QListWidgetItem(film.ad)
            item.setData(Qt.UserRole, film)
            self.ui.film_listesi.addItem(item)

    def film_secildi(self, item):
        film = item.data(Qt.UserRole)
        film.icerik_izle(self.kullanici)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())