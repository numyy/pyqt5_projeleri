from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLabel, QLineEdit, QInputDialog, QMessageBox, QCalendarWidget
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QDate, Qt
import sys
import re

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
        fiyatlar = [1000, 2000, 2500, 2000, 1500, 2200, 2800, 3000, 2700, 2900]
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
        self.otel_sayfasi = OtelSayfasi(secilen_ulke, self.ulkeler)
        self.otel_sayfasi.show()
        self.close()

class OtelSayfasi(QWidget):
    def __init__(self, secilen_ulke, ulkeler):
        super().__init__()
        self.setWindowTitle("Otel Seçimi")

        # Arayüz elemanlarını oluşturuyor
        ana_layout = QVBoxLayout()

        self.otel_label = QLabel("Otel Seçin:")
        ana_layout.addWidget(self.otel_label)

        self.otel_listesi = QListWidget()
        self.oteller = {
            "Türkiye": ["Hilton Otel", "Romance Istanbul Hotel", "Divan Cave House Hotel"],
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

        self.kaydet_butonu = QPushButton("Kaydet")
        self.kaydet_butonu.clicked.connect(self.secimi_kaydet)
        ana_layout.addWidget(self.kaydet_butonu)

        self.setLayout(ana_layout)

    def secimi_kaydet(self):
        secilen_otel = self.otel_listesi.currentItem().text()
        bilgiler = (
            f"İsim Soyisim: {self.parent().isim_soyisim_girisi.text()}\n"
            f"TC: {self.parent().tc_girisi.text()}\n"
            f"Seçilen Ülke: {self.parent().ulke_listesi.currentItem().text().split(' - ')[0]}\n"
            f"Seçilen Otel: {secilen_otel}"
        )
        mesaj = QMessageBox()
        mesaj.setWindowTitle("Seçimler")
        mesaj.setText(bilgiler)
        mesaj.setInformativeText("Bilgiler kaydedilsin mi?")
        mesaj.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mesaj.setDefaultButton(QMessageBox.Ok)
        cevap = mesaj.exec_()

        if cevap == QMessageBox.Ok:
            QMessageBox.information(self, "Bilgi", "Bilgiler kaydedildi.")
            self.close()

if __name__ == "__main__":
    app = QApplication([])
    bilgi_girisi_sayfasi = BilgiGirisiSayfasi()
    bilgi_girisi_sayfasi.show()
    app.exec_()