import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QListWidget, QTextEdit, QMessageBox, QInputDialog

def create_connection():
    conn = sqlite3.connect('recipes.db')
    return conn

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM recipes')
    if cursor.fetchone()[0] == 0:
        initial_recipes = [
            ("Kısır", "2 su bardağı ince bulgur, 2 yemek kaşığı salça, 1 demet yeşil soğan, 1 demet maydanoz, yarım demet nane, 1 çay bardağı zeytinyağı, limon suyu, tuz, pul biber",
             "Bulguru kaynar su ile ıslatıp şişmesini bekleyin. Salçayı ve baharatları ekleyip karıştırın. İnce doğranmış yeşillikleri ve zeytinyağını ekleyip harmanlayın. Limon suyu ile tatlandırın ve soğuk servis yapın."),
            ("Menemen", "3 adet yumurta, 2 adet domates, 1 adet yeşil biber, 1 soğan, 2 yemek kaşığı zeytinyağı, tuz, karabiber, pul biber",
             "Soğan ve biberleri zeytinyağında kavurun. Domatesleri küp şeklinde doğrayıp ekleyin. Domatesler suyunu çekince çırpılmış yumurtaları ekleyin ve karıştırarak pişirin.")
        ]
        cursor.executemany('INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)', initial_recipes)
        conn.commit()
    conn.close()

class RecipeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        initialize_db()
        self.load_initial_recipes()

    def initUI(self):
        self.setWindowTitle('Yemek Tarifi Uygulaması')
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        add_layout = QHBoxLayout()
        self.tarif_adi_input = QLineEdit()
        self.tarif_adi_input.setPlaceholderText('Tarif Adı')
        add_layout.addWidget(self.tarif_adi_input)
        self.malzemeler_input = QTextEdit()
        self.malzemeler_input.setPlaceholderText('Malzemeler')
        add_layout.addWidget(self.malzemeler_input)
        self.tarif_icerik_input = QTextEdit()
        self.tarif_icerik_input.setPlaceholderText('Tarif İçeriği')
        add_layout.addWidget(self.tarif_icerik_input)
        ekle_button = QPushButton('Tarif Ekle')
        ekle_button.clicked.connect(self.add_recipe)
        add_layout.addWidget(ekle_button)
        layout.addLayout(add_layout)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Tarif Ara')
        search_layout.addWidget(self.search_input)
        search_button = QPushButton('Ara')
        search_button.clicked.connect(self.search_recipes)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)
        self.initial_recipes_list = QListWidget()
        self.initial_recipes_list.itemDoubleClicked.connect(self.show_recipe_details)
        layout.addWidget(self.initial_recipes_list)
        delete_button = QPushButton('Tarifi Sil')
        delete_button.clicked.connect(self.delete_recipe)
        layout.addWidget(delete_button)
        self.setCentralWidget(central_widget)

    def load_initial_recipes(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM recipes')
        initial_recipes = cursor.fetchall()
        for recipe in initial_recipes:
            self.initial_recipes_list.addItem(recipe[0])
        conn.close()

    def add_recipe(self):
        name = self.tarif_adi_input.text()
        ingredients = self.malzemeler_input.toPlainText()
        instructions = self.tarif_icerik_input.toPlainText()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)', (name, ingredients, instructions))
        conn.commit()
        conn.close()
        self.initial_recipes_list.addItem(name)
        QMessageBox.information(self, 'Tarif Eklendi', f'{name} başarıyla eklendi!')

    def search_recipes(self):
        search_text = self.search_input.text()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM recipes WHERE name LIKE ?', ('%' + search_text + '%',))
        results = cursor.fetchall()
        self.initial_recipes_list.clear()
        for recipe in results:
            self.initial_recipes_list.addItem(recipe[0])
        conn.close()

    def show_recipe_details(self, item):
        recipe_name = item.text()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT ingredients, instructions FROM recipes WHERE name = ?', (recipe_name,))
        recipe_details = cursor.fetchone()
        conn.close()
        QMessageBox.information(self, recipe_name, f"Malzemeler:\n{recipe_details[0]}\n\nYapılışı:\n{recipe_details[1]}")
        score, ok = QInputDialog.getItem(self, "Puan Ver", "Yemeğe puan verin:", [str(i) for i in range(1, 11)], 0, False)
        if ok:
            QMessageBox.information(self, recipe_name, f"Verilen Puan: {score}")

    def delete_recipe(self):
        selected_item = self.initial_recipes_list.currentItem()
        if selected_item:
            selected_name = selected_item.text()
            reply = QMessageBox.question(self, 'Tarifi Sil', f'{selected_name} tarifini silmek istediğinizden emin misiniz?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute('DELETE FROM recipes WHERE name = ?', (selected_name,))
                conn.commit()
                conn.close()
                self.initial_recipes_list.takeItem(self.initial_recipes_list.row(selected_item))
                QMessageBox.information(self, 'Tarif Silindi', f'{selected_name} başarıyla silindi!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RecipeApp()
    ex.show()
    sys.exit(app.exec_())
