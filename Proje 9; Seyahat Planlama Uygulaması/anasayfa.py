from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QListWidget,
    QLabel,
    QLineEdit,
    QInputDialog,
    QMessageBox,
    QCalendarWidget,
    QPlainTextEdit,
    QDialog,
    QDialogButtonBox
)
from PyQt5.QtCore import QRegExp, QDate, Qt
import sys
import re
import datetime
import threading

class BilgiGirisiSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seyahat Planlama Uygulaması")

        # Arayüz elemanlarını oluşturuyor
        ana_layout = QVBoxLayout()

        # İsim ve soyisim input kısmı
        self.isim_soyisim_label = QLabel("İsim ve Soyisim:")
        self.isim_soyisim_girisi = QLineEdit()
        self.isim_soyisim_girisi.textChanged.connect(self.isim_soyisim_kontrol)
        ana_layout.addWidget(self.isim_soyisim_label)
        ana_layout.addWidget(self.isim_soyisim_girisi)

        # TC kimlik numarası input kısmı limitörlü
        self.tc_label = QLabel("TC Kimlik Numarası:")
        self.tc_girisi = QLineEdit()
        self.tc_girisi.setMaxLength(11)
        self.tc_girisi.textChanged.connect(self.tc_kontrol)
        ana_layout.addWidget(self.tc_label)
        ana_layout.addWidget(self.tc_girisi)

        # Ülke seçim ekranı
        self.ulke_label = QLabel("Ülke Seçin:")
        self.ulke_listesi = QListWidget()
        self.ulkeler = ["Türkiye", "İspanya", "Fransa", "İtalya", "Yunanistan", "Portekiz", "Almanya", "İngiltere", "Avusturya", "Hollanda"]
        fiyatlar = [600, 1100, 1300, 1700, 800, 1400, 1500, 2000, 1800, 1100]
        for i in range(len(self.ulkeler)):
            ulke_fiyat = f"{self.ulkeler[i]} - {fiyatlar[i]} $"
            self.ulke_listesi.addItem(ulke_fiyat)
        ana_layout.addWidget(self.ulke_label)
        ana_layout.addWidget(self.ulke_listesi)

        self.ileri_butonu = QPushButton("İleri")
        self.ileri_butonu.clicked.connect(self.otel_sayfasina_git)
        ana_layout.addWidget(self.ileri_butonu)

        self.setLayout(ana_layout)

    def isim_soyisim_kontrol(self, text):
        if not re.match(r'^[a-zA-ZÇĞİÖŞÜçğıöşü\s]+$', text):
            self.isim_soyisim_girisi.setStyleSheet("color: red;")
            QMessageBox.warning(self, "Uyarı", "İsim ve soyisim alanına sadece harf girebilirsiniz.")
        else:
            self.isim_soyisim_girisi.setStyleSheet("")

    def tc_kontrol(self, text):
        if not text.isdigit() or len(text) > 11:
            self.tc_girisi.setStyleSheet("color: red;")
            QMessageBox.warning(self, "Uyarı", "TC kimlik numarası alanına sadece rakam girebilirsiniz ve 11 karakteri geçemez.")
        else:
            self.tc_girisi.setStyleSheet("")

    def otel_sayfasina_git(self):
        isim_soyisim = self.isim_soyisim_girisi.text().strip()
        tc = self.tc_girisi.text().strip()

        if not isim_soyisim:
            QMessageBox.warning(self, "Uyarı", "Lütfen isim ve soyisim giriniz.")
            return

        if not tc:
            QMessageBox.warning(self, "Uyarı", "Lütfen TC kimlik numarası giriniz.")
            return

        if not self.ulke_listesi.currentItem():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir ülke seçiniz.")
            return

        secilen_ulke = self.ulke_listesi.currentItem().text().split(" - ")[0]
        self.otel_sayfasi = OtelSayfasi(secilen_ulke, self.ulkeler, self, isim_soyisim, tc)
        self.otel_sayfasi.show()

    def dosya_kaydet(self, icerik, dosya_ismi):
        try:
            with open(f"{dosya_ismi}.txt", "w", encoding="utf-8") as dosya:
                dosya.write(icerik)
            QMessageBox.information(self, "Bilgi", f"{dosya_ismi}.txt dosyası kaydedildi.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Dosya kaydedilemedi: {str(e)}")

class OtelSayfasi(QWidget):
    def __init__(self, secilen_ulke, ulkeler, ana_pencere, isim_soyisim, tc):
        super().__init__()
        self.ana_pencere = ana_pencere
        self.isim_soyisim = isim_soyisim
        self.tc = tc
        self.setWindowTitle("Otel Seçimi")

        ana_layout = QVBoxLayout()

        self.otel_label = QLabel("Otel Seçin:")
        ana_layout.addWidget(self.otel_label)

        self.otel_listesi = QListWidget()
        self.oteller = {
            "Türkiye": ["Hilton Otel, İstanbul", "Romance Istanbul Hotel", "Divan Cave House Hotel, İstanbul"],
            "İspanya": ["Marbella Club Hotel", "Hotel Arts Barcelona", "Las Colinas Alicante"],
            "Fransa": ["Hôtel Plaza Paris", "Le Bristol Paris", "Hôtel Fouquet's Paris"],
            "İtalya": ["Hotel Hassler Roma", "Aman Venice, Venedik", "Grand Hotel Tremezzo, Como"],
            "Yunanistan": ["Amanzoe, Santorini", "Constance Léopoldo", "The St. Regis, Atina"],
            "Portekiz": ["Six Senses Douro, Douro", "Hotel Tivoli Avenida Liberdade", "Palacio da Foz, Cascais"],
            "Almanya": ["Bayerischer Hof, Münih", "Hotel Adlon Kempinski Berlin", "The Fontenay Hamburg, Hamburg"],
            "İngiltere": ["The Lowry Hotel", "Montcalm Royal London House ", "Corinthia Hotel London"],
            "Avusturya": ["Sacher Hotel Wien, Viyana", "The Ritz-Carlton, Viyana", "Schloss Fuschl Resort, Salzburg"],
            "Hollanda": ["Conservatorium Hotel, Amsterdam", "Hotel Okura Amsterdam", "Andaz Amsterdam Prinsengracht"]
        }
        self.otel_listesi.addItems(self.oteller[secilen_ulke])
        ana_layout.addWidget(self.otel_listesi)

        self.devam_et_butonu = QPushButton("Devam Et")
        self.devam_et_butonu.clicked.connect(self.yeni_pencere_ac)
        ana_layout.addWidget(self.devam_et_butonu)

        self.setLayout(ana_layout)

    def yeni_pencere_ac(self):
        self.yeni_pencere = QDialog(self)
        self.yeni_pencere.setWindowTitle("Seyahat Planı")

        layout = QVBoxLayout()

        # Seçilen otelin ismini göstermek için
        secilen_otel = self.otel_listesi.currentItem().text()
        otel_label = QLabel(f"Seçilen Otel: {secilen_otel}")
        layout.addWidget(otel_label)

        # Takvim oluşturmak için
        self.takvim = QCalendarWidget()
        self.takvim.setGridVisible(True)
        self.takvim.clicked.connect(self.tarih_sec)
        layout.addWidget(self.takvim)

        # Seçilen tarihleri göstermek için
        self.secilen_tarihler_label = QLabel("Seçilen Tarihler:")
        layout.addWidget(self.secilen_tarihler_label)
        self.secilen_tarihler_alani = QPlainTextEdit()
        self.secilen_tarihler_alani.setReadOnly(True)
        layout.addWidget(self.secilen_tarihler_alani)

        # Oda tipi seçimi için
        self.oda_tipi_label = QLabel("Oda Tipi:")
        layout.addWidget(self.oda_tipi_label)
        self.oda_tipi_listesi = QListWidget()
        self.oda_tipleri = ["Standart Oda", "Suit Oda", "Aile Odası"]
        self.oda_tipi_listesi.addItems(self.oda_tipleri)
        self.oda_tipi_listesi.currentItemChanged.connect(self.oda_tipi_secildi)
        layout.addWidget(self.oda_tipi_listesi)

        # Ücret göstergesi için
        self.ucret_label = QLabel("Ücret: 0 TL")
        layout.addWidget(self.ucret_label)

        self.yeni_pencere.setLayout(layout)
        self.yeni_pencere.show()

        self.secilen_tarihler = []
        self.secilen_oda_tipi = None

    def tarih_sec(self, date):
        secilen_tarih = date.toString("dd.MM.yyyy")
        if secilen_tarih not in self.secilen_tarihler:
            if len(self.secilen_tarihler) < 2:
                self.secilen_tarihler.append(secilen_tarih)
                self.secilen_tarihler_alani.setPlainText("\n".join(self.secilen_tarihler))
                if len(self.secilen_tarihler) == 2:
                    self.ucret_hesapla()
            else:
                QMessageBox.warning(self, "Uyarı", "Sadece iki tarih seçebilirsiniz.")
        else:
            self.secilen_tarihler.remove(secilen_tarih)
            self.secilen_tarihler_alani.setPlainText("\n".join(self.secilen_tarihler))
            self.ucret_label.setText("Ücret: 0 TL")

    def gun_farki(self):
        format_str = "dd.MM.yyyy"
        baslangic = datetime.strptime(self.secilen_tarihler[0], format_str)
        bitis = datetime.strptime(self.secilen_tarihler[1], format_str)
        return (bitis - baslangic).days + 1

    def oda_tipi_secildi(self, item):
        self.secilen_oda_tipi = item.text()
        if len(self.secilen_tarihler) == 2:
            self.ucret_hesapla()

    def ucret_hesapla(self):
        if self.secilen_oda_tipi is not None:
            gun_sayisi = self.gun_farki()
            if self.secilen_oda_tipi == "Standart Oda":
                ucret = gun_sayisi * 80
            elif self.secilen_oda_tipi == "Suit Oda":
                ucret = gun_sayisi * 140
            elif self.secilen_oda_tipi == "Aile Odası":
                ucret = gun_sayisi * 280
            self.ucret_label.setText(f"Ücret: {ucret} Dolar")

            # Ücret hesaplandıktan sonra bir onay penceresi gösteriyoruz
            reply = QMessageBox.question(self, 'Onay',
                                         f'Seçilen oda tipi: {self.secilen_oda_tipi}\nÜcret: {ucret} TL\n\nOnaylıyor musunuz?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # Kullanıcı onayladıysa, rezervasyon işlemini gerçekleştirin
                print("Rezervasyon tamamlandı.")
                # İsterseniz, başka işlemler yapabilirsiniz
            else:
                # Kullanıcı iptal ettiyse, hiçbir şey yapmayın
                pass

if __name__ == "__main__":
    app = QApplication([])
    bilgi_girisi_sayfasi = BilgiGirisiSayfasi()
    bilgi_girisi_sayfasi.show()
    app.exec_()
