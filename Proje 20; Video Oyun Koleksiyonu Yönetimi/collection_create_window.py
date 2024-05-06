from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLineEdit, QLabel, QVBoxLayout, QListWidget, QHBoxLayout, \
    QComboBox, QWidget, QListWidgetItem, QSpinBox, QInputDialog

from collection import Collection
from game import Game

class CollectionCreateWindow(QWidget):
    def __init__(self, player, parent=None):
        super().__init__()
        self.setWindowTitle("Koleksiyon Oluştur")
        self.setGeometry(100, 100, 600, 400)
        self.player = player
        self.parent = parent

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Koleksiyon adı ve oyuncu adı girişi
        info_layout = QHBoxLayout()
        main_layout.addLayout(info_layout)

        name_label = QLabel("Koleksiyon Adı:")
        info_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        info_layout.addWidget(self.name_input)

        player_label = QLabel("Oluşturan Oyuncu:")
        info_layout.addWidget(player_label)
        self.player_input = QLineEdit()
        self.player_input.setText(self.player.name)
        self.player_input.setReadOnly(True)
        info_layout.addWidget(self.player_input)

        # Oyun ekleme bölümü
        add_game_layout = QHBoxLayout()
        main_layout.addLayout(add_game_layout)

        name_label = QLabel("Oyun Adı:")
        add_game_layout.addWidget(name_label)
        self.game_name_input = QLineEdit()
        add_game_layout.addWidget(self.game_name_input)

        genre_label = QLabel("Tür:")
        add_game_layout.addWidget(genre_label)
        self.genre_input = QComboBox()
        self.genre_input.addItems(["Açık Dünya", "Macera", "RPG", "Strateji", "Spor","MMO","FPS","Rogue Like"])
        add_game_layout.addWidget(self.genre_input)

        platform_label = QLabel("Platform:")
        add_game_layout.addWidget(platform_label)
        self.platform_input = QComboBox()
        self.platform_input.addItems(["PC", "PlayStation", "Xbox", "Nintendo"])
        add_game_layout.addWidget(self.platform_input)

        add_button = QPushButton("Ekle")
        add_button.clicked.connect(self.add_game)
        add_game_layout.addWidget(add_button)

        # Koleksiyon ve favori oyunlar bölümü
        collection_layout = QHBoxLayout()
        main_layout.addLayout(collection_layout)

        self.game_list = QListWidget()
        collection_layout.addWidget(self.game_list)

        self.favorite_list = QListWidget()  # Favori oyunlar için ayrı bir liste
        collection_layout.addWidget(self.favorite_list)

        favorite_layout = QVBoxLayout()
        collection_layout.addLayout(favorite_layout)

        favorite_label = QLabel("Favori Oyun:")
        favorite_layout.addWidget(favorite_label)
        self.favorite_input = QLineEdit()
        favorite_layout.addWidget(self.favorite_input)
        set_favorite_button = QPushButton("Ekle")
        set_favorite_button.clicked.connect(self.set_favorite_game)
        favorite_layout.addWidget(set_favorite_button)

        create_button = QPushButton("Koleksiyonu Oluştur")
        create_button.clicked.connect(self.create_collection)
        main_layout.addWidget(create_button)

        self.new_collection = None

    def add_game(self):
        name = self.game_name_input.text()
        genre = self.genre_input.currentText()
        platform = self.platform_input.currentText()
        game_info = f"{name} ({genre}) - {platform}"
        self.game_list.addItem(game_info)
        self.game_name_input.clear()

        if self.new_collection is None:
            self.new_collection = Collection()
            self.new_collection.games = []
            self.new_collection.favorite_games = []

        game = Game(name, genre, platform)
        self.new_collection.games.append(game)

    def set_favorite_game(self):
        favorite_game_name = self.favorite_input.text()
        if self.new_collection:
            for game in self.new_collection.games:
                if game.name == favorite_game_name:
                    game_info = f"★ {game.name} ({game.genre}) - {game.platform}"
                    self.favorite_list.addItem(game_info)
                    self.new_collection.favorite_games.append(game)
                    self.favorite_input.clear()
                    break
            else:
                QMessageBox.warning(self, "Uyarı", "Girdiğiniz oyun koleksiyonunuzda bulunamadı.")

    def create_collection(self):
        if self.new_collection:
            collection_name = self.name_input.text()
            player_name = self.player_input.text()
            if collection_name and player_name:
                favorite_games = [game.name for game in self.new_collection.favorite_games]
                new_collection = {
                    "name": collection_name,
                    "player": player_name,
                    "games": self.new_collection.games,
                    "favorite_games": favorite_games,
                    "rating": 0,
                    "recommendation": ""
                }
                self.parent.add_collection(new_collection)
                self.close()
            else:
                QMessageBox.warning(self, "Uyarı", "Lütfen koleksiyon adı ve oyuncu adı girin.")