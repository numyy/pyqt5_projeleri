from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QComboBox, QPushButton, \
    QMessageBox

from game import Game


class CollectionEditWindow(QWidget):
    def __init__(self, collection, parent=None):
        super().__init__()
        self.setWindowTitle("Koleksiyon Düzenle")
        self.setGeometry(100, 100, 600, 400)
        self.collection = collection
        self.parent = parent

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Koleksiyon adı
        name_layout = QHBoxLayout()
        main_layout.addLayout(name_layout)
        name_label = QLabel("Koleksiyon Adı:")
        name_layout.addWidget(name_label)
        self.name_input = QLineEdit(collection["name"])
        name_layout.addWidget(self.name_input)

        # Oyunlar
        games_layout = QVBoxLayout()
        main_layout.addLayout(games_layout)
        games_label = QLabel("Oyunlar")
        games_layout.addWidget(games_label)
        self.game_list = QListWidget()
        self.update_game_list()
        games_layout.addWidget(self.game_list)

        # Oyun düzenleme
        edit_game_layout = QHBoxLayout()
        games_layout.addLayout(edit_game_layout)
        self.game_name_input = QLineEdit()
        edit_game_layout.addWidget(self.game_name_input)
        self.genre_input = QComboBox()
        self.genre_input.addItems(["Açık Dünya", "Macera", "RPG", "Strateji", "Spor", "MMO", "FPS", "Rogue Like"])
        edit_game_layout.addWidget(self.genre_input)
        self.platform_input = QComboBox()
        self.platform_input.addItems(["PC", "PlayStation", "Xbox", "Nintendo"])
        edit_game_layout.addWidget(self.platform_input)
        edit_button = QPushButton("Düzenle")
        edit_button.clicked.connect(self.edit_game)
        edit_game_layout.addWidget(edit_button)
        remove_button = QPushButton("Kaldır")
        remove_button.clicked.connect(self.remove_game)
        edit_game_layout.addWidget(remove_button)

        # Oyun ekleme
        add_game_layout = QHBoxLayout()
        games_layout.addLayout(add_game_layout)
        add_game_button = QPushButton("Oyun Ekle")
        add_game_button.clicked.connect(self.add_game)
        add_game_layout.addWidget(add_game_button)

        # Butonu kaydetme
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_changes)
        main_layout.addWidget(save_button)

    def update_game_list(self):
        self.game_list.clear()
        for game in self.collection["games"]:
            game_info = f"{game.name} ({game.genre}) - {game.platform}"
            self.game_list.addItem(game_info)

    def add_game(self):
        game_name = self.game_name_input.text()
        game_genre = self.genre_input.currentText()
        game_platform = self.platform_input.currentText()

        if game_name and game_genre and game_platform:
            new_game = Game(game_name, game_genre, game_platform)
            self.collection["games"].append(new_game)
            self.update_game_list()
            self.game_name_input.clear()
            self.genre_input.setCurrentIndex(0)
            self.platform_input.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen oyun adı, tür ve platform bilgilerini girin.")
    def edit_game(self):
        selected_items = self.game_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            row = self.game_list.row(selected_item)
            game = self.collection["games"][row]

            new_name = self.game_name_input.text()
            new_genre = self.genre_input.currentText()
            new_platform = self.platform_input.currentText()

            if new_name:
                game.name = new_name
            if new_genre:
                game.genre = new_genre
            if new_platform:
                game.platform = new_platform

            self.update_game_list()

    def remove_game(self):
        selected_items = self.game_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            row = self.game_list.row(selected_item)
            self.collection["games"].pop(row)
            self.update_game_list()

    def save_changes(self):
        new_name = self.name_input.text()
        if new_name:
            self.collection["name"] = new_name
        self.parent.update_collection(self.collection)
        self.close()