from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import pyqtSignal

class GorevAtamaPenceresi(QDialog):
    gorev_atandi = pyqtSignal(int, int)

    def __init__(self, projeler, calisanlar, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Görev Atama")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Proje seçme bölümü
        proje_secme_layout = QHBoxLayout()
        proje_secme_label = QLabel("Proje Seçin:")
        proje_secme_layout.addWidget(proje_secme_label)
        self.proje_secme_combo = QComboBox()
        self.proje_secme_combo.addItems([proje.proje_adi for proje in projeler])
        proje_secme_layout.addWidget(self.proje_secme_combo)
        layout.addLayout(proje_secme_layout)

        # Görev seçme bölümü
        gorev_secme_layout = QHBoxLayout()
        gorev_secme_label = QLabel("Görev Seçin:")
        gorev_secme_layout.addWidget(gorev_secme_label)
        self.gorev_secme_combo = QComboBox()
        gorev_secme_layout.addWidget(self.gorev_secme_combo)
        layout.addLayout(gorev_secme_layout)

        # Çalışan seçme bölümü
        calisan_secme_layout = QHBoxLayout()
        calisan_secme_label = QLabel("Çalışan Seçin:")
        calisan_secme_layout.addWidget(calisan_secme_label)
        self.calisan_secme_combo = QComboBox()
        self.calisan_secme_combo.addItems([f"{calisan.isim} {calisan.soyisim}" for calisan in calisanlar])
        calisan_secme_layout.addWidget(self.calisan_secme_combo)
        layout.addLayout(calisan_secme_layout)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["Proje", "Başlangıç Tarihi", "Bitiş Tarihi", "Görev", "Çalışan", "Durum"])
        layout.addWidget(self.tablo)

        # Kaydet butonu
        kaydet_butonu = QPushButton("Kaydet")
        kaydet_butonu.clicked.connect(self.gorev_ata)
        layout.addWidget(kaydet_butonu)

        self.setLayout(layout)

        self.proje_secme_combo.currentIndexChanged.connect(self.proje_secildi)

    def proje_secildi(self, index):
        proje = self.parent().projeler[index]
        self.gorev_secme_combo.clear()
        self.gorev_secme_combo.addItems([gorev.gorev_adi for gorev in proje.gorevler])
        self.tablo_guncelle(proje)

    def tablo_guncelle(self, proje):
        self.tablo.setRowCount(len(proje.gorevler))
        for i, gorev in enumerate(proje.gorevler):
            self.tablo.setItem(i, 0, QTableWidgetItem(proje.proje_adi))
            self.tablo.setItem(i, 1, QTableWidgetItem(proje.baslangic_tarihi))
            self.tablo.setItem(i, 2, QTableWidgetItem(proje.bitis_tarihi))
            self.tablo.setItem(i, 3, QTableWidgetItem(gorev.gorev_adi))
            calisan_adi = gorev.calisan.isim + " " + gorev.calisan.soyisim if gorev.calisan else ""
            self.tablo.setItem(i, 4, QTableWidgetItem(calisan_adi))
            self.tablo.setItem(i, 5, QTableWidgetItem(gorev.durum))

    def gorev_ata(self):
        proje_index = self.proje_secme_combo.currentIndex()
        gorev_index = self.gorev_secme_combo.currentIndex()
        calisan_index = self.calisan_secme_combo.currentIndex()

        proje = self.parent().projeler[proje_index]
        gorev = proje.gorevler[gorev_index]
        calisan = self.parent().calisan_yonetimi.calisanlari_getir()[calisan_index]

        gorev.calisan_ata(calisan)
        self.tablo_guncelle(proje)

        self.gorev_atandi.emit(proje_index, gorev_index)