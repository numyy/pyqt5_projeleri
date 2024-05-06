from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QMessageBox, QLabel, QLineEdit, QHBoxLayout, QPushButton

class DetailsWindow(QWidget):
    def __init__(self, collection, player, parent=None):
        super().__init__()
        self.setWindowTitle("Koleksiyon Detayları")
        self.setGeometry(100, 100, 600, 400)
        self.collection = collection
        self.player = player

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        details_text = f"Koleksiyon Adı: {collection['name']}\n"
        details_text += f"Oluşturan Oyuncu: {collection['player']}\n"
        details_text += "Oyunlar:\n"

        favorite_games = []
        if "favorite_games" in collection:
            favorite_games = collection["favorite_games"]
        elif hasattr(player, "favorite_games"):
            favorite_games = [game.name for game in player.favorite_games]

        for game in collection["games"]:
            is_favorite = game.name in favorite_games
            favorite_symbol = "★ " if is_favorite else ""
            details_text += f"- {favorite_symbol}{game.name} ({game.genre}) - {game.platform}\n"

        details_text += f"\nOyun Sayısı: {len(collection['games'])}\n"

        if "rating" in collection:
            details_text += f"Değerlendirme: {collection['rating']}\n"

        if "recommendation" in collection:
            details_text += f"Öneri: {collection['recommendation']}\n"

        details_text_edit = QTextEdit()
        details_text_edit.setPlainText(details_text)
        details_text_edit.setReadOnly(True)
        main_layout.addWidget(details_text_edit)

    def get_recommendations(self, collection):
        recommendations = []
        if "rating" in collection and collection["rating"] >= 4:
            for other_collection in self.player.collection.games:
                for game in other_collection["games"]:
                    if game not in collection["games"]:
                        recommendations.append(game)
        return recommendations