import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
from datetime import datetime, timedelta
from musaitlik_takvimi import MusaitlikTakvimi

hastalar = []
doktorlar = [
    {"isim": "Ahmet Kaya", "uzmanlık_alani": "Dahiliye", "musaitlik_durumu": True, "musaitlik_takvimi": []},
    {"isim": "Mehmet Öz", "uzmanlık_alani": "Kardiyoloji", "musaitlik_durumu": True, "musaitlik_takvimi": []},
    {"isim": "Fatma Şahin", "uzmanlık_alani": "Göz Hastalıkları", "musaitlik_durumu": True, "musaitlik_takvimi": []},
    {"isim": "Ali Demir", "uzmanlık_alani": "Ortopedi", "musaitlik_durumu": True, "musaitlik_takvimi": []},
    {"isim": "Ayşe Yılmaz", "uzmanlık_alani": "Kulak Burun Boğaz", "musaitlik_durumu": True, "musaitlik_takvimi": []},
    {"isim": "Hasan Çelik", "uzmanlık_alani": "Nöroloji", "musaitlik_durumu": True, "musaitlik_takvimi": []},
    {"isim": "Zeynep Aksoy", "uzmanlık_alani": "Çocuk Hastalıkları", "musaitlik_durumu": True, "musaitlik_takvimi": []},
    {"isim": "Mustafa Kara", "uzmanlık_alani": "Dermatoloji", "musaitlik_durumu": True},
    {"isim": "Elif Öztürk", "uzmanlık_alani": "Kadın Hastalıkları ve Doğum", "musaitlik_durumu": True, "musaitlik_takvimi": []},
    {"isim": "Mert Aydın", "uzmanlık_alani": "Üroloji", "musaitlik_durumu": True, "musaitlik_takvimi": []}
]

class RandevuSistemi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hastane Randevu Sistemi")
        self.setGeometry(100, 100, 400, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()

        # Hasta Seçimi
        self.hasta_isim_label = QLabel("Hasta İsmi:")
        self.hasta_isim_input = QLineEdit()
        self.hasta_soyisim_label = QLabel("Hasta Soyismi:")
        self.hasta_soyisim_input = QLineEdit()
        self.hasta_tc_label = QLabel("TC Numarası (11 Haneli):")
        self.hasta_tc_input = QLineEdit()
        self.hasta_tc_layout = QHBoxLayout()
        self.hasta_tc_layout.addWidget(self.hasta_isim_label)
        self.hasta_tc_layout.addWidget(self.hasta_isim_input)
        self.hasta_tc_layout.addWidget(self.hasta_soyisim_label)
        self.hasta_tc_layout.addWidget(self.hasta_soyisim_input)
        self.hasta_tc_layout.addWidget(self.hasta_tc_label)
        self.hasta_tc_layout.addWidget(self.hasta_tc_input)

        # Doktor Seçimi
        self.doktor_label = QLabel("Doktor Seçimi:")
        self.doktor_combobox = QComboBox()
        for doktor in doktorlar:
            self.doktor_combobox.addItem(f"{doktor['isim']} - {doktor['uzmanlık_alani']}")
        self.doktor_layout = QHBoxLayout()
        self.doktor_layout.addWidget(self.doktor_label)
        self.doktor_layout.addWidget(self.doktor_combobox)

        # Randevu Tarihi
        self.tarih_label = QLabel("Randevu Tarihi (gg/aa/yyyy):")
        self.tarih_input = QLineEdit()
        self.tarih_layout = QHBoxLayout()
        self.tarih_layout.addWidget(self.tarih_label)
        self.tarih_layout.addWidget(self.tarih_input)

        # Randevu Saati
        self.saat_label = QLabel("Randevu Saati (hh:mm):")
        self.saat_input = QLineEdit()
        self.saat_layout = QHBoxLayout()
        self.saat_layout.addWidget(self.saat_label)
        self.saat_layout.addWidget(self.saat_input)

        # Butonlar
        self.randevu_al_button = QPushButton("Randevu Al")
        self.randevu_al_button.clicked.connect(self.randevu_al)
        self.randevu_iptal_button = QPushButton("Randevu İptal")
        self.randevu_iptal_button.clicked.connect(self.randevu_iptal)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.randevu_al_button)
        self.button_layout.addWidget(self.randevu_iptal_button)

        # Randevu Geçmişi
        self.randevu_gecmisi_label = QLabel("Randevu Geçmişi:")
        self.randevu_gecmisi_list = QListWidget()
        self.randevu_gecmisi_layout = QVBoxLayout()
        self.randevu_gecmisi_layout.addWidget(self.randevu_gecmisi_label)
        self.randevu_gecmisi_layout.addWidget(self.randevu_gecmisi_list)

        self.main_layout.addLayout(self.hasta_tc_layout)
        self.main_layout.addLayout(self.doktor_layout)
        self.main_layout.addLayout(self.tarih_layout)
        self.main_layout.addLayout(self.saat_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.randevu_gecmisi_layout)
        self.central_widget.setLayout(self.main_layout)

        # Müsaitlik Takvimi Bağlantı Kısmı
        self.doktor_combobox.currentIndexChanged.connect(self.musaitlik_takvimi_goster)

    def musaitlik_takvimi_goster(self, index):
        if index >= 0:
            doktor = doktorlar[index]
            musaitlik_takvimi = MusaitlikTakvimi(doktor, self)
            musaitlik_takvimi.show()

    def randevu_al(self):
        hasta_isim = self.hasta_isim_input.text()
        hasta_soyisim = self.hasta_soyisim_input.text()
        hasta_tc = self.hasta_tc_input.text()
        if len(hasta_tc) != 11:
            QMessageBox.warning(self, "Uyarı", "TC numarası 11 haneli olmalıdır.")
            return
        if hasta_isim and hasta_soyisim and hasta_tc:
            hasta = next((h for h in hastalar if h["tc"] == hasta_tc), None)
            if hasta is None:
                hasta = {"isim": hasta_isim, "soyisim": hasta_soyisim, "tc": hasta_tc, "randevu_gecmisi": []}
                hastalar.append(hasta)
            else:
                QMessageBox.warning(self, "Uyarı", "Bu hasta zaten kayıtlı.")

            secilen_doktor_index = self.doktor_combobox.currentIndex()
            doktor = doktorlar[secilen_doktor_index]

            tarih_str = self.tarih_input.text()
            try:
                randevu_tarihi = datetime.strptime(tarih_str, "%d/%m/%Y")
            except ValueError:
                QMessageBox.warning(self, "Uyarı", "Tarih formatı geçersiz. (gg/aa/yyyy)")
                return

            bugun = datetime.now().date()
            if randevu_tarihi.date() < bugun:
                QMessageBox.warning(self, "Uyarı", "Geçmiş bir tarih için randevu alamazsınız.")
                return

            if randevu_tarihi in doktor["musaitlik_takvimi"]:
                QMessageBox.warning(self, "Uyarı", "Seçilen doktor bu tarihte müsait değil.")
                return

            saat_str = self.saat_input.text()
            try:
                randevu_saati = datetime.strptime(saat_str, "%H:%M").time()
                randevu_tarihi = datetime.combine(randevu_tarihi.date(), randevu_saati)
            except ValueError:
                QMessageBox.warning(self, "Uyarı", "Saat formatı geçersiz. (hh:mm)")
                return

            if randevu_tarihi in [datetime.combine(tarih.date(), tarih.time()) for tarih in
                                  doktor["musaitlik_takvimi"]]:
                QMessageBox.warning(self, "Uyarı", "Seçilen doktor bu tarihte müsait değil.")
                return

            for randevu in hasta["randevu_gecmisi"]:
                if randevu["doktor"] == doktor:
                    son_randevu_tarihi = randevu["tarih"]
                    sekiz_ay_sonra = son_randevu_tarihi + timedelta(days=365 // 12 * 8)
                    if randevu_tarihi < sekiz_ay_sonra:
                        QMessageBox.warning(self, "Uyarı", "Aynı doktora önümüzdeki 8 ay içinde randevu alamazsınız.")
                        return

            randevu = {"tarih": randevu_tarihi, "doktor": doktor, "hasta": hasta}
            hasta["randevu_gecmisi"].append(randevu)
            doktor["musaitlik_takvimi"].append(randevu_tarihi)
            self.randevu_gecmisi_list.addItem(
                f"{randevu_tarihi} - {doktor['isim']} - {hasta['isim']} {hasta['soyisim']}")
            QMessageBox.information(self, "Başarılı", "Randevu başarıyla oluşturuldu.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")

    def randevu_iptal(self):
        hasta_tc = self.hasta_tc_input.text()
        hasta = next((h for h in hastalar if h["tc"] == hasta_tc), None)
        if hasta is None:
            QMessageBox.warning(self, "Uyarı", "Geçersiz TC numarası.")
            return
        if not hasta["randevu_gecmisi"]:
            QMessageBox.warning(self, "Uyarı", "Randevu geçmişiniz boş.")
            return

        selected_item = self.randevu_gecmisi_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen iptal etmek istediğiniz randevuyu seçin.")
            return

        selected_index = self.randevu_gecmisi_list.currentRow()
        iptal_edilen_randevu = hasta["randevu_gecmisi"].pop(selected_index)
        iptal_edilen_randevu["doktor"]["musaitlik_durumu"] = True  # Doktoru tekrar müsait yap
        self.randevu_gecmisi_list.takeItem(selected_index)
        QMessageBox.information(self, "Başarılı", "Randevu başarıyla iptal edildi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    randevu_sistemi = RandevuSistemi()
    randevu_sistemi.show()
    sys.exit(app.exec_())

    from PyQt5.QtGui import QColor, QPainter
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget
    from PyQt5.QtCore import Qt
    from datetime import datetime

    class MusaitlikTakvimi(QWidget):
        def __init__(self, doktor, parent=None):
            super().__init__(parent)
            self.doktor = doktor
            self.setWindowTitle(f"MusaitlikTakvimi_{doktor['isim']}")
            self.setWindowFlags(Qt.Window)

            layout = QVBoxLayout()
            self.takvim = QCalendarWidget()
            self.takvim.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

            for tarih in doktor["musaitlik_takvimi"]:
                self.takvim.setDateTextColor(tarih, QColor(255, 0, 0))

            layout.addWidget(self.takvim)
            self.setLayout(layout)

        def paintCell(self, painter, rect, date):
            super().paintCell(painter, rect, date)

            tarihi = datetime(date.year(), date.month(), date.day())

            for randevu_tarihi in self.doktor["musaitlik_takvimi"]:
                if randevu_tarihi.date() == tarihi.date():
                    painter.setPen(QColor(255, 0, 0))
                    painter.drawText(rect, Qt.AlignCenter, randevu_tarihi.strftime("%H:%M"))