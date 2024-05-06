from PyQt5.QtWidgets import (QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton)

class UrunGuncellemePenceresi(QDialog):
    def __init__(self, urunler, parent=None):
        super().__init__(parent)
        self.urunler = urunler
        self.setWindowTitle("Ürün Güncelleme")
        self.setGeometry(100, 100, 420, 400)
        self.initUI()

    def initUI(self):
        # Ürün tablosu oluşturma
        self.urun_tablosu = QTableWidget()
        self.urun_tablosu.setColumnCount(4)
        self.urun_tablosu.setHorizontalHeaderLabels(["Barkod Numarası", "Ürün Adı", "Stok Miktarı", "Ürün Fiyatı"])
        self.urun_tablosu.setEditTriggers(QTableWidget.DoubleClicked)  # Hücreleri düzenlenebilir yap
        self.urun_tablosunu_guncelle()

        # Kaydet butonu oluşturma
        kaydet_butonu = QPushButton("Kaydet")
        kaydet_butonu.clicked.connect(self.urunleri_kaydet)

        # Layout oluşturma
        layout = QVBoxLayout()
        layout.addWidget(self.urun_tablosu)
        layout.addWidget(kaydet_butonu)
        self.setLayout(layout)

    def urun_tablosunu_guncelle(self):
        self.urun_tablosu.setRowCount(len(self.urunler))
        for i, urun in enumerate(self.urunler):
            self.urun_tablosu.setItem(i, 0, QTableWidgetItem(urun["barkod"]))
            self.urun_tablosu.setItem(i, 1, QTableWidgetItem(urun["urun_adi"]))
            self.urun_tablosu.setItem(i, 2, QTableWidgetItem(urun["stok_miktari"]))
            self.urun_tablosu.setItem(i, 3, QTableWidgetItem(urun["urun_fiyati"]))

    def urunleri_kaydet(self):
        guncellenmus_urunler = []
        for i in range(self.urun_tablosu.rowCount()):
            eski_barkod = self.urunler[i]["barkod"]
            barkod = self.urun_tablosu.item(i, 0).text()
            urun_adi = self.urun_tablosu.item(i, 1).text()
            stok_miktari = self.urun_tablosu.item(i, 2).text()
            urun_fiyati = self.urun_tablosu.item(i, 3).text()

            urun = {"barkod": barkod, "urun_adi": urun_adi, "stok_miktari": stok_miktari, "urun_fiyati": urun_fiyati}

            if barkod != eski_barkod:
                guncellenmus_urunler.append(urun)
            else:
                self.urunler[i].update(urun)
                guncellenmus_urunler.append(self.urunler[i])

        self.urunler = guncellenmus_urunler
        self.close()

    def urun_bul(self, barkod):
        for urun in self.urunler:
            if urun["barkod"] == barkod:
                return urun
        return None