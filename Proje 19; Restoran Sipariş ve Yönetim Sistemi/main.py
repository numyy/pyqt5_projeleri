import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

# Veritabanı işlevleri
def initialize_database():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()

    # Siparişler tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                (order_number INTEGER PRIMARY KEY, customer_name TEXT, customer_address TEXT, order_items TEXT)''')

    # Menü tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS menu
                (id INTEGER PRIMARY KEY, category TEXT, item_name TEXT, price REAL, stock INTEGER)''')

    # Menüye öğeleri ekle
    c.execute("SELECT count(*) FROM menu")
    if c.fetchone()[0] == 0:  # Eğer menü boşsa, öğeleri ekleyin
        menu_items = [
            ("Yemek", "Pizza", 20.0, 100),
            ("Yemek", "Burger", 15.0, 100),
            ("Yemek", "Salad", 10.0, 100),
            ("Yemek", "Pasta", 18.0, 100),
            ("Yemek", "Steak", 25.0, 100),
            ("Yemek", "Chicken", 12.0, 100),
            ("Yemek", "Salmon", 20.0, 100),
            ("Yemek", "Sushi", 18.0, 100),
            ("Yemek", "Lasagna", 16.0, 100),
            ("Yemek", "Tacos", 14.0, 100),
            ("Tatlı", "Cheesecake", 6.0, 100),
            ("Tatlı", "Brownie", 4.0, 100),
            ("Tatlı", "Ice Cream", 5.0, 100),
            ("Tatlı", "Tiramisu", 7.0, 100),
            ("Tatlı", "Creme Brulee", 6.0, 100),
            ("Tatlı", "Apple Pie", 5.0, 100),
            ("Tatlı", "Chocolate Cake", 6.0, 100),
            ("Tatlı", "Baklava", 5.0, 100),
            ("Tatlı", "Profiteroles", 6.0, 100),
            ("Tatlı", "Lava Cake", 7.0, 100),
            ("İçecek", "Soda", 2.0, 100),
            ("İçecek", "Coffee", 3.0, 100),
            ("İçecek", "Tea", 2.5, 100),
            ("İçecek", "Beer", 4.0, 100),
            ("İçecek", "Wine", 5.0, 100)
        ]
        for category, item_name, price, stock in menu_items:
            c.execute("INSERT INTO menu (category, item_name, price, stock) VALUES (?, ?, ?, ?)",
                      (category, item_name, price, stock))

    # Müşteriler tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS customers
                (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, email TEXT, phone TEXT, password TEXT)''')

    # Çalışanlar tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

    # Örnek çalışan ekleyin
    c.execute("SELECT count(*) FROM employees WHERE username='admin'")
    if c.fetchone()[0] == 0:  # Eğer admin yoksa ekleyin
        c.execute("INSERT INTO employees (username, password) VALUES ('admin', 'password')")

    conn.commit()

# Çalışan giriş penceresi
class EmployeeLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Çalışan Girişi")

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı Adı")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.verify_credentials)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def verify_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        result = check_credentials(username, password)
        if result:
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre.")
            self.reject()

    def accept(self):
        self.done(QDialog.Accepted)

    def reject(self):
        self.done(QDialog.Rejected)

# Ürün sınıfı
class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

# Sipariş sınıfı
class Order:
    def __init__(self, order_number, items, customer_info):
        self.order_number = order_number
        self.items = items
        self.customer_info = customer_info

# Müşteri sınıfı
class Customer:
    def __init__(self, name, surname, address):
        self.name = name
        self.surname = surname
        self.address = address
        self.order_history = []

# Ana pencere sınıfı
class MainWindow(QMainWindow):
    def __init__(self, role):
        super().__init__()
        self.setWindowTitle("YemekSever")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        if role == "Çalışan":
            self.init_employee_view()
        else:
            self.init_customer_view()

        self.role_label = QLabel(f"Rol: {role}")
        self.layout.addWidget(self.role_label)

    def init_employee_view(self):
        self.create_stock_update_section()
        self.create_order_list_section()
        self.create_delete_order_button()

    def init_customer_view(self):
        self.create_menu_section()
        self.create_cart_section()
        self.create_order_button()

    def show_update_stock_dialog(self, item):
        selected_product = item.text().split(" - ")[0]
        product_info = self.product_details.get(selected_product)
        if product_info is None:
            return
        category, price, current_stock = product_info

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Stok Güncelleme - {selected_product}")
        layout = QVBoxLayout()

        label = QLabel(f"Güncel Stok: {current_stock}")
        layout.addWidget(label)

        new_stock_input = QLineEdit()
        new_stock_input.setValidator(QIntValidator(0, 10000))
        layout.addWidget(new_stock_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(
            lambda: self.update_stock(selected_product, category, price, new_stock_input.text(), dialog))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def create_stock_update_section(self):
        stock_layout = QVBoxLayout()
        stock_label = QLabel("Stok Güncelleme:")
        stock_layout.addWidget(stock_label)

        self.product_list = QListWidget()
        menu_data = get_menu()
        self.product_details = {}
        for item_id, category, item_name, price, stock in menu_data:
            item_text = f"{item_name} - Stok: {stock}"
            self.product_list.addItem(item_text)
            self.product_details[item_name] = (category, price, stock)
        stock_layout.addWidget(self.product_list)
        self.product_list.itemDoubleClicked.connect(self.show_update_stock_dialog)

        self.layout.addLayout(stock_layout)

    def create_order_list_section(self):
        order_layout = QVBoxLayout()
        order_label = QLabel("Siparişler:")
        order_layout.addWidget(order_label)

        self.order_list = QListWidget()
        order_layout.addWidget(self.order_list)

        self.layout.addLayout(order_layout)
        self.load_orders()

    def create_delete_order_button(self):
        self.delete_order_button = QPushButton("Siparişi Sil")
        self.delete_order_button.clicked.connect(self.delete_selected_order)
        self.layout.addWidget(self.delete_order_button)

    def create_menu_section(self):
        menu_layout = QHBoxLayout()
        menu_label = QLabel("Menü:")
        menu_layout.addWidget(menu_label)

        self.menu_list = QListWidget()
        self.product_details = {}
        menu_data = get_menu()
        for item_id, category, item_name, price, stock in menu_data:
            item_text = f"{category}: {item_name} - ${price:.2f}"
            self.menu_list.addItem(item_text)
            self.product_details[item_name] = (category, price, stock)
        self.menu_list.itemDoubleClicked.connect(self.add_to_cart)
        menu_layout.addWidget(self.menu_list)

        self.layout.addLayout(menu_layout)

    def create_cart_section(self):
        cart_layout = QHBoxLayout()
        cart_label = QLabel("Sepet:")
        cart_layout.addWidget(cart_label)

        self.cart_list = QListWidget()
        cart_layout.addWidget(self.cart_list)

        self.layout.addLayout(cart_layout)

        self.cart = []

    def create_order_button(self):
        order_button = QPushButton("Sipariş Gönder")
        order_button.clicked.connect(self.show_cart)
        self.layout.addWidget(order_button)

    def update_stock(self, product_name, category, price, new_stock, dialog):
        new_stock = int(new_stock)
        update_stock_in_db(product_name, category, new_stock, price)
        QMessageBox.information(dialog, "Stok Güncellendi", f"{product_name} stoğu {new_stock} olarak güncellendi.")

        # Menü ve stok listelerini güncelleyin
        menu_data = get_menu()
        self.menu_list.clear()
        self.product_details.clear()
        for item_id, category, item_name, price, stock in menu_data:
            item_text = f"{category}: {item_name} - ${price:.2f}"
            self.menu_list.addItem(item_text)
            self.product_details[item_name] = (category, price, stock)

        self.product_list.clear()
        for item_id, category, item_name, price, stock in menu_data:
            item_text = f"{item_name} - Stok: {stock}"
            self.product_list.addItem(item_text)

    def load_orders(self):
        orders = get_orders()
        self.order_list.clear()

        for order_number, customer_name, customer_address, order_items in orders:
            order_details = f"Müşteri: {customer_name}\nAdres: {customer_address}\n"
            order_details += "Sipariş İçeriği:\n"
            for item in order_items.split(","):
                item_details = item.split(":")
                if len(item_details) == 2:
                    item_name, item_price = item_details
                    order_details += f"- {item_name}: ${item_price}\n"
            self.order_list.addItem(order_details)

    def add_to_cart(self, item):
        item_text = item.text()
        self.cart.append(item_text)
        self.cart_list.addItem(item_text)

    def show_cart(self):
        if not self.cart:
            QMessageBox.information(self, "Sepet Boş", "Sepetinizde ürün bulunmamaktadır.")
            return

        cart_dialog = CartConfirmationDialog(self.cart, self.product_details, self)
        result = cart_dialog.exec_()
        if result == QDialog.Accepted:
            self.submit_order()

    def submit_order(self):
        items = [item.split(": ")[1] for item in self.cart]
        address_dialog = AddressDialog(self)
        address_result = address_dialog.exec_()
        if address_result == QDialog.Accepted:
            customer_name = "Online Customer"  # Default isim yerine müşteri ismi kullanılacak
            customer_address = address_dialog.address_input.text()

            # Kullanıcıdan isim ve soyisim bilgisi al
            customer_name_dialog = CustomerNameDialog(self)
            name_result = customer_name_dialog.exec_()
            if name_result == QDialog.Accepted:
                customer_name = f"{customer_name_dialog.name_input.text()} {customer_name_dialog.surname_input.text()}"

            customer = Customer(customer_name, customer_address)
            order_number = len(get_orders()) + 1
            order = Order(order_number, items, customer)
            add_order(order)

            for item in self.cart:
                product_name, _ = item.split(" - $")
                _, price, stock = self.product_details[product_name]
                new_stock = stock - 1
                update_stock_in_db(product_name, 'Yemek', new_stock, price)

            self.cart.clear()
            self.cart_list.clear()

            QMessageBox.information(self, "Sipariş Onayı", "Siparişiniz alındı. Teşekkür ederiz!")
            self.load_orders()

    def delete_selected_order(self):
        selected_order = self.order_list.currentRow()
        if selected_order == -1:
            QMessageBox.information(self, "Hata", "Lütfen silmek istediğiniz siparişi seçin.")
            return

        order_number = selected_order + 1
        delete_order(order_number)
        self.load_orders()
        QMessageBox.information(self, "Sipariş Silindi", "Seçilen sipariş başarıyla silindi.")

class CartConfirmationDialog(QDialog):
    def __init__(self, cart, product_details, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sepet Onayı")
        self.product_details = product_details

        layout = QVBoxLayout()

        # Sepet içeriğini görüntüle
        self.cart_list = QListWidget()
        for item in cart:
            self.cart_list.addItem(item)
        layout.addWidget(self.cart_list)

        # Toplam fiyatı görüntüle
        total_price = sum(self.get_item_price(item) for item in cart)
        total_price_label = QLabel(f"Toplam Fiyat: ${total_price:.2f}")
        layout.addWidget(total_price_label)

        # Onay düğmesi
        confirm_button = QPushButton("Sepeti Onayla")
        confirm_button.clicked.connect(self.accept)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def get_item_price(self, item):
        # Ürün detaylarından fiyatı alın
        _, item_price = item.split(" - $")
        return float(item_price)

class AddressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adres Bilgisi Gir")

        layout = QVBoxLayout()

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Adresinizi girin")
        layout.addWidget(self.address_input)

        confirm_button = QPushButton("Siparişi Tamamla")
        confirm_button.clicked.connect(self.accept)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

class CustomerNameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Müşteri Bilgisi Gir")

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("İsim")
        layout.addWidget(self.name_input)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Soyisim")
        layout.addWidget(self.surname_input)

        confirm_button = QPushButton("Bilgileri Onayla")
        confirm_button.clicked.connect(self.accept)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Müşteri Girişi")

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta Adresi")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.verify_credentials)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def verify_credentials(self):
        email = self.email_input.text()
        password = self.password_input.text()

        result = check_customer_credentials(email, password)
        if result:
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz e-posta adresi veya şifre.")
            self.reject()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setGeometry(100, 100, 300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        customer_button = QPushButton("Müşteri Olarak Giriş Yap")
        customer_button.clicked.connect(self.open_main_window_customer)
        layout.addWidget(customer_button)

        employee_button = QPushButton("Çalışan Olarak Giriş Yap")
        employee_button.clicked.connect(self.open_main_window_employee)
        layout.addWidget(employee_button)

        register_button = QPushButton("Kayıt Ol")
        register_button.clicked.connect(self.register_window)
        layout.addWidget(register_button)

    def register_window(self):
        register_dialog = RegisterDialog(self)
        register_dialog.exec_()

    def open_main_window_customer(self):
        login_dialog = LoginDialog(self)
        result = login_dialog.exec_()
        if result == QDialog.Accepted:
            self.main_window = MainWindow("Müşteri")
            self.main_window.show()
            self.close()

    def open_main_window_employee(self):
        login_dialog = EmployeeLoginDialog(self)
        result = login_dialog.exec_()
        if result == QDialog.Accepted:
            self.main_window = MainWindow("Çalışan")
            self.main_window.show()
            self.hide()

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Müşteri Kaydı")

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("İsim")
        layout.addWidget(self.name_input)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Soyisim")
        layout.addWidget(self.surname_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta Adresi")
        layout.addWidget(self.email_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefon Numarası")
        layout.addWidget(self.phone_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.register_customer)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def register_customer(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        password = self.password_input.text()

        result = register_customer(name, surname, email, phone, password)
        if result:
            QMessageBox.information(self, "Kayıt Başarılı", "Müşteri kaydı başarıyla tamamlandı.")
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Müşteri kaydı sırasında bir hata oluştu.")
            self.reject()

# Veritabanı işlevlerinin tanımı
def register_customer(name, surname, email, phone, password):
    try:
        conn = sqlite3.connect('restaurant.db')
        c = conn.cursor()
        c.execute("INSERT INTO customers (name, surname, email, phone, password) VALUES (?, ?, ?, ?, ?)",
                  (name, surname, email, phone, password))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Hata: {e}")
        return False

def check_customer_credentials(email, password):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE email=? AND password=?", (email, password))
    result = c.fetchone()
    return bool(result)

def add_order(order):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    order_items = ", ".join(f"{item.split(' - $')[0]}: {item.split(' - $')[1]}" for item in order.items)
    c.execute("INSERT INTO orders (customer_name, customer_address, order_items) VALUES (?, ?, ?)",
              (order.customer_info.name, order.customer_info.address, order_items))
    conn.commit()

    # Update stock in the database for each item ordered
    for item in order.items:
        product_name, _ = item.split(" - $")
        _, _, stock = product_details[product_name]
        new_stock = stock - 1
        update_stock_in_db(product_name, 'Yemek', new_stock)  # Assuming 'Yemek' as default category

def get_orders():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("SELECT order_number, customer_name, customer_address, order_items FROM orders")
    return c.fetchall()

def delete_order(order_number):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE order_number = ?", (order_number,))
    conn.commit()

def get_menu():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("SELECT * FROM menu")
    return c.fetchall()

def update_stock_in_db(product_name, category, new_stock, price=None):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    if price is not None:
        c.execute("UPDATE menu SET stock = ? WHERE item_name = ? AND category = ? AND price = ?",
                  (new_stock, product_name, category, price))
    else:
        c.execute("UPDATE menu SET stock = ? WHERE item_name = ? AND category = ?",
                  (new_stock, product_name, category))
    conn.commit()

def check_credentials(username, password):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    return bool(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    initialize_database()
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
