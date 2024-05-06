from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

from game_manager_window import GameManagerWindow


class PlayerRegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oyuncu Kaydı")
        self.setGeometry(100, 100, 300, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        name_layout = QHBoxLayout()
        layout.addLayout(name_layout)
        name_label = QLabel("Oyuncu Adı:")
        name_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)

        register_button = QPushButton("Kayıt Ol")
        register_button.clicked.connect(self.register_player)
        layout.addWidget(register_button)

    def register_player(self):
        player_name = self.name_input.text()
        if player_name:
            self.game_manager_window = GameManagerWindow(player_name)
            self.game_manager_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir oyuncu adı girin.")