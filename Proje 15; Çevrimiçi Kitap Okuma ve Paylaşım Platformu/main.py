import sys
from PyQt5.QtWidgets import QApplication
from giris_ekranı import LoginWindow
from book_add_window import BookAddWindow
from kitap_okuma_penceresi import BookReadWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())