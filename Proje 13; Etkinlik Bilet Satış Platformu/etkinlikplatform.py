from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QMessageBox, QTableWidget, QTableWidgetItem, QCalendarWidget, QSpinBox
import sys
import sqlite3

conn = sqlite3.connect('etkinlik_db.sqlite')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS kullanicilar
             (id INTEGER PRIMARY KEY AUTOINCREMENT, kullanici_adi TEXT, sifre TEXT, ad TEXT, soyad TEXT,rol TEXT DEFAULT 'kullanici')""")

c.execute("""CREATE TABLE IF NOT EXISTS etkinlikler
             (id INTEGER PRIMARY KEY AUTOINCREMENT, adi TEXT, tarih TEXT, mekan TEXT, fiyat REAL, kontenjan INTEGER, satis_sayisi INTEGER DEFAULT 0)""")

c.execute("""CREATE TABLE IF NOT EXISTS biletler
             (id INTEGER PRIMARY KEY AUTOINCREMENT, etkinlik_id INTEGER, kullanici_id INTEGER)""")

conn.commit()
conn.close()

class HesapOlusturPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hesap Oluştur")
        self.setGeometry(100, 100, 300, 200)

        self.kullanici_adi_label = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_input = QLineEdit()
        self.sifre_label = QLabel("Şifre:")
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.ad_label = QLabel("Ad:")
        self.ad_input = QLineEdit()
        self.soyad_label = QLabel("Soyad:")
        self.soyad_input = QLineEdit()
        self.hesap_olustur_button = QPushButton("Hesap Oluştur")
        self.hesap_olustur_button.clicked.connect(self.hesap_olustur)

        layout = QVBoxLayout()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_input)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_input)
        layout.addWidget(self.ad_label)
        layout.addWidget(self.ad_input)
        layout.addWidget(self.soyad_label)
        layout.addWidget(self.soyad_input)
        layout.addWidget(self.hesap_olustur_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def hesap_olustur(self):
        kullanici_adi = self.kullanici_adi_input.text()
        sifre = self.sifre_input.text()
        ad = self.ad_input.text()
        soyad = self.soyad_input.text()
        rol = 'kullanici'  # Varsayılan olarak normal kullanıcı rolü ataması

        if kullanici_adi and sifre and ad and soyad:
            if kullanici_adi == 'admin':  # Eğer kullanıcı adı 'admin' ise, yönetici rolü ata
                rol = 'admin'

            conn = sqlite3.connect('etkinlik_db.sqlite')
            c = conn.cursor()
            c.execute("INSERT INTO kullanicilar (kullanici_adi, sifre, ad, soyad, rol) VALUES (?, ?, ?, ?, ?)",
                      (kullanici_adi, sifre, ad, soyad, rol))
            conn.commit()
            conn.close()

            self.close()
            self.girisPenceresi = GirisPenceresi()
            self.girisPenceresi.show()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")

class GirisPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setGeometry(100, 100, 300, 150)

        self.kullanici_adi_label = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_input = QLineEdit()
        self.sifre_label = QLabel("Şifre:")
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.giris_button = QPushButton("Giriş Yap")
        self.giris_button.clicked.connect(self.kullanici_girisi)
        self.hesap_olustur_button = QPushButton("Hesap Oluştur")
        self.hesap_olustur_button.clicked.connect(self.hesap_olustur)

        layout = QVBoxLayout()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_input)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_input)
        layout.addWidget(self.giris_button)
        layout.addWidget(self.hesap_olustur_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def hesap_olustur(self):
        self.close()
        self.hesap_olustur_penceresi = HesapOlusturPenceresi()
        self.hesap_olustur_penceresi.show()

    def kullanici_girisi(self):
        kullanici_adi = self.kullanici_adi_input.text()
        sifre = self.sifre_input.text()

        conn = sqlite3.connect('etkinlik_db.sqlite')
        c = conn.cursor()
        c.execute("SELECT id, ad, soyad FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        kullanici = c.fetchone()
        conn.close()

        if kullanici:
            kullanici_id, ad, soyad = kullanici
            self.close()
            self.anaPencere = EtkinlikPlatformu(kullanici_adi, ad, soyad)
            self.anaPencere.show()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre.")

class EtkinlikPlatformu(QMainWindow):
    def __init__(self, kullanici_adi, ad, soyad):
        super().__init__()
        self.setWindowTitle("Etkinlik ve Bilet Satış Platformu")
        self.setGeometry(100, 100, 800, 400)
        self.kullanici_adi = kullanici_adi
        self.biletler = []

        # Kullanıcı rolünü kontrol et
        conn = sqlite3.connect('etkinlik_db.sqlite')
        c = conn.cursor()
        c.execute("SELECT rol FROM kullanicilar WHERE kullanici_adi=?", (kullanici_adi,))
        rol = c.fetchone()[0]
        conn.close()

        # Kullanıcı adı ve soyadı labelini ekle
        kullanici_bilgi_label = QLabel(f"Hoşgeldiniz, {ad} {soyad}")
        font = kullanici_bilgi_label.font()
        font.setPointSize(12)
        kullanici_bilgi_label.setFont(font)

        # satis_sayisi sütunu kontrolü
        conn = sqlite3.connect('etkinlik_db.sqlite')
        c = conn.cursor()
        c.execute("PRAGMA table_info(etkinlikler)")
        columns = c.fetchall()
        if not any(col[1] == 'satis_sayisi' for col in columns):
            c.execute("ALTER TABLE etkinlikler ADD COLUMN satis_sayisi INTEGER DEFAULT 0")
        conn.commit()
        conn.close()

        self.etkinlik_olustur_button = QPushButton("Etkinlik Oluştur")
        self.etkinlik_olustur_button.clicked.connect(self.etkinlik_olustur_penceresi_ac)
        self.etkinlik_tablosu = QTableWidget()
        self.etkinlik_tablosu.setColumnCount(3)
        self.etkinlik_tablosu.setHorizontalHeaderLabels(["Etkinlik Adı", "Tarih", "Mekan"])
        self.etkinlik_sil_button = QPushButton("Etkinlik Sil")
        self.etkinlik_sil_button.clicked.connect(self.etkinlik_sil)

        self.bilet_al_button = QPushButton("Bilet Al")
        self.bilet_al_button.clicked.connect(self.bilet_al)
        self.biletlerim_button = QPushButton("Biletlerim")
        self.biletlerim_button.clicked.connect(self.biletleri_goster)
        self.bilet_tablosu = QTableWidget()  # Bilet tablosunu burada tanımla
        self.bilet_tablosu.setColumnCount(3)
        self.bilet_tablosu.setHorizontalHeaderLabels(["Etkinlik Adı", "Tarih", "Mekan"])

        layout = QVBoxLayout()
        layout.addWidget(kullanici_bilgi_label)

        # Eğer rol 'kullanici' ise, etkinlik oluştur butonunu gizle
        if rol == 'kullanici':
            self.etkinlik_olustur_button.setVisible(False)
            self.etkinlik_sil_button.setVisible(False)
        else:
            layout.addWidget(self.etkinlik_olustur_button)

        layout.addWidget(self.etkinlik_sil_button)
        layout.addWidget(self.etkinlik_tablosu)
        layout.addWidget(self.bilet_al_button)
        layout.addWidget(self.biletlerim_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.etkinlikleri_yukle()
        self.biletleri_yukle()

    def etkinlik_sil(self):
        secili_satir = self.etkinlik_tablosu.currentRow()
        if secili_satir != -1:
            etkinlik_adi = self.etkinlik_tablosu.item(secili_satir, 0).text()
            cevap = QMessageBox.question(self, "Etkinlik Sil",
                                         f"{etkinlik_adi} etkinliğini silmek istediğinize emin misiniz?",
                                         QMessageBox.Yes | QMessageBox.No)
            if cevap == QMessageBox.Yes:
                conn = sqlite3.connect('etkinlik_db.sqlite')
                c = conn.cursor()
                c.execute("DELETE FROM etkinlikler WHERE adi=?", (etkinlik_adi,))
                conn.commit()
                conn.close()
                self.etkinlikleri_guncelle()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir etkinlik seçin.")
    def etkinlikleri_guncelle(self):
        self.etkinlik_tablosu.setRowCount(0)  # Tabloyu sıfırla
        self.etkinlikleri_yukle()  # Etkinlikleri yeniden yükle

    def etkinlik_olustur_penceresi_ac(self):
        self.etkinlik_olustur_penceresi = EtkinlikOlusturPenceresi(self)
        self.etkinlik_olustur_penceresi.show()

    def etkinlikleri_yukle(self):
        conn = sqlite3.connect('etkinlik_db.sqlite')
        c = conn.cursor()
        c.execute("SELECT adi, tarih, mekan, fiyat, kontenjan, satis_sayisi FROM etkinlikler")
        etkinlikler = c.fetchall()
        conn.close()

        self.etkinlik_tablosu.setRowCount(len(etkinlikler))
        self.etkinlik_tablosu.setColumnCount(6)
        self.etkinlik_tablosu.setHorizontalHeaderLabels(
            ["Etkinlik Adı", "Tarih", "Mekan", "Bilet Fiyatı", "Kontenjan", "Satış Sayısı", "Kalan Kontenjan"])

        for i, etkinlik in enumerate(etkinlikler):
            self.etkinlik_tablosu.setItem(i, 0, QTableWidgetItem(etkinlik[0]))
            self.etkinlik_tablosu.setItem(i, 1, QTableWidgetItem(etkinlik[1]))
            self.etkinlik_tablosu.setItem(i, 2, QTableWidgetItem(etkinlik[2]))
            self.etkinlik_tablosu.setItem(i, 3, QTableWidgetItem(str(etkinlik[3])))
            self.etkinlik_tablosu.setItem(i, 4, QTableWidgetItem(str(etkinlik[4])))
            self.etkinlik_tablosu.setItem(i, 5, QTableWidgetItem(str(etkinlik[5])))
            kalan_kontenjan = etkinlik[4] - etkinlik[5]
            self.etkinlik_tablosu.setItem(i, 6, QTableWidgetItem(str(kalan_kontenjan)))

    def bilet_al(self):
        secili_satir = self.etkinlik_tablosu.currentRow()
        if secili_satir != -1:
            etkinlik_adi = self.etkinlik_tablosu.item(secili_satir, 0).text()
            tarih = self.etkinlik_tablosu.item(secili_satir, 1).text()
            mekan = self.etkinlik_tablosu.item(secili_satir, 2).text()

            self.bilet_satin_alma_penceresi = BiletSatinAlmaPenceresi(self, etkinlik_adi, tarih, mekan)
            self.bilet_satin_alma_penceresi.show()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir etkinlik seçin.")

    def biletleri_goster(self):
        self.bilet_tablosu = QTableWidget()
        self.bilet_tablosu.setColumnCount(3)
        self.bilet_tablosu.setHorizontalHeaderLabels(["Etkinlik Adı", "Tarih", "Mekan"])
        self.biletleri_yukle()

        self.bilet_penceresi = QMainWindow()
        self.bilet_penceresi.setWindowTitle("Biletlerim")
        self.bilet_penceresi.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        layout.addWidget(self.bilet_tablosu)

        widget = QWidget()
        widget.setLayout(layout)
        self.bilet_penceresi.setCentralWidget(widget)
        self.bilet_penceresi.show()

    def biletleri_yukle(self):
        conn = sqlite3.connect('etkinlik_db.sqlite')
        c = conn.cursor()
        c.execute("SELECT id FROM kullanicilar WHERE kullanici_adi=?", (self.kullanici_adi,))
        kullanici_id = c.fetchone()[0]
        c.execute("""
            SELECT etkinlikler.adi, etkinlikler.tarih, etkinlikler.mekan, COUNT(biletler.id) AS bilet_sayisi
            FROM biletler
            JOIN etkinlikler ON biletler.etkinlik_id = etkinlikler.id
            WHERE biletler.kullanici_id=?
            GROUP BY etkinlikler.id
        """, (kullanici_id,))
        biletler = c.fetchall()
        conn.close()

        self.bilet_tablosu.setRowCount(len(biletler))
        self.bilet_tablosu.setColumnCount(4)
        self.bilet_tablosu.setHorizontalHeaderLabels(["Etkinlik Adı", "Tarih", "Mekan", "Bilet Sayısı"])

        for i, bilet in enumerate(biletler):
            etkinlik_adi, tarih, mekan, bilet_sayisi = bilet
            self.bilet_tablosu.setItem(i, 0, QTableWidgetItem(etkinlik_adi))
            self.bilet_tablosu.setItem(i, 1, QTableWidgetItem(tarih))
            self.bilet_tablosu.setItem(i, 2, QTableWidgetItem(mekan))
            self.bilet_tablosu.setItem(i, 3, QTableWidgetItem(str(bilet_sayisi)))
class EtkinlikOlusturPenceresi(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Etkinlik Oluştur")
        self.setGeometry(100, 100, 400, 400)

        self.etkinlik_adi_label = QLabel("Etkinlik Adı:")
        self.etkinlik_adi_input = QLineEdit()
        self.etkinlik_mekan_label = QLabel("Etkinlik Mekanı:")
        self.etkinlik_mekan_input = QLineEdit()
        self.etkinlik_fiyat_label = QLabel("Bilet Fiyatı:")
        self.etkinlik_fiyat_input = QLineEdit()
        self.etkinlik_kontenjan_label = QLabel("Kontenjan:")
        self.etkinlik_kontenjan_input = QLineEdit()
        self.etkinlik_olustur_button = QPushButton("Etkinlik Oluştur")
        self.etkinlik_olustur_button.clicked.connect(self.etkinlik_olustur)
        self.etkinlik_tarih_input = ""
        self.takvim = QCalendarWidget()
        self.takvim.selectionChanged.connect(self.tarih_secildi)

        layout = QVBoxLayout()
        layout.addWidget(self.etkinlik_adi_label)
        layout.addWidget(self.etkinlik_adi_input)
        layout.addWidget(self.etkinlik_mekan_label)
        layout.addWidget(self.etkinlik_mekan_input)
        layout.addWidget(self.etkinlik_fiyat_label)
        layout.addWidget(self.etkinlik_fiyat_input)
        layout.addWidget(self.etkinlik_kontenjan_label)
        layout.addWidget(self.etkinlik_kontenjan_input)
        layout.addWidget(self.takvim)
        layout.addWidget(self.etkinlik_olustur_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def tarih_secildi(self):
        secili_tarih = self.takvim.selectedDate()
        bugun = QDate.currentDate()
        if secili_tarih >= bugun:
            self.etkinlik_tarih_input = secili_tarih.toString("dd/MM/yyyy")
        else:
            QMessageBox.warning(self, "Hata",
                                "Geçmiş bir tarih seçemezsiniz. Lütfen bugünün veya gelecek bir tarih seçin.")
            self.takvim.setSelectedDate(bugun)

    def etkinlik_olustur(self):
        adi = self.etkinlik_adi_input.text()
        tarih = self.etkinlik_tarih_input
        mekan = self.etkinlik_mekan_input.text()
        fiyat = self.etkinlik_fiyat_input.text()
        kontenjan = self.etkinlik_kontenjan_input.text()
        if adi and tarih and mekan and fiyat and kontenjan:
            tarih_object = QDate.fromString(tarih, "dd/MM/yyyy")
            bugun = QDate.currentDate()
            if tarih_object >= bugun:
                conn = sqlite3.connect('etkinlik_db.sqlite')
                c = conn.cursor()
                c.execute("INSERT INTO etkinlikler (adi, tarih, mekan, fiyat, kontenjan) VALUES (?, ?, ?, ?, ?)",
                          (adi, tarih, mekan, fiyat, kontenjan))
                conn.commit()
                conn.close()

                self.close()
                self.parent().etkinlikleri_guncelle()
            else:
                QMessageBox.warning(self, "Hata", "Geçmiş bir tarih için etkinlik oluşturamazsınız.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")

class BiletSatinAlmaPenceresi(QMainWindow):
    def __init__(self, parent=None, etkinlik_adi=None, tarih=None, mekan=None):
        super().__init__(parent)
        self.setWindowTitle("Bilet Satın Alma")
        self.setGeometry(100, 100, 400, 300)
        self.parent = parent
        self.etkinlik_adi = etkinlik_adi
        self.tarih = tarih
        self.mekan = mekan
        self.biletler = []

        self.bilet_sayisi_label = QLabel("Bilet Sayısı:")
        self.bilet_sayisi_spin = QSpinBox()
        self.kart_numarasi_label = QLabel("Kart Numarası:")
        self.kart_numarasi_input = QLineEdit()
        self.son_kullanma_tarihi_label = QLabel("Son Kullanma Tarihi (AA/YY):")
        self.son_kullanma_tarihi_input = QLineEdit()
        self.guvenlik_kodu_label = QLabel("Güvenlik Kodu:")
        self.guvenlik_kodu_input = QLineEdit()
        self.satin_al_button = QPushButton("Satın Al")
        self.satin_al_button.clicked.connect(self.bilet_satin_al)

        layout = QVBoxLayout()
        layout.addWidget(self.bilet_sayisi_label)
        layout.addWidget(self.bilet_sayisi_spin)
        layout.addWidget(self.kart_numarasi_label)
        layout.addWidget(self.kart_numarasi_input)
        layout.addWidget(self.son_kullanma_tarihi_label)
        layout.addWidget(self.son_kullanma_tarihi_input)
        layout.addWidget(self.guvenlik_kodu_label)
        layout.addWidget(self.guvenlik_kodu_input)
        layout.addWidget(self.satin_al_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def bilet_satin_al(self):
        bilet_sayisi = self.bilet_sayisi_spin.value()
        kart_numarasi = self.kart_numarasi_input.text()
        son_kullanma_tarihi = self.son_kullanma_tarihi_input.text()
        guvenlik_kodu = self.guvenlik_kodu_input.text()

        if bilet_sayisi > 0 and kart_numarasi and son_kullanma_tarihi and guvenlik_kodu:
            conn = sqlite3.connect('etkinlik_db.sqlite')
            c = conn.cursor()
            c.execute("SELECT id FROM kullanicilar WHERE kullanici_adi=?", (self.parent.kullanici_adi,))
            kullanici_id = c.fetchone()[0]
            c.execute("SELECT id, kontenjan, satis_sayisi FROM etkinlikler WHERE adi=? AND tarih=? AND mekan=?",
                      (self.etkinlik_adi, self.tarih, self.mekan))
            etkinlik = c.fetchone()

            if etkinlik:
                etkinlik_id, kontenjan, satis_sayisi = etkinlik
                if satis_sayisi + bilet_sayisi <= kontenjan:
                    # Ödeme işlemi simülasyonu
                    QMessageBox.information(self, "Ödeme", "Ödeme işlemi gerçekleştirildi.")

                    # Biletleri ekle
                    for _ in range(bilet_sayisi):
                        c.execute("INSERT INTO biletler (etkinlik_id, kullanici_id) VALUES (?, ?)",
                                  (etkinlik_id, kullanici_id))

                    # satis_sayisi sütununu güncelle
                    yeni_satis_sayisi = satis_sayisi + bilet_sayisi
                    c.execute("UPDATE etkinlikler SET satis_sayisi=? WHERE id=?",
                              (yeni_satis_sayisi, etkinlik_id))

                    conn.commit()
                    self.parent.etkinlikleri_guncelle()  # Etkinlik tablosunu güncelle
                    self.parent.biletleri_yukle()  # Bilet tablosunu güncelle
                    QMessageBox.information(self, "Başarılı", f"{bilet_sayisi} adet bilet başarıyla satın alındı.")
                else:
                    QMessageBox.warning(self, "Hata", "Maalesef kontenjan yetersiz.")
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz etkinlik bilgileri.")

            conn.close()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
    def biletleri_yukle(self):
        self.bilet_tablosu.setRowCount(len(self.biletler))
        for i, bilet in enumerate(self.biletler):
            etkinlik_adi, tarih, mekan = bilet
            self.bilet_tablosu.setItem(i, 0, QTableWidgetItem(etkinlik_adi))
            self.bilet_tablosu.setItem(i, 1, QTableWidgetItem(tarih))
            self.bilet_tablosu.setItem(i, 2, QTableWidgetItem(mekan))
            self.parent.bilet_tablosu.setRowCount(0)
            self.parent.biletleri_yukle()


class Etkinlik:
    def __init__(self, adi, tarih, mekan):
        self.adi = adi
        self.tarih = tarih
        self.mekan = mekan

    def etkinlik_ekle(self):
        conn = sqlite3.connect('etkinlik_db.sqlite')
        c = conn.cursor()
        c.execute("INSERT INTO etkinlikler (adi, tarih, mekan) VALUES (?, ?, ?)", (self.adi, self.tarih, self.mekan))
        conn.commit()
        conn.close()

    def bilet_sat(self, kullanici_id):
        conn = sqlite3.connect('etkinlik_db.sqlite')
        c = conn.cursor()
        c.execute("SELECT id FROM etkinlikler WHERE adi=? AND tarih=? AND mekan=?", (self.adi, self.tarih, self.mekan))
        etkinlik = c.fetchone()
        if etkinlik:
            etkinlik_id = etkinlik[0]
            c.execute("INSERT INTO biletler (etkinlik_id, kullanici_id) VALUES (?, ?)", (etkinlik_id, kullanici_id))
            conn.commit()
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    girisPenceresi = GirisPenceresi()
    girisPenceresi.show()
    sys.exit(app.exec_())
