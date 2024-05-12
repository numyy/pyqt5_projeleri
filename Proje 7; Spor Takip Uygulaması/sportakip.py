from database import VeriTabani
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QListWidget, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

class Sporcu:
    def __init__(self, ad, soyad, spor_dali, yas):
        self.ad = ad
        self.soyad = soyad
        self.spor_dali = spor_dali
        self.yas = yas
        self.antrenman_programlari = []
        self.ilerleme_yuzdesi = 0
        self.veritabani = VeriTabani()  # Veritabanı nesnesi oluştur
        self.sporcular = self.veritabani.sporcular_getir()
        self.sporcular_list = QListWidget()  # Sporcular listesi için QListWidget nesnesi
        self.sporcular_listesini_guncelle()  # Başlangıçta listeyi doldur

    def sporcular_listesini_guncelle(self):
        self.sporcular_list.clear()
        self.sporcular = self.veritabani.sporcular_getir()
        self.sporcular_list.addItems([f"{ad} {soyad} - {spor_dali} - {yas} - {spor_dali}" for ad, soyad, spor_dali, yas in self.sporcular])

    def program_olustur(self, program_adi, spor_dali, antrenman_suresi):
        program = AntrenmanProgrami(program_adi, spor_dali, antrenman_suresi)
        self.antrenman_programlari.append(program)
        self.veritabani.antrenman_programi_ekle(program_adi, self.ad, self.soyad, spor_dali, antrenman_suresi)
        return program

    def ilerleme_kaydet(self, program, antrenman, ilerleme):
        takip = Takip(self, antrenman, ilerleme)
        program.takip_listesi.append(takip)
        self.veritabani.ilerleme_kaydet(self.ad, self.soyad, antrenman.antrenman_adi, program.program_adi, ilerleme)

    def rapor_al(self, program_adi):
        rapor = ""
        for program in self.antrenman_programlari:
            if program.program_adi == program_adi:
                rapor += str(program) + "\n\nAntrenmanlar:\n"
                if program.antrenmanlar:
                    for antrenman in program.antrenmanlar:
                        rapor += f"- {antrenman.antrenman_adi}\n  Detaylar: {antrenman.detaylar}\n  Süre: {antrenman.sure} saat\n"
                else:
                    rapor += "Bu program için henüz antrenman eklenmemiş.\n"
                rapor += "\nTakip Bilgileri:\n"
                if program.takip_listesi:
                    for takip in program.takip_listesi:
                        rapor += "Antrenman: {0}\nİlerleme: {1}\n".format(
                            takip.antrenman.antrenman_adi, takip.ilerleme_kaydi)
                else:
                    rapor += "Bu program için henüz ilerleme kaydedilmemiş.\n"
                break
        return rapor

    def programlari_getir(self):
        self.imlec.execute(
            "SELECT program_adi, sporcu_ad, sporcu_soyad, spor_dali, antrenman_suresi FROM antrenman_programlari")
        return self.imlec.fetchall()

    def program_bilgileri_getir(self):
        programlar = self.veritabani.programlari_getir()
        program_bilgileri = []
        gorulmus_programlar = set()  # Görülen programları takip etmek için bir set oluşturun
        for program in programlar:
            if program[1] == self.ad and program[2] == self.soyad:
                program_bilgisi = f"{program[0]} - {program[1]} {program[2]} - {program[3]} - {program[4]}"
                if program_bilgisi not in gorulmus_programlar:  # Programa daha önce eklenmemişse ekleyin
                    program_bilgileri.append(program_bilgisi)
                    gorulmus_programlar.add(program_bilgisi)
        return program_bilgileri

    def ilerleme_kaydet_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("İlerleme Kaydet")
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        program_label = QLabel("Program:")
        layout.addWidget(program_label)
        program_combo = QComboBox()
        program_combo.addItems([program.program_adi for program in self.antrenman_programlari])
        layout.addWidget(program_combo)

        antrenman_label = QLabel("Antrenman:")
        layout.addWidget(antrenman_label)
        antrenman_combo = QComboBox()
        layout.addWidget(antrenman_combo)

        ilerleme_label = QLabel("İlerleme:")
        layout.addWidget(ilerleme_label)
        ilerleme_edit = QLineEdit()
        layout.addWidget(ilerleme_edit)

        kaydet_button = QPushButton("Kaydet")
        kaydet_button.clicked.connect(
            lambda: self.ilerleme_kaydet(program_combo.currentText(), antrenman_combo.currentText(),
                                         ilerleme_edit.text()))
        layout.addWidget(kaydet_button)

        dialog.exec_()

    def rapor_goster(self, program_bilgisi, rapor_label):
        program_adi, ad_soyad, spor_dali, antrenman_suresi = program_bilgisi.split(" - ")
        ad, soyad = ad_soyad.split()
        sporcu = self.get_sporcu(ad, soyad)
        for program in sporcu.antrenman_programlari:
            if program.program_adi == program_adi:
                rapor_label.setText(sporcu.rapor_al(program))
                break

class AntrenmanProgrami:
    def __init__(self, program_adi, spor_dali, antrenman_suresi):
        self.program_adi = program_adi
        self.spor_dali = spor_dali
        self.antrenman_suresi = antrenman_suresi
        self.antrenmanlar = []
        self.takip_listesi = []

    def __str__(self):
        return f"Program Adı: {self.program_adi}\nSpor Dalı: {self.spor_dali}\nAntrenman Süresi: {self.antrenman_suresi} saat"

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
        self.veritabani = VeriTabani()
        self.sporcular = self.veritabani.sporcular_getir()  # Veritabanından sporcuları al
        self.setup_ui()
        self.sporcular_listesini_guncelle()  # Başlangıçta listeyi doldur

    def setup_ui(self):
        ana_widget = QWidget()
        self.setCentralWidget(ana_widget)

        v_layout = QVBoxLayout()
        ana_widget.setLayout(v_layout)

        sporcu_bilgileri_label = QLabel("Sporcu Bilgileri")
        v_layout.addWidget(sporcu_bilgileri_label)

        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        self.ad_soyad_line_edit = QLineEdit()
        self.ad_soyad_line_edit.setPlaceholderText("Ad Soyad")
        self.ad_soyad_line_edit.setValidator(QRegExpValidator(QRegExp(r'^[a-zA-Z\s]+$'), self.ad_soyad_line_edit))
        self.ad_soyad_line_edit.textChanged.connect(self.ad_soyad_degistir)
        h_layout.addWidget(self.ad_soyad_line_edit)

        self.yas_line_edit = QLineEdit()
        self.yas_line_edit.setPlaceholderText("Yaş")
        self.yas_line_edit.setValidator(QRegExpValidator(QRegExp(r'^[1-9][0-9]?$|^100$'), self.yas_line_edit))
        self.yas_line_edit.textChanged.connect(self.yas_degistir)
        h_layout.addWidget(self.yas_line_edit)

        self.spor_dali_combo = QComboBox()
        self.spor_dali_combo.addItems(["Futbol", "Basketbol", "Yüzme", "Koşu"])
        h_layout.addWidget(self.spor_dali_combo)

        sporcu_ekle_butonu = QPushButton("Sporcu Ekle")
        sporcu_ekle_butonu.clicked.connect(self.sporcu_ekle)
        h_layout.addWidget(sporcu_ekle_butonu)

        self.sporcular_list = QListWidget()
        v_layout.addWidget(self.sporcular_list)

        self.devam_et_butonu = QPushButton("Devam Et")
        self.devam_et_butonu.clicked.connect(self.degistir_sayfa)
        v_layout.addWidget(self.devam_et_butonu)

    def sporcular_listesini_guncelle(self):
        self.sporcular_list.clear()
        self.sporcular = self.veritabani.sporcular_getir()
        self.sporcular_list.addItems([f"{ad} {soyad} - {yas} - {spor_dali}" for ad, soyad, spor_dali, yas in self.sporcular])

    def sporcu_ekle(self):
        ad_soyad = self.ad_soyad_line_edit.text()
        yas = self.yas_line_edit.text()
        spor_dali = self.spor_dali_combo.currentText()

        if ad_soyad and yas and spor_dali:
            ad_soyad_list = ad_soyad.split()
            if len(ad_soyad_list) < 2:
                QMessageBox.warning(self, "Uyarı", "Lütfen ad ve soyad girin.")
            else:
                ad, soyad = ad_soyad_list
                self.veritabani.sporcu_ekle(ad, soyad, spor_dali, int(yas))
                self.sporcular_listesini_guncelle()  # Listeyi güncelle
                self.ad_soyad_line_edit.clear()
                self.yas_line_edit.clear()

    def degistir_sayfa(self):
        secili_item = self.sporcular_list.currentItem()
        if secili_item:
            secili_sporcu = secili_item.text().split(" - ")
            ad_soyad, yas, spor_dali = secili_sporcu

            self.sporcu_bilgi_penceresi = QDialog(self)
            self.sporcu_bilgi_penceresi.setWindowTitle("Sporcu Bilgileri")
            self.sporcu_bilgi_penceresi.setMinimumSize(400, 300)  # Pencere boyutunu ayarlayın
            layout = QVBoxLayout()
            self.sporcu_bilgi_penceresi.setLayout(layout)

            ad, soyad = ad_soyad.split()  # ad ve soyadı ayır
            ad_soyad_label = QLabel(f"Ad Soyad: {ad} {soyad}")
            ad_soyad_label.setStyleSheet("font-size: 16px;")  # Yazı boyutu
            yas_label = QLabel(f"Yaş: {yas}")
            spor_dali_label = QLabel(f"Spor Dalı: {spor_dali}")

            layout.addWidget(ad_soyad_label)
            layout.addWidget(yas_label)
            layout.addWidget(spor_dali_label)

            # Buton ekleme
            program_olustur_button = QPushButton("Program Oluştur")
            program_olustur_button.clicked.connect(self.program_olustur_dialog)
            layout.addWidget(program_olustur_button)

            rapor_al_button = QPushButton("Rapor Al")
            rapor_al_button.clicked.connect(self.rapor_al_dialog)
            layout.addWidget(rapor_al_button)

            onayla_butonu = QPushButton("Ana Sayfaya Dön")
            onayla_butonu.clicked.connect(self.sporcu_bilgi_penceresi.accept)
            layout.addWidget(onayla_butonu)

            self.sporcu_bilgi_penceresi.show()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir sporcu seçin.")

    def get_sporcu(self, ad, soyad):
        for sporcu in self.sporcular:
            if sporcu[0] == ad and sporcu[1] == soyad:
                return Sporcu(ad, soyad, sporcu[2], sporcu[3])


    def ad_soyad_degistir(self, text):
        if any(char.isdigit() for char in text):
            self.ad_soyad_line_edit.clear()
            QMessageBox.warning(self, "Uyarı", "Lütfen sadece harf girin.")

    def yas_degistir(self, text):
        if text == "":
            return
        if not text.isdigit() or not (1 <= int(text) <= 100):
            self.yas_line_edit.clear()
            QMessageBox.warning(self, "Uyarı", "Lütfen 1-100 arasında bir yaş girin.")

    def sporcu_ekle(self):
        ad_soyad = self.ad_soyad_line_edit.text()
        yas = self.yas_line_edit.text()
        spor_dali = self.spor_dali_combo.currentText()

        if ad_soyad and yas and spor_dali:
            ad_soyad_list = ad_soyad.split()
            if len(ad_soyad_list) < 2:
                QMessageBox.warning(self, "Uyarı", "Lütfen ad ve soyad girin.")
            else:
                ad, soyad = ad_soyad_list
                self.veritabani.sporcu_ekle(ad, soyad, spor_dali, int(yas))
                self.sporcular = self.veritabani.sporcular_getir()
                self.sporcular_list.clear()
                self.sporcular_list.addItems([f"{ad} {soyad} - {yas} - {spor_dali}" for ad, soyad, spor_dali, yas in self.sporcular])
                self.ad_soyad_line_edit.clear()
                self.yas_line_edit.clear()

    def program_olustur_dialog(self):
        secili_item = self.sporcular_list.currentItem()
        if secili_item:
            secili_sporcu = secili_item.text().split(" - ")
            ad_soyad, yas, spor_dali = secili_sporcu
            ad, soyad = ad_soyad.split()
            sporcu = self.get_sporcu(ad, soyad)

            dialog = QDialog(self)
            dialog.setWindowTitle("Program Oluştur")
            layout = QVBoxLayout()
            dialog.setLayout(layout)

            program_adi_label = QLabel("Program Adı:")
            layout.addWidget(program_adi_label)
            program_adi_edit = QLineEdit()
            layout.addWidget(program_adi_edit)

            spor_dali_label = QLabel("Spor Dalı:")
            layout.addWidget(spor_dali_label)
            spor_dali_combo = QComboBox()
            spor_dali_combo.addItems(["Futbol", "Basketbol", "Yüzme", "Koşu"])
            layout.addWidget(spor_dali_combo)

            antrenman_suresi_label = QLabel("Antrenman Süresi (saat):")
            layout.addWidget(antrenman_suresi_label)
            antrenman_suresi_edit = QLineEdit()
            layout.addWidget(antrenman_suresi_edit)

            kaydet_button = QPushButton("Kaydet")
            # Program adının benzersiz olup olmadığını kontrol et
            kaydet_button.clicked.connect(
                lambda: self.program_olustur_kontrol(sporcu, program_adi_edit.text(), spor_dali_combo.currentText(),
                                                     int(antrenman_suresi_edit.text())))
            layout.addWidget(kaydet_button)

            dialog.exec_()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir sporcu seçin.")

    def program_olustur_kontrol(self, sporcu, program_adi, spor_dali, antrenman_suresi):
        programlar = self.veritabani.programlari_getir()
        program_adlari = [program[0] for program in programlar]

        if program_adi in program_adlari:
            QMessageBox.warning(self, "Uyarı",
                                f"{program_adi} adlı bir program zaten mevcut. Lütfen farklı bir ad girin.")
        else:
            self.program_olustur(sporcu, program_adi, spor_dali, antrenman_suresi)

    def rapor_al_dialog(self):
        secili_item = self.sporcular_list.currentItem()
        if secili_item:
            secili_sporcu = secili_item.text().split(" - ")
            ad_soyad, yas, spor_dali = secili_sporcu
            ad, soyad = ad_soyad.split()
            sporcu = self.get_sporcu(ad, soyad)

            dialog = QDialog(self)
            dialog.setWindowTitle("Rapor Göster")
            layout = QVBoxLayout()
            dialog.setLayout(layout)

            program_label = QLabel("Program:")
            layout.addWidget(program_label)
            self.program_combo = QComboBox()
            program_bilgileri = sporcu.program_bilgileri_getir()
            self.program_combo.addItems(program_bilgileri)
            layout.addWidget(self.program_combo)

            self.rapor_label = QLabel("")
            layout.addWidget(self.rapor_label)

            self.program_combo.currentTextChanged.connect(
                lambda: self.rapor_goster(self.program_combo.currentText(), self.rapor_label))

            onayla_butonu = QPushButton("Önceki Sayfaya Dön")
            onayla_butonu.clicked.connect(dialog.accept)
            layout.addWidget(onayla_butonu)

            dialog.exec_()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir sporcu seçin.")



    def program_olustur(self, sporcu, program_adi, spor_dali, antrenman_suresi):
        program = sporcu.program_olustur(program_adi, spor_dali, antrenman_suresi)
        self.veritabani.antrenman_programi_ekle(program_adi, sporcu.ad, sporcu.soyad, spor_dali, antrenman_suresi)
        QMessageBox.information(self, "Bilgi", f"{program_adi} programı başarıyla oluşturuldu.")
        dialog = self.findChild(QDialog)
        if dialog:
            dialog.done(QDialog.Accepted)

    def rapor_goster(self, program_bilgisi, rapor_label):
        program_adi, ad_soyad, spor_dali, antrenman_suresi = program_bilgisi.split(" - ")
        ad, soyad = ad_soyad.split()
        sporcu = self.get_sporcu(ad, soyad)
        rapor = ""
        for program in sporcu.antrenman_programlari:
            if program.program_adi == program_adi:
                rapor = sporcu.rapor_al(program_adi)
                break
        rapor_label.setText(rapor)



if __name__ == "__main__":
    import sys
    from PyQt5 import QtGui, QtCore
    app = QApplication(sys.argv)
    uygulama = AnaUygulama()
    uygulama.show()
    sys.exit(app.exec_())
