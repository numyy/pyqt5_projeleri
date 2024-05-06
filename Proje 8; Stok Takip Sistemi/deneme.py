import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QHBoxLayout,
                             QVBoxLayout, QDialog)
from urun_guncelleme import UrunGuncellemePenceresi
from siparis_penceresi import SiparisPenceresi
import pickle
class StokTakipSistemi(QWidget):
    def __init__(self):
        super().__init__()
        self.urunleri_yukle()
        self.setGeometry(100, 100, 430, 540)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Stok Takip Sistemi")

        # Orta kısım
        barkod_label = QLabel("Barkod Numarası:")
        self.barkod_edit = QLineEdit()
        urun_adi_label = QLabel("Ürün Adı:")
        self.urun_adi_edit = QLineEdit()
        stok_miktari_label = QLabel("Stok Miktarı:")
        self.stok_miktari_edit = QLineEdit()
        urun_fiyati_label = QLabel("Ürün Fiyatı:")
        self.urun_fiyati_edit = QLineEdit()

        ekle_button = QPushButton("Ekle")
        cikar_button = QPushButton("Çıkar")
        siparisleri_yonet_button = QPushButton("Siparişleri Yönet")

        ekle_button.clicked.connect(self.urun_ekle)
        cikar_button.clicked.connect(self.urun_cikar)
        siparisleri_yonet_button.clicked.connect(self.siparisleri_yonet)

        arama_label = QLabel("Ara:")
        self.arama_kutusu = QLineEdit()
        self.arama_kutusu.textChanged.connect(self.urunleri_filtrele)

        orta_layout = QVBoxLayout()
        orta_layout.addWidget(barkod_label)
        orta_layout.addWidget(self.barkod_edit)
        orta_layout.addWidget(urun_adi_label)
        orta_layout.addWidget(self.urun_adi_edit)
        orta_layout.addWidget(stok_miktari_label)
        orta_layout.addWidget(self.stok_miktari_edit)
        orta_layout.addWidget(urun_fiyati_label)
        orta_layout.addWidget(self.urun_fiyati_edit)
        orta_layout.addWidget(ekle_button)
        orta_layout.addWidget(cikar_button)
        orta_layout.addWidget(arama_label)
        orta_layout.addWidget(self.arama_kutusu)
        orta_layout.addWidget(siparisleri_yonet_button)

        # Alt kısım
        self.urun_tablosu = QTableWidget()
        self.urun_tablosu.setColumnCount(4)
        self.urun_tablosu.setHorizontalHeaderLabels(["Barkod Numarası", "Ürün Adı", "Stok Miktarı", "Ürün Fiyatı"])

        urun_guncelleme_button = QPushButton("Ürün Güncelleme")
        urun_guncelleme_button.clicked.connect(self.urun_guncelleme_penceresi_ac)

        yenile_button = QPushButton("Yenile")
        yenile_button.clicked.connect(self.yenile_button_clicked)

        alt_layout = QVBoxLayout()
        alt_layout.addWidget(self.urun_tablosu)
        alt_layout.addWidget(urun_guncelleme_button)
        alt_layout.addWidget(yenile_button)

        # Ana layout
        ana_layout = QVBoxLayout()
        ana_layout.addLayout(orta_layout)
        ana_layout.addLayout(alt_layout)

        self.setLayout(ana_layout)

    def yenile_button_clicked(self):
        self.barkod_edit.clear()
        self.urun_adi_edit.clear()
        self.stok_miktari_edit.clear()
        self.urun_fiyati_edit.clear()
        self.urun_tablosunu_guncelle()

    def urun_guncelleme_penceresi_ac(self):
        urun_guncelleme_penceresi = UrunGuncellemePenceresi(self.urunler.copy(), self)
        urun_guncelleme_penceresi.exec_()
        self.urunler = urun_guncelleme_penceresi.urunler
        self.urun_tablosunu_guncelle()

    def siparisleri_yonet(self):
        siparis_penceresi = SiparisPenceresi(self.urunler.copy(), parent=self)
        siparis_penceresi.exec_()
        self.urunler = siparis_penceresi.urunler
        self.urun_tablosunu_guncelle()

    def urunleri_filtrele(self):
        aranan_metin = self.arama_kutusu.text().lower()
        filtrelenmis_urunler = []
        for urun in self.urunler:
            if (aranan_metin in urun["barkod"].lower() or
                    aranan_metin in urun["urun_adi"].lower() or
                    aranan_metin in urun["stok_miktari"] or
                    aranan_metin in urun["urun_fiyati"]):
                filtrelenmis_urunler.append(urun)

        self.urun_tablosunu_guncelle(filtrelenmis_urunler)

    def urun_ekle(self):
        barkod = self.barkod_edit.text()
        urun_adi = self.urun_adi_edit.text()
        try:
            stok_miktari = int(self.stok_miktari_edit.text())
            urun_fiyati = float(self.urun_fiyati_edit.text())
        except ValueError:
            # Hata mesajı göster
            return

        mevcut_urun = self.urun_bul(barkod)
        if mevcut_urun:
            mevcut_urun["stok_miktari"] = str(int(mevcut_urun["stok_miktari"]) + stok_miktari)
        else:
            self.urunler.append({
                "barkod": barkod,
                "urun_adi": urun_adi,
                "stok_miktari": str(stok_miktari),
                "urun_fiyati": str(urun_fiyati)
            })

        self.urun_tablosunu_guncelle()
        self.urunleri_kaydet()

    def urun_cikar(self):
        cikar_penceresi = QDialog()
        cikar_penceresi.setWindowTitle("Ürün Çıkar")
        cikar_penceresi.setGeometry(100, 100, 440, 280)

        urun_tablosu = QTableWidget()
        urun_tablosu.setColumnCount(4)
        urun_tablosu.setHorizontalHeaderLabels(["Ürün Adı", "Barkod Numarası", "Stok Miktarı", "Ürün Fiyatı"])

        for i, urun in enumerate(self.urunler):
            urun_tablosu.insertRow(i)
            urun_tablosu.setItem(i, 0, QTableWidgetItem(urun["urun_adi"]))
            urun_tablosu.setItem(i, 1, QTableWidgetItem(urun["barkod"]))
            urun_tablosu.setItem(i, 2, QTableWidgetItem(urun["stok_miktari"]))
            urun_tablosu.setItem(i, 3, QTableWidgetItem(urun["urun_fiyati"]))

        urun_tablosu.setSelectionBehavior(QTableWidget.SelectRows)
        urun_tablosu.setSelectionMode(QTableWidget.MultiSelection)

        cikar_butonu = QPushButton("Çıkar")
        cikar_butonu.clicked.connect(lambda: self.urunleri_cikar(urun_tablosu.selectedItems(), cikar_penceresi))

        iptal_butonu = QPushButton("İptal")
        iptal_butonu.clicked.connect(cikar_penceresi.close)

        buton_layout = QHBoxLayout()
        buton_layout.addWidget(cikar_butonu)
        buton_layout.addWidget(iptal_butonu)

        layout = QVBoxLayout()
        layout.addWidget(urun_tablosu)
        layout.addLayout(buton_layout)
        cikar_penceresi.setLayout(layout)

        cikar_penceresi.exec_()

    def urunleri_cikar(self, secili_urunler, cikar_penceresi):
        secili_satirlar = set()
        for secili_urun in secili_urunler:
            secili_satirlar.add(secili_urun.row())

        for satir in sorted(secili_satirlar, reverse=True):
            self.urunler.pop(satir)

        self.urun_tablosunu_guncelle()
        self.urunleri_kaydet()
        cikar_penceresi.close()

    def urun_bul(self, barkod):
        for urun in self.urunler:
            if urun["barkod"] == barkod:
                return urun
        return None

    def urunleri_guncelle(self, guncellenmus_urun):
        for i, urun in enumerate(self.urunler):
            if urun["barkod"] == guncellenmus_urun["barkod"]:
                self.urunler[i] = guncellenmus_urun
                break
        self.urun_tablosunu_guncelle()

    def urun_tablosunu_guncelle(self, urunler=None):
        if urunler is None:
            urunler = self.urunler
        elif not isinstance(urunler, list):
            # Hata mesajı göster
            return

        self.urun_tablosu.setRowCount(len(urunler))
        for i, urun in enumerate(urunler):
            self.urun_tablosu.setItem(i, 0, QTableWidgetItem(urun["barkod"]))
            self.urun_tablosu.setItem(i, 1, QTableWidgetItem(urun["urun_adi"]))
            self.urun_tablosu.setItem(i, 2, QTableWidgetItem(urun["stok_miktari"]))
            self.urun_tablosu.setItem(i, 3, QTableWidgetItem(urun["urun_fiyati"]))

    def siparisleri_yonet(self):
        siparis_penceresi = SiparisPenceresi(self.urunler.copy())
        siparis_penceresi.exec_()
        # Sipariş penceresi kapandıktan sonra ürünleri güncelle
        self.urunler = siparis_penceresi.urunler
        self.urun_tablosunu_guncelle()

    def siparis_guncellendi(self):
        self.urun_tablosunu_guncelle()
        self.urunleri_kaydet()

    def urunleri_kaydet(self):
        with open("urunler.pkl", "wb") as dosya:
            pickle.dump(self.urunler, dosya)

    def urunleri_yukle(self):
        try:
            with open("urunler.pkl", "rb") as dosya:
                self.urunler = pickle.load(dosya)
        except (FileNotFoundError, EOFError):
            self.urunler = []

    def closeEvent(self, event):
        self.urunleri_kaydet()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stok_takip_sistemi = StokTakipSistemi()
    stok_takip_sistemi.show()
    sys.exit(app.exec_())