from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QPlainTextEdit, QInputDialog, QFileDialog, QMessageBox
from proje import Proje
from proje import Gorev
from proje import Calisan
from calisan import CalisanYonetimi
from calisan import CalisanSilmePenceresi
from gorev_atama_penceresi import GorevAtamaPenceresi

class GorevDetayPenceresi(QDialog):
    def __init__(self, gorev, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Görev Detayları: {gorev.gorev_adi}")

        layout = QVBoxLayout()

        gorev_adi_label = QLabel(f"Görev Adı: {gorev.gorev_adi}")
        layout.addWidget(gorev_adi_label)

        sorumlu_label = QLabel(f"Sorumlu: {gorev.sorumlu.isim}")
        layout.addWidget(sorumlu_label)

        durum_label = QLabel(f"Durum: {gorev.durum}")
        layout.addWidget(durum_label)

        ilerleme_label = QLabel(f"İlerleme: %{gorev.ilerleme}")
        layout.addWidget(ilerleme_label)

        aciklama_label = QLabel("Açıklama:")
        layout.addWidget(aciklama_label)
        self.aciklama_text = QPlainTextEdit()
        layout.addWidget(self.aciklama_text)

        self.setLayout(layout)

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İş Takip ve Yönetim Sistemi")
        self.setGeometry(100, 100, 1700, 830)

        self.projeler = []
        self.gorevler = []
        self.sorumlular = []

        ana_widget = QWidget()
        self.setCentralWidget(ana_widget)
        ana_layout = QVBoxLayout()
        ana_widget.setLayout(ana_layout)

        ust_bolum = QHBoxLayout()
        ana_layout.addLayout(ust_bolum)

        proje_bilgileri = QVBoxLayout()
        ust_bolum.addLayout(proje_bilgileri)

        proje_adi_label = QLabel("Proje Adı:")
        proje_bilgileri.addWidget(proje_adi_label)
        self.proje_adi_input = QLineEdit()
        proje_bilgileri.addWidget(self.proje_adi_input)

        baslangic_tarihi_label = QLabel("Başlangıç Tarihi:")
        proje_bilgileri.addWidget(baslangic_tarihi_label)
        self.baslangic_tarihi_input = QLineEdit()
        proje_bilgileri.addWidget(self.baslangic_tarihi_input)

        bitis_tarihi_label = QLabel("Bitiş Tarihi:")
        proje_bilgileri.addWidget(bitis_tarihi_label)
        self.bitis_tarihi_input = QLineEdit()
        proje_bilgileri.addWidget(self.bitis_tarihi_input)

        oncelik_label = QLabel("Öncelik:")
        proje_bilgileri.addWidget(oncelik_label)
        self.oncelik_input = QComboBox()
        self.oncelik_input.addItems(["Düşük", "Orta", "Yüksek"])
        proje_bilgileri.addWidget(self.oncelik_input)

        gorev_bilgileri = QVBoxLayout()
        ust_bolum.addLayout(gorev_bilgileri)

        gorev_adi_label = QLabel("Görev Adı:")
        gorev_bilgileri.addWidget(gorev_adi_label)
        self.gorev_adi_input = QLineEdit()
        gorev_bilgileri.addWidget(self.gorev_adi_input)

        sorumlu_label = QLabel("Sorumlu:")
        gorev_bilgileri.addWidget(sorumlu_label)
        self.sorumlu_input = QComboBox()
        gorev_bilgileri.addWidget(self.sorumlu_input)

        self.calisan_yonetimi = CalisanYonetimi()

        alt_bolum = QHBoxLayout()
        ana_layout.addLayout(alt_bolum)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(8)
        self.tablo.setHorizontalHeaderLabels(
            ["Proje Adı", "Sorumlu", "Başlangıç Tarihi", "Bitiş Tarihi", "Öncelik", "Görev", "Çalışan", "Durum"])
        alt_bolum.addWidget(self.tablo)

        buton_layout = QVBoxLayout()
        alt_bolum.addLayout(buton_layout)

        self.proje_olustur_butonu = QPushButton("Proje Oluştur")
        buton_layout.addWidget(self.proje_olustur_butonu)
        self.proje_olustur_butonu.clicked.connect(self.proje_olustur)

        self.proje_sil_butonu = QPushButton("Proje Sil")
        buton_layout.addWidget(self.proje_sil_butonu)
        self.proje_sil_butonu.clicked.connect(self.proje_sil)

        self.gorev_olustur_butonu = QPushButton("Görev Oluştur")
        buton_layout.addWidget(self.gorev_olustur_butonu)
        self.gorev_olustur_butonu.clicked.connect(self.gorev_olustur)

        self.sorumlu_ekle_butonu = QPushButton("Sorumlu Ekle")
        buton_layout.addWidget(self.sorumlu_ekle_butonu)
        self.sorumlu_ekle_butonu.clicked.connect(self.sorumlu_ekle)

        self.calisan_islemleri_butonu = QPushButton("Çalışan Ekle | Sil")
        buton_layout.addWidget(self.calisan_islemleri_butonu)
        self.calisan_islemleri_butonu.clicked.connect(self.calisan_islemleri)

        # Çalışan Tablosu
        self.calisan_tablosu = QTableWidget()
        self.calisan_tablosu.setColumnCount(4)
        self.calisan_tablosu.setHorizontalHeaderLabels(["İsim", "Soyisim", "Departman", "Rol"])
        alt_bolum.addWidget(self.calisan_tablosu)

        self.gorev_atama_butonu = QPushButton("Görev Atama")
        buton_layout.addWidget(self.gorev_atama_butonu)
        self.gorev_atama_butonu.clicked.connect(self.gorev_atama_penceresi_ac)

    def proje_olustur(self):
        proje_adi = self.proje_adi_input.text()
        baslangic_tarihi = self.baslangic_tarihi_input.text()
        bitis_tarihi = self.bitis_tarihi_input.text()
        oncelik = self.oncelik_input.currentText()
        sorumlu_adi = self.sorumlu_input.currentText()
        sorumlu = next((c for c in self.sorumlular if c.isim == sorumlu_adi), None)

        if not sorumlu:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir sorumlu seçin.")
            return

        yeni_proje = Proje(proje_adi, baslangic_tarihi, bitis_tarihi, oncelik)
        yeni_proje.sorumlu = sorumlu
        self.projeler.append(yeni_proje)

        self.tablo.setRowCount(len(self.projeler))
        for i, proje in enumerate(self.projeler):
            self.tablo.setItem(i, 0, QTableWidgetItem(proje.proje_adi))
            self.tablo.setItem(i, 1, QTableWidgetItem(proje.sorumlu.isim))
            self.tablo.setItem(i, 2, QTableWidgetItem(proje.baslangic_tarihi))
            self.tablo.setItem(i, 3, QTableWidgetItem(proje.bitis_tarihi))
            self.tablo.setItem(i, 4, QTableWidgetItem(proje.oncelik))
            gorev_metni = "\n".join([gorev.gorev_adi for gorev in proje.gorevler])
            self.tablo.setItem(i, 5, QTableWidgetItem(gorev_metni))
            self.tablo.setItem(i, 7, QTableWidgetItem("Beklemede"))

        self.oncelik_input.setCurrentIndex(0)

    def gorev_olustur(self):
        gorev_adi = self.gorev_adi_input.text()
        sorumlu_adi = self.sorumlu_input.currentText()
        sorumlu = next((c for c in self.sorumlular if c.isim == sorumlu_adi), None)

        if not gorev_adi:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir görev adı girin.")
            return

        if sorumlu:
            yeni_gorev = Gorev(gorev_adi, sorumlu)
            secili_proje = self.tablo.currentRow()
            if secili_proje >= 0:
                proje = self.projeler[secili_proje]
                proje.gorev_ata(yeni_gorev)
                sorumlu.gorev_ata(yeni_gorev)

                self.tablo.setItem(secili_proje, 5,
                                   QTableWidgetItem("\n".join([gorev.gorev_adi for gorev in proje.gorevler])))

        self.gorev_adi_input.clear()

    def sorumlu_ekle(self):
        isim, durum = QInputDialog.getText(self, "Sorumlu Ekle", "Sorumlu İsmini ve Soyismini Girin:")
        if durum and isim:
            rol, durum = QInputDialog.getItem(self, "Sorumlu Rolü", "Rolü Seçin:",
                                              ["Geliştirici", "Analist", "Test Uzmanı", "Sistem Yöneticisi", "Proje Yöneticisi"], 0, False)
            if durum:
                yeni_sorumlu = Calisan(isim, rol)
                self.sorumlular.append(yeni_sorumlu)
                self.sorumlu_input.addItem(isim)

    # def ilerleme_kaydet(self):
    #     secili_proje = self.tablo.currentRow()
    #     secili_gorev = self.tablo.currentColumn()
    #     if secili_proje >= 0 and secili_gorev >= 4:
    #         proje = self.projeler[secili_proje]
    #         gorev_adi, durum = QInputDialog.getText(self, "İlerleme Kaydet", "Görev Adını Girin:")
    #         if durum and gorev_adi:
    #             ilerleme, durum = QInputDialog.getInt(self, "İlerleme Kaydet", "İlerleme Yüzdesini Girin:", min=0,
    #                                                   max=100)
    #             if durum:
    #                 proje.ilerleme_kaydet(gorev_adi, ilerleme)
    #                 self.tablo.setItem(secili_proje, secili_gorev, QTableWidgetItem(str(ilerleme)))

    def calisan_islemleri(self):
        islem, durum = QInputDialog.getItem(self, "Çalışan İşlemleri", "İşlem Seçin:", ["Ekle", "Sil"], 0, False)
        if durum:
            if islem == "Ekle":
                self.calisan_ekle()
            else:
                self.calisan_sil()

    def calisan_ekle(self):
        isim, durum = QInputDialog.getText(self, "Çalışan Ekle", "İsim:")
        if durum and isim:
            soyisim, durum = QInputDialog.getText(self, "Çalışan Ekle", "Soyisim:")
            if durum and soyisim:
                departman, durum = QInputDialog.getText(self, "Çalışan Ekle", "Departman:")
                if durum and departman:
                    rol, durum = QInputDialog.getItem(self, "Çalışan Ekle", "Rol:",
                                                      ["Geliştirici", "Tasarımcı", "Analist",
                                                       "Test Uzmanı", "Operatör", "Sistem Yöneticisi", "İş Analizcisi",
                                                       "Veri Bilimcisi", "Ağ Uzmanı", "Siber Güvenlik Uzmanı",
                                                       "Teknik Yazılımcı", "DevOps Mühendisi", "Mobil Geliştirici",
                                                       "Gömülü Yazılım Geliştirici", "UI/UX Tasarımcısı"], 0, False)
                    if durum:
                        self.calisan_yonetimi.calisan_ekle(isim, soyisim, departman, rol)
                        self.calisan_tablosu_guncelle()
    def calisan_sil(self):
        calisanlar = self.calisan_yonetimi.calisanlari_getir()
        if calisanlar:
            calisan_silme_penceresi = CalisanSilmePenceresi(calisanlar, self)
            calisan_silme_penceresi.exec_()

    def calisan_tablosu_guncelle(self):
        self.calisan_tablosu.setRowCount(len(self.calisan_yonetimi.calisanlar))
        for i, calisan in enumerate(self.calisan_yonetimi.calisanlari_getir()):
            self.calisan_tablosu.setItem(i, 0, QTableWidgetItem(calisan.isim))
            self.calisan_tablosu.setItem(i, 1, QTableWidgetItem(calisan.soyisim))
            self.calisan_tablosu.setItem(i, 2, QTableWidgetItem(calisan.departman))
            self.calisan_tablosu.setItem(i, 3, QTableWidgetItem(calisan.rol))

    def gorev_atama_penceresi_ac(self):
        calisanlar = self.calisan_yonetimi.calisanlari_getir()
        if calisanlar:
            gorev_atama_penceresi = GorevAtamaPenceresi(self.projeler, calisanlar, self)
            gorev_atama_penceresi.gorev_atandi.connect(self.ana_tablo_guncelle)
            gorev_atama_penceresi.exec_()

    def ana_tablo_guncelle(self, proje_index, gorev_index):
        proje = self.projeler[proje_index]
        gorev = proje.gorevler[gorev_index]

        for i in range(self.tablo.rowCount()):
            tablo_proje_adi = self.tablo.item(i, 0).text()
            tablo_gorev_adi = self.tablo.item(i, 5).text().split("\n")[gorev_index]

            if tablo_proje_adi == proje.proje_adi and tablo_gorev_adi == gorev.gorev_adi:
                calisan_adi = gorev.calisan.isim + " " + gorev.calisan.soyisim if gorev.calisan else ""
                self.tablo.setItem(i, 6, QTableWidgetItem(calisan_adi))
                self.tablo.setItem(i, 7, QTableWidgetItem(gorev.durum))
                break

    def proje_sil(self):
        secili_proje = self.tablo.currentRow()
        if secili_proje >= 0:
            cevap = QMessageBox.question(self, "Proje Sil", "Seçili projeyi silmek istediğinizden emin misiniz?",
                                         QMessageBox.Yes | QMessageBox.No)
            if cevap == QMessageBox.Yes:
                self.projeler.pop(secili_proje)
                self.tablo.removeRow(secili_proje)
