import random
import pickle
from datetime import datetime
from PyQt5.QtWidgets import (QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QHeaderView)

class SiparisPenceresi(QDialog):
    def __init__(self, urunler, parent=None):
        super().__init__(parent)
        self.parent = parent  # Ana pencereyi sakla
        self.urunler = urunler
        self.siparisler = self.siparisleri_yukle()
        self.siparis_numarasi = self.siparisleri_baslangic_numarasi()
        self.setWindowTitle("Sipariş Yönetimi")
        self.setGeometry(100, 100, 710, 545)
        self.initUI()

    def initUI(self):
        # Ürün tablosu oluşturma
        self.urun_tablosu = QTableWidget()
        self.urun_tablosu.setColumnCount(4)
        self.urun_tablosu.setHorizontalHeaderLabels(["Barkod Numarası", "Ürün Adı", "Stok Miktarı", "Ürün Fiyatı"])
        self.urun_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.urun_tablosunu_guncelle()

        # Sipariş bölümü
        siparis_label = QLabel("Sipariş Miktarı:")
        self.siparis_miktari_edit = QLineEdit()
        siparis_butonu = QPushButton("Sipariş Ver")
        siparis_butonu.clicked.connect(self.siparis_ver)

        siparis_layout = QHBoxLayout()
        siparis_layout.addWidget(siparis_label)
        siparis_layout.addWidget(self.siparis_miktari_edit)
        siparis_layout.addWidget(siparis_butonu)

        # Sipariş tablosu oluşturma
        self.siparis_tablosu = QTableWidget()
        self.siparis_tablosu.setColumnCount(6)
        self.siparis_tablosu.setHorizontalHeaderLabels(["Sipariş Numarası", "Tarih", "Barkod Numarası", "Ürün Adı", "Ürün Sipariş Adeti", "Sipariş Tutarı"])
        self.siparis_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.siparis_tablosu.setSelectionBehavior(QTableWidget.SelectRows)
        self.siparis_tablosu.setSelectionMode(QTableWidget.MultiSelection)
        self.siparis_tablosunu_guncelle()

        # Sipariş silme butonu
        sil_butonu = QPushButton("Seçili Siparişleri Sil")
        sil_butonu.clicked.connect(self.secili_siparisleri_sil)

        # Layout oluşturma
        layout = QVBoxLayout()
        layout.addWidget(self.urun_tablosu)
        layout.addLayout(siparis_layout)
        layout.addWidget(self.siparis_tablosu)
        layout.addWidget(sil_butonu)
        self.setLayout(layout)

    def urun_tablosunu_guncelle(self):
        self.urun_tablosu.setRowCount(len(self.urunler))
        for i, urun in enumerate(self.urunler):
            self.urun_tablosu.setItem(i, 0, QTableWidgetItem(urun["barkod"]))
            self.urun_tablosu.setItem(i, 1, QTableWidgetItem(urun["urun_adi"]))
            self.urun_tablosu.setItem(i, 2, QTableWidgetItem(urun["stok_miktari"]))
            self.urun_tablosu.setItem(i, 3, QTableWidgetItem(urun["urun_fiyati"]))

    def siparis_ver(self):
        secili_satir = self.urun_tablosu.currentRow()
        if secili_satir == -1:
            return

        siparis_miktari = self.siparis_miktari_edit.text()
        if not siparis_miktari:
            return

        try:
            siparis_miktari = int(siparis_miktari)
        except ValueError:
            return

        urun = self.urunler[secili_satir]
        stok_miktari = int(urun["stok_miktari"])

        if siparis_miktari > stok_miktari:
            return

        urun_fiyati = float(urun["urun_fiyati"])
        siparis_tutari = siparis_miktari * urun_fiyati

        # Rastgele bir sipariş numarası oluştur
        siparis_numarasi = random.randint(1, 10000)

        # Sipariş ekle
        self.siparisler.append({
            "siparis_numarasi": siparis_numarasi,
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "barkod_numarasi": urun["barkod"],
            "urun_adi": urun["urun_adi"],
            "urun_siparis_adeti": siparis_miktari,
            "siparis_tutari": siparis_tutari
        })
        self.siparisleri_kaydet()

        # Stok miktarını güncelle
        urun["stok_miktari"] = str(stok_miktari - siparis_miktari)

        self.urun_tablosunu_guncelle()
        self.siparis_tablosunu_guncelle()

    def siparis_tablosunu_guncelle(self):
        self.siparis_tablosu.setRowCount(len(self.siparisler))
        for i, siparis in enumerate(self.siparisler):
            self.siparis_tablosu.setItem(i, 0, QTableWidgetItem(str(siparis["siparis_numarasi"])))
            self.siparis_tablosu.setItem(i, 1, QTableWidgetItem(siparis["tarih"]))
            self.siparis_tablosu.setItem(i, 2, QTableWidgetItem(siparis["barkod_numarasi"]))
            self.siparis_tablosu.setItem(i, 3, QTableWidgetItem(siparis["urun_adi"]))
            self.siparis_tablosu.setItem(i, 4, QTableWidgetItem(str(siparis["urun_siparis_adeti"])))
            self.siparis_tablosu.setItem(i, 5, QTableWidgetItem(str(siparis["siparis_tutari"])))

    def secili_siparisleri_sil(self):
        secili_satirlar = self.siparis_tablosu.selectionModel().selectedRows()
        for satir in sorted([i.row() for i in secili_satirlar], reverse=True):
            siparis = self.siparisler.pop(satir)

            # Stok miktarını güncelle
            urun = self.urun_bul(siparis["barkod_numarasi"])
            if urun:
                urun["stok_miktari"] = str(int(urun["stok_miktari"]) + siparis["urun_siparis_adeti"])

        self.siparisleri_kaydet()
        self.siparis_tablosunu_guncelle()
        self.urun_tablosunu_guncelle()

    def urun_bul(self, barkod):
        for urun in self.urunler:
            if urun["barkod"] == barkod:
                return urun
        return None

    def siparisleri_kaydet(self):
        with open("siparisler.pkl", "wb") as dosya:
            pickle.dump(self.siparisler, dosya)

    def siparisleri_yukle(self):
        try:
            with open("siparisler.pkl", "rb") as dosya:
                siparisler = pickle.load(dosya)
        except FileNotFoundError:
            siparisler = []
        return siparisler

    def siparisleri_baslangic_numarasi(self):
        if not self.siparisler:
            return 1
        else:
            return max(siparis["siparis_numarasi"] for siparis in self.siparisler) + 1