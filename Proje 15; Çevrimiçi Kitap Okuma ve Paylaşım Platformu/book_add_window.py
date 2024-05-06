from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
import os
import shutil
import json
from PyQt5.QtCore import Qt

books = []

try:
    with open('books.json', 'r') as f:
        books = json.load(f)
except FileNotFoundError:
    pass

class BookAddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Ekle")
        self.setGeometry(200, 200, 800, 500)

        self.book_table = QTableWidget()
        self.book_table.setColumnCount(6)
        self.book_table.setHorizontalHeaderLabels(["Kitap Adı", "Yazar", "Yayınevi", "Sayfa Sayısı", "Tür", "Dosya"])

        try:
            with open('books.json', 'r') as f:
                books = json.load(f)
                for book in books:
                    row_count = self.book_table.rowCount()
                    self.book_table.insertRow(row_count)
                    self.book_table.setItem(row_count, 0, QTableWidgetItem(book['title']))
                    self.book_table.setItem(row_count, 1, QTableWidgetItem(book['author']))
                    self.book_table.setItem(row_count, 2, QTableWidgetItem(book['publisher']))
                    self.book_table.setItem(row_count, 3, QTableWidgetItem(book['page_count']))
                    self.book_table.setItem(row_count, 4, QTableWidgetItem(book['genre']))
                    self.book_table.setItem(row_count, 5, QTableWidgetItem(book['file_name']))
                    self.book_table.item(row_count, 5).setData(Qt.UserRole, book['file_path'])
                    book_files_dir = os.path.join(os.getcwd(), "book_files")
                    if not os.path.exists(book_files_dir):
                        os.makedirs(book_files_dir)
                    source_path = book['file_path']
                    file_name = os.path.basename(source_path)
                    destination_path = os.path.join(book_files_dir, file_name)
                    shutil.copy(source_path, destination_path)
        except FileNotFoundError:
            pass

        self.save_books()

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.book_title_input = QLineEdit(placeholderText="Kitap Adı")
        self.author_input = QLineEdit(placeholderText="Yazar")
        self.publisher_input = QLineEdit(placeholderText="Yayınevi")
        self.page_count_input = QLineEdit(placeholderText="Sayfa Sayısı")
        self.genre_input = QLineEdit(placeholderText="Tür")
        add_book_button = QPushButton("Kitap Ekle")
        add_book_button.clicked.connect(self.add_book)
        upload_file_button = QPushButton("Dosya Yükle")
        upload_file_button.clicked.connect(self.upload_file)

        remove_book_button = QPushButton("Kitap Sil")
        remove_book_button.clicked.connect(self.remove_book)

        layout.addWidget(QLabel("Kitap Adı:"))
        layout.addWidget(self.book_title_input)
        layout.addWidget(QLabel("Yazar:"))
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel("Yayınevi:"))
        layout.addWidget(self.publisher_input)
        layout.addWidget(QLabel("Sayfa Sayısı:"))
        layout.addWidget(self.page_count_input)
        layout.addWidget(QLabel("Tür:"))
        layout.addWidget(self.genre_input)
        layout.addWidget(upload_file_button)
        layout.addWidget(add_book_button)
        layout.addWidget(remove_book_button)
        layout.addWidget(self.book_table)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.uploaded_file_path = None

    def add_book(self):
        book_title = self.book_title_input.text()
        author = self.author_input.text()
        publisher = self.publisher_input.text()
        page_count = self.page_count_input.text()
        genre = self.genre_input.text()
        file_name = os.path.basename(self.uploaded_file_path) if self.uploaded_file_path else ""
        file_path = self.uploaded_file_path

        row_count = self.book_table.rowCount()
        self.book_table.insertRow(row_count)
        self.book_table.setItem(row_count, 0, QTableWidgetItem(book_title))
        self.book_table.setItem(row_count, 1, QTableWidgetItem(author))
        self.book_table.setItem(row_count, 2, QTableWidgetItem(publisher))
        self.book_table.setItem(row_count, 3, QTableWidgetItem(page_count))
        self.book_table.setItem(row_count, 4, QTableWidgetItem(genre))
        self.book_table.setItem(row_count, 5, QTableWidgetItem(file_name))
        self.book_table.item(row_count, 5).setData(Qt.UserRole, file_path)

        self.book_title_input.clear()
        self.author_input.clear()
        self.publisher_input.clear()
        self.page_count_input.clear()
        self.genre_input.clear()
        self.uploaded_file_path = None

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seçin", "", "PDF Dosyaları (*.pdf)")
        if file_path:
            self.uploaded_file_path = file_path

            # Dosyanın bir kopyasını uygulama klasörüne kaydet
            book_files_dir = os.path.join(os.getcwd(), "book_files")
            if not os.path.exists(book_files_dir):
                os.makedirs(book_files_dir)
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(book_files_dir, file_name)
            try:
                shutil.copy(file_path, destination_path)
            except shutil.Error:
                print(f"Dosya kopyalama işlemi başarısız: {file_path}")
            except IOError:
                print(f"Dosya kopyalama işlemi başarısız: {file_path}")

    def save_books(self):
        books = []
        for row in range(self.book_table.rowCount()):
            book = {
                'title': self.book_table.item(row, 0).text(),
                'author': self.book_table.item(row, 1).text(),
                'publisher': self.book_table.item(row, 2).text(),
                'page_count': self.book_table.item(row, 3).text(),
                'genre': self.book_table.item(row, 4).text(),
                'file_name': self.book_table.item(row, 5).text(),
                'file_path': self.book_table.item(row, 5).data(Qt.UserRole)
            }
            books.append(book)

        with open('books.json', 'w') as f:
            json.dump(books, f)

    def remove_book(self):
        selected_row = self.book_table.currentRow()
        if selected_row >= 0:
            book_file_path = self.book_table.item(selected_row, 5).data(Qt.UserRole)
            book_file_name = os.path.basename(book_file_path)
            book_files_dir = os.path.join(os.getcwd(), "book_files")
            file_path = os.path.join(book_files_dir, book_file_name)

            reply = QMessageBox.question(self, "Kitap Sil",
                                         f"{self.book_table.item(selected_row, 0).text()} adlı kitabı silmek istediğinizden emin misiniz?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    os.remove(file_path)
                    self.book_table.removeRow(selected_row)
                except FileNotFoundError:
                    QMessageBox.warning(self, "Hata", f"{book_file_name} dosyası bulunamadı.")
                except Exception as e:
                    QMessageBox.warning(self, "Hata", str(e))

    def closeEvent(self, event):
        self.save_books()
        event.accept()