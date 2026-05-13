import tkinter as tk
from tkinter import messagebox


# "class" = bir şablon (kalıp). Bu kalıptan "nesne" (örnek) üretirsin.
# Her Katilimci nesnesi kendi id, ad ve e-posta bilgisini taşır.
class Katilimci:
    # __init__ = nesne doğduğunda çalışan özel metod (kurucu / constructor).
    # "self" = o an oluşturulan nesnenin kendisi; alanları self.ad gibi bu nesneye bağlarsın.
    def __init__(self, katilimci_id, ad, email):
        self.katilimci_id = katilimci_id
        self.ad = ad
        self.email = email


# Etkinlik de bir sınıf: her etkinliğin id, ad, tarih, kapasitesi ve kayıtlı kişi listesi olur.
class Etkinlik:
    def __init__(self, etkinlik_id, ad, tarih, kapasite):
        self.etkinlik_id = etkinlik_id
        self.ad = ad
        self.tarih = tarih
        self.kapasite = int(kapasite)
        # Bu etkinliğe kayıtlı Katilimci nesnelerini tutan liste (boş başlar).
        self.kayitli_katilimcilar = []

    # Normal metod: bir Etkinlik nesnesi üzerinden çağrılır (etkinlik.katilimci_ekle(...)).
    # İçinde self ile o etkinliğin listesine ve kapasitesine erişirsin.
    def katilimci_ekle(self, katilimci):
        if len(self.kayitli_katilimcilar) < self.kapasite:
            self.kayitli_katilimcilar.append(katilimci)
            return True
        else:
            return False


# Bilet, bir Etkinlik ile bir Katilimci nesnesini bir arada temsil eder (ilişki).
class Bilet:
    def __init__(self, bilet_id, etkinlik, katilimci):
        self.bilet_id = bilet_id
        self.etkinlik = etkinlik
        self.katilimci = katilimci

    # @staticmethod: Bilet sınıfına ait ama "henüz bir bilet nesnesi yokken" de çağrılabilen metod.
    # İlk önce kapasiteyi kontrol edip bilet yaratır; nesne oluşturma mantığını tek yerde toplar.
    @staticmethod
    def bilet_olustur(bilet_id, etkinlik, katilimci):
        if etkinlik.katilimci_ekle(katilimci):
            yeni_bilet = Bilet(bilet_id, etkinlik, katilimci)
            return yeni_bilet
        else:
            return None


# Bu sınıf hem veriyi (etkinlik/katılımcı listeleri) hem de pencereyi yönetir: arayüz + iş mantığı bir arada.
class EtkinlikUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Etkinlik Kayıt Sistemi")
        self.root.geometry("450x750")

        # Anahtar = id (metin), değer = Etkinlik veya Katilimci nesnesi. Böylece id ile nesneyi hızlıca bulursun.
        self.etkinlikler = {}
        self.katilimcilar = {}
        self.biletler = []

        self.arayuz_tasarla()

    def arayuz_tasarla(self):
        frame_etkinlik = tk.LabelFrame(self.root, text="Etkinlik Ekle", padx=10, pady=10)
        frame_etkinlik.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_etkinlik, text="Etkinlik ID:").grid(row=0, column=0, sticky="w")
        self.entry_etkinlik_id = tk.Entry(frame_etkinlik)
        self.entry_etkinlik_id.grid(row=0, column=1, pady=2)

        tk.Label(frame_etkinlik, text="Etkinlik Adı:").grid(row=1, column=0, sticky="w")
        self.entry_etkinlik_ad = tk.Entry(frame_etkinlik)
        self.entry_etkinlik_ad.grid(row=1, column=1, pady=2)

        tk.Label(frame_etkinlik, text="Tarih:").grid(row=2, column=0, sticky="w")
        self.entry_etkinlik_tarih = tk.Entry(frame_etkinlik)
        self.entry_etkinlik_tarih.grid(row=2, column=1, pady=2)

        tk.Label(frame_etkinlik, text="Kapasite:").grid(row=3, column=0, sticky="w")
        self.entry_etkinlik_kapasite = tk.Entry(frame_etkinlik)
        self.entry_etkinlik_kapasite.grid(row=3, column=1, pady=2)

        # command=... : düğmeye basılınca bu sınıfın bir metodu çalışır; self otomatik verilir.
        tk.Button(frame_etkinlik, text="Etkinlik Ekle", command=self.etkinlik_ekle_cmd).grid(row=4, column=0, columnspan=2, pady=5)

        frame_katilimci = tk.LabelFrame(self.root, text="Katılımcı Ekle", padx=10, pady=10)
        frame_katilimci.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_katilimci, text="Katılımcı ID:").grid(row=0, column=0, sticky="w")
        self.entry_katilimci_id = tk.Entry(frame_katilimci)
        self.entry_katilimci_id.grid(row=0, column=1, pady=2)

        tk.Label(frame_katilimci, text="Ad Soyad:").grid(row=1, column=0, sticky="w")
        self.entry_katilimci_ad = tk.Entry(frame_katilimci)
        self.entry_katilimci_ad.grid(row=1, column=1, pady=2)

        tk.Label(frame_katilimci, text="E-mail:").grid(row=2, column=0, sticky="w")
        self.entry_katilimci_email = tk.Entry(frame_katilimci)
        self.entry_katilimci_email.grid(row=2, column=1, pady=2)

        tk.Button(frame_katilimci, text="Katılımcı Ekle", command=self.katilimci_ekle_cmd).grid(row=3, column=0, columnspan=2, pady=5)

        frame_bilet = tk.LabelFrame(self.root, text="Bilet Kes / Kayıt Yap", padx=10, pady=10)
        frame_bilet.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_bilet, text="Bilet ID:").grid(row=0, column=0, sticky="w")
        self.entry_bilet_id = tk.Entry(frame_bilet)
        self.entry_bilet_id.grid(row=0, column=1, pady=2)

        tk.Label(frame_bilet, text="Etkinlik ID:").grid(row=1, column=0, sticky="w")
        self.entry_bilet_etkinlik_id = tk.Entry(frame_bilet)
        self.entry_bilet_etkinlik_id.grid(row=1, column=1, pady=2)

        tk.Label(frame_bilet, text="Katılımcı ID:").grid(row=2, column=0, sticky="w")
        self.entry_bilet_katilimci_id = tk.Entry(frame_bilet)
        self.entry_bilet_katilimci_id.grid(row=2, column=1, pady=2)

        tk.Button(frame_bilet, text="Bilet Oluştur", command=self.bilet_olustur_cmd).grid(row=3, column=0, columnspan=2, pady=5)

        frame_rapor = tk.LabelFrame(self.root, text="Etkinlik Raporları", padx=10, pady=10)
        frame_rapor.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Button(frame_rapor, text="Katılım Raporunu Göster", command=self.rapor_goster_cmd).pack(pady=5)

        self.text_rapor = tk.Text(frame_rapor, height=10, width=45)
        self.text_rapor.pack(pady=5)

    def etkinlik_ekle_cmd(self):
        # Formdan yazıları oku; bunlar henüz nesne değil, düz metin.
        e_id = self.entry_etkinlik_id.get()
        ad = self.entry_etkinlik_ad.get()
        tarih = self.entry_etkinlik_tarih.get()
        kapasite = self.entry_etkinlik_kapasite.get()

        if e_id and ad and tarih and kapasite.isdigit():
            # Etkinlik(...) ile yeni bir Etkinlik nesnesi üretilir; sözlüğe id ile kaydedilir.
            yeni_etkinlik = Etkinlik(e_id, ad, tarih, kapasite)
            self.etkinlikler[e_id] = yeni_etkinlik
            messagebox.showinfo("Başarılı", f"{ad} etkinliği sisteme eklendi.")
            self.entry_etkinlik_id.delete(0, tk.END)
            self.entry_etkinlik_ad.delete(0, tk.END)
            self.entry_etkinlik_tarih.delete(0, tk.END)
            self.entry_etkinlik_kapasite.delete(0, tk.END)
        else:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doğru doldurun (Kapasite sayı olmalı).")

    def katilimci_ekle_cmd(self):
        k_id = self.entry_katilimci_id.get()
        ad = self.entry_katilimci_ad.get()
        email = self.entry_katilimci_email.get()

        if k_id and ad and email:
            yeni_katilimci = Katilimci(k_id, ad, email)
            self.katilimcilar[k_id] = yeni_katilimci
            messagebox.showinfo("Başarılı", f"{ad} adlı katılımcı sisteme eklendi.")
            self.entry_katilimci_id.delete(0, tk.END)
            self.entry_katilimci_ad.delete(0, tk.END)
            self.entry_katilimci_email.delete(0, tk.END)
        else:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")

    def bilet_olustur_cmd(self):
        b_id = self.entry_bilet_id.get()
        e_id = self.entry_bilet_etkinlik_id.get()
        k_id = self.entry_bilet_katilimci_id.get()

        if b_id and e_id and k_id:
            # Sözlükte id var mı diye bakıyoruz; varsa değer zaten Etkinlik / Katilimci nesnesi.
            if e_id in self.etkinlikler and k_id in self.katilimcilar:
                etkinlik = self.etkinlikler[e_id]
                katilimci = self.katilimcilar[k_id]

                # Sınıf üzerinden çağrı: içeride etkinlik.katilimci_ekle ile kapasite kontrol edilir.
                yeni_bilet = Bilet.bilet_olustur(b_id, etkinlik, katilimci)

                if yeni_bilet:
                    self.biletler.append(yeni_bilet)
                    messagebox.showinfo("Başarılı", f"Bilet kesildi! {katilimci.ad}, {etkinlik.ad} etkinliğine kaydedildi.")
                else:
                    messagebox.showerror("Hata", "Bu etkinliğin kapasitesi dolmuştur!")
            else:
                messagebox.showerror("Hata", "Geçersiz Etkinlik ID veya Katılımcı ID.")
        else:
            messagebox.showwarning("Hata", "Lütfen bilet için tüm alanları doldurun.")

    def rapor_goster_cmd(self):
        # Her Etkinlik nesnesinin kendi kayitli_katilimcilar listesi var; len(...) katılan sayısını verir.
        self.text_rapor.delete(1.0, tk.END)
        self.text_rapor.insert(tk.END, "--- ETKİNLİK KATILIM RAPORU ---\n\n")

        if not self.etkinlikler:
            self.text_rapor.insert(tk.END, "Sistemde henüz etkinlik bulunmuyor.")
            return

        # .items() ile hem id hem de o id'ye bağlı Etkinlik nesnesini döngüde alırsın.
        for e_id, etkinlik in self.etkinlikler.items():
            katilan_sayisi = len(etkinlik.kayitli_katilimcilar)
            bos_yer = etkinlik.kapasite - katilan_sayisi
            rapor_metni = f"Etkinlik: {etkinlik.ad} (ID: {e_id})\n"
            rapor_metni += f"Tarih: {etkinlik.tarih}\n"
            rapor_metni += f"Kapasite: {etkinlik.kapasite} | Katılan: {katilan_sayisi} | Boş Yer: {bos_yer}\n"
            rapor_metni += "-" * 35 + "\n"
            self.text_rapor.insert(tk.END, rapor_metni)


# Bu dosya doğrudan çalıştırılıyorsa pencere açılır; başka dosyadan import edilirse burası çalışmaz.
if __name__ == "__main__":
    pencere = tk.Tk()
    # EtkinlikUygulamasi(pencere) = uygulama nesnesi; tüm arayüz ve veri bu nesnenin içinde yaşar.
    uygulama = EtkinlikUygulamasi(pencere)
    pencere.mainloop()
