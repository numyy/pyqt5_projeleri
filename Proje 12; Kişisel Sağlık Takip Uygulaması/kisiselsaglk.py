import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QMessageBox, QInputDialog, QDialog, QTextEdit, QSpinBox
from PyQt5.QtCore import Qt

class KisiProfili:
    def __init__(self, ad, soyad, yas, cinsiyet, boy, kilo):
        self.ad = ad
        self.soyad = soyad
        self.yas = yas
        self.cinsiyet = cinsiyet
        self.boy = boy
        self.kilo = kilo
        self.vke = self.vke_hesapla()
        self.egzersizler = []

    def vke_hesapla(self):
        boy_metre = self.boy / 100
        vke = self.kilo / (boy_metre ** 2)
        return vke

    def egzersiz_ekle(self, egzersiz):
        self.egzersizler.append(egzersiz)

class SaglikTakipUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kişisel Sağlık Takip Uygulaması")
        self.setMinimumSize(800, 600)

        self.kullanici_profilleri = []

        # Widget'lar oluşturulur
        self.ad_label = QLabel("Ad:")
        self.ad_input = QLineEdit()
        self.soyad_label = QLabel("Soyad:")
        self.soyad_input = QLineEdit()
        self.yas_label = QLabel("Yaş:")
        self.yas_input = QLineEdit()
        self.cinsiyet_label = QLabel("Cinsiyet:")
        self.cinsiyet_input = QComboBox()
        self.cinsiyet_input.addItems(["Erkek", "Kadın", "Diğer"])
        self.boy_label = QLabel("Boy (cm):")
        self.boy_input = QLineEdit()
        self.kilo_label = QLabel("Kilo (kg):")
        self.kilo_input = QLineEdit()

        self.kullanici_profilleri_tablosu = QTableWidget()
        self.kullanici_profilleri_tablosu.setColumnCount(7)
        self.kullanici_profilleri_tablosu.setHorizontalHeaderLabels(["Ad", "Soyad", "Yaş", "Cinsiyet", "Boy", "Kilo", "Egzersizler"])
        self.kullanici_profilleri_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.vke_hesapla_butonu = QPushButton("Vücut Kitle Endeksi Hesapla")
        self.vke_hesapla_butonu.clicked.connect(self.vke_hesapla)

        self.egzersiz_ekle_butonu = QPushButton("Egzersiz Ekle")
        self.egzersiz_ekle_butonu.clicked.connect(self.egzersiz_ekle)

        self.kullanici_ekle_butonu = QPushButton("Kullanıcı Ekle")
        self.kullanici_ekle_butonu.clicked.connect(self.kullanici_profili_olustur)

        self.egzersizleri_goster_butonu = QPushButton("Egzersizleri Göster")
        self.egzersizleri_goster_butonu.clicked.connect(self.egzersizleri_goster)

        # Layout oluşturulur
        kullanici_bilgileri_layout = QVBoxLayout()
        kullanici_bilgileri_layout.addWidget(self.ad_label)
        kullanici_bilgileri_layout.addWidget(self.ad_input)
        kullanici_bilgileri_layout.addWidget(self.soyad_label)
        kullanici_bilgileri_layout.addWidget(self.soyad_input)
        kullanici_bilgileri_layout.addWidget(self.yas_label)
        kullanici_bilgileri_layout.addWidget(self.yas_input)
        kullanici_bilgileri_layout.addWidget(self.cinsiyet_label)
        kullanici_bilgileri_layout.addWidget(self.cinsiyet_input)
        kullanici_bilgileri_layout.addWidget(self.boy_label)
        kullanici_bilgileri_layout.addWidget(self.boy_input)
        kullanici_bilgileri_layout.addWidget(self.kilo_label)
        kullanici_bilgileri_layout.addWidget(self.kilo_input)
        kullanici_bilgileri_layout.addWidget(self.kullanici_ekle_butonu)

        tablo_layout = QVBoxLayout()
        tablo_layout.addWidget(self.kullanici_profilleri_tablosu)

        buton_layout = QHBoxLayout()
        buton_layout.addWidget(self.vke_hesapla_butonu)
        buton_layout.addWidget(self.egzersiz_ekle_butonu)
        buton_layout.addWidget(self.egzersizleri_goster_butonu)

        ana_layout = QVBoxLayout()
        ana_layout.addLayout(kullanici_bilgileri_layout)
        ana_layout.addLayout(tablo_layout)
        ana_layout.addLayout(buton_layout)

        merkez_widget = QWidget()
        merkez_widget.setLayout(ana_layout)
        self.setCentralWidget(merkez_widget)

    def kullanici_profili_olustur(self):
        ad = self.ad_input.text()
        soyad = self.soyad_input.text()
        yas = self.yas_input.text()
        cinsiyet = self.cinsiyet_input.currentText()
        boy = self.boy_input.text()
        kilo = self.kilo_input.text()

        if not ad or not soyad or not yas or not boy or not kilo:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        try:
            yas = int(yas)
            boy = int(boy)
            kilo = int(kilo)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Geçersiz yaş, boy veya kilo formatı.")
            return

        profil = KisiProfili(ad, soyad, yas, cinsiyet, boy, kilo)
        self.kullanici_profilleri.append(profil)

        satir_sayisi = self.kullanici_profilleri_tablosu.rowCount()
        self.kullanici_profilleri_tablosu.insertRow(satir_sayisi)
        self.kullanici_profilleri_tablosu.setItem(satir_sayisi, 0, QTableWidgetItem(profil.ad))
        self.kullanici_profilleri_tablosu.setItem(satir_sayisi, 1, QTableWidgetItem(profil.soyad))
        self.kullanici_profilleri_tablosu.setItem(satir_sayisi, 2, QTableWidgetItem(str(profil.yas)))
        self.kullanici_profilleri_tablosu.setItem(satir_sayisi, 3, QTableWidgetItem(profil.cinsiyet))
        self.kullanici_profilleri_tablosu.setItem(satir_sayisi, 4, QTableWidgetItem(str(profil.boy)))
        self.kullanici_profilleri_tablosu.setItem(satir_sayisi, 5, QTableWidgetItem(str(profil.kilo)))
        self.kullanici_profilleri_tablosu.setItem(satir_sayisi, 6, QTableWidgetItem(
            ", ".join([egzersiz["ad"] for egzersiz in profil.egzersizler])))

        self.ad_input.clear()
        self.soyad_input.clear()
        self.yas_input.clear()
        self.boy_input.clear()
        self.kilo_input.clear()

        QMessageBox.information(self, "Başarılı", "Kullanıcı profili başarıyla oluşturuldu.")

    def vke_hesapla(self):
        secili_satir = self.kullanici_profilleri_tablosu.currentRow()
        if secili_satir == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kullanıcı profili seçin.")
            return

        profil = self.kullanici_profilleri[secili_satir]
        vke = profil.vke
        QMessageBox.information(self, "Vücut Kitle Endeksi",
                                f"{profil.ad} {profil.soyad}'ın Vücut Kitle Endeksi: {vke:.2f}")

    def egzersiz_ekle(self):
        secili_satir = self.kullanici_profilleri_tablosu.currentRow()
        if secili_satir == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kullanıcı profili seçin.")
            return

        profil = self.kullanici_profilleri[secili_satir]

        egzersiz_dialog = QDialog(self)
        egzersiz_dialog.setWindowTitle("Egzersiz Ekle")

        layout = QVBoxLayout()

        # Egzersiz Adı
        egzersiz_adi_label = QLabel("Egzersiz Adını Girin:")
        egzersiz_adi_input = QLineEdit()
        layout.addWidget(egzersiz_adi_label)
        layout.addWidget(egzersiz_adi_input)

        # Egzersiz Detayı
        egzersiz_detayi_label = QLabel("Egzersiz Detayı:")
        egzersiz_detayi_input = QTextEdit()
        egzersiz_detayi_input.setMinimumSize(300, 100)  # Geometri ayarı
        layout.addWidget(egzersiz_detayi_label)
        layout.addWidget(egzersiz_detayi_input)

        # Haftalık Egzersiz Tekrarı
        egzersiz_tekrari_label = QLabel("Haftalık Egzersiz Tekrarı (Gün):")
        egzersiz_tekrari_input = QSpinBox()
        egzersiz_tekrari_input.setMinimum(1)
        egzersiz_tekrari_input.setMaximum(7)
        layout.addWidget(egzersiz_tekrari_label)
        layout.addWidget(egzersiz_tekrari_input)

        # Butonlar
        buton_layout = QHBoxLayout()
        kaydet_butonu = QPushButton("Egzersizi Kaydet")
        iptal_butonu = QPushButton("İptal")
        buton_layout.addWidget(kaydet_butonu)
        buton_layout.addWidget(iptal_butonu)
        layout.addLayout(buton_layout)

        egzersiz_dialog.setLayout(layout)

        def egzersiz_kaydet():
            egzersiz_adi = egzersiz_adi_input.text()
            egzersiz_detayi = egzersiz_detayi_input.toPlainText()
            egzersiz_tekrari = egzersiz_tekrari_input.value()

            if not egzersiz_adi:
                QMessageBox.warning(self, "Uyarı", "Lütfen egzersiz adını girin.")
                return

            egzersiz = {
                "ad": egzersiz_adi,
                "detay": egzersiz_detayi,
                "tekrar": egzersiz_tekrari
            }

            profil.egzersiz_ekle(egzersiz)
            self.kullanici_profilleri_tablosu.setItem(secili_satir, 6, QTableWidgetItem(", ".join([egzersiz["ad"] for egzersiz in profil.egzersizler])))
            QMessageBox.information(self, "Başarılı", f"{egzersiz_adi} egzersizi {profil.ad} {profil.soyad} için eklendi.")
            egzersiz_dialog.close()

        kaydet_butonu.clicked.connect(egzersiz_kaydet)
        iptal_butonu.clicked.connect(egzersiz_dialog.close)

        egzersiz_dialog.exec_()

    def egzersizleri_goster(self):
        secili_satir = self.kullanici_profilleri_tablosu.currentRow()
        if secili_satir == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kullanıcı profili seçin.")
            return

        profil = self.kullanici_profilleri[secili_satir]

        if not profil.egzersizler:
            QMessageBox.information(self, "Bilgi", "Bu kullanıcı için henüz bir egzersiz eklenmemiş.")
            return

        egzersiz_dialog = QDialog(self)
        egzersiz_dialog.setWindowTitle(f"{profil.ad} {profil.soyad}'ın Egzersizleri")

        layout = QVBoxLayout()

        for egzersiz in profil.egzersizler:
            egzersiz_widget = QWidget()
            egzersiz_layout = QVBoxLayout()

            ad_label = QLabel(f"Egzersiz Adı: {egzersiz['ad']}")
            detay_label = QLabel(f"Egzersiz Detayı: {egzersiz['detay']}")
            tekrar_label = QLabel(f"Haftalık Tekrar: {egzersiz['tekrar']} gün")

            egzersiz_layout.addWidget(ad_label)
            egzersiz_layout.addWidget(detay_label)
            egzersiz_layout.addWidget(tekrar_label)

            egzersiz_widget.setLayout(egzersiz_layout)
            layout.addWidget(egzersiz_widget)

        egzersiz_dialog.setLayout(layout)
        egzersiz_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    saglik_takip = SaglikTakipUygulamasi()
    saglik_takip.show()
    sys.exit(app.exec_())
