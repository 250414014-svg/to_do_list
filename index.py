# Kelas Induk
class Karakter:
    def serang(self):
        pass


# Kelas Anak
class Ksatria(Karakter):
    def serang(self):
        return "Ksatria mengayunkan pedang! (Damage Fisik)"


class Penyihir(Karakter):
    def serang(self):
        return "Penyihir merapalkan mantra bola api! (Damage Magic)"


class Pemanah(Karakter):
    def serang(self):
        return "Pemanah menembakkan panah beracun! (Damage Jarak Jauh)"


# Fungsi Polimorfisme
def simulasi_serangan(pasukan):
    for karakter in pasukan:
        print(karakter.serang())


# Membuat objek
ksatria = Ksatria()
penyihir = Penyihir()
pemanah = Pemanah()

# List pasukan
pasukan = [ksatria, penyihir, pemanah]

# Menjalankan simulasi
simulasi_serangan(pasukan)