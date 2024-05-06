import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, QHBoxLayout

class Etkinlik:
    def __init__(self, ad, tarih, mekan):
        self.ad = ad
        self.tarih = tarih
        self.mekan = mekan
        self.biletler = []

    def bilet_sat(self, bilet):
        self.biletler.append(bilet)

    def bilet_al(self, bilet_no):
        for bilet in self.biletler:
            if bilet.no == bilet_no:
                self.biletler.remove(bilet)
                return bilet
        return None

class Bilet:
    def __init__(self, no, etkinlik):
        self.no = no
        self.etkinlik = etkinlik

class Kullanici:
    def __init__(self, ad):
        self.ad = ad
        self.biletler = []

    def bilet_al(self, bilet):
        self.biletler.append(bilet)

class EtkinlikPlatformu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Etkinlik ve Bilet Satış Platformu")
        self.setGeometry(100, 100, 800, 600)

        self.etkinlikler = []
        self.kullanicilar = []

        # Arayüz elemanları
        self.etkinlik_listesi = QListWidget()
        self.etkinlik_adi = QLineEdit()
        self.etkinlik_tarih = QLineEdit()
        self.etkinlik_mekan = QLineEdit()
        self.ekle_butonu = QPushButton("Etkinlik Ekle")
        self.ekle_butonu.clicked.connect(self.etkinlik_ekle)

        self.bilet_no = QLineEdit()
        self.bilet_sat_butonu = QPushButton("Bilet Sat")
        self.bilet_sat_butonu.clicked.connect(self.bilet_satis)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Etkinlikler"))
        layout.addWidget(self.etkinlik_listesi)
        layout.addWidget(QLabel("Yeni Etkinlik"))
        layout.addWidget(QLabel("Etkinlik Adı:"))
        layout.addWidget(self.etkinlik_adi)
        layout.addWidget(QLabel("Tarih:"))
        layout.addWidget(self.etkinlik_tarih)
        layout.addWidget(QLabel("Mekan:"))
        layout.addWidget(self.etkinlik_mekan)
        layout.addWidget(self.ekle_butonu)
        layout.addWidget(QLabel("Bilet Satışı"))
        layout.addWidget(QLabel("Bilet No:"))
        layout.addWidget(self.bilet_no)
        layout.addWidget(self.bilet_sat_butonu)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def etkinlik_ekle(self):
        ad = self.etkinlik_adi.text()
        tarih = self.etkinlik_tarih.text()
        mekan = self.etkinlik_mekan.text()
        etkinlik = Etkinlik(ad, tarih, mekan)
        self.etkinlikler.append(etkinlik)
        self.etkinlik_listesi.addItem(f"{ad} - {tarih} - {mekan}")
        self.etkinlik_adi.clear()
        self.etkinlik_tarih.clear()
        self.etkinlik_mekan.clear()

    def bilet_satis(self):
        bilet_no = int(self.bilet_no.text())
        secili_etkinlik = self.etkinlik_listesi.currentItem().text().split(" - ")
        ad, tarih, mekan = secili_etkinlik
        etkinlik = next((e for e in self.etkinlikler if e.ad == ad and e.tarih == tarih and e.mekan == mekan), None)
        if etkinlik:
            bilet = Bilet(bilet_no, etkinlik)
            etkinlik.bilet_sat(bilet)
            print(f"Bilet no {bilet_no} satıldı.")
        else:
            print("Geçerli bir etkinlik seçilmedi.")
        self.bilet_no.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    platform = EtkinlikPlatformu()
    platform.show()
    sys.exit(app.exec_())