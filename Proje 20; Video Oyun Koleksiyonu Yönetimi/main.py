import sys
from PyQt5.QtWidgets import QApplication
from player_registration_window import PlayerRegistrationWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    registration_window = PlayerRegistrationWindow()
    registration_window.show()
    sys.exit(app.exec_())