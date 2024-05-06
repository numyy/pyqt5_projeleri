from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QTextEdit, QLabel, QMessageBox, QLineEdit
import json

class CommentWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Yorum Yap")
        self.setGeometry(100, 100, 800, 600)

        self.load_comments()  # Yorumları yükle
        self.comments_by_user = {}  # Kullanıcı adına göre yorumları gruplandır
        for book_title, comment_data in self.comments.items():
            if isinstance(comment_data, dict):
                for user, comment in comment_data.items():
                    if user not in self.comments_by_user:
                        self.comments_by_user[user] = {}
                    self.comments_by_user[user][book_title] = comment
            else:
                # Eski yorumları tek kullanıcı altında topla
                legacy_user = 'legacy_user'
                if legacy_user not in self.comments_by_user:
                    self.comments_by_user[legacy_user] = {}
                self.comments_by_user[legacy_user][book_title] = comment_data

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Arama çubuğu
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Kitap Ara...")
        self.search_input.textChanged.connect(self.filter_books)
        main_layout.addWidget(self.search_input)

        # Kitap listesi
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(5)
        self.book_table.setHorizontalHeaderLabels(["Kitap Adı", "Yazar", "Yayınevi", "Sayfa Sayısı", "Tür"])
        self.load_books()
        main_layout.addWidget(self.book_table)

        # Yorum yazma alanı
        comment_layout = QHBoxLayout()
        self.comment_text_edit = QTextEdit()
        self.comment_text_edit.setMaximumHeight(100)  # Yorum yazma alanının yüksekliğini sınırlayalım
        comment_layout.addWidget(self.comment_text_edit)
        comment_button = QPushButton("Yorum Yap")
        comment_button.clicked.connect(self.add_comment)
        comment_layout.addWidget(comment_button)
        main_layout.addLayout(comment_layout)

        # Yorumlar alanı
        self.comment_label = QLabel()
        self.comment_label.setWordWrap(True)  # Metni otomatik olarak kaydıralım
        font = self.comment_label.font()
        font.setPointSize(14)  # Font boyutunu artıralım
        self.comment_label.setFont(font)
        main_layout.addWidget(self.comment_label, stretch=1)  # Yorumlar alanını büyütelim

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.update_comment_label()  # Önceki yorumları göster

    def load_books(self):
        try:
            with open('books.json', 'r') as f:
                books = json.load(f)
                self.all_books = books  # Tüm kitapları sakla
                self.filter_books()  # İlk yükleme için kitapları filtrele
        except FileNotFoundError:
            pass

    def filter_books(self):
        search_text = self.search_input.text().lower()
        self.book_table.setRowCount(0)  # Tabloyu temizle

        for book in self.all_books:
            if search_text in book['title'].lower() or \
               search_text in book['author'].lower() or \
               search_text in book['publisher'].lower() or \
               search_text in book['genre'].lower():
                row_count = self.book_table.rowCount()
                self.book_table.insertRow(row_count)
                self.book_table.setItem(row_count, 0, QTableWidgetItem(book['title']))
                self.book_table.setItem(row_count, 1, QTableWidgetItem(book['author']))
                self.book_table.setItem(row_count, 2, QTableWidgetItem(book['publisher']))
                self.book_table.setItem(row_count, 3, QTableWidgetItem(book['page_count']))
                self.book_table.setItem(row_count, 4, QTableWidgetItem(book['genre']))

    def add_comment(self):
        selected_row = self.book_table.currentRow()
        if selected_row >= 0:
            book_title = self.book_table.item(selected_row, 0).text()
            comment_text = self.comment_text_edit.toPlainText()
            if book_title in self.comments:
                if self.username in self.comments[book_title]:
                    QMessageBox.warning(self, "Hata", "Birden fazla yorum yapamazsınız!")
                else:
                    self.comments[book_title][self.username] = comment_text
            else:
                self.comments[book_title] = {self.username: comment_text}
            self.save_comments()
            self.comment_text_edit.clear()
            self.update_comment_label()

    def update_comment_label(self):
        comments_text = ""
        for book_title, user_comments in self.comments.items():
            comments_text += f"({book_title}  kitabına yorum yaptı)<br>"
            for user, comment in user_comments.items():
                comments_text += f"<b>{user}:</b> {comment}<br>"
            comments_text += "<br>"
        self.comment_label.setText(comments_text)

    def load_comments(self):
        try:
            with open('comments.json', 'r') as f:
                self.comments = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.comments = {}
    def save_comments(self):
        with open('comments.json', 'w') as f:
            json.dump(self.comments, f, indent=4)

    def closeEvent(self, event):
        self.save_comments()  # Yorumları kaydet
        event.accept()