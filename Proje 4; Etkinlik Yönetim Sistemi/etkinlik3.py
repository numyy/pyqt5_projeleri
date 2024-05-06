from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QMessageBox, QComboBox, QHeaderView
import sys

class Etkinlik:
    def __init__(self, etkinlik_adi, etkinlik_tarihi, etkinlik_yeri, etkinlik_aciklamasi, kontenjan, bilet_fiyati):
        self.etkinlik_adi = etkinlik_adi
        self.etkinlik_tarihi = etkinlik_tarihi
        self.etkinlik_yeri = etkinlik_yeri
        self.etkinlik_aciklamasi = etkinlik_aciklamasi
        self.kontenjan = kontenjan
        self.kalan_kontenjan = kontenjan
        self.bilet_fiyati = bilet_fiyati
        self.biletler = []

    def guncel_kontenjan(self):
        self.kalan_kontenjan = self.kontenjan - len(self.biletler)

class Katilimci:
    def __init__(self, ad, soyad, email, telefon):
        self.ad = ad
        self.soyad = soyad
        self.email = email
        self.telefon = telefon

    def bilet_satin_al(self, etkinlik, bilet_sayisi):
        if etkinlik.kalan_kontenjan >= bilet_sayisi:
            for _ in range(bilet_sayisi):
                bilet = Bilet(len(etkinlik.biletler) + 1, etkinlik, self, etkinlik.etkinlik_tarihi,
                              etkinlik.bilet_fiyati)
                etkinlik.biletler.append(bilet)
            etkinlik.kalan_kontenjan -= bilet_sayisi
            print(
                f"{self.ad} {self.soyad} '{etkinlik.etkinlik_adi}' etkinliği için {bilet_sayisi} adet bilet satın aldı.")
            return True
        else:
            print(f"Üzgünüz, '{etkinlik.etkinlik_adi}' etkinliği için yeterli kontenjan bulunmuyor.")
            return False

class Bilet:
    def __init__(self, bilet_no, etkinlik, katilimci, satis_tarihi, ucret):
        self.bilet_no = bilet_no
        self.etkinlik = etkinlik
        self.katilimci = katilimci
        self.satis_tarihi = satis_tarihi
        self.ucret = ucret

class EtkinlikYonetimSistemi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.etkinlikler = []
        self.katilimcilar = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Etkinlik Yönetim Sistemi")
        self.setGeometry(100, 100, 800, 600)
        # Ana menü
        ana_menu_widget = QWidget()
        layout = QVBoxLayout()

        etkinlik_olustur_button = QPushButton("Etkinlik Oluştur")
        etkinlik_olustur_button.clicked.connect(self.etkinlik_olustur_penceresi)
        layout.addWidget(etkinlik_olustur_button)

        etkinlik_duzenle_button = QPushButton("Etkinlik Düzenle")
        etkinlik_duzenle_button.clicked.connect(self.etkinlik_duzenle_penceresi)
        layout.addWidget(etkinlik_duzenle_button)

        etkinlik_sil_button = QPushButton("Etkinlik Sil")
        etkinlik_sil_button.clicked.connect(self.etkinlik_sil)
        layout.addWidget(etkinlik_sil_button)

        bilet_satin_al_button = QPushButton("Bilet Satın Al")
        bilet_satin_al_button.clicked.connect(self.bilet_satin_al_penceresi)
        layout.addWidget(bilet_satin_al_button)

        self.etkinlik_tablosu = QTableWidget()
        self.etkinlik_tablosu.setColumnCount(7)  # Sütun sayısını 7'ye çıkarıyoruz
        self.etkinlik_tablosu.setHorizontalHeaderLabels(
            ["Etkinlik Adı", "Tarih", "Yer", "Kontenjan", "Satılan Bilet", "Bilet Fiyatı", "Kalan Kontenjan"])
        self.etkinlik_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.etkinlik_tablosu)

        ana_menu_widget.setLayout(layout)
        self.setCentralWidget(ana_menu_widget)

        self.etkinlik_listesini_guncelle()

    def etkinlik_olustur_penceresi(self):
        etkinlik_olustur_penceresi = QDialog()
        etkinlik_olustur_penceresi.setWindowTitle("Etkinlik Oluştur")
        layout = QFormLayout()

        etkinlik_adi_input = QLineEdit()
        etkinlik_tarihi_input = QDateEdit()
        etkinlik_yeri_input = QLineEdit()
        etkinlik_aciklamasi_input = QLineEdit()
        kontenjan_input = QLineEdit()
        bilet_fiyati_input = QLineEdit()

        layout.addRow("Etkinlik Adı:", etkinlik_adi_input)
        layout.addRow("Etkinlik Tarihi:", etkinlik_tarihi_input)
        layout.addRow("Etkinlik Yeri:", etkinlik_yeri_input)
        layout.addRow("Etkinlik Açıklaması:", etkinlik_aciklamasi_input)
        layout.addRow("Kontenjan:", kontenjan_input)
        layout.addRow("Bilet Fiyatı:", bilet_fiyati_input)

        olustur_button = QPushButton("Oluştur")
        olustur_button.clicked.connect(lambda: self.etkinlik_olustur(
            etkinlik_adi_input.text(),
            etkinlik_tarihi_input.date().toPyDate(),
            etkinlik_yeri_input.text(),
            etkinlik_aciklamasi_input.text(),
            int(kontenjan_input.text()),
            float(bilet_fiyati_input.text())
        ))
        layout.addWidget(olustur_button)

        etkinlik_olustur_penceresi.setLayout(layout)
        etkinlik_olustur_penceresi.exec_()

    def etkinlik_olustur(self, etkinlik_adi, etkinlik_tarihi, etkinlik_yeri, etkinlik_aciklamasi, kontenjan, bilet_fiyati):
        yeni_etkinlik = Etkinlik(etkinlik_adi, etkinlik_tarihi, etkinlik_yeri, etkinlik_aciklamasi, kontenjan, bilet_fiyati)
        self.etkinlikler.append(yeni_etkinlik)
        self.etkinlik_listesini_guncelle()
        QMessageBox.information(self, "Etkinlik Oluşturuldu", f"Etkinlik '{etkinlik_adi}' başarıyla oluşturuldu.")

    def etkinlik_duzenle_penceresi(self):
        etkinlik_duzenle_penceresi = QDialog()
        etkinlik_duzenle_penceresi.setWindowTitle("Etkinlik Düzenle")
        layout = QFormLayout()

        etkinlik_secimi = QComboBox()
        etkinlik_secimi.addItems([etkinlik.etkinlik_adi for etkinlik in self.etkinlikler])
        layout.addRow("Etkinlik Seçimi:", etkinlik_secimi)

        etkinlik_adi_input = QLineEdit()
        etkinlik_tarihi_input = QDateEdit()
        etkinlik_yeri_input = QLineEdit()
        etkinlik_aciklamasi_input = QLineEdit()
        kontenjan_input = QLineEdit()
        bilet_fiyati_input = QLineEdit()

        layout.addRow("Etkinlik Adı:", etkinlik_adi_input)
        layout.addRow("Etkinlik Tarihi:", etkinlik_tarihi_input)
        layout.addRow("Etkinlik Yeri:", etkinlik_yeri_input)
        layout.addRow("Etkinlik Açıklaması:", etkinlik_aciklamasi_input)
        layout.addRow("Kontenjan:", kontenjan_input)
        layout.addRow("Bilet Fiyatı:", bilet_fiyati_input)

        def etkinlik_bilgilerini_yukle():
            secili_etkinlik_index = etkinlik_secimi.currentIndex()
            if secili_etkinlik_index != -1:
                secili_etkinlik = self.etkinlikler[secili_etkinlik_index]
                etkinlik_adi_input.setText(secili_etkinlik.etkinlik_adi)
                etkinlik_tarihi_input.setDate(secili_etkinlik.etkinlik_tarihi)
                etkinlik_yeri_input.setText(secili_etkinlik.etkinlik_yeri)
                etkinlik_aciklamasi_input.setText(secili_etkinlik.etkinlik_aciklamasi)
                kontenjan_input.setText(str(secili_etkinlik.kontenjan))
                bilet_fiyati_input.setText(str(secili_etkinlik.bilet_fiyati))

        etkinlik_secimi.currentIndexChanged.connect(etkinlik_bilgilerini_yukle)

        duzenle_button = QPushButton("Düzenle")
        duzenle_button.clicked.connect(lambda: self.etkinlik_duzenle(
            etkinlik_secimi.currentIndex(),
            etkinlik_adi_input.text(),
            etkinlik_tarihi_input.date().toPyDate(),
            etkinlik_yeri_input.text(),
            etkinlik_aciklamasi_input.text(),
            int(kontenjan_input.text()),
            float(bilet_fiyati_input.text())
        ))
        layout.addWidget(duzenle_button)

        etkinlik_duzenle_penceresi.setLayout(layout)
        etkinlik_duzenle_penceresi.exec_()

    def etkinlik_duzenle(self, etkinlik_index, yeni_etkinlik_adi, yeni_etkinlik_tarihi, yeni_etkinlik_yeri,
                         yeni_etkinlik_aciklamasi, yeni_kontenjan, yeni_bilet_fiyati):
        try:
            etkinlik = self.etkinlikler[etkinlik_index]
            etkinlik.etkinlik_adi = yeni_etkinlik_adi
            etkinlik.etkinlik_tarihi = yeni_etkinlik_tarihi
            etkinlik.etkinlik_yeri = yeni_etkinlik_yeri
            etkinlik.etkinlik_aciklamasi = yeni_etkinlik_aciklamasi
            etkinlik.kontenjan = yeni_kontenjan
            etkinlik.bilet_fiyati = yeni_bilet_fiyati
            etkinlik.guncel_kontenjan()  # Kalan kontenjani güncelle
            self.etkinlik_listesini_guncelle()
            QMessageBox.information(self, "Etkinlik Düzenlendi",
                                    f"Etkinlik '{yeni_etkinlik_adi}' başarıyla düzenlendi.")
        except IndexError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir etkinlik seçin.")

    def etkinlik_sil(self):
        etkinlik_sil_penceresi = QDialog()
        etkinlik_sil_penceresi.setWindowTitle("Etkinlik Sil")
        layout = QFormLayout()

        etkinlik_secimi = QComboBox()
        etkinlik_secimi.addItems([etkinlik.etkinlik_adi for etkinlik in self.etkinlikler])
        layout.addRow("Etkinlik Seçimi:", etkinlik_secimi)

        sil_button = QPushButton("Sil")
        sil_button.clicked.connect(lambda: self.etkinlik_sil_islemi(etkinlik_secimi.currentIndex()))
        layout.addWidget(sil_button)

        etkinlik_sil_penceresi.setLayout(layout)
        etkinlik_sil_penceresi.exec_()

    def etkinlik_sil_islemi(self, etkinlik_index):
        try:
            etkinlik = self.etkinlikler[etkinlik_index]
            self.etkinlikler.remove(etkinlik)
            self.etkinlik_listesini_guncelle()
            QMessageBox.information(self, "Etkinlik Silindi", f"Etkinlik '{etkinlik.etkinlik_adi}' başarıyla silindi.")
        except IndexError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir etkinlik seçin.")

    def bilet_satin_al_penceresi(self):
        bilet_satin_al_penceresi = QDialog()
        bilet_satin_al_penceresi.setWindowTitle("Bilet Satın Al")
        layout = QFormLayout()

        etkinlik_secimi = QComboBox()
        etkinlik_secimi.addItems([etkinlik.etkinlik_adi for etkinlik in self.etkinlikler])
        layout.addRow("Etkinlik Seçimi:", etkinlik_secimi)

        katilimci_ad_input = QLineEdit()
        katilimci_soyad_input = QLineEdit()
        katilimci_email_input = QLineEdit()
        katilimci_telefon_input = QLineEdit()
        layout.addRow("Katılımcı Adı:", katilimci_ad_input)
        layout.addRow("Katılımcı Soyadı:", katilimci_soyad_input)
        layout.addRow("Katılımcı E-posta:", katilimci_email_input)
        layout.addRow("Katılımcı Telefon:", katilimci_telefon_input)

        bilet_sayisi_input = QLineEdit()
        layout.addRow("Bilet Sayısı:", bilet_sayisi_input)

        satin_al_button = QPushButton("Satın Al")
        satin_al_button.clicked.connect(lambda: self.bilet_satin_al(
            etkinlik_secimi.currentIndex(),
            katilimci_ad_input.text(),
            katilimci_soyad_input.text(),
            katilimci_email_input.text(),
            katilimci_telefon_input.text(),
            int(bilet_sayisi_input.text())
        ))
        layout.addWidget(satin_al_button)

        bilet_satin_al_penceresi.setLayout(layout)
        bilet_satin_al_penceresi.exec_()

    def bilet_satin_al(self, etkinlik_index, katilimci_ad, katilimci_soyad, katilimci_email, katilimci_telefon,
                       bilet_sayisi):
        try:
            etkinlik = self.etkinlikler[etkinlik_index]
            katilimci = Katilimci(katilimci_ad, katilimci_soyad, katilimci_email, katilimci_telefon)
            self.katilimcilar.append(katilimci)
            if katilimci.bilet_satin_al(etkinlik, bilet_sayisi):
                self.etkinlik_listesini_guncelle()
                QMessageBox.information(self, "Bilet Satın Alındı",
                                        f"{katilimci_ad} {katilimci_soyad} için {bilet_sayisi} adet bilet satın alındı.")
        except IndexError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir etkinlik seçin.")

    def etkinlik_listesini_guncelle(self):
        self.etkinlik_tablosu.setRowCount(len(self.etkinlikler))
        for i, etkinlik in enumerate(self.etkinlikler):
            etkinlik.guncel_kontenjan()  # Kalan kontenjani güncelle
            self.etkinlik_tablosu.setItem(i, 0, QTableWidgetItem(etkinlik.etkinlik_adi))
            self.etkinlik_tablosu.setItem(i, 1, QTableWidgetItem(etkinlik.etkinlik_tarihi.strftime("%d/%m/%Y")))
            self.etkinlik_tablosu.setItem(i, 2, QTableWidgetItem(etkinlik.etkinlik_yeri))
            self.etkinlik_tablosu.setItem(i, 3, QTableWidgetItem(str(etkinlik.kontenjan)))
            self.etkinlik_tablosu.setItem(i, 4, QTableWidgetItem(str(len(etkinlik.biletler))))
            self.etkinlik_tablosu.setItem(i, 5, QTableWidgetItem(str(etkinlik.bilet_fiyati)))
            self.etkinlik_tablosu.setItem(i, 6, QTableWidgetItem(str(etkinlik.kalan_kontenjan)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    etkinlik_yonetim_sistemi = EtkinlikYonetimSistemi()
    etkinlik_yonetim_sistemi.show()
    sys.exit(app.exec_())