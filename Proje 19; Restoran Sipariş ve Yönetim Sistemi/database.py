# database.py
import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect('restaurant.db')
c = conn.cursor()

# Çalışan tablosunu oluştur
c.execute('''CREATE TABLE IF NOT EXISTS employees
             (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

# Örnek veriler ekle
c.execute("INSERT INTO employees (username, password) VALUES ('admin', 'password')")
conn.commit()

def check_credentials(username, password):
    c.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    return bool(result)