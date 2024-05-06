import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QHeaderView, QLineEdit, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import Qt


class Kitap:
    def __init__(self, kitap_id, ad, yazar):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.odunc_durumu = False

    def durum_guncelle(self, durum):
        if durum == "Ödünç Alındı":
            self.odunc_durumu = True
        elif durum == "Rafta":
            self.odunc_durumu = False
        print(f"{self.ad} kitabının durumu '{durum}' olarak güncellendi.")


class Uye:
    def __init__(self, uye_id, ad, soyad):
        self.uye_id = uye_id
        self.ad = ad
        self.soyad = soyad
        self.odunc_kitaplar = []


class Odunc:
    def __init__(self, kitap, uye):
        self.kitap = kitap
        self.uye = uye

    def odunc_al(self):
        if not self.kitap.odunc_durumu:
            self.kitap.durum_guncelle("Ödünç Alındı")
            self.uye.odunc_kitaplar.append(self.kitap.ad)
            print(f"{self.uye.ad} {self.uye.soyad} tarafından '{self.kitap.ad}' kitabı ödünç alındı.")
        else:
            print("Kitap zaten ödünç alınmış.")

    def iade_et(self):
        if self.kitap.ad in self.uye.odunc_kitaplar:
            self.kitap.durum_guncelle("Rafta")
            self.uye.odunc_kitaplar.remove(self.kitap.ad)
            print(f"{self.uye.ad} {self.uye.soyad} tarafından '{self.kitap.ad}' kitabı iade edildi.")
        else:
            print("Bu kitap bu üye tarafından ödünç alınmamış.")


class OduncAlmaPenceresi(QWidget):
    def __init__(self, kitaplar, uyeler):
        super().__init__()
        self.setWindowTitle("Ödünç Alma")
        self.setGeometry(100, 100, 400, 200)

        self.kitaplar = kitaplar
        self.uyeler = uyeler
        self.app = QApplication.instance()

        self.kitap_combo = QComboBox()
        self.kitap_combo.addItems([kitap.ad for kitap in self.kitaplar])

        self.uye_combo = QComboBox()
        self.uye_combo.addItems([f"{uye.ad} {uye.soyad}" for uye in self.uyeler])

        self.odunc_al_button = QPushButton("Ödünç Al")
        self.odunc_al_button.clicked.connect(self.odunc_al)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Kitap:"))
        layout.addWidget(self.kitap_combo)
        layout.addWidget(QLabel("Üye:"))
        layout.addWidget(self.uye_combo)
        layout.addWidget(self.odunc_al_button)
        self.setLayout(layout)

    def closeEvent(self, event):

        self.close()

    def odunc_al(self):
        secili_kitap_adi = self.kitap_combo.currentText()
        secili_uye_adi = self.uye_combo.currentText()

        kitap = next((k for k in self.kitaplar if k.ad == secili_kitap_adi), None)
        uye = next((u for u in self.uyeler if f"{u.ad} {u.soyad}" == secili_uye_adi), None)

        if kitap and uye:
            odunc = Odunc(kitap, uye)
            odunc.odunc_al()
        else:
            print("Geçersiz kitap veya üye seçimi.")

    def exec_(self):
        self.show()
        return self.app.exec_()


class IadeEtmePenceresi(QWidget):
    def __init__(self, kitaplar, uyeler):
        super().__init__()
        self.setWindowTitle("Kitap İade")
        self.setGeometry(100, 100, 400, 200)

        self.kitaplar = kitaplar
        self.uyeler = uyeler
        self.app = QApplication.instance()

        self.kitap_combo = QComboBox()
        self.kitap_combo.addItems([kitap.ad for kitap in self.kitaplar if kitap.odunc_durumu])

        self.uye_combo = QComboBox()
        self.uye_combo.addItems([f"{uye.ad} {uye.soyad}" for uye in self.uyeler])

        self.iade_et_button = QPushButton("İade Et")
        self.iade_et_button.clicked.connect(self.iade_et)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Kitap:"))
        layout.addWidget(self.kitap_combo)
        layout.addWidget(QLabel("Üye:"))
        layout.addWidget(self.uye_combo)
        layout.addWidget(self.iade_et_button)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.close()

    def iade_et(self):
        secili_kitap_adi = self.kitap_combo.currentText()
        secili_uye_adi = self.uye_combo.currentText()

        kitap = next((k for k in self.kitaplar if k.ad == secili_kitap_adi), None)
        uye = next((u for u in self.uyeler if f"{u.ad} {u.soyad}" == secili_uye_adi), None)

        if kitap and uye:
            odunc = Odunc(kitap, uye)
            odunc.iade_et()
        else:
            print("Geçersiz kitap veya üye seçimi.")

    def exec_(self):
        self.show()
        return self.app.exec_()


class KutuphaneUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kütüphane Uygulaması")
        self.setGeometry(100, 100, 800, 800)

        self.kitaplar = [Kitap(1, "Kitap 1", "Yazar 1"), Kitap(2, "Kitap 2", "Yazar 2")]
        self.uyeler = [Uye(1, "Ahmet", "Yılmaz"), Uye(2, "Ayşe", "Demir")]

        self.kitap_tablosu = QTableWidget()
        self.kitap_tablosu.setColumnCount(4)
        self.kitap_tablosu.setHorizontalHeaderLabels(["Kitap ID", "Kitap Adı", "Yazar", "Durum"])
        self.kitap_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.uye_tablosu = QTableWidget()
        self.uye_tablosu.setColumnCount(4)
        self.uye_tablosu.setHorizontalHeaderLabels(["Üye ID", "Ad", "Soyad", "Aldığı Kitap"])
        self.uye_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.kitap_adi_input = QLineEdit()
        self.yazar_input = QLineEdit()
        self.kitap_ekle_button = QPushButton("Kitap Ekle")
        self.kitap_ekle_button.clicked.connect(self.kitap_ekle)

        self.uye_adi_input = QLineEdit()
        self.uye_soyadi_input = QLineEdit()
        self.uye_ekle_button = QPushButton("Üye Ekle")
        self.uye_ekle_button.clicked.connect(self.uye_ekle)

        self.odunc_al_button = QPushButton("Ödünç Al")
        self.odunc_al_button.clicked.connect(self.odunc_alma_penceresi_ac)

        self.iade_et_button = QPushButton("Kitap İade Et")
        self.iade_et_button.clicked.connect(self.iade_etme_penceresi_ac)

        self.yenile_button = QPushButton("Yenile")
        self.yenile_button.clicked.connect(self.yenile)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Kitaplar"))
        layout.addWidget(self.kitap_tablosu)
        layout.addWidget(QLabel("Kitap Adı"))
        layout.addWidget(self.kitap_adi_input)
        layout.addWidget(QLabel("Kitap Yazarı"))
        layout.addWidget(self.yazar_input)
        layout.addWidget(self.kitap_ekle_button)
        layout.addWidget(QLabel("Üyeler"))
        layout.addWidget(self.uye_tablosu)
        layout.addWidget(QLabel("Üye Adı"))
        layout.addWidget(self.uye_adi_input)
        layout.addWidget(QLabel("Üye Soyadı"))
        layout.addWidget(self.uye_soyadi_input)
        layout.addWidget(self.uye_ekle_button)
        layout.addWidget(self.odunc_al_button)
        layout.addWidget(self.iade_et_button)
        layout.addWidget(self.yenile_button)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.kitaplari_yukle()
        self.uyeleri_yukle()

    def yenile(self):
        self.kitaplari_yukle()
        self.uyeleri_yukle()

    def kitaplari_yukle(self):
        self.kitap_tablosu.setRowCount(len(self.kitaplar))
        for i, kitap in enumerate(self.kitaplar):
            self.kitap_tablosu.setItem(i, 0, QTableWidgetItem(str(kitap.kitap_id)))
            self.kitap_tablosu.setItem(i, 1, QTableWidgetItem(kitap.ad))
            self.kitap_tablosu.setItem(i, 2, QTableWidgetItem(kitap.yazar))
            if kitap.odunc_durumu:
                self.kitap_tablosu.setItem(i, 3, QTableWidgetItem("Ödünç Alındı"))
            else:
                self.kitap_tablosu.setItem(i, 3, QTableWidgetItem("Rafta"))

    def uyeleri_yukle(self):
        self.uye_tablosu.setRowCount(len(self.uyeler))
        for i, uye in enumerate(self.uyeler):
            self.uye_tablosu.setItem(i, 0, QTableWidgetItem(str(uye.uye_id)))
            self.uye_tablosu.setItem(i, 1, QTableWidgetItem(uye.ad))
            self.uye_tablosu.setItem(i, 2, QTableWidgetItem(uye.soyad))
            if uye.odunc_kitaplar:
                self.uye_tablosu.setItem(i, 3, QTableWidgetItem(uye.odunc_kitaplar[0]))
            else:
                self.uye_tablosu.setItem(i, 3, QTableWidgetItem("Boş"))

    def kitap_ekle(self):
        kitap_adi = self.kitap_adi_input.text()
        yazar = self.yazar_input.text()
        if kitap_adi and yazar:
            kitap_id = len(self.kitaplar) + 1
            yeni_kitap = Kitap(kitap_id, kitap_adi, yazar)
            self.kitaplar.append(yeni_kitap)
            self.kitaplari_yukle()
            self.kitap_adi_input.clear()
            self.yazar_input.clear()

    def uye_ekle(self):
        uye_adi = self.uye_adi_input.text()
        uye_soyadi = self.uye_soyadi_input.text()
        if uye_adi and uye_soyadi:
            uye_id = len(self.uyeler) + 1
            yeni_uye = Uye(uye_id, uye_adi, uye_soyadi)
            self.uyeler.append(yeni_uye)
            self.uyeleri_yukle()
            self.uye_adi_input.clear()
            self.uye_soyadi_input.clear()

    def odunc_alma_penceresi_ac(self):
        self.odunc_alma_penceresi = OduncAlmaPenceresi(self.kitaplar, self.uyeler)
        self.odunc_alma_penceresi.exec_()

    def iade_etme_penceresi_ac(self):
        self.iade_etme_penceresi = IadeEtmePenceresi(self.kitaplar, self.uyeler)
        self.iade_etme_penceresi.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    uygulama = KutuphaneUygulamasi()
    uygulama.show()
    sys.exit(app.exec_())
