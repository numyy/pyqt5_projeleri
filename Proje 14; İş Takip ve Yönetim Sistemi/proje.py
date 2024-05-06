class Proje:
    def __init__(self, proje_adi, baslangic_tarihi, bitis_tarihi, oncelik):
        self.proje_adi = proje_adi
        self.baslangic_tarihi = baslangic_tarihi
        self.bitis_tarihi = bitis_tarihi
        self.oncelik = oncelik
        self.gorevler = []

    def gorev_ata(self, gorev):
        self.gorevler.append(gorev)

    def ilerleme_kaydet(self, gorev, ilerleme):
        for g in self.gorevler:
            if g.gorev_adi == gorev:
                g.ilerleme = ilerleme

class Gorev:
    def __init__(self, gorev_adi, sorumlu):
        self.gorev_adi = gorev_adi
        self.sorumlu = sorumlu
        self.ilerleme = 0
        self.durum = "Beklemede"
        self.calisan = None  # Yeni özellik

    def durum_guncelle(self, yeni_durum):
        self.durum = yeni_durum

    def calisan_ata(self, calisan):  # Yeni metot
        self.calisan = calisan
        self.durum = "Aktif"

class Calisan:
    def __init__(self, isim, rol):
        self.isim = isim
        self.rol = rol
        self.gorevler = []

    def gorev_ata(self, gorev):
        self.gorevler.append(gorev)