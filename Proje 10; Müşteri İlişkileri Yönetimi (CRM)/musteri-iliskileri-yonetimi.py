from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, \
    QFormLayout, QDialog, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt  # QtCore modülünden Qt sınıfını import ediyoruz


class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM Uygulaması")

        self.genel_layout = QVBoxLayout()

        self.kaydedilen_bilgiler = []  # Kullanıcı tarafından girilen bilgileri saklamak için liste

        self.liste = QListWidget()
        self.initial_item = QListWidgetItem("Kaydedilecek bilgiler...")
        self.initial_item.setForeground(QColor(128, 128, 128, 128))  # Yarı saydam font rengi
        self.liste.addItem(self.initial_item)
        self.genel_layout.addWidget(self.liste)

        self.musteri_ekle_buton = QPushButton("Müşteri Ekle")
        self.musteri_ekle_buton.clicked.connect(self.musteri_ekle_dialog)

        self.satis_ekle_buton = QPushButton("Satış Ekle")
        self.satis_ekle_buton.clicked.connect(self.satis_ekle_dialog)

        self.destek_talebi_buton = QPushButton("Destek Talebi Oluştur")
        self.destek_talebi_buton.clicked.connect(self.destek_talebi_dialog)

        self.genel_layout.addWidget(self.musteri_ekle_buton)
        self.genel_layout.addWidget(self.satis_ekle_buton)
        self.genel_layout.addWidget(self.destek_talebi_buton)

        merkez_widget = QWidget()
        merkez_widget.setLayout(self.genel_layout)
        self.setCentralWidget(merkez_widget)

    def check_initial_item(self):
        # Eğer başlangıç metni hala listeye ekliyse, ilk veri eklendiğinde onu kaldır
        items = self.liste.findItems("Kaydedilecek bilgiler...", Qt.MatchExactly)
        if items:
            self.liste.takeItem(self.liste.row(items[0]))

    def musteri_ekle_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Müşteri Ekle")
        layout = QFormLayout()

        ad = QLineEdit()
        iletisim = QLineEdit()

        layout.addRow(QLabel("Müşteri Adı:"), ad)
        layout.addRow(QLabel("İletişim Bilgileri:"), iletisim)

        ekle_buton = QPushButton("Ekle")
        ekle_buton.clicked.connect(lambda: self.musteri_ekle(ad.text(), iletisim.text(), dialog))
        layout.addWidget(ekle_buton)

        dialog.setLayout(layout)
        dialog.exec_()

    def musteri_ekle(self, ad, iletisim, dialog):
        self.check_initial_item()
        kayit = f"Müşteri: {ad}, İletişim: {iletisim}"
        self.liste.addItem(kayit)
        self.kaydedilen_bilgiler.append(kayit)
        QMessageBox.information(dialog, "Müşteri Eklendi",
                                f"Müşteri Adı: {ad} ve İletişim Bilgileri başarıyla eklendi.")
        dialog.accept()

    def satis_ekle_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Satış Ekle")
        layout = QFormLayout()

        satis_numarasi = QLineEdit()
        urunler = QLineEdit()

        layout.addRow(QLabel("Satış Numarası:"), satis_numarasi)
        layout.addRow(QLabel("Satılan Ürünler:"), urunler)

        ekle_buton = QPushButton("Ekle")
        ekle_buton.clicked.connect(lambda: self.satis_ekle(satis_numarasi.text(), urunler.text(), dialog))
        layout.addWidget(ekle_buton)

        dialog.setLayout(layout)
        dialog.exec_()

    def satis_ekle(self, satis_numarasi, urunler, dialog):
        self.check_initial_item()
        kayit = f"Satış: {satis_numarasi}, {urunler}"
        self.liste.addItem(kayit)
        self.kaydedilen_bilgiler.append(kayit)
        QMessageBox.information(dialog, "Satış Eklendi",
                                f"Satış Numarası: {satis_numarasi} ve Satılan Ürünler başarıyla eklendi.")
        dialog.accept()

    def destek_talebi_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Destek Talebi Oluştur")
        layout = QFormLayout()

        talep_numarasi = QLineEdit()
        detaylar = QLineEdit()

        layout.addRow(QLabel("Talep Numarası:"), talep_numarasi)
        layout.addRow(QLabel("Talep Detayları:"), detaylar)

        olustur_buton = QPushButton("Oluştur")
        olustur_buton.clicked.connect(
            lambda: self.destek_talebi_olustur(talep_numarasi.text(), detaylar.text(), dialog))
        layout.addWidget(olustur_buton)

        dialog.setLayout(layout)
        dialog.exec_()

    def destek_talebi_olustur(self, talep_numarasi, detaylar, dialog):
        self.check_initial_item()
        kayit = f"Destek Talebi: {talep_numarasi}, {detaylar}"
        self.liste.addItem(kayit)
        self.kaydedilen_bilgiler.append(kayit)
        QMessageBox.information(dialog, "Destek Talebi Oluşturuldu",
                                f"Talep Numarası: {talep_numarasi} ve Talep Detayları başarıyla oluşturuldu.")
        dialog.accept()

    def closeEvent(self, event):
        print("Uygulamadan çıkılıyor. Kaydedilen bilgiler:")
        for bilgi in self.kaydedilen_bilgiler:
            print(bilgi)
        event.accept()


def uygulamayi_baslat():
    app = QApplication([])
    ana_pencere = AnaPencere()
    ana_pencere.show()
    app.exec_()


uygulamayi_baslat()
