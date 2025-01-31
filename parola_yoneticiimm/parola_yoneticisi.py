from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(kendi):
        kendi.key = None
        kendi.sifre_dosyasi = None
        kendi.sifre_sozluk = {}

    def olustur_key(kendi, yol):
        kendi.key = Fernet.generate_key()
        with open(yol, 'wb') as f:
            f.write(kendi.key)

    def yukle_key(kendi, yol):
        with open(yol, 'rb') as f:
            kendi.key = f.read()

    def olustur_sifre_dosyasi(kendi, yol, baslangic_degerleri=None):
        kendi.sifre_dosyasi = yol

        if baslangic_degerleri is not None:
            for key, deger in baslangic_degerleri.items():
                kendi.ekle_sifre(key, deger)


    def yukle_sifre_dosyasi(kendi, yol):
        kendi.sifre_dosyasi = yol

        with open(yol, 'r') as f:
            for satir in f:
                site, encrypted = satir.split(":")
                kendi.sifre_sozluk[site] = Fernet(kendi.key).decrypt(encrypted.encode()).decode()


    def ekle_sifre(kendi, site, sifre):
        kendi.sifre_sozluk[site] = sifre

        if kendi.sifre_dosyasi is not None:
            with open(kendi.sifre_dosyasi, 'a+') as f:
                encrypted = Fernet(kendi.key).encrypt(sifre.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    
    def ulas_sifre(kendi, site):
        return kendi.sifre_sozluk[site]

    
    def gosterhepsini_sifre_dosyasi(kendi, yol):
        kendi.sifre_dosyasi = yol

        with open(yol, 'r') as f:
            for satir in f.readlines():
                data = satir.rstrip()
                site, kendi.sifre_sozluk[site] = data.split(":")


def main():
    sifre = {
        "email": "1234567",
        "facebook": "denemefbsifresi",
        "youtube": "denemeyoutubesifre",
        "something": "denemesifre123"
    }

    pm = PasswordManager()

    print("""\nLütfen yapmak istediğiniz işlemi tuşlayınız.\n
    (1) Yeni bir anahtar oluştur
    (2) Mevcut bir anahtarı yükle
    (3) Yeni şifre dosyası oluştur
    (4) Mevcut şifre dosyasını yükle
    (5) Şifre dosyanıza yeni bir site & şifre ekleyin
    (6) Şifrene ulaş
    (7) Bütün Şifreleri Göster
    (q) Çıkış         
    """)

    done = False

    while not done:

        secim = input("Lütfen işlem tercihinizi tuşlayınız: ")
        if secim == "1":
            yol = input("''ornek.key'' şeklinde isim girerek anahtar oluşturunuz: ")
            pm.olustur_key(yol)
        elif secim == "2":
            yol = input("Anahtar isminizi ''anahtar.key'' şeklinde giriniz: ")
            pm.yukle_key(yol)
        elif secim == "3":
            yol = input("Şifre dosyası oluşturmak için ''ornek.pass'' şeklinde yazınız: ")
            pm.olustur_sifre_dosyasi(yol, sifre)
        elif secim == "4":
            yol = input("Şifre dosyanızı yüklemek için ''ornek.pass'' şeklinde giriniz: ")
            pm.yukle_sifre_dosyasi(yol)
        elif secim == "5":
            site = input("Siteyi giriniz: ")
            sifre = input("Şifrenizi tuşlayınız: ")
            pm.ekle_sifre(site, sifre)
        elif secim == "6":
            site = input ("Bilgilerinize ulaşmak istediğiniz siteyi giriniz: ")
            print(f"{site} sitesi için şifreniz: {pm.ulas_sifre(site)}")
        elif secim == "7":
            print(f"sitesi için şifreniz: {pm.gosterhepsini_sifre_dosyasi}")
        elif secim == "q":
            done = True
            print("\nKendine iyi bak :)\n")
        else:
            print("Geçersiz secenek!")



if __name__ == "__main__":
    main()
    






    




    






