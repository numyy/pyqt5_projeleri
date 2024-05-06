import sys
import random

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QListWidget, QMessageBox, QAbstractItemView

class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Araç Kiralama Sistemi")
        self.arabalar = [
            (10012, "Renault Clio", "Kiralık değil"),
            (89432, "Fiat Egea", "Kiralık"),
            (70012, "Volkswagen Passat", "Kiralık"),
            (50107, "Toyota Corolla", "Kiralık değil"),
            (66705, "Hyundai i20", "Kiralık"),
            (91220, "Ford Fiesta", "Kiralık değil"),
            (70504, "Opel Astra", "Kiralık"),
            (20045, "Peugeot 301", "Kiralık değil"),
            (62004, "Citroën C-Elysee", "Kiralık"),
            (30050, "Dacia Sandero", "Kiralık")
        ]
        self.kiralananlar = []

        # Kullanıcı Arayüzünü Oluşturma Kısmı
        self.baslikLabel = QLabel("Araç Kiralama Sistemi", self)
        self.isimLabel = QLabel("Adınız:", self)
        self.isimLineEdit = QLineEdit(self)
        self.soyisimLabel = QLabel("Soyadınız:", self)
        self.soyisimLineEdit = QLineEdit(self)
        self.yasLabel = QLabel("Yaşınız:", self)
        self.yasLineEdit = QLineEdit(self)
        self.arabalarLabel = QLabel("Mevcut Araçlar:", self)
        self.arabalarListWidget = QListWidget(self)
        self.arabalarListWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.kiralaButton = QPushButton("Kirala", self)
        self.kiralamaiptalButton = QPushButton("Kiralama İptal", self)

        # Araç Listesini Kullanıcı Arayüzüne Eklendiği Kısım
        for arac_id, araba, durum in self.arabalar:
            if araba in self.kiralananlar:
                self.arabalarListWidget.addItem(f"{arac_id} - {araba} (+) ({durum})")
            else:
                self.arabalarListWidget.addItem(f"{arac_id} - {araba} ({durum})")

        # Kullanıcı Arayüzünü Yerleştirme Kısmı
        grid = QGridLayout(self)
        grid.addWidget(self.baslikLabel, 0, 0, 1, 2)
        grid.addWidget(self.isimLabel, 1, 0)
        grid.addWidget(self.isimLineEdit, 1, 1)
        grid.addWidget(self.soyisimLabel, 2, 0)
        grid.addWidget(self.soyisimLineEdit, 2, 1)
        grid.addWidget(self.yasLabel, 3, 0)
        grid.addWidget(self.yasLineEdit, 3, 1)
        grid.addWidget(self.arabalarLabel, 4, 0)
        grid.addWidget(self.arabalarListWidget, 5, 0, 1, 2)
        grid.addWidget(self.kiralaButton, 6, 0, 1, 2)
        grid.addWidget(self.kiralamaiptalButton, 7, 0, 1, 2)

        # Sinyal Bağlantıları Kurulduğu Kısım
        self.kiralaButton.clicked.connect(self.kirala)
        self.kiralamaiptalButton.clicked.connect(self.kiralamaiptal)
        self.arabalarListWidget.itemSelectionChanged.connect(self.secilen_arac_degisti)

    def kirala(self):
        isim = self.isimLineEdit.text()
        soyisim = self.soyisimLineEdit.text()
        yas = int(self.yasLineEdit.text())

        if not isim or not soyisim or not yas:
            QMessageBox.warning(self, "Hata", "Lütfen adınızı, soyadınızı ve yaşınızı doldurun.")
            return

        if yas < 18:
            QMessageBox.warning(self, "Hata", "18 yaşının altındakiler araç kiralayamaz!")
            return

        secilmisAraba = self.arabalarListWidget.currentItem()
        if not secilmisAraba:
            QMessageBox.warning(self, "Hata", "Lütfen bir araç seçin.")
            return

        arac_id, secilmisAraba, durum = self.arabalar[self.arabalarListWidget.currentRow()]
        if durum == "Kiralık değil":
            QMessageBox.warning(self, "Hata", "Seçilen araç şu anda kiralık değil.")
            return

        self.kiralananlar.append(secilmisAraba)
        self.arabalar[self.arabalarListWidget.currentRow()] = (arac_id, secilmisAraba, "Kiralık değil")
        self.arabalarListWidget.takeItem(self.arabalarListWidget.currentRow())
        self.arabalarListWidget.insertItem(self.arabalarListWidget.currentRow(), f"{arac_id} - {secilmisAraba} (+) (Kiralık değil)")
        self.arabalarListWidget.setCurrentRow(self.arabalarListWidget.currentRow())

        dialog = QMessageBox(QMessageBox.Information, "Araç Kiralandı", f"{isim} {soyisim}, {secilmisAraba} kiralandı!")
        dialog.exec_()

    def kiralamaiptal(self):
        selectedItems = self.arabalarListWidget.selectedItems()
        if selectedItems:
            secilmisAraba = selectedItems[0].text().split(" - ")[1].split(" (")[0].replace(" (+)", "")
            if secilmisAraba in self.kiralananlar:
                arac_id = \
                [arac[0] for arac in self.arabalar if arac[1] == secilmisAraba and arac[2] == "Kiralık değil"][0]
                self.arabalar[self.arabalar.index((arac_id, secilmisAraba, "Kiralık değil"))] = (
                arac_id, secilmisAraba, "Kiralık")
                self.kiralananlar.remove(secilmisAraba)
                self.arabalarListWidget.takeItem(self.arabalarListWidget.currentRow())
                self.arabalarListWidget.insertItem(self.arabalarListWidget.currentRow(),
                                                   f"{arac_id} - {secilmisAraba} (Kiralık)")
                self.arabalarListWidget.setCurrentRow(self.arabalarListWidget.currentRow())
            else:
                QMessageBox.warning(self, "Hata", "Bu aracı siz kiralamadınız.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir araç seçin.")

    def secilen_arac_degisti(self):
        self.arabalarListWidget.setCurrentRow(self.arabalarListWidget.currentRow())

    def rastgele_durum_ata(self):
        for i, (arac_id, araba, durum) in enumerate(self.arabalar):
            self.arabalar[i] = (arac_id, araba, "Kiralık" if random.randint(0, 1) else "Kiralık değil")
            self.arabalarListWidget.takeItem(i)
            if araba in self.kiralananlar:
                self.arabalarListWidget.insertItem(i, f"{arac_id} - {araba} (+) ({self.arabalar[i][2]})")
            else:
                self.arabalarListWidget.insertItem(i, f"{arac_id} - {araba} ({self.arabalar[i][2]})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.rastgele_durum_ata()
    pencere.show()
    sys.exit(app.exec_())