import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QTabWidget
from PyQt5.QtCore import Qt

class Olay:
    def __init__(self, ad, tarih, aciklama):
        self.ad = ad
        self.tarih = tarih
        self.aciklama = aciklama

class Sahsiyet:
    def __init__(self, ad, donem):
        self.ad = ad
        self.donem = donem

class Donem:
    def __init__(self, ad, baslangic, bitis):
        self.ad = ad
        self.baslangic = baslangic
        self.bitis = bitis

class TarihciArayuzu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarihçi")
        self.setMinimumSize(800, 600)

        self.olaylar = []
        self.sahsiyetler = []
        self.donemler = []

        # Merkezi widget oluşturma
        merkezi_widget = QWidget()
        merkezi_layout = QVBoxLayout()
        merkezi_widget.setLayout(merkezi_layout)

        # Sekme widget'ı oluşturma
        self.sekme_widget = QTabWidget()
        merkezi_layout.addWidget(self.sekme_widget)

        # Olay ekleme sekmesi oluşturma
        olay_ekleme_widget = QWidget()
        olay_ekleme_layout = QVBoxLayout()
        olay_ekleme_widget.setLayout(olay_ekleme_layout)

        self.olay_adi_input = QLineEdit()
        self.olay_tarihi_input = QLineEdit()
        self.olay_aciklama_input = QTextEdit()
        olay_ekle_button = QPushButton("Olay Ekle")
        olay_ekle_button.clicked.connect(self.olay_ekle)

        olay_ekleme_layout.addWidget(QLabel("Olay Adı:"))
        olay_ekleme_layout.addWidget(self.olay_adi_input)
        olay_ekleme_layout.addWidget(QLabel("Olay Tarihi:"))
        olay_ekleme_layout.addWidget(self.olay_tarihi_input)
        olay_ekleme_layout.addWidget(QLabel("Olay Açıklaması:"))
        olay_ekleme_layout.addWidget(self.olay_aciklama_input)
        olay_ekleme_layout.addWidget(olay_ekle_button)

        self.sekme_widget.addTab(olay_ekleme_widget, "Olay Ekle")

        # Görüntüleme sekmesi oluşturma
        goruntuleme_widget = QWidget()
        goruntuleme_layout = QVBoxLayout()
        goruntuleme_widget.setLayout(goruntuleme_layout)

        self.goruntuleme_alani = QTextEdit()
        self.goruntuleme_alani.setReadOnly(True)
        goruntuleme_layout.addWidget(self.goruntuleme_alani)

        self.sekme_widget.addTab(goruntuleme_widget, "Görüntüle")

        self.setCentralWidget(merkezi_widget)

    def olay_ekle(self):
        ad = self.olay_adi_input.text()
        tarih = self.olay_tarihi_input.text()
        aciklama = self.olay_aciklama_input.toPlainText()

        olay = Olay(ad, tarih, aciklama)
        self.olaylar.append(olay)

        self.olay_adi_input.clear()
        self.olay_tarihi_input.clear()
        self.olay_aciklama_input.clear()

        self.goruntuleme_alani.append(f"Olay Adı: {ad}\nTarihi: {tarih}\nAçıklaması: {aciklama}\n\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arayuz = TarihciArayuzu()
    arayuz.show()
    sys.exit(app.exec_())