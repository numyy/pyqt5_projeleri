from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTextEdit, \
    QHBoxLayout, QLineEdit, QTableWidgetItem, QSpinBox, QMessageBox

from collection_create_window import CollectionCreateWindow
from collection_edit_window import CollectionEditWindow
from details_window import DetailsWindow
from game import Game
from player import Player


class GameManagerWindow(QMainWindow):
    def __init__(self, player_name):
        super().__init__()
        self.setWindowTitle("Video Oyun Koleksiyonu Yönetimi")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.player_label = QLabel(f"Oyuncu: {player_name}")
        main_layout.addWidget(self.player_label)

        create_collection_button = QPushButton("Koleksiyon Oluştur")
        create_collection_button.clicked.connect(self.open_collection_create)
        main_layout.addWidget(create_collection_button)

        # Koleksiyonlar bölümü
        collections_layout = QVBoxLayout()
        main_layout.addLayout(collections_layout)

        collections_label = QLabel("Koleksiyonlar")
        collections_layout.addWidget(collections_label)

        edit_collection_button = QPushButton("Seçili Koleksiyonu Düzenle")
        edit_collection_button.clicked.connect(self.open_collection_edit)
        main_layout.addWidget(edit_collection_button)

        self.collections_table = QTableWidget()
        self.collections_table.setColumnCount(4)
        self.collections_table.setHorizontalHeaderLabels(
            ["Koleksiyon Adı", "Oyuncu Adı", "Oyun Sayısı", "Değerlendirme"])
        collections_layout.addWidget(self.collections_table)

        # Koleksiyon detayları bağlantısı
        self.collections_table.itemDoubleClicked.connect(self.show_details_window)

        rate_layout = QHBoxLayout()
        main_layout.addLayout(rate_layout)

        rate_label = QLabel("Seçili Koleksiyonu Değerlendir:")
        rate_layout.addWidget(rate_label)

        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 5)
        rate_layout.addWidget(self.rating_input)

        self.recommendation_input = QLineEdit()
        rate_layout.addWidget(self.recommendation_input)

        rate_button = QPushButton("Değerlendir ve Öner")
        rate_button.clicked.connect(self.rate_and_recommend)
        rate_layout.addWidget(rate_button)

        self.player = Player(player_name)
        self.collections = []

        game1 = Game("Oyun 1", "Aksiyon", "PC")
        game2 = Game("Oyun 2", "Macera", "PlayStation")
        game3 = Game("Oyun 3", "RPG", "Xbox")
        game4 = Game("Oyun 4", "Strateji", "PC")
        game5 = Game("Oyun 5", "RPG", "PlayStation")
        game6 = Game("Oyun 6", "Macera", "Xbox")
        game7 = Game("Oyun 7", "Spor", "PC")
        game8 = Game("Oyun 8", "Spor", "PlayStation")

        collection1 = {"name": "Aksiyon Oyunları", "player": "Oyuncu 1", "games": [game1, game2, game3]}
        collection2 = {"name": "RPG Koleksiyonu", "player": "Oyuncu 2", "games": [game4, game5, game6]}
        collection3 = {"name": "Spor Oyunları", "player": "Oyuncu 3", "games": [game7, game8]}

        self.collections.extend([collection1, collection2, collection3])

        for collection in self.collections:
            row_count = self.collections_table.rowCount()
            self.collections_table.insertRow(row_count)
            self.collections_table.setItem(row_count, 0, QTableWidgetItem(collection["name"]))
            self.collections_table.setItem(row_count, 1, QTableWidgetItem(collection["player"]))
            self.collections_table.setItem(row_count, 2, QTableWidgetItem(str(len(collection["games"]))))
            rating = collection.get("rating", 0)
            rating_text = str(rating) if rating > 0 else "Değerlendirilmemiş"
            self.collections_table.setItem(row_count, 3, QTableWidgetItem(rating_text))
        self.selected_collection = None

    def open_collection_create(self):
        self.collection_create_window = CollectionCreateWindow(self.player, parent=self)
        self.collection_create_window.show()

    def add_collection(self, new_collection):
        self.collections.append(new_collection)
        row_count = self.collections_table.rowCount()
        self.collections_table.insertRow(row_count)
        self.collections_table.setItem(row_count, 0, QTableWidgetItem(new_collection["name"]))
        self.collections_table.setItem(row_count, 1, QTableWidgetItem(new_collection["player"]))
        self.collections_table.setItem(row_count, 2, QTableWidgetItem(str(len(new_collection["games"]))))

        self.update_collection_rating(new_collection)

        # Favori oyunları güncelle
        for game_name in new_collection["favorite_games"]:
            game = Game(game_name, "", "")
            self.player.favorite_games.append(game)

    def create_collection(self):
        if self.new_collection:
            collection_name = self.name_input.text()
            player_name = self.player_input.text()
            if collection_name and player_name:
                rating = self.rating_input.value()
                recommendation = self.recommendation_input.text()
                new_collection = {
                    "name": collection_name,
                    "player": player_name,
                    "games": [game.name for game in self.new_collection.games],
                    "rating": rating,
                    "recommendation": recommendation
                }
                self.parent.add_collection(new_collection)
                self.close()
            else:
                QMessageBox.warning(self, "Uyarı", "Lütfen koleksiyon adı ve oyuncu adı girin.")

    def rate_and_recommend(self):
        if self.selected_collection:
            rating = self.rating_input.value()
            recommendation = self.recommendation_input.text()
            self.selected_collection["rating"] = rating
            self.selected_collection["recommendation"] = recommendation
            self.update_collection_rating(self.selected_collection)

    def show_details_window(self, item):
        if item:
            self.selected_collection = self.collections[item.row()]
        self.details_window = DetailsWindow(self.selected_collection, self.player, parent=self)
        self.details_window.show()

    def update_collection_rating(self, collection):
        for row in range(self.collections_table.rowCount()):
            item = self.collections_table.item(row, 0)
            if item and item.text() == collection["name"]:
                rating = collection.get("rating", 0)
                rating_text = str(rating) if rating > 0 else "Değerlendirilmemiş"
                self.collections_table.setItem(row, 3, QTableWidgetItem(rating_text))
                break

    def open_collection_edit(self):
        if self.selected_collection:
            self.edit_window = CollectionEditWindow(self.selected_collection, parent=self)
            self.edit_window.show()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir koleksiyon seçin.")

    def update_collection(self, updated_collection):
        row_index = -1
        for i, collection in enumerate(self.collections):
            if collection["name"] == updated_collection["name"]:
                self.collections[i] = updated_collection
                row_index = i
                break

        self.collections_table.clearContents()
        self.collections_table.setRowCount(0)  # Tüm satırları sil

        for row, collection in enumerate(self.collections):
            self.collections_table.insertRow(row)
            self.collections_table.setItem(row, 0, QTableWidgetItem(collection["name"]))
            self.collections_table.setItem(row, 1, QTableWidgetItem(collection["player"]))
            self.collections_table.setItem(row, 2, QTableWidgetItem(str(len(collection["games"]))))
            rating = collection.get("rating", 0)
            rating_text = str(rating) if rating > 0 else "Değerlendirilmemiş"
            self.collections_table.setItem(row, 3, QTableWidgetItem(rating_text))

        if row_index != -1:
            self.collections_table.selectRow(row_index)  # Güncellenmiş koleksiyonun satırını seç