import sys
import sqlite3
from datetime import datetime

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QAbstractItemView, QDialogButtonBox, QDialog, QHBoxLayout,
                             QDateEdit, QMessageBox, QComboBox, QInputDialog,
                             )

class TarihciUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarihçi - Tarihi Olaylar Veritabanı")
        self.setGeometry(100, 100, 800, 600)

        self.conn = sqlite3.connect("tarihci.db")
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS olaylar
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, tarih TEXT, aciklama TEXT, sahsiyet_id INTEGER, donem_id INTEGER)"""
        )
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS sahsiyetler
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT)"""
        )
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS donemler
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, baslangic_tarihi TEXT, bitis_tarihi TEXT)"""
        )

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.olay_label = QLabel("Olay Adı:")
        self.olay_input = QLineEdit()
        self.tarih_label = QLabel("Tarih:")
        self.tarih_input = QDateEdit()
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDateRange(QDate(1, 1, 1), QDate.currentDate())

        self.aciklama_label = QLabel("Açıklama:")
        self.aciklama_input = QTextEdit()

        self.sahsiyet_label = QLabel("Şahsiyet:")
        self.sahsiyet_input = QComboBox()
        self.sahsiyet_ekle_button = QPushButton("Şahsiyet Ekle")
        self.sahsiyet_ekle_button.clicked.connect(self.sahsiyet_ekle)

        self.donem_label = QLabel("Dönem:")
        self.donem_input = QComboBox()
        self.donem_ekle_button = QPushButton("Dönem Ekle")
        self.donem_ekle_button.clicked.connect(self.donem_ekle)

        self.ekle_button = QPushButton("Olay Ekle")
        self.ekle_button.clicked.connect(self.olay_ekle)
        self.olaylari_goruntule_button = QPushButton("Olayları Görüntüle")
        self.olaylari_goruntule_button.clicked.connect(self.olaylari_goruntule)

        self.sahsiyetleri_goruntule_button = QPushButton("Şahsiyetleri Görüntüle")
        self.sahsiyetleri_goruntule_button.clicked.connect(self.sahsiyetleri_goruntule)

        self.donemleri_goruntule_button = QPushButton("Dönemleri Görüntüle")
        self.donemleri_goruntule_button.clicked.connect(self.donemleri_goruntule)

        layout.addWidget(self.olay_label)
        layout.addWidget(self.olay_input)
        layout.addWidget(self.tarih_label)
        layout.addWidget(self.tarih_input)
        layout.addWidget(self.aciklama_label)
        layout.addWidget(self.aciklama_input)
        layout.addWidget(self.sahsiyet_label)
        layout.addWidget(self.sahsiyet_input)
        layout.addWidget(self.sahsiyet_ekle_button)
        layout.addWidget(self.donem_label)
        layout.addWidget(self.donem_input)
        layout.addWidget(self.donem_ekle_button)
        layout.addWidget(self.ekle_button)
        layout.addWidget(self.olaylari_goruntule_button)
        layout.addWidget(self.sahsiyetleri_goruntule_button)
        layout.addWidget(self.donemleri_goruntule_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.sahsiyetleri_yukle()
        self.donemleri_yukle()

    def olay_ekle(self):
        ad = self.olay_input.text().strip()
        tarih = self.tarih_input.date().toString("yyyy-MM-dd")
        aciklama = self.aciklama_input.toPlainText().strip()
        sahsiyet_id = self.sahsiyet_input.currentData()
        donem_id = self.donem_input.currentData()

        if not ad or not aciklama:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen olay adı ve açıklamayı giriniz.")
            return

        self.c.execute(
            "INSERT INTO olaylar (ad, tarih, aciklama, sahsiyet_id, donem_id) VALUES (?, ?, ?, ?, ?)",
            (ad, tarih, aciklama, sahsiyet_id, donem_id),
        )
        self.conn.commit()

        self.olay_input.clear()
        self.tarih_input.clear()
        self.aciklama_input.clear()

    def olaylari_goruntule(self):
        self.olaylar_penceresi = OlaylarPenceresi(self.conn)
        self.olaylar_penceresi.show()

    def sahsiyet_ekle(self):
        ad, ok = QInputDialog.getText(self, "Şahsiyet Ekle", "Şahsiyet Adı:")
        if ok and ad:
            self.c.execute("INSERT INTO sahsiyetler (ad) VALUES (?)", (ad,))
            self.conn.commit()
            self.sahsiyetleri_yukle()

    def sahsiyetleri_goruntule(self):
        self.sahsiyetler_penceresi = SahsiyetlerPenceresi(self.conn)
        self.sahsiyetler_penceresi.show()

    def donem_ekle(self):
        ad, ok_ad = QInputDialog.getText(self, "Dönem Ekle", "Dönem Adı:")
        if not ok_ad or not ad:
            return

        baslangic_tarihi, ok_baslangic = QInputDialog.getText(self, "Dönem Ekle", "Başlangıç Tarihi (yyyy-AA-gg):")
        if not ok_baslangic:
            return

        bitis_tarihi, ok_bitis = QInputDialog.getText(self, "Dönem Ekle", "Bitiş Tarihi (yyyy-AA-gg):")
        if not ok_bitis:
            return

        self.c.execute(
            "INSERT INTO donemler (ad, baslangic_tarihi, bitis_tarihi) VALUES (?, ?, ?)",
            (ad, baslangic_tarihi, bitis_tarihi),
        )
        self.conn.commit()
        self.donemleri_yukle()

    def donemleri_goruntule(self):
        self.donemler_penceresi = DonemlerPenceresi(self.conn)
        self.donemler_penceresi.show()

    def sahsiyetleri_yukle(self):
        self.sahsiyet_input.clear()
        self.c.execute("SELECT id, ad FROM sahsiyetler")
        sahsiyetler = self.c.fetchall()
        self.sahsiyet_input.addItem("Şahsiyet Seçin", None)
        for sahsiyet in sahsiyetler:
            self.sahsiyet_input.addItem(sahsiyet[1], sahsiyet[0])

    def donemleri_yukle(self):
        self.donem_input.clear()
        self.c.execute("SELECT id, ad, baslangic_tarihi, bitis_tarihi FROM donemler")
        donemler = self.c.fetchall()
        self.donem_input.addItem("Dönem Seçin", None)
        for donem in donemler:
            self.donem_input.addItem(f"{donem[1]} ({donem[2]} - {donem[3]})", donem[0])

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


class OlaylarPenceresi(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.setWindowTitle("Olaylar")
        self.setGeometry(100, 100, 800, 600)
        self.conn = conn

        layout = QVBoxLayout()

        self.olaylar_tablosu = QTableWidget()
        self.olaylar_tablosu.setColumnCount(5)
        self.olaylar_tablosu.setHorizontalHeaderLabels(["Olay Adı", "Tarih", "Açıklama", "Şahsiyet", "Dönem"])
        self.olaylar_tablosu.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.olaylar_tablosu.doubleClicked.connect(self.olay_detaylari)

        c = conn.cursor()
        c.execute(
            """SELECT o.id, o.ad, o.tarih, o.aciklama, s.ad, d.ad
               FROM olaylar o
               LEFT JOIN sahsiyetler s ON o.sahsiyet_id = s.id
               LEFT JOIN donemler d ON o.donem_id = d.id"""
        )
        olaylar = c.fetchall()

        self.olaylar_tablosu.setRowCount(len(olaylar))
        for i, olay in enumerate(olaylar):
            self.olaylar_tablosu.setItem(i, 0, QTableWidgetItem(olay[1]))
            self.olaylar_tablosu.item(i, 0).setData(Qt.UserRole, olay[0])
            self.olaylar_tablosu.setItem(i, 1, QTableWidgetItem(olay[2]))
            self.olaylar_tablosu.setItem(i, 2, QTableWidgetItem(olay[3]))
            self.olaylar_tablosu.setItem(i, 3, QTableWidgetItem(olay[4] if olay[4] else ""))
            self.olaylar_tablosu.setItem(i, 4, QTableWidgetItem(olay[5] if olay[5] else ""))

        layout.addWidget(self.olaylar_tablosu)
        self.setLayout(layout)

    def olay_detaylari(self, index):
        secili_olay_id = self.olaylar_tablosu.item(index.row(), 0).data(Qt.UserRole)
        secili_olay_adi = self.olaylar_tablosu.item(index.row(), 0).text()
        secili_olay_tarihi = self.olaylar_tablosu.item(index.row(), 1).text()
        secili_olay_aciklama = self.olaylar_tablosu.item(index.row(), 2).text()
        secili_olay_sahsiyet = self.olaylar_tablosu.item(index.row(), 3).text()
        secili_olay_donem = self.olaylar_tablosu.item(index.row(), 4).text()

        self.olay_detay_penceresi = OlayDetayPenceresi(
            secili_olay_id,
            secili_olay_adi,
            secili_olay_tarihi,
            secili_olay_aciklama,
            secili_olay_sahsiyet,
            secili_olay_donem,
            self.conn,
            parent=self,
        )
        self.olay_detay_penceresi.show()


class OlayDetayPenceresi(QDialog):
    def __init__(
            self,
            olay_id,
            olay_adi,
            olay_tarihi,
            olay_aciklama,
            olay_sahsiyet,
            olay_donem,
            conn,
            parent=None,
    ):
        super().__init__(parent)
        self.conn = conn
        self.setWindowTitle("Olay Detayları")
        self.setGeometry(200, 200, 400, 400)

        main_layout = QVBoxLayout()

        olay_adi_label = QLabel("Olay Adı:")
        self.olay_adi_value = QLabel(olay_adi)

        self.olay_tarihi_value = QDateEdit()
        self.olay_tarihi_value.setCalendarPopup(True)
        self.olay_tarihi_value.setDateRange(QDate(1, 1, 1), QDate(9999, 12, 31))

        tarih_format = QDate.fromString(olay_tarihi, "yyyy-MM-dd")
        if tarih_format.isValid():
            self.olay_tarihi_value.setDate(tarih_format)
        else:
            self.olay_tarihi_value.setDate(QDate.currentDate())

        self.olay_tarihi_value.setReadOnly(True)

        olay_aciklama_label = QLabel("Açıklama:")
        self.olay_aciklama_value = QTextEdit()
        self.olay_aciklama_value.setPlainText(olay_aciklama)
        self.olay_aciklama_value.setReadOnly(True)

        olay_sahsiyet_label = QLabel("Şahsiyet:")
        self.olay_sahsiyet_value = QLabel(olay_sahsiyet)

        olay_donem_label = QLabel("Dönem:")
        self.olay_donem_value = QLabel(olay_donem)

        self.sil_button = QPushButton("Olayı Sil")
        self.sil_button.clicked.connect(lambda: self.olayi_sil(olay_id, conn))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        main_layout.addWidget(olay_adi_label)
        main_layout.addWidget(self.olay_adi_value)
        main_layout.addWidget(self.olay_tarihi_value)
        main_layout.addWidget(olay_aciklama_label)
        main_layout.addWidget(self.olay_aciklama_value)
        main_layout.addWidget(olay_sahsiyet_label)
        main_layout.addWidget(self.olay_sahsiyet_value)
        main_layout.addWidget(olay_donem_label)
        main_layout.addWidget(self.olay_donem_value)
        main_layout.addWidget(self.sil_button)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def olayi_sil(self, olay_id, conn):
        c = conn.cursor()
        c.execute("DELETE FROM olaylar WHERE id = ?", (olay_id,))
        conn.commit()
        self.accept()
        olay_tablosu = self.parent()
        olay_tablosu.olaylar_tablosu.removeRow(olay_tablosu.olaylar_tablosu.currentRow())

class SahsiyetlerPenceresi(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.setWindowTitle("Şahsiyetler")
        self.setGeometry(100, 100, 400, 400)
        self.conn = conn

        layout = QVBoxLayout()

        self.sahsiyetler_tablosu = QTableWidget()
        self.sahsiyetler_tablosu.setColumnCount(2)
        self.sahsiyetler_tablosu.setHorizontalHeaderLabels(["ID", "Şahsiyet Adı"])
        self.sahsiyetler_tablosu.setEditTriggers(QAbstractItemView.NoEditTriggers)

        c = conn.cursor()
        c.execute("SELECT id, ad FROM sahsiyetler")
        sahsiyetler = c.fetchall()

        self.sahsiyetler_tablosu.setRowCount(len(sahsiyetler))
        for i, sahsiyet in enumerate(sahsiyetler):
            self.sahsiyetler_tablosu.setItem(i, 0, QTableWidgetItem(str(sahsiyet[0])))
            self.sahsiyetler_tablosu.setItem(i, 1, QTableWidgetItem(sahsiyet[1]))

        layout.addWidget(self.sahsiyetler_tablosu)
        self.setLayout(layout)

class DonemlerPenceresi(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.setWindowTitle("Dönemler")
        self.setGeometry(100, 100, 600, 400)
        self.conn = conn

        layout = QVBoxLayout()

        self.donemler_tablosu = QTableWidget()
        self.donemler_tablosu.setColumnCount(4)
        self.donemler_tablosu.setHorizontalHeaderLabels(["ID", "Dönem Adı", "Başlangıç Tarihi", "Bitiş Tarihi"])
        self.donemler_tablosu.setEditTriggers(QAbstractItemView.NoEditTriggers)

        c = conn.cursor()
        c.execute("SELECT id, ad, baslangic_tarihi, bitis_tarihi FROM donemler")
        donemler = c.fetchall()

        self.donemler_tablosu.setRowCount(len(donemler))
        for i, donem in enumerate(donemler):
            self.donemler_tablosu.setItem(i, 0, QTableWidgetItem(str(donem[0])))
            self.donemler_tablosu.setItem(i, 1, QTableWidgetItem(donem[1]))
            self.donemler_tablosu.setItem(i, 2, QTableWidgetItem(donem[2]))
            self.donemler_tablosu.setItem(i, 3, QTableWidgetItem(donem[3]))

        layout.addWidget(self.donemler_tablosu)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    uygulama = TarihciUygulamasi()
    uygulama.show()
    sys.exit(app.exec_())
