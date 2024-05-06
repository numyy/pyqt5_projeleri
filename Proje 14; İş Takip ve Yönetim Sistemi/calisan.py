from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QPushButton, QMessageBox
class Calisan:
    def __init__(self, isim, soyisim, departman, rol):
        self.isim = isim
        self.soyisim = soyisim
        self.departman = departman
        self.rol = rol

    def __str__(self):
        return f"{self.isim} {self.soyisim} - {self.departman} - {self.rol}"

class CalisanYonetimi:
    def __init__(self):
        self.calisanlar = []

    def calisan_ekle(self, isim, soyisim, departman, rol):
        yeni_calisan = Calisan(isim, soyisim, departman, rol)
        self.calisanlar.append(yeni_calisan)

    def calisan_nesne_sil(self, calisan):
        self.calisanlar.remove(calisan)

    def calisanlari_getir(self):
        return self.calisanlar

class CalisanSilmePenceresi(QDialog):
    def __init__(self, calisanlar, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Çalışan Silme")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.calisan_tablosu = QTableWidget()
        self.calisan_tablosu.setColumnCount(4)
        self.calisan_tablosu.setHorizontalHeaderLabels(["İsim", "Soyisim", "Departman", "Rol"])
        self.calisan_tablosu.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.calisan_tablosu.setSelectionMode(QAbstractItemView.MultiSelection)

        for i, calisan in enumerate(calisanlar):
            self.calisan_tablosu.insertRow(i)
            self.calisan_tablosu.setItem(i, 0, QTableWidgetItem(calisan.isim))
            self.calisan_tablosu.setItem(i, 1, QTableWidgetItem(calisan.soyisim))
            self.calisan_tablosu.setItem(i, 2, QTableWidgetItem(calisan.departman))
            self.calisan_tablosu.setItem(i, 3, QTableWidgetItem(calisan.rol))

        layout.addWidget(self.calisan_tablosu)

        sil_butonu = QPushButton("Sil")
        sil_butonu.clicked.connect(self.sil)
        layout.addWidget(sil_butonu)

        self.setLayout(layout)

    def sil(self):
        secili_satirlar = self.calisan_tablosu.selectedIndexes()
        if secili_satirlar:
            cevap = QMessageBox.question(self, "Çalışan Sil", "Seçili çalışanları silmek istediğinizden emin misiniz?",
                                         QMessageBox.Yes | QMessageBox.No)
            if cevap == QMessageBox.Yes:
                calisanlar_listesi = list(self.parent().calisan_yonetimi.calisanlari_getir())
                satirlar = set()
                for index in secili_satirlar:
                    satirlar.add(index.row())
                for satir in sorted(satirlar, reverse=True):
                    calisan = calisanlar_listesi[satir]
                    self.parent().calisan_yonetimi.calisan_nesne_sil(calisan)
                self.parent().calisan_tablosu_guncelle()
                self.close()