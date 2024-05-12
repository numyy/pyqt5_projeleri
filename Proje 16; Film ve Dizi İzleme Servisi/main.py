import sys
import os
import pickle
import shutil
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QComboBox,
    QFileDialog,
    QSpinBox,
    QListWidget,
    QSlider,
    QStyle,
    QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import QUrl, QTimer

# Uygulamanın bulunduğu dizini al
app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# mp4_files klasörünün tam yolunu oluştur
media_dir = os.path.join(app_dir, 'mp4_files')

# mp4_files klasörünü oluştur, eğer yoksa
os.makedirs(media_dir, exist_ok=True)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Ekranı")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        font = QFont("Arial", 14, QFont.Bold)

        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_label.setFont(font)
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont("Arial", 14))
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Şifre:")
        self.password_label.setFont(font)
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont("Arial", 14))
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setFont(QFont("Arial", 16))
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.central_widget.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin123":
            self.admin_window = AdminWindow()
            self.admin_window.show()
        elif username == "kullanıcı1903" and password == "12345":
            try:
                with open("data.pickle", "rb") as file:
                    data = pickle.load(file)
            except FileNotFoundError:
                data = []

            self.watch_window = WatchWindow(data)
            self.watch_window.show()
            self.close()  # Giriş penceresini kapat
        else:
            self.error_window = QMessageBox()
            self.error_window.setIcon(QMessageBox.Warning)
            self.error_window.setText("Girdiğiniz bilgiler yanlış. Tekrar deneyiniz.")
            self.error_window.exec_()

class SeasonEpisodeWindow(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sezon ve Bölüm Seçin")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.season_label = QLabel("Sezon:")
        self.season_combo = QComboBox()
        layout.addWidget(self.season_label)
        layout.addWidget(self.season_combo)

        self.episode_label = QLabel("Bölüm:")
        self.episode_combo = QComboBox()
        layout.addWidget(self.episode_label)
        layout.addWidget(self.episode_combo)

        self.watch_button = QPushButton("İZLE")
        self.watch_button.clicked.connect(self.play_episode)
        layout.addWidget(self.watch_button)

        self.setLayout(layout)

        self.data = data
        self.load_seasons()
        self.load_episodes()

    def load_seasons(self):
        seasons = sorted(set(int(item[4]) for item in self.data if item[4] != "-"))
        self.season_combo.clear()
        self.season_combo.addItems([str(season) for season in seasons])
        self.season_combo.currentIndexChanged.connect(self.load_episodes)

    def load_episodes(self):
        selected_season = int(self.season_combo.currentText())
        episodes = set()  # Bölümleri benzersiz bir şekilde tutmak için set kullanıyoruz
        for item in self.data:
            if item[4] != "-" and int(item[4]) == selected_season:
                episodes.add(int(item[5]))

        episodes = sorted(list(episodes))  # Bölümleri sıralıyoruz
        self.episode_combo.clear()
        self.episode_combo.addItems([str(episode) for episode in episodes])

    def play_episode(self):
        selected_season = int(self.season_combo.currentText())
        selected_episode = int(self.episode_combo.currentText())
        matching_files = []
        for item in self.data:
            if item[4] != "-" and int(item[4]) == selected_season and int(item[5]) == selected_episode:
                file_path = item[7]
                if os.path.exists(file_path):
                    matching_files.append(file_path)

        if matching_files:
            for file_path in matching_files:
                self.video_player_window = VideoPlayerWindow(file_path)
                self.video_player_window.show()
        else:
            print("Eşleşen dosya bulunamadı.")
            QMessageBox.warning(self, "Dosya Bulunamadı", "Eşleşen dosya bulunamadı.")

class WatchWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Film ve Dizi İzle")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        self.media_dir = media_dir

        # Sol taraf: Kapak fotoğrafı ve bilgiler
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget)

        self.cover_label = QLabel()
        self.cover_label.setFixedSize(400, 600)
        left_layout.addWidget(self.cover_label, alignment=Qt.AlignCenter)

        self.info_widget = QWidget()
        info_layout = QVBoxLayout()
        self.info_widget.setLayout(info_layout)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        info_layout.addWidget(self.title_label)

        self.director_label = QLabel()
        info_layout.addWidget(self.director_label)

        self.genre_label = QLabel()
        info_layout.addWidget(self.genre_label)

        self.duration_label = QLabel()
        info_layout.addWidget(self.duration_label)

        self.play_button = QPushButton("İZLE")
        self.play_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.play_button.clicked.connect(self.play_media)
        info_layout.addWidget(self.play_button)

        left_layout.addWidget(self.info_widget)

        # Sağ taraf: Öğe seçme listesi
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget)

        # Buton grubu ekleme
        button_group = QWidget()
        button_layout = QHBoxLayout()
        button_group.setLayout(button_layout)
        right_layout.addWidget(button_group)

        self.film_button = QPushButton("Film")
        self.film_button.clicked.connect(lambda: self.filter_list("Film"))
        button_layout.addWidget(self.film_button)

        self.dizi_button = QPushButton("Dizi")
        self.dizi_button.clicked.connect(lambda: self.filter_list("Dizi"))
        button_layout.addWidget(self.dizi_button)

        self.all_button = QPushButton("Hepsini Göster")
        self.all_button.clicked.connect(lambda: self.filter_list(None))
        button_layout.addWidget(self.all_button)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size: 16px;")
        self.list_widget.currentItemChanged.connect(self.load_item)
        right_layout.addWidget(self.list_widget)

        self.video_widget = QVideoWidget()
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        self.play_button.clicked.connect(self.play_media)
        left_layout.addWidget(self.video_widget)

        self.watchlist = []  # İzlenecekler listesi
        self.load_watchlist()

        watchlist_label = QLabel("İzlenecekler Listesi")
        watchlist_layout = QVBoxLayout()
        watchlist_layout.addWidget(watchlist_label)

        self.watchlist_widget = QListWidget()
        #self.watchlist_widget.setParent(None)
        #self.watchlist_widget.setWindowFlags(Qt.Widget)
        #right_layout.addWidget(self.watchlist_widget)

        add_to_watchlist_button = QPushButton("Listeye Ekle")
        add_to_watchlist_button.clicked.connect(self.add_to_watchlist)
        watchlist_layout.addWidget(add_to_watchlist_button)

        show_watchlist_button = QPushButton("Listeyi Görüntüle")
        show_watchlist_button.clicked.connect(self.show_watchlist)
        watchlist_layout.addWidget(show_watchlist_button)

        right_layout.addLayout(watchlist_layout)

        self.data = data
        self.filter_list(None)

    def filter_list(self, item_type):
        self.list_widget.clear()
        filtered_data = []
        show_names = set()  # Gösterilen dizi isimlerini takip etmek için

        for item_data in self.data:
            if item_type is None or item_data[6] == item_type:
                name, show_type = item_data[0], item_data[6]
                if show_type == "Dizi" and name not in show_names:
                    filtered_data.append(item_data)
                    show_names.add(name)
                elif show_type == "Film":
                    filtered_data.append(item_data)

        self.list_widget.addItems([item[0] for item in filtered_data])
        self.filtered_data = filtered_data

        # İlk öğeyi yükle
        if filtered_data:
            self.load_item(self.list_widget.item(0))

    def load_item(self, current_item):
        if current_item is None:
            return

        item_index = self.list_widget.currentRow()
        item_data = self.filtered_data[item_index]

        name = item_data[0]
        director = item_data[1]
        genre = item_data[2]
        duration = item_data[3]
        cover_path = item_data[8]

        self.title_label.setText(name)
        self.director_label.setText(f"Yönetmen: {director}")
        self.genre_label.setText(f"Tür: {genre}")
        self.duration_label.setText(f"Süre: {duration} dk")

        if os.path.exists(cover_path):
            cover_pixmap = QPixmap(cover_path)
            self.cover_label.setPixmap(cover_pixmap.scaled(self.cover_label.size(), Qt.KeepAspectRatio))
        else:
            self.cover_label.clear()

    def play_item(self):
        self.player.play()

    def play_media(self):
        current_item = self.list_widget.currentItem()
        if current_item is None:
            return
        item_index = self.list_widget.currentRow()
        item_data = self.filtered_data[item_index]
        if item_data[6] == "Film":  # Film ise direkt oynat
            file_path = item_data[7]
            if os.path.exists(file_path):
                self.video_player_window = VideoPlayerWindow(file_path)
                self.video_player_window.show()
            else:
                print(f"Dosya bulunamadı: {file_path}")
                QMessageBox.warning(self, "Dosya Bulunamadı", f"Dosya bulunamadı: {file_path}")
        else:  # Dizi ise Sezon/Bölüm penceresini aç, sadece bu diziyi filtrele
            filtered_data = [item for item in self.data if item[0] == item_data[0]]
            self.season_episode_window = SeasonEpisodeWindow(filtered_data)
            self.season_episode_window.show()

    def add_to_watchlist(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            item_data = self.filtered_data[self.list_widget.currentRow()]
            item_name = item_data[0]  # Sadece ismi al
            self.watchlist.append(item_name)  # Sadece ismi ekle
            self.watchlist_widget.addItem(item_name)  # Sadece ismi listeye ekle
            self.save_watchlist()

    def show_watchlist(self):
        self.watchlist_window = WatchlistWindow(self.watchlist)
        self.watchlist_window.show()

    def load_watchlist(self):
        try:
            with open("watchlist.pickle", "rb") as file:
                self.watchlist = pickle.load(file)
                for item in self.watchlist:
                    self.list_widget.addItem(item)  # item zaten isim
        except FileNotFoundError:
            self.watchlist = []

    def save_watchlist(self):
        with open("watchlist.pickle", "wb") as file:
            pickle.dump(self.watchlist, file)

class VideoPlayerWindow(QMainWindow):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("Q-Q5 Media Player")
        self.setGeometry(100, 100, 800, 600)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(videoWidget)

        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.statusLabel = QLabel("Durdu")
        self.statusLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.statusLabel)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(videoWidget)
        mainLayout.addLayout(controlLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_duration)
        self.timer.start(1000)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusLabel.setText("Hata")

    def update_duration(self):
        current_position = self.mediaPlayer.position() // 1000  # to seconds
        duration = self.mediaPlayer.duration() // 1000  # to seconds
        self.statusLabel.setText(
            f"{current_position // 60:02}:{current_position % 60:02} / {duration // 60:02}:{duration % 60:02}"
        )

    def closeEvent(self, event):
        self.mediaPlayer.stop()  # Pencere kapatılınca videoyu durdur
        event.accept()


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Paneli")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        welcome_label = QLabel("Hoşgeldin,")
        welcome_label.setFont(QFont("Arial", 36, QFont.Bold))
        top_layout.addWidget(welcome_label, alignment=Qt.AlignHCenter)

        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(0)
        main_layout.addLayout(middle_layout, stretch=1)

        add_button = QPushButton("Film ve Dizi Ekle")
        add_button.setFont(QFont("Arial", 20))
        add_button.setMinimumSize(300, 50)
        add_button.clicked.connect(self.open_add_window)
        middle_layout.addWidget(add_button, alignment=Qt.AlignCenter)

        watch_button = QPushButton("Film ve Dizi İzle")
        watch_button.setFont(QFont("Arial", 20))
        watch_button.setMinimumSize(300, 50)
        watch_button.clicked.connect(self.open_watch_window)
        middle_layout.addWidget(watch_button, alignment=Qt.AlignCenter)

    def open_add_window(self):
        self.add_window = AddWindow(self)
        self.add_window.show()

    def open_watch_window(self):
        try:
            with open("data.pickle", "rb") as file:
                data = pickle.load(file)
        except FileNotFoundError:
            data = []

        self.watch_window = WatchWindow(data)
        self.watch_window.show()


class AddWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Film veya Dizi Ekle")
        self.setGeometry(100, 100, 840, 600)

        self.media_dir = media_dir

        layout = QVBoxLayout()

        self.type_label = QLabel("Türü Seçin:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Film", "Dizi"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        self.name_label = QLabel("İsim:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.director_label = QLabel("Yönetmen:")
        self.director_input = QLineEdit()
        layout.addWidget(self.director_label)
        layout.addWidget(self.director_input)

        self.genre_label = QLabel("Tür:")
        self.genre_input = QLineEdit()
        layout.addWidget(self.genre_label)
        layout.addWidget(self.genre_input)

        self.duration_label = QLabel("Süre:")
        self.duration_input = QLineEdit()
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_input)

        self.season_label = QLabel("Sezon:")
        self.season_input = QSpinBox()
        self.season_input.setEnabled(False)
        layout.addWidget(self.season_label)
        layout.addWidget(self.season_input)

        self.episode_label = QLabel("Bölüm:")
        self.episode_input = QSpinBox()
        self.episode_input.setEnabled(False)
        layout.addWidget(self.episode_label)
        layout.addWidget(self.episode_input)

        # Kapak fotoğrafı seçme bölümü
        self.cover_label = QLabel("Kapak Fotoğrafı:")
        self.cover_button = QPushButton("Kapak Ekle")
        self.cover_button.clicked.connect(self.open_cover_dialog)
        self.cover_path = None
        cover_layout = QHBoxLayout()
        cover_layout.addWidget(self.cover_label)
        cover_layout.addWidget(self.cover_button)
        layout.addLayout(cover_layout)

        self.file_button = QPushButton("Dosya Yükle")
        self.file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.file_button)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["İsim", "Yönetmen", "Tür", "Süre", "Sezon", "Bölüm", "Biçim", "Dosya Yolu", "Kapak Fotoğrafı"]
        )
        layout.addWidget(self.table)

        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Seçiliyi Sil")
        self.remove_button.clicked.connect(self.remove_item)
        layout.addWidget(self.remove_button)

        self.type_combo.currentTextChanged.connect(self.toggle_season_episode)

        self.setLayout(layout)

        self.file_path = None
        self.load_data()

    def open_cover_dialog(self):
        cover_dialog = QFileDialog()
        cover_path, _ = cover_dialog.getOpenFileName(
            self, "Kapak Fotoğrafı Seçin", os.path.expanduser("~"), "Image Files (*.jpg *.png)"
        )
        if cover_path:
            cover_name = os.path.basename(cover_path)
            self.cover_path = os.path.join(self.media_dir, cover_name)
            shutil.copy(cover_path, self.cover_path)

    def load_data(self):
        try:
            with open("data.pickle", "rb") as file:
                data = pickle.load(file)
                for row in data:
                    row_count = self.table.rowCount()
                    self.table.insertRow(row_count)
                    for col, value in enumerate(row):
                        if col == 7:  # Dosya yolu sütunu
                            file_path = os.path.join(self.media_dir, os.path.basename(value))
                            if not os.path.exists(file_path):
                                shutil.copy(value, file_path)
                            self.table.setItem(row_count, col, QTableWidgetItem(file_path))
                        elif col == 8:  # Kapak fotoğrafı yolu sütunu
                            cover_path = os.path.join(self.media_dir, os.path.basename(value))
                            if not os.path.exists(cover_path):
                                shutil.copy(value, cover_path)
                            self.table.setItem(row_count, col, QTableWidgetItem(cover_path))
                        else:
                            self.table.setItem(row_count, col, QTableWidgetItem(str(value)))
        except FileNotFoundError:
            pass

    def save_data(self):
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None:
                    if col == 7:  # Dosya yolu sütunu
                        file_path = item.text()
                        row_data.append(file_path)
                    elif col == 8:  # Kapak fotoğrafı yolu sütunu
                        cover_path = item.text()
                        row_data.append(cover_path)
                    else:
                        row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        with open("data.pickle", "wb") as file:
            pickle.dump(data, file)

    def toggle_season_episode(self, item_type):
        if item_type == "Film":
            self.season_input.setEnabled(False)
            self.episode_input.setEnabled(False)
        else:
            self.season_input.setEnabled(True)
            self.episode_input.setEnabled(True)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Dosya Seçin", os.path.expanduser("~"), "Video Files (*.mp4)"
        )
        if file_path:
            file_name = os.path.basename(file_path)
            self.file_path = os.path.join(self.media_dir, file_name)
            shutil.copy(file_path, self.file_path)

    def add_item(self):
        item_type = self.type_combo.currentText()
        name = self.name_input.text()
        director = self.director_input.text()
        genre = self.genre_input.text()
        duration = self.duration_input.text()
        season = str(self.season_input.value()) if self.season_input.isEnabled() else "-"
        episode = str(self.episode_input.value()) if self.episode_input.isEnabled() else "-"
        file_path = self.file_path
        cover_path = self.cover_path  # Kapak fotoğrafı yolunu da ekledik

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QTableWidgetItem(name))
        self.table.setItem(row_count, 1, QTableWidgetItem(director))
        self.table.setItem(row_count, 2, QTableWidgetItem(genre))
        self.table.setItem(row_count, 3, QTableWidgetItem(duration))
        self.table.setItem(row_count, 4, QTableWidgetItem(season))
        self.table.setItem(row_count, 5, QTableWidgetItem(episode))
        self.table.setItem(row_count, 6, QTableWidgetItem(item_type))
        self.table.setItem(row_count, 7, QTableWidgetItem(file_path))
        self.table.setItem(row_count, 8, QTableWidgetItem(cover_path))  # Kapak fotoğrafı yolunu da ekledik

        self.save_data()

    def remove_item(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            file_path = self.table.item(selected_row, 7).text()
            if os.path.exists(file_path):
                os.remove(file_path)
            self.table.removeRow(selected_row)
            self.save_data()

class WatchlistWindow(QDialog):
    def __init__(self, watchlist, parent=None):
        super().__init__(parent)
        self.setWindowTitle("İzlenecekler Listesi")
        self.setGeometry(200, 200, 400, 400)
        layout = QVBoxLayout()

        self.watchlist_widget = QListWidget()
        for item_name in watchlist:
            self.watchlist_widget.addItem(item_name)

        layout.addWidget(self.watchlist_widget)

        remove_button = QPushButton("Listeden Sil")
        remove_button.clicked.connect(self.remove_from_watchlist)
        layout.addWidget(remove_button)

        self.setLayout(layout)
        self.watchlist = watchlist

    def remove_from_watchlist(self):
        selected_item = self.watchlist_widget.currentItem()
        if selected_item:
            item_name = selected_item.text()
            item_index = self.watchlist_widget.currentRow()
            self.watchlist_widget.takeItem(item_index)
            self.watchlist.remove(item_name)
            self.save_watchlist()

    def save_watchlist(self):
        with open("watchlist.pickle", "wb") as file:
            pickle.dump(self.watchlist, file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
