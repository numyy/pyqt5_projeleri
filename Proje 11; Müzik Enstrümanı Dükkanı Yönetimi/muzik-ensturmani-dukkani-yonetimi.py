from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QDialog, QMessageBox, QTabWidget, QListWidget, QListWidgetItem, QDateEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIntValidator, QDoubleValidator
import sqlite3

class Database:
    def __init__(self, db_name='muzik_dukkani.db'):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS instruments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_number TEXT NOT NULL,
                date TEXT NOT NULL,
                details TEXT NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS supports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                support_number TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT NOT NULL
            )
            ''')
            conn.commit()

    def add_instrument(self, name, quantity, price):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO instruments (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
            conn.commit()

    def delete_instrument(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM instruments WHERE id=?", (id,))
            conn.commit()

    def get_instruments(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM instruments")
            return cursor.fetchall()

    def add_customer(self, name, phone, email):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
            conn.commit()

    def delete_customer(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id=?", (id,))
            conn.commit()

    def get_customers(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            return cursor.fetchall()

    def add_sale(self, sale_number, date, details):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sales (sale_number, date, details) VALUES (?, ?, ?)", (sale_number, date, details))
            conn.commit()

    def delete_sale(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sales WHERE id=?", (id,))
            conn.commit()

    def get_sales(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sales")
            return cursor.fetchall()

    def add_support(self, support_number, date, status, details):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO supports (support_number, date, status, details) VALUES (?, ?, ?, ?)", (support_number, date, status, details))
            conn.commit()

    def delete_support(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM supports WHERE id=?", (id,))
            conn.commit()

    def get_supports(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM supports")
            return cursor.fetchall()

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Müzik Enstrümanı Dükkanı Yönetimi')
        self.setGeometry(100, 100, 800, 600)
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(self.create_instrument_tab(), "Enstrüman Yönetimi")
        self.tabs.addTab(self.create_customer_tab(), "Müşteri Yönetimi")
        self.tabs.addTab(self.create_sale_tab(), "Satış Yönetimi")
        self.tabs.addTab(self.create_support_tab(), "Destek Yönetimi")

    def create_instrument_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.instrument_list = QListWidget()
        self.instrument_list.itemDoubleClicked.connect(self.edit_instrument)
        layout.addWidget(self.instrument_list)
        add_button = QPushButton("Enstrüman Ekle")
        add_button.clicked.connect(self.show_add_instrument_dialog)
        delete_button = QPushButton("Enstrüman Sayısını Sil")
        delete_button.clicked.connect(self.delete_selected_instrument)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        widget.setLayout(layout)
        self.refresh_instrument_list()
        return widget

    def edit_instrument(self, item):
        dialog = QDialog()
        dialog.setWindowTitle("Enstrümanı Düzenle")
        layout = QFormLayout()
        name_input = QLineEdit(item.text().split(" - ")[0])
        quantity_input = QLineEdit()
        price_input = QLineEdit()
        layout.addRow("Enstrüman Adı:", name_input)
        layout.addRow("Stok Miktarı:", quantity_input)
        layout.addRow("Fiyat:", price_input)
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(
            lambda: self.save_instrument(name_input.text(), int(quantity_input.text()), float(price_input.text()),
                                         item))
        layout.addWidget(save_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def save_instrument(self, name, quantity, price, item):
        # Veritabanını güncelleme ve liste öğesini güncelleme kodunu buraya ekleyin
        QMessageBox.information(self, "Enstrüman Güncelleme",
                                f"{name} başarıyla güncellendi. Stok: {quantity}, Fiyat: {price}")
        self.refresh_instrument_list()

    # Müşteri, satış ve destek sekmeleri için benzer işlevler ekleyin.

    def show_add_instrument_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Enstrüman Ekle")
        layout = QFormLayout()
        name_input = QLineEdit()
        quantity_input = QLineEdit()
        quantity_input.setValidator(QIntValidator(0, 10000))
        price_input = QLineEdit()
        price_input.setValidator(QDoubleValidator(0.99, 99999.99, 2))
        layout.addRow("Enstrüman Adı:", name_input)
        layout.addRow("Stok Miktarı:", quantity_input)
        layout.addRow("Fiyat:", price_input)
        add_button = QPushButton("Ekle")
        add_button.clicked.connect(lambda: self.add_instrument(name_input.text(), int(quantity_input.text()), float(price_input.text())))
        layout.addWidget(add_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def add_instrument(self, name, quantity, price):
        self.db.add_instrument(name, quantity, price)
        QMessageBox.information(self, "Enstrüman Ekleme", f"{name} başarıyla eklendi. Stok: {quantity}, Fiyat: {price}")
        self.refresh_instrument_list()

    def save_instrument(self, name, quantity, price, item):
        # Veritabanını güncelleme ve liste öğesini güncelleme kodunu buraya ekleyin
        QMessageBox.information(self, "Enstrüman Güncelleme",
                                f"{name} başarıyla güncellendi. Stok: {quantity}, Fiyat: {price}")
        self.refresh_instrument_list()


    def delete_selected_instrument(self):
        selected_items = self.instrument_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            id = item.data(Qt.UserRole)
            self.db.delete_instrument(id)
            self.refresh_instrument_list()

    def refresh_instrument_list(self):
        self.instrument_list.clear()
        instruments = self.db.get_instruments()
        for instrument in instruments:
            list_item = QListWidgetItem(f"{instrument[1]} - Stok: {instrument[2]}, Fiyat: {instrument[3]}")
            list_item.setData(Qt.UserRole, instrument[0])
            self.instrument_list.addItem(list_item)

    def create_customer_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.customer_list = QListWidget()
        self.customer_list.itemDoubleClicked.connect(self.edit_customer)
        layout.addWidget(self.customer_list)
        add_button = QPushButton("Müşteri Ekle")
        add_button.clicked.connect(self.show_add_customer_dialog)
        delete_button = QPushButton("Müşteriyi Sil")
        delete_button.clicked.connect(self.delete_selected_customer)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        widget.setLayout(layout)
        self.refresh_customer_list()
        return widget

    def edit_customer(self, item):
        dialog = QDialog()
        dialog.setWindowTitle("Müşteriyi Düzenle")
        layout = QFormLayout()
        name_input = QLineEdit()
        phone_input = QLineEdit()
        email_input = QLineEdit()
        layout.addRow("Müşteri Adı:", name_input)
        layout.addRow("Telefon Numarası:", phone_input)
        layout.addRow("E-posta Adresi:", email_input)
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(
            lambda: self.save_customer(name_input.text(), phone_input.text(), email_input.text(), item))
        layout.addWidget(save_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def save_customer(self, name, phone, email, item):
        # Veritabanını güncelleme ve liste öğesini güncelleme kodunu buraya ekleyin
        QMessageBox.information(self, "Müşteri Güncelleme", f"{name} başarıyla güncellendi.")
        self.refresh_customer_list()

    def show_add_customer_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Müşteri Ekle")
        layout = QFormLayout()
        name_input = QLineEdit()
        phone_input = QLineEdit()
        email_input = QLineEdit()
        layout.addRow("Müşteri Adı:", name_input)
        layout.addRow("Telefon Numarası:", phone_input)
        layout.addRow("E-posta Adresi:", email_input)
        add_button = QPushButton("Ekle")
        add_button.clicked.connect(lambda: self.add_customer(name_input.text(), phone_input.text(), email_input.text()))
        layout.addWidget(add_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def add_customer(self, name, phone, email):
        self.db.add_customer(name, phone, email)
        QMessageBox.information(self, "Müşteri Ekleme", f"{name} başarıyla eklendi.")
        self.refresh_customer_list()

    def delete_selected_customer(self):
        selected_items = self.customer_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            id = item.data(Qt.UserRole)
            self.db.delete_customer(id)
            self.refresh_customer_list()

    def refresh_customer_list(self):
        self.customer_list.clear()
        customers = self.db.get_customers()
        for customer in customers:
            list_item = QListWidgetItem(f"{customer[1]} - Tel: {customer[2]}, Email: {customer[3]}")
            list_item.setData(Qt.UserRole, customer[0])
            self.customer_list.addItem(list_item)

    def create_sale_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.sale_list = QListWidget()
        self.sale_list.itemDoubleClicked.connect(self.edit_sale)
        layout.addWidget(self.sale_list)
        add_button = QPushButton("Satış Ekle")
        add_button.clicked.connect(self.show_add_sale_dialog)
        delete_button = QPushButton("Satışı Sil")
        delete_button.clicked.connect(self.delete_selected_sale)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        widget.setLayout(layout)
        self.refresh_sale_list()
        return widget

    def edit_sale(self, item):
        dialog = QDialog()
        dialog.setWindowTitle("Satışı Düzenle")
        layout = QFormLayout()
        sale_number_input = QLineEdit()
        date_input = QDateEdit()
        date_input.setDate(QDate.currentDate())
        details_input = QLineEdit()
        layout.addRow("Satış Numarası:", sale_number_input)
        layout.addRow("Tarih:", date_input)
        layout.addRow("Detaylar:", details_input)
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(
            lambda: self.save_sale(sale_number_input.text(), date_input.date().toString("yyyy-MM-dd"),
                                   details_input.text(), item))
        layout.addWidget(save_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def save_sale(self, sale_number, date, details, item):
        # Veritabanını güncelleme ve liste öğesini güncelleme kodunu buraya ekleyin
        QMessageBox.information(self, "Satış Güncelleme", f"Satış {sale_number} başarıyla güncellendi.")
        self.refresh_sale_list()

    def show_add_sale_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Satış Ekle")
        layout = QFormLayout()
        sale_number_input = QLineEdit()
        date_input = QDateEdit()
        date_input.setDate(QDate.currentDate())
        details_input = QLineEdit()
        layout.addRow("Satış Numarası:", sale_number_input)
        layout.addRow("Tarih:", date_input)
        layout.addRow("Detaylar:", details_input)
        add_button = QPushButton("Ekle")
        add_button.clicked.connect(lambda: self.add_sale(sale_number_input.text(), date_input.date().toString("yyyy-MM-dd"), details_input.text()))
        layout.addWidget(add_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def add_sale(self, sale_number, date, details):
        self.db.add_sale(sale_number, date, details)
        QMessageBox.information(self, "Satış Ekleme", f"Satış eklendi: {sale_number} - {date}")
        self.refresh_sale_list()

    def delete_selected_sale(self):
        selected_items = self.sale_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            id = item.data(Qt.UserRole)
            self.db.delete_sale(id)
            self.refresh_sale_list()

    def refresh_sale_list(self):
        self.sale_list.clear()
        sales = self.db.get_sales()
        for sale in sales:
            list_item = QListWidgetItem(f"Satış No: {sale[1]}, Tarih: {sale[2]}, Detaylar: {sale[3]}")
            list_item.setData(Qt.UserRole, sale[0])
            self.sale_list.addItem(list_item)

    def create_support_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.support_list = QListWidget()
        self.support_list.itemDoubleClicked.connect(self.edit_support)
        layout.addWidget(self.support_list)
        add_button = QPushButton("Destek Talebi Ekle")
        add_button.clicked.connect(self.show_add_support_dialog)
        delete_button = QPushButton("Destek Talebini Sil")
        delete_button.clicked.connect(self.delete_selected_support)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        widget.setLayout(layout)
        self.refresh_support_list()
        return widget

    def edit_support(self, item):
        dialog = QDialog()
        dialog.setWindowTitle("Destek Talebini Düzenle")
        layout = QFormLayout()
        support_number_input = QLineEdit()
        date_input = QDateEdit()
        date_input.setDate(QDate.currentDate())
        status_input = QLineEdit()
        details_input = QLineEdit()
        layout.addRow("Destek Numarası:", support_number_input)
        layout.addRow("Tarih:", date_input)
        layout.addRow("Durum:", status_input)
        layout.addRow("Detaylar:", details_input)
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(
            lambda: self.save_support(support_number_input.text(), date_input.date().toString("yyyy-MM-dd"),
                                      status_input.text(), details_input.text(), item))
        layout.addWidget(save_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def save_support(self, support_number, date, status, details, item):
        # Veritabanını güncelleme ve liste öğesini güncelleme kodunu buraya ekleyin
        QMessageBox.information(self, "Destek Güncelleme", f"Destek {support_number} başarıyla güncellendi.")
        self.refresh_support_list()

    def show_add_support_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Destek Talebi Ekle")
        layout = QFormLayout()
        support_number_input = QLineEdit()
        date_input = QDateEdit()
        date_input.setDate(QDate.currentDate())
        status_input = QLineEdit()
        details_input = QLineEdit()
        layout.addRow("Destek Numarası:", support_number_input)
        layout.addRow("Tarih:", date_input)
        layout.addRow("Durum:", status_input)
        layout.addRow("Detaylar:", details_input)
        add_button = QPushButton("Ekle")
        add_button.clicked.connect(lambda: self.add_support(support_number_input.text(), date_input.date().toString("yyyy-MM-dd"), status_input.text(), details_input.text()))
        layout.addWidget(add_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def add_support(self, support_number, date, status, details):
        self.db.add_support(support_number, date, status, details)
        QMessageBox.information(self, "Destek Talebi Ekleme", f"Destek Talebi eklendi: {support_number}")
        self.refresh_support_list()

    def delete_selected_support(self):
        selected_items = self.support_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            id = item.data(Qt.UserRole)
            self.db.delete_support(id)
            self.refresh_support_list()

    def refresh_support_list(self):
        self.support_list.clear()
        supports = self.db.get_supports()
        for support in supports:
            list_item = QListWidgetItem(f"Destek No: {support[1]}, Tarih: {support[2]}, Durum: {support[3]}, Detaylar: {support[4]}")
            list_item.setData(Qt.UserRole, support[0])
            self.support_list.addItem(list_item)


if __name__ == '__main__':
    app = QApplication([])
    main_app = MainApplication()
    main_app.show()
    app.exec_()
