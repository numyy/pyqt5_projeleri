import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QMessageBox,
    QFormLayout, QDialog, QDialogButtonBox, QListWidgetItem
)

class Ders:
    def __init__(self, ders_adi, icerik, ogretmen):
        self.ders_adi = ders_adi
        self.icerik = icerik
        self.ogretmen = ogretmen
        self.materyaller = []
        self.sorular = []

    def materyal_yukle(self, materyal):
        self.materyaller.append(materyal)

    def materyal_eris(self):
        return self.materyaller

    def soru_sor(self, soru):
        self.sorular.append(soru)

class Ogrenci:
    def __init__(self, isim, numara):
        self.isim = isim
        self.numara = numara
        self.dersler = []

    def ders_ekle(self, ders):
        self.dersler.append(ders)

    def ders_cikar(self, ders):
        self.dersler.remove(ders)

    def soru_sor(self, ders, soru):
        ders.soru_sor(soru)

class Materyal:
    def __init__(self, materyal_adi, turu, icerik):
        self.materyal_adi = materyal_adi
        self.turu = turu
        self.icerik = icerik

    def icerik_goster(self):
        return self.icerik

class AddCourseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Ders Ekle')
        self.layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.course_name_input = QLineEdit()
        self.content_input = QTextEdit()
        self.teacher_input = QLineEdit()

        form_layout.addRow("Ders Adı:", self.course_name_input)
        form_layout.addRow("İçerik:", self.content_input)
        form_layout.addRow("Öğretmen:", self.teacher_input)

        self.layout.addLayout(form_layout)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_details(self):
        return {
            'course_name': self.course_name_input.text(),
            'content': self.content_input.toPlainText(),
            'teacher': self.teacher_input.text()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eğitim Materyali Paylaşım Platformu")
        self.setGeometry(100, 100, 800, 600)

        # Veri yapısı
        self.courses = []
        self.students = []

        # Ana düzen
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Ders listesi
        self.course_list = QListWidget()
        self.course_list.currentItemChanged.connect(self.display_course_details)
        main_layout.addWidget(QLabel("Dersler:"))
        main_layout.addWidget(self.course_list)

        # Ders ekleme butonu
        self.add_course_button = QPushButton("Ders Ekle")
        self.add_course_button.clicked.connect(self.add_course)
        button_layout.addWidget(self.add_course_button)

        # Materyal ve soruları görüntüleme
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        main_layout.addWidget(QLabel("Ders Detayları:"))
        main_layout.addWidget(self.details_text)

        # Layouts
        main_layout.addLayout(button_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_course(self):
        dialog = AddCourseDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            details = dialog.get_details()
            new_course = Ders(details['course_name'], details['content'], details['teacher'])
            self.courses.append(new_course)
            self.course_list.addItem(details['course_name'])

    def display_course_details(self, current, previous):
        if current:
            course_name = current.text()
            course = next((course for course in self.courses if course.ders_adi == course_name), None)
            if course:
                details = f"Ders Adı: {course.ders_adi}\nİçerik: {course.icerik}\nÖğretmen: {course.ogretmen}\nMateryaller:\n" + "\n".join([m.materyal_adi for m in course.materyaller])
                self.details_text.setText(details)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
