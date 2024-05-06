from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QCursor
import json
import os
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage
import fitz
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

class BookCoverLabel(QLabel):
    def __init__(self, book_file_path, parent_window, parent=None):
        super().__init__(parent)
        self.book_file_path = book_file_path
        self.parent_window = parent_window  # Store the reference
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        book_file_path = os.path.join(os.getcwd(), "book_files", self.book_file_path)
        if os.path.exists(book_file_path):
            self.parent_window.show_pdf(book_file_path)  # Call show_pdf on the instance
        else:
            print(f"Dosya bulunamadı: {book_file_path}")

class BookReadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Oku")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        grid_layout = QGridLayout()

        # books.json dosyasından kitap bilgilerini okuyun
        with open('books.json', 'r') as f:
            books = json.load(f)

        row, col = 0, 0
        max_cols = 3  # Yan yana gösterilecek maksimum kitap sayısı

        for book in books:
            book_widget = QWidget()
            layout = QVBoxLayout()

            # Kitap kapağını (pdf'in ilk sayfasını) göster
            book_file_path = os.path.join(os.getcwd(), "book_files", book["file_name"])
            pdf_file = fitz.open(book_file_path)
            page = pdf_file[0]  # PDF dosyasının ilk sayfası
            pix = page.get_pixmap()
            cover_image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            cover_image_label = BookCoverLabel(book["file_name"], self, self)
            cover_image_label.setPixmap(QPixmap.fromImage(cover_image).scaled(200, 300, Qt.KeepAspectRatio))

            # Kitap başlığı ve yazar ismini birleştir
            book_title_author_label = QLabel(f"{book['title']}\n{book['author']}")
            font = QFont()
            font.setPointSize(12)
            book_title_author_label.setFont(font)

            layout.addWidget(cover_image_label)
            layout.addWidget(book_title_author_label, 0, Qt.AlignTop)

            book_widget.setLayout(layout)
            grid_layout.addWidget(book_widget, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

    def open_book(self, file_path):
        self.show_pdf(file_path)

    def show_pdf(self, file_path):
        self.pdf_viewer = QWebEngineView()
        self.pdf_viewer.load(QUrl.fromLocalFile(file_path))
        self.pdf_viewer.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.pdf_viewer.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, False)

        pdf_window = QMainWindow()
        pdf_window.setWindowTitle(os.path.basename(file_path))
        pdf_window.setCentralWidget(self.pdf_viewer)
        pdf_window.resize(1200, 900)

        # PDF yüklendikten sonra pencereyi göster
        self.pdf_viewer.loadFinished.connect(lambda: pdf_window.show())