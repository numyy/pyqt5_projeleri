import sys
import sqlite3  # sqlite3 modülünü import et
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QMessageBox, QDialog, QDialogButtonBox
import database

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

        result = database.check_credentials(username, password)

        if result:
            self.accept()
            self.parent().open_main_window_employee()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre.")

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
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.order_history = []

# Veri yapıları
products = [Product("Pizza", 20, 10), Product("Burger", 15, 15), Product("Salad", 10, 20)]
orders = []
customers = [Customer("John Doe", "123 Main St."), Customer("Jane Smith", "456 Elm St.")]

# Ana pencere sınıfı
class MainWindow(QMainWindow):
    def __init__(self, role):
        super().__init__()
        self.setWindowTitle("Restoran Sipariş ve Yönetim Sistemi")
        self.setGeometry(100, 100, 800, 600)

        # Widget oluşturma
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Menü görüntüleme
        menu_layout = QHBoxLayout()
        menu_label = QLabel("Menü:")
        menu_layout.addWidget(menu_label)
        self.menu_list = QListWidget()
        for product in products:
            item = f"{product.name} - ${product.price} (Stok: {product.stock})"
            self.menu_list.addItem(item)
        menu_layout.addWidget(self.menu_list)
        layout.addLayout(menu_layout)

        # Sipariş verme
        order_layout = QHBoxLayout()
        order_label = QLabel("Sipariş:")
        order_layout.addWidget(order_label)
        self.order_text = QTextEdit()
        order_layout.addWidget(self.order_text)
        layout.addLayout(order_layout)

        # Müşteri bilgileri
        customer_layout = QHBoxLayout()
        customer_label = QLabel("Müşteri Bilgileri:")
        customer_layout.addWidget(customer_label)
        self.customer_name = QLineEdit()
        self.customer_address = QLineEdit()
        customer_layout.addWidget(self.customer_name)
        customer_layout.addWidget(self.customer_address)
        layout.addLayout(customer_layout)

        # Sipariş gönderme
        submit_button = QPushButton("Sipariş Ver")
        submit_button.clicked.connect(self.submit_order)
        layout.addWidget(submit_button)

        # Kullanıcı rolünü göster
        role_label = QLabel(f"Rol: {role}")
        layout.addWidget(role_label)

    def submit_order(self):
        # Sipariş içeriğini al
        order_text = self.order_text.toPlainText()
        items = order_text.split("\n")

        # Müşteri bilgilerini al
        customer_name = self.customer_name.text()
        customer_address = self.customer_address.text()
        customer = Customer(customer_name, customer_address)

        # Sipariş numarası oluştur
        order_number = len(orders) + 1

        # Sipariş oluştur
        order = Order(order_number, items, customer)
        orders.append(order)
        customer.order_history.append(order_number)

        # Onay mesajı göster
        message = f"Sipariş #{order_number} başarıyla alındı.\n"
        message += f"Müşteri: {customer_name}\n"
        message += f"Adres: {customer_address}\n"
        message += "Sipariş İçeriği:\n"
        for item in items:
            message += f"- {item}\n"
        QMessageBox.information(self, "Sipariş Onayı", message)

        # Formu temizle
        self.order_text.clear()
        self.customer_name.clear()
        self.customer_address.clear()

# Giriş arayüzü
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

    def open_main_window_customer(self):
        self.main_window = MainWindow("Müşteri")
        self.main_window.show()
        self.close()

    def open_main_window_employee(self):
        # Çalışan girişi için ek doğrulama işlemleri yapılabilir
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())