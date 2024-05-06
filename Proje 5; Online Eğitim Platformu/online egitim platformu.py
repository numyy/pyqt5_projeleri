import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout, QPushButton,
                             QLabel, QComboBox, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QLineEdit,
                             QMessageBox)

class Egitmen:
    def __init__(self, isim, uzmanlik):
        self.isim = isim
        self.uzmanlik = uzmanlik

class Ogrenci:
    def __init__(self, isim, soyisim, eposta):
        self.isim = isim
        self.soyisim = soyisim
        self.eposta = eposta

class Kurs:
    def __init__(self, ad, egitmen, konular):
        self.ad = ad
        self.egitmen = egitmen
        self.konular = konular
        self.kayitli_ogrenciler = []

    def ogrenci_kaydet(self, ogrenci):
        self.kayitli_ogrenciler.append(ogrenci)

class ContentDialog(QDialog):
    def __init__(self, kurs_adi, konular, egitmen, parent=None):
        super().__init__(parent)
        self.kurs_adi = kurs_adi
        self.konular = konular
        self.egitmen = egitmen
        self.parent = parent
        self.setWindowTitle(f"{kurs_adi} Ders İçeriği")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.icerik_tablosu = QTableWidget()
        self.icerik_tablosu.setRowCount(len(konular))
        self.icerik_tablosu.setColumnCount(1)
        self.icerik_tablosu.setHorizontalHeaderLabels(["Konular"])
        for i, konu in enumerate(konular):
            self.icerik_tablosu.setItem(i, 0, QTableWidgetItem(konu))
        self.icerik_tablosu.setSelectionMode(QTableWidget.SingleSelection)
        self.icerik_tablosu.setSelectionBehavior(QTableWidget.SelectRows)
        sec_button = QPushButton("Seç")
        sec_button.clicked.connect(self.sec_konu)
        layout.addWidget(self.icerik_tablosu)
        layout.addWidget(sec_button)
        self.setLayout(layout)

    def sec_konu(self):
        selected_items = self.icerik_tablosu.selectedItems()
        if selected_items:
            selected_konu = selected_items[0].text()
            self.parent.secilen_konular.append(f"{self.kurs_adi}: {selected_konu}")
            self.parent.update_secilen_konular()
            print(f"Öğrenci: {self.parent.ogrenci_ismi_entry.text()} {self.parent.ogrenci_soyismi_entry.text()}, Eğitmen: {self.egitmen}, Ders: {self.kurs_adi}, Konu: {selected_konu}")
            self.accept()

class KursArayuzu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Online Eğitim Platformu")
        self.setGeometry(100, 100, 800, 600)
        self.secilen_konular = []

        # Eğitmen isimleri ve diğer ayarlamalar
        isimler = ["Elif Kaya", "Emre Demir", "Ayşe Öztürk", "Mehmet Yılmaz", "Deniz Aktaş", "Cemile Arslan", "Seda Altın", "Can Polat",
                   "Lale Tekin", "Sinan Çetin", "Banu Koç", "Kaan Gül", "Zeynep Dağ", "Onur Kurt", "Dilara Aydın", "Eren Duman",
                   "Pelin Vural", "Serkan Demirtaş", "Nihal Sarı", "Tahir Ulu", "Nesrin Kartal", "Volkan Korkmaz", "Derya Uzun",
                   "Barış Elmas", "Sibel Karaca", "Murat Tezcan", "Fatma Çelik", "İlker Başar"]
        random.shuffle(isimler)  # İsimler karıştırılıyor

        self.kurs_konular = {
            "Matematik": ["Algebra", "Kalkülüs", "Geometri", "İstatistik", "Trigonometri", "Analitik Geometri"],
            "Türkçe": ["Dil Bilgisi", "Edebiyat", "Yazım Kuralları", "Şiir", "Anlatım Bozuklukları", "Deyimler ve Atasözleri"],
            "Fizik": ["Dinamik", "Statik", "Optik", "Elektrik", "Magnetizma", "Modern Fizik"],
            "Kimya": ["Organik Kimya", "Anorganik Kimya", "Asitler ve Bazlar", "Redoks Reaksiyonları", "Kimyasal Bağlar", "Çözeltiler"],
            "Biyoloji": ["Hücre Biyolojisi", "Genetik", "Evolüsyon", "Ekoloji", "Anatomi", "Fizyoloji"],
            "Tarih": ["Kurtuluş Savaşı", "Osmanlı Tarihi", "Çağdaş Türk ve Dünya Tarihi", "İnkılap Tarihi", "Ortaçağ Avrupası", "Türk İslam Tarihi"],
            "Coğrafya": ["Fiziki Coğrafya", "Beşeri Coğrafya", "Türkiye Coğrafyası", "Küresel Sorunlar", "İklim Bilimi", "Doğal Kaynaklar"]
        }

        self.grid_layout = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

        self.ogrenci_ismi_label = QLabel("Öğrenci İsmi:")
        self.ogrenci_ismi_entry = QLineEdit()
        self.ogrenci_soyismi_label = QLabel("Öğrenci Soyismi:")
        self.ogrenci_soyismi_entry = QLineEdit()
        self.eposta_label = QLabel("Öğrenci E-posta:")
        self.eposta_entry = QLineEdit()

        self.kurs_adi_label = QLabel("Kurs Adı:")
        self.kurs_adi_combo = QComboBox()
        self.kurs_adi_combo.addItems(list(self.kurs_konular.keys()))
        self.kurs_adi_combo.currentIndexChanged.connect(self.update_egitmenler)

        self.egitmen_ismi_label = QLabel("Eğitmen İsmi:")
        self.egitmen_ismi_combo = QComboBox()

        self.ders_icerigi_button = QPushButton("Ders İçeriğini Göster")
        self.ders_icerigi_button.clicked.connect(self.goster_icerik)

        self.kaydol_button = QPushButton("Kaydol")
        self.kaydol_button.clicked.connect(self.kayit_basarili)

        self.secilen_konular_label = QLabel("Seçilen Dersler:")
        self.secilen_konular_display = QLabel("")
        self.secilen_konular_display.setWordWrap(True)

        self.grid_layout.addWidget(self.ogrenci_ismi_label, 0, 0)
        self.grid_layout.addWidget(self.ogrenci_ismi_entry, 0, 1)
        self.grid_layout.addWidget(self.ogrenci_soyismi_label, 1, 0)
        self.grid_layout.addWidget(self.ogrenci_soyismi_entry, 1, 1)
        self.grid_layout.addWidget(self.eposta_label, 2, 0)
        self.grid_layout.addWidget(self.eposta_entry, 2, 1)
        self.grid_layout.addWidget(self.kurs_adi_label, 3, 0)
        self.grid_layout.addWidget(self.kurs_adi_combo, 3, 1)
        self.grid_layout.addWidget(self.egitmen_ismi_label, 4, 0)
        self.grid_layout.addWidget(self.egitmen_ismi_combo, 4, 1)
        self.grid_layout.addWidget(self.ders_icerigi_button, 5, 0, 1, 2)
        self.grid_layout.addWidget(self.secilen_konular_label, 6, 0)
        self.grid_layout.addWidget(self.secilen_konular_display, 6, 1)
        self.grid_layout.addWidget(self.kaydol_button, 7, 1)

        self.update_egitmenler()

    def kayit_basarili(self):
        QMessageBox.information(self, "Kayıt Başarılı", "Kurs kaydınız başarıyla tamamlanmıştır.")
        print(f"Öğrenci: {self.ogrenci_ismi_entry.text()} {self.ogrenci_soyismi_entry.text()}, Eğitmen: {self.egitmen_ismi_combo.currentText()}, Ders: {self.kurs_adi_combo.currentText()}")

    def goster_icerik(self):
        kurs_adi = self.kurs_adi_combo.currentText()
        konular = random.sample(self.kurs_konular[kurs_adi], len(self.kurs_konular[kurs_adi]))
        egitmen = self.egitmen_ismi_combo.currentText()
        dialog = ContentDialog(kurs_adi, konular, egitmen, self)
        dialog.exec_()

    def update_secilen_konular(self):
        self.secilen_konular_display.setText("\n".join(self.secilen_konular))

    def update_egitmenler(self):
        kurs_adi = self.kurs_adi_combo.currentText()
        egitmen_gruplari = {
            "Matematik": ["Elif Kaya", "Emre Demir", "Ayşe Öztürk", "Mehmet Yılmaz"],
            "Türkçe": ["Deniz Aktaş", "Cemile Arslan", "Seda Altın", "Can Polat"],
            "Fizik": ["Lale Tekin", "Sinan Çetin", "Banu Koç", "Kaan Gül"],
            "Kimya": ["Zeynep Dağ", "Onur Kurt", "Dilara Aydın", "Eren Duman"],
            "Biyoloji": ["Pelin Vural", "Serkan Demirtaş", "Nihal Sarı", "Tahir Ulu"],
            "Tarih": ["Nesrin Kartal", "Volkan Korkmaz", "Derya Uzun", "Barış Elmas"],
            "Coğrafya": ["Sibel Karaca", "Murat Tezcan", "Fatma Çelik", "İlker Başar"]
        }
        self.egitmen_ismi_combo.clear()
        self.egitmen_ismi_combo.addItems(egitmen_gruplari[kurs_adi])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arayuz = KursArayuzu()
    arayuz.show()
    sys.exit(app.exec_())
