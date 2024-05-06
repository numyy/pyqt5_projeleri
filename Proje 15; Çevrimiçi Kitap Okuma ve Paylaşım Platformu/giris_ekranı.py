from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit,QMessageBox
from book_add_window import BookAddWindow
from kitap_okuma_penceresi import BookReadWindow
from yorum_penceresi import CommentWindow
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Okuma Uygulaması")
        self.setGeometry(100, 100, 300, 300)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin123":
            # Admin girişi, ana ekranı göster
            self.main_window = MainWindow(username, is_admin=True)
            self.main_window.show()
            self.close()
        elif username == "kullanıcı1903" and password == "12345":
            # Kullanıcı girişi, ana ekranı göster
            self.main_window = MainWindow(username, is_admin=False)
            self.main_window.show()
            self.close()
        else:
            # Yanlış bilgiler girildi, hata mesajı göster
            QMessageBox.warning(self, "Hata", "Girdiğiniz Bilgiler Yanlış.")

class MainWindow(QMainWindow):
    def __init__(self, username, is_admin):
        super().__init__()
        self.setWindowTitle("Kitap Okuma Uygulaması")
        self.setGeometry(100, 100, 260, 400)

        self.username = username
        self.is_admin = is_admin

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        if self.is_admin:
            add_book_button = QPushButton("Kitap Ekle")
            add_book_button.setFixedSize(250, 150)
            add_book_button.clicked.connect(self.show_book_add_window)
            main_layout.addWidget(add_book_button)

        read_book_button = QPushButton("Kitap Oku")
        read_book_button.setFixedSize(250, 150)
        read_book_button.clicked.connect(self.show_book_read_window)
        main_layout.addWidget(read_book_button)

        comment_button = QPushButton("Yorum Yap")
        comment_button.setFixedSize(250, 150)
        comment_button.clicked.connect(self.show_comment_window)
        main_layout.addWidget(comment_button)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.book_add_window = None
        self.comment_window = None

    def show_book_add_window(self):
        if not self.book_add_window:
            self.book_add_window = BookAddWindow()
        self.book_add_window.show()

    def show_book_read_window(self):
        self.book_read_window = BookReadWindow()
        self.book_read_window.show()

    def show_comment_window(self):
        if not self.comment_window:
            self.comment_window = CommentWindow(self.username)
        self.comment_window.show()