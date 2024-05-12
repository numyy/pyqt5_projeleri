import os
import sqlite3

veritabani_adi = "sportakip.db"

# Veritabanı dosyası yoksa oluştur
if not os.path.exists(veritabani_adi):
    with sqlite3.connect(veritabani_adi) as conn:
        print(f"{veritabani_adi} veritabanı oluşturuldu.")

class VeriTabani:
    def __init__(self):
        self.baglanti = sqlite3.connect(veritabani_adi)
        self.imlec = self.baglanti.cursor()
        self.sporcular_tablosu_olustur()
        self.antrenman_programlari_tablosu_olustur()
        self.antrenmanlar_tablosu_olustur()  # Bu satırı ekleyin
        self.takip_tablosu_olustur()

    def sporcular_tablosu_olustur(self):
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS sporcular
                              (ad TEXT, soyad TEXT, spor_dali TEXT, yas INTEGER, PRIMARY KEY (ad, soyad))""")
        self.baglanti.commit()

    def takip_tablosu_olustur(self):
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS takip
                              (sporcu_ad TEXT, sporcu_soyad TEXT, antrenman_adi TEXT, program_adi TEXT, ilerleme_kaydi TEXT, PRIMARY KEY (sporcu_ad, sporcu_soyad, antrenman_adi, program_adi))""")
        self.baglanti.commit()

    def sporcu_ekle(self, ad, soyad, spor_dali, yas):
        self.imlec.execute("INSERT OR IGNORE INTO sporcular VALUES (?, ?, ?, ?)", (ad, soyad, spor_dali, yas))
        self.baglanti.commit()

    def sporcu_sil(self, ad, soyad):
        self.imlec.execute("DELETE FROM sporcular WHERE ad=? AND soyad=?", (ad, soyad))
        self.baglanti.commit()

    def sporcular_getir(self):
        self.imlec.execute("SELECT * FROM sporcular")
        return self.imlec.fetchall()


    def ilerleme_kaydet(self, sporcu_ad, sporcu_soyad, antrenman_adi, program_adi, ilerleme_kaydi):
        self.imlec.execute("INSERT OR REPLACE INTO takip VALUES (?, ?, ?, ?, ?)", (sporcu_ad, sporcu_soyad, antrenman_adi, program_adi, ilerleme_kaydi))
        self.baglanti.commit()

    def antrenmanlar_tablosu_olustur(self):
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS antrenmanlar
                              (antrenman_adi TEXT, detaylar TEXT, sure INTEGER, program_adi TEXT, sporcu_ad TEXT, sporcu_soyad TEXT, PRIMARY KEY (antrenman_adi, program_adi))""")
        self.baglanti.commit()

    def antrenman_programlari_tablosu_olustur(self):
        self.imlec.execute("""CREATE TABLE IF NOT EXISTS antrenman_programlari
                              (program_adi TEXT PRIMARY KEY, sporcu_ad TEXT, sporcu_soyad TEXT, spor_dali TEXT, antrenman_suresi INTEGER)""")
        self.baglanti.commit()

    def antrenman_programi_ekle(self, program_adi, sporcu_ad, sporcu_soyad, spor_dali, antrenman_suresi):
        self.imlec.execute("INSERT INTO antrenman_programlari VALUES (?, ?, ?, ?, ?)",
                           (program_adi, sporcu_ad, sporcu_soyad, spor_dali, antrenman_suresi))
        self.baglanti.commit()

    def antrenman_ekle(self, antrenman_adi, detaylar, sure, program_adi, sporcu_ad, sporcu_soyad):
        self.imlec.execute("INSERT INTO antrenmanlar VALUES (?, ?, ?, ?, ?, ?)",
                           (antrenman_adi, detaylar, sure, program_adi, sporcu_ad, sporcu_soyad))
        self.baglanti.commit()

    def programlari_getir(self):
        self.imlec.execute(
            "SELECT program_adi, sporcu_ad, sporcu_soyad, spor_dali, antrenman_suresi FROM antrenman_programlari")
        return self.imlec.fetchall()

    def baglanti_kapat(self):
        self.baglanti.close()