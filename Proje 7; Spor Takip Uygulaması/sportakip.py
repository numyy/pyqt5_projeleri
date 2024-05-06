import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QListWidget, QHBoxLayout, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator

class Sporcu:
    def __init__(self, ad, soyad, spor_dali, yas):
        self.ad = ad
        self.soyad = soyad
        self.spor_dali = spor_dali
        self.yas = yas
        self.antrenman_programlari = []
        self.ilerleme_yuzdesi = 0

    def program_olustur(self, program_adi):
        program = AntrenmanProgrami(program_adi)
        self.antrenman_programlari.append(program)
        return program

    def ilerleme_kaydet(self, program, antrenman, ilerleme):
        takip = Takip(self, antrenman, ilerleme)
        program.takip_listesi.append(takip)

    def rapor_al(self, program):
        rapor = "Sporcu: {0} {1}\nSpor Dalı: {2}\nAntrenman Programı: {3}\n\nTakip Bilgileri:\n".format(
            self.ad, self.soyad, self.spor_dali, program.program_adi)
        for takip in program.takip_listesi:
            rapor += "Antrenman: {0}\nİlerleme: {1}\n".format(
                takip.antrenman.antrenman_adi, takip.ilerleme_kaydi)
        return rapor


class AntrenmanProgrami:
    def __init__(self, program_adi):
        self.program_adi = program_adi
        self.antrenmanlar = []
        self.takip_listesi = []

    def antrenman_ekle(self, antrenman_adi, detaylar, sure):
        antrenman = Antrenman(antrenman_adi, detaylar, sure)
        self.antrenmanlar.append(antrenman)

    def antrenman_guncelle(self, antrenman, yeni_detaylar, yeni_sure):
        antrenman.detaylar = yeni_detaylar
        antrenman.sure = yeni_sure

    def antrenman_sil(self, antrenman):
        self.antrenmanlar.remove(antrenman)


class Antrenman:
    def __init__(self, antrenman_adi, detaylar, sure):
        self.antrenman_adi = antrenman_adi
        self.detaylar = detaylar
        self.sure = sure


class Takip:
    def __init__(self, sporcu, antrenman, ilerleme_kaydi):
        self.sporcu = sporcu
        self.antrenman = antrenman
        self.ilerleme_kaydi = ilerleme_kaydi


class AnaUygulama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spor Takip Uygulaması")
        self.sporcular = {}
        self.setup_ui()

    def setup_ui(self):
        # Ana widget
        ana_widget = QWidget()
        self.setCentralWidget(ana_widget)

        # Dikey layout
        v_layout = QVBoxLayout()
        ana_widget.setLayout(v_layout)

        # Sporcu bilgileri
        sporcu_bilgileri_label = QLabel("Sporcu Bilgileri")
        v_layout.addWidget(sporcu_bilgileri_label)

        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        # Ad ve Soyad
        self.ad_soyad_line_edit = QLineEdit()
        self.ad_soyad_line_edit.setPlaceholderText("Ad Soyad")
        self.ad_soyad_line_edit.setValidator(QRegExpValidator(QRegExp(r'^[a-zA-Z\s]+$'), self.ad_soyad_line_edit))
        self.ad_soyad_line_edit.textChanged.connect(self.ad_soyad_degistir)
        h_layout.addWidget(self.ad_soyad_line_edit)

        # Yaş
        self.yas_line_edit = QLineEdit()
        self.yas_line_edit.setPlaceholderText("Yaş")
        self.yas_line_edit.setValidator(QRegExpValidator(QRegExp(r'^[1-9][0-9]?$|^100$'), self.yas_line_edit))
        self.yas_line_edit.textChanged.connect(self.yas_degistir)
        h_layout.addWidget(self.yas_line_edit)

        # Spor Dalı
        self.spor_dali_combo = QComboBox()
        self.spor_dali_combo.addItems(["Futbol", "Basketbol", "Yüzme", "Koşu"])
        h_layout.addWidget(self.spor_dali_combo)

        # Sporcu Ekle Butonu
        sporcu_ekle_butonu = QPushButton("Sporcu Ekle")
        sporcu_ekle_butonu.clicked.connect(self.sporcu_ekle)
        h_layout.addWidget(sporcu_ekle_butonu)

        # Sporcular Listesi
        self.sporcular_list = QListWidget()
        v_layout.addWidget(self.sporcular_list)

        # Devam Et Butonu
        self.devam_et_butonu = QPushButton("Devam Et")
        self.devam_et_butonu.clicked.connect(self.degistir_sayfa)
        v_layout.addWidget(self.devam_et_butonu)

        # Sayfa Görüntüleme
        self.stacked_widget = QStackedWidget()
        v_layout.addWidget(self.stacked_widget)

        # İlk Sayfa (Sporcu Ekleme)
        ilk_sayfa = QWidget()
        ilk_sayfa_layout = QVBoxLayout()
        ilk_sayfa.setLayout(ilk_sayfa_layout)

        self.stacked_widget.addWidget(ilk_sayfa)

        # İkinci Sayfa (Sporcuların Gösterimi)
        ikinci_sayfa = QWidget()
        ikinci_sayfa_layout = QVBoxLayout()
        ikinci_sayfa.setLayout(ikinci_sayfa_layout)

        self.sporcular_listesi = QListWidget()
        ikinci_sayfa_layout.addWidget(self.sporcular_listesi)

        self.stacked_widget.addWidget(ikinci_sayfa)

    def ad_soyad_degistir(self, text):
        if any(char.isdigit() for char in text):
            self.ad_soyad_line_edit.clear()
            QMessageBox.warning(self, "Uyarı", "Lütfen sadece harf girin.")

    def yas_degistir(self, text):
        if not text.isdigit() or not (1 <= int(text) <= 100):
            self.yas_line_edit.clear()
            QMessageBox.warning(self, "Uyarı", "Lütfen 1-100 arasında bir yaş girin.")

    def sporcu_ekle(self):
        ad_soyad = self.ad_soyad_line_edit.text()
        yas = self.yas_line_edit.text()
        spor_dali = self.spor_dali_combo.currentText()

        if ad_soyad and yas and spor_dali:
            ad, soyad = ad_soyad.split()
            sporcu = Sporcu(ad, soyad, spor_dali, int(yas))
            self.sporcular["{0} {1}".format(ad, soyad)] = sporcu
            self.sporcular_list.addItem("{0} {1} - {2} - {3}".format(ad, soyad, spor_dali, yas))
            self.ad_soyad_line_edit.clear()
            self.yas_line_edit.clear()

    def program_olustur(self):
        secili_sporcu_adi = self.sporcular_list.currentItem().text().split(" - ")[0]
        sporcu = self.sporcular[secili_sporcu_adi]
        program_adi = self.program_adi_line_edit.text()

        if program_adi:
            program = sporcu.program_olustur(program_adi)
            self.program_adi_line_edit.clear()
            # Burası antrenman ekleme, güncelleme, silme ve ilerleme kaydı için geliştirilecek

    # Diğer metodlar...

if __name__ == "__main__":
    import sys
    from PyQt5 import QtGui, QtCore
    app = QApplication(sys.argv)
    uygulama = AnaUygulama()
    uygulama.show()
    sys.exit(app.exec_())