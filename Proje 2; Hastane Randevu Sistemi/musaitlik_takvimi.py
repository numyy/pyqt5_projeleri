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