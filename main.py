from tkinter import messagebox

import customtkinter as ctk


class Katilimci:
    def __init__(self, katilimci_id, ad, email):
        self.katilimci_id = katilimci_id
        self.ad = ad
        self.email = email


class Etkinlik:
    def __init__(self, etkinlik_id, ad, tarih, kapasite):
        self.etkinlik_id = etkinlik_id
        self.ad = ad
        self.tarih = tarih
        self.kapasite = int(kapasite)
        self.kayitli_katilimcilar = []

    def katilimci_ekle(self, katilimci):
        if len(self.kayitli_katilimcilar) < self.kapasite:
            self.kayitli_katilimcilar.append(katilimci)
            return True
        return False


class Bilet:
    def __init__(self, bilet_id, etkinlik, katilimci):
        self.bilet_id = bilet_id
        self.etkinlik = etkinlik
        self.katilimci = katilimci

    @staticmethod
    def bilet_olustur(bilet_id, etkinlik, katilimci):
        if etkinlik.katilimci_ekle(katilimci):
            return Bilet(bilet_id, etkinlik, katilimci)
        return None


COLORS = {
    "bg": "#0f1117",
    "sidebar": "#161b26",
    "card": "#1c2333",
    "card_hover": "#242d42",
    "accent": "#6366f1",
    "accent_hover": "#818cf8",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "text": "#f1f5f9",
    "text_muted": "#94a3b8",
    "border": "#2d3748",
    "input_bg": "#252f3f",
}


class EtkinlikUygulamasi(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Etkinlik Kayıt Sistemi")
        self.geometry("1180x720")
        self.minsize(960, 600)
        self.configure(fg_color=COLORS["bg"])

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.etkinlikler = {}
        self.katilimcilar = {}
        self.biletler = []
        self.aktif_sayfa = None

        self._arayuz_olustur()
        self._sayfa_goster("panel")

    def _arayuz_olustur(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._sidebar_olustur()
        self.icerik = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        self.icerik.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)
        self.icerik.grid_columnconfigure(0, weight=1)
        self.icerik.grid_rowconfigure(1, weight=1)

        self.sayfalar = {}
        for ad in ("panel", "etkinlik", "katilimci", "bilet", "rapor"):
            frame = ctk.CTkScrollableFrame(
                self.icerik,
                fg_color=COLORS["bg"],
                scrollbar_button_color=COLORS["accent"],
                scrollbar_button_hover_color=COLORS["accent_hover"],
            )
            frame.grid(row=1, column=0, sticky="nsew", padx=28, pady=(0, 24))
            frame.grid_columnconfigure(0, weight=1)
            self.sayfalar[ad] = frame

        self._panel_sayfasi()
        self._etkinlik_sayfasi()
        self._katilimci_sayfasi()
        self._bilet_sayfasi()
        self._rapor_sayfasi()

    def _sidebar_olustur(self):
        sidebar = ctk.CTkFrame(self, width=240, fg_color=COLORS["sidebar"], corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(28, 32))

        ctk.CTkLabel(
            logo_frame,
            text="🎫",
            font=ctk.CTkFont(size=32),
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="Etkinlik Kayıt",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w", pady=(8, 0))

        ctk.CTkLabel(
            logo_frame,
            text="Yönetim Paneli",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w")

        self.nav_butonlar = {}
        nav_items = [
            ("panel", "📊  Panel"),
            ("etkinlik", "📅  Etkinlikler"),
            ("katilimci", "👥  Katılımcılar"),
            ("bilet", "🎟️ Biletler"),
            ("rapor", "📋  Raporlar"),
        ]

        nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=12)

        for key, label in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=label,
                anchor="w",
                height=44,
                corner_radius=10,
                font=ctk.CTkFont(family="Segoe UI", size=14),
                fg_color="transparent",
                text_color=COLORS["text_muted"],
                hover_color=COLORS["card_hover"],
                command=lambda k=key: self._sayfa_goster(k),
            )
            btn.pack(fill="x", pady=3)
            self.nav_butonlar[key] = btn

        ctk.CTkLabel(
            sidebar,
            text="v2.0  ·  Masaüstü",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"],
        ).pack(side="bottom", pady=20)

    def _sayfa_baslik(self, parent, baslik, alt):
        header = ctk.CTkFrame(self.icerik, fg_color=COLORS["bg"], height=80)
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 0))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=baslik,
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=COLORS["text"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text=alt,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=COLORS["text_muted"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        return header

    def _sayfa_goster(self, ad):
        basliklar = {
            "panel": ("Genel Bakış", "Sistemin anlık durumunu görüntüleyin"),
            "etkinlik": ("Etkinlik Yönetimi", "Yeni etkinlik oluşturun ve mevcutları görün"),
            "katilimci": ("Katılımcı Yönetimi", "Katılımcıları kaydedin ve listeleyin"),
            "bilet": ("Bilet & Kayıt", "Katılımcıları etkinliklere kaydedin"),
            "rapor": ("Katılım Raporları", "Etkinlik doluluk ve katılım özeti"),
        }
        baslik, alt = basliklar[ad]

        if hasattr(self, "sayfa_header") and self.sayfa_header.winfo_exists():
            self.sayfa_header.destroy()
        self.sayfa_header = self._sayfa_baslik(self.icerik, baslik, alt)

        for key, frame in self.sayfalar.items():
            if key == ad:
                frame.grid()
            else:
                frame.grid_remove()

        for key, btn in self.nav_butonlar.items():
            if key == ad:
                btn.configure(
                    fg_color=COLORS["accent"],
                    text_color="#ffffff",
                    hover_color=COLORS["accent_hover"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_muted"],
                    hover_color=COLORS["card_hover"],
                )

        self.aktif_sayfa = ad
        if ad == "panel":
            self._panel_guncelle()
        elif ad == "rapor":
            self._rapor_guncelle()

    def _kart(self, parent, baslik=None):
        kart = ctk.CTkFrame(
            parent,
            fg_color=COLORS["card"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )
        if baslik:
            ctk.CTkLabel(
                kart,
                text=baslik,
                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                text_color=COLORS["text"],
                anchor="w",
            ).pack(fill="x", padx=22, pady=(18, 12))
        return kart

    def _form_alani(self, parent, etiket, placeholder=""):
        satir = ctk.CTkFrame(parent, fg_color="transparent")
        satir.pack(fill="x", padx=22, pady=6)

        ctk.CTkLabel(
            satir,
            text=etiket,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=COLORS["text_muted"],
            width=130,
            anchor="w",
        ).pack(side="left")

        entry = ctk.CTkEntry(
            satir,
            placeholder_text=placeholder,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
        )
        entry.pack(side="left", fill="x", expand=True)
        return entry

    def _birincil_buton(self, parent, metin, komut):
        btn = ctk.CTkButton(
            parent,
            text=metin,
            command=komut,
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
        )
        return btn

    def _panel_sayfasi(self):
        p = self.sayfalar["panel"]
        p.grid_columnconfigure((0, 1, 2), weight=1)

        self.stat_kartlar = {}
        stats = [
            ("etkinlik", "Etkinlikler", "📅", COLORS["accent"]),
            ("katilimci", "Katılımcılar", "👥", COLORS["success"]),
            ("bilet", "Kesilen Biletler", "🎟️", COLORS["warning"]),
        ]
        for i, (key, label, icon, renk) in enumerate(stats):
            kart = ctk.CTkFrame(p, fg_color=COLORS["card"], corner_radius=14, border_width=1, border_color=COLORS["border"])
            kart.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0), pady=(0, 16))
            ctk.CTkLabel(kart, text=icon, font=ctk.CTkFont(size=28)).pack(anchor="w", padx=20, pady=(20, 0))
            sayi = ctk.CTkLabel(kart, text="0", font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"), text_color=renk)
            sayi.pack(anchor="w", padx=20, pady=(8, 0))
            ctk.CTkLabel(kart, text=label, font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"]).pack(anchor="w", padx=20, pady=(4, 20))
            self.stat_kartlar[key] = sayi

        hizli = self._kart(p, "Hızlı Başlangıç")
        hizli.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 16))

        adimlar = [
            ("1", "Etkinlik ekleyin", "Tarih ve kapasite ile etkinlik tanımlayın.", "etkinlik"),
            ("2", "Katılımcı kaydedin", "Ad soyad ve e-posta bilgilerini girin.", "katilimci"),
            ("3", "Bilet kesin", "Etkinlik ve katılımcı ID ile kayıt yapın.", "bilet"),
            ("4", "Raporu inceleyin", "Doluluk oranlarını kontrol edin.", "rapor"),
        ]
        for no, baslik, aciklama, hedef in adimlar:
            satir = ctk.CTkFrame(hizli, fg_color="transparent")
            satir.pack(fill="x", padx=22, pady=8)
            ctk.CTkLabel(
                satir, text=no, width=32, height=32, corner_radius=16,
                fg_color=COLORS["accent"], font=ctk.CTkFont(size=14, weight="bold"),
            ).pack(side="left", padx=(0, 14))
            metin_frame = ctk.CTkFrame(satir, fg_color="transparent")
            metin_frame.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(metin_frame, text=baslik, font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(anchor="w")
            ctk.CTkLabel(metin_frame, text=aciklama, font=ctk.CTkFont(size=12), text_color=COLORS["text_muted"], anchor="w").pack(anchor="w")
            ctk.CTkButton(
                satir, text="Git →", width=70, height=32, corner_radius=8,
                fg_color=COLORS["card_hover"], hover_color=COLORS["accent"],
                command=lambda h=hedef: self._sayfa_goster(h),
            ).pack(side="right")

        self.panel_etkinlik_liste = self._kart(p, "Son Etkinlikler")
        self.panel_etkinlik_liste.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.panel_etkinlik_icerik = ctk.CTkFrame(self.panel_etkinlik_liste, fg_color="transparent")
        self.panel_etkinlik_icerik.pack(fill="x", padx=22, pady=(0, 18))

    def _panel_guncelle(self):
        self.stat_kartlar["etkinlik"].configure(text=str(len(self.etkinlikler)))
        self.stat_kartlar["katilimci"].configure(text=str(len(self.katilimcilar)))
        self.stat_kartlar["bilet"].configure(text=str(len(self.biletler)))

        for w in self.panel_etkinlik_icerik.winfo_children():
            w.destroy()

        if not self.etkinlikler:
            ctk.CTkLabel(
                self.panel_etkinlik_icerik,
                text="Henüz etkinlik eklenmedi.",
                text_color=COLORS["text_muted"],
                font=ctk.CTkFont(size=13),
            ).pack(anchor="w")
            return

        for e_id, etkinlik in list(self.etkinlikler.items())[:5]:
            dolu = len(etkinlik.kayitli_katilimcilar)
            oran = dolu / etkinlik.kapasite if etkinlik.kapasite else 0
            satir = ctk.CTkFrame(self.panel_etkinlik_icerik, fg_color=COLORS["input_bg"], corner_radius=10)
            satir.pack(fill="x", pady=4)
            sol = ctk.CTkFrame(satir, fg_color="transparent")
            sol.pack(side="left", fill="x", expand=True, padx=16, pady=12)
            ctk.CTkLabel(sol, text=etkinlik.ad, font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(anchor="w")
            ctk.CTkLabel(sol, text=f"{etkinlik.tarih}  ·  ID: {e_id}", font=ctk.CTkFont(size=11), text_color=COLORS["text_muted"], anchor="w").pack(anchor="w")
            sag = ctk.CTkFrame(satir, fg_color="transparent")
            sag.pack(side="right", padx=16, pady=12)
            ctk.CTkLabel(sag, text=f"{dolu}/{etkinlik.kapasite}", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLORS["accent"]).pack()
            bar_frame = ctk.CTkFrame(sag, width=80, height=6, fg_color=COLORS["border"], corner_radius=3)
            bar_frame.pack(pady=(4, 0))
            bar_frame.pack_propagate(False)
            renk = COLORS["danger"] if oran >= 1 else COLORS["warning"] if oran >= 0.8 else COLORS["success"]
            ctk.CTkFrame(bar_frame, width=max(4, int(80 * oran)), height=6, fg_color=renk, corner_radius=3).place(x=0, y=0)

    def _etkinlik_sayfasi(self):
        p = self.sayfalar["etkinlik"]
        ust = ctk.CTkFrame(p, fg_color="transparent")
        ust.pack(fill="both", expand=True)
        ust.grid_columnconfigure((0, 1), weight=1)

        form_kart = self._kart(ust, "Yeni Etkinlik")
        form_kart.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.entry_etkinlik_id = self._form_alani(form_kart, "Etkinlik ID", "ör. E001")
        self.entry_etkinlik_ad = self._form_alani(form_kart, "Etkinlik Adı", "ör. Python Atölyesi")
        self.entry_etkinlik_tarih = self._form_alani(form_kart, "Tarih", "ör. 14.05.2026")
        self.entry_etkinlik_kapasite = self._form_alani(form_kart, "Kapasite", "ör. 50")

        btn_frame = ctk.CTkFrame(form_kart, fg_color="transparent")
        btn_frame.pack(fill="x", padx=22, pady=(12, 20))
        self._birincil_buton(btn_frame, "Etkinlik Ekle", self.etkinlik_ekle_cmd).pack(fill="x")

        liste_kart = self._kart(ust, "Kayıtlı Etkinlikler")
        liste_kart.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.etkinlik_liste_frame = ctk.CTkFrame(liste_kart, fg_color="transparent")
        self.etkinlik_liste_frame.pack(fill="both", expand=True, padx=22, pady=(0, 18))

    def _etkinlik_liste_guncelle(self):
        for w in self.etkinlik_liste_frame.winfo_children():
            w.destroy()
        if not self.etkinlikler:
            ctk.CTkLabel(self.etkinlik_liste_frame, text="Henüz etkinlik yok.", text_color=COLORS["text_muted"]).pack(anchor="w")
            return
        for e_id, etkinlik in self.etkinlikler.items():
            dolu = len(etkinlik.kayitli_katilimcilar)
            item = ctk.CTkFrame(self.etkinlik_liste_frame, fg_color=COLORS["input_bg"], corner_radius=10)
            item.pack(fill="x", pady=4)
            ctk.CTkLabel(item, text=etkinlik.ad, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(10, 0))
            ctk.CTkLabel(
                item,
                text=f"ID: {e_id}  ·  {etkinlik.tarih}  ·  {dolu}/{etkinlik.kapasite} kişi",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", padx=14, pady=(2, 10))

    def _katilimci_sayfasi(self):
        p = self.sayfalar["katilimci"]
        ust = ctk.CTkFrame(p, fg_color="transparent")
        ust.pack(fill="both", expand=True)
        ust.grid_columnconfigure((0, 1), weight=1)

        form_kart = self._kart(ust, "Yeni Katılımcı")
        form_kart.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.entry_katilimci_id = self._form_alani(form_kart, "Katılımcı ID", "ör. K001")
        self.entry_katilimci_ad = self._form_alani(form_kart, "Ad Soyad", "ör. Ayşe Yılmaz")
        self.entry_katilimci_email = self._form_alani(form_kart, "E-posta", "ör. ayse@mail.com")

        btn_frame = ctk.CTkFrame(form_kart, fg_color="transparent")
        btn_frame.pack(fill="x", padx=22, pady=(12, 20))
        self._birincil_buton(btn_frame, "Katılımcı Ekle", self.katilimci_ekle_cmd).pack(fill="x")

        liste_kart = self._kart(ust, "Kayıtlı Katılımcılar")
        liste_kart.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.katilimci_liste_frame = ctk.CTkFrame(liste_kart, fg_color="transparent")
        self.katilimci_liste_frame.pack(fill="both", expand=True, padx=22, pady=(0, 18))

    def _katilimci_liste_guncelle(self):
        for w in self.katilimci_liste_frame.winfo_children():
            w.destroy()
        if not self.katilimcilar:
            ctk.CTkLabel(self.katilimci_liste_frame, text="Henüz katılımcı yok.", text_color=COLORS["text_muted"]).pack(anchor="w")
            return
        for k_id, k in self.katilimcilar.items():
            item = ctk.CTkFrame(self.katilimci_liste_frame, fg_color=COLORS["input_bg"], corner_radius=10)
            item.pack(fill="x", pady=4)
            ctk.CTkLabel(item, text=k.ad, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(10, 0))
            ctk.CTkLabel(item, text=f"ID: {k_id}  ·  {k.email}", font=ctk.CTkFont(size=11), text_color=COLORS["text_muted"]).pack(anchor="w", padx=14, pady=(2, 10))

    def _bilet_sayfasi(self):
        p = self.sayfalar["bilet"]
        ust = ctk.CTkFrame(p, fg_color="transparent")
        ust.pack(fill="both", expand=True)
        ust.grid_columnconfigure((0, 1), weight=1)

        form_kart = self._kart(ust, "Bilet Oluştur")
        form_kart.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.entry_bilet_id = self._form_alani(form_kart, "Bilet ID", "ör. B001")
        self.entry_bilet_etkinlik_id = self._form_alani(form_kart, "Etkinlik ID", "Kayıtlı etkinlik ID")
        self.entry_bilet_katilimci_id = self._form_alani(form_kart, "Katılımcı ID", "Kayıtlı katılımcı ID")

        btn_frame = ctk.CTkFrame(form_kart, fg_color="transparent")
        btn_frame.pack(fill="x", padx=22, pady=(12, 20))
        self._birincil_buton(btn_frame, "Bilet Oluştur", self.bilet_olustur_cmd).pack(fill="x")

        bilgi = self._kart(ust, "Kayıt Bilgisi")
        bilgi.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ctk.CTkLabel(
            bilgi,
            text="Bilet kesmeden önce etkinlik ve katılımcının\nsisteme kayıtlı olduğundan emin olun.",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_muted"],
            justify="left",
        ).pack(anchor="w", padx=22, pady=(0, 12))
        self.bilet_liste_frame = ctk.CTkFrame(bilgi, fg_color="transparent")
        self.bilet_liste_frame.pack(fill="both", expand=True, padx=22, pady=(0, 18))

    def _bilet_liste_guncelle(self):
        for w in self.bilet_liste_frame.winfo_children():
            w.destroy()
        if not self.biletler:
            ctk.CTkLabel(self.bilet_liste_frame, text="Henüz bilet kesilmedi.", text_color=COLORS["text_muted"]).pack(anchor="w")
            return
        for b in reversed(self.biletler[-8:]):
            item = ctk.CTkFrame(self.bilet_liste_frame, fg_color=COLORS["input_bg"], corner_radius=10)
            item.pack(fill="x", pady=4)
            ctk.CTkLabel(
                item,
                text=f"🎟️  {b.katilimci.ad} → {b.etkinlik.ad}",
                font=ctk.CTkFont(size=13, weight="bold"),
            ).pack(anchor="w", padx=14, pady=(10, 0))
            ctk.CTkLabel(
                item,
                text=f"Bilet: {b.bilet_id}",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", padx=14, pady=(2, 10))

    def _rapor_sayfasi(self):
        p = self.sayfalar["rapor"]
        ust = ctk.CTkFrame(p, fg_color="transparent")
        ust.pack(fill="x", pady=(0, 12))
        self._birincil_buton(ust, "Raporu Yenile", self._rapor_guncelle).pack(side="left")

        self.rapor_frame = ctk.CTkFrame(p, fg_color="transparent")
        self.rapor_frame.pack(fill="both", expand=True)

    def _rapor_guncelle(self):
        for w in self.rapor_frame.winfo_children():
            w.destroy()

        if not self.etkinlikler:
            bos = self._kart(self.rapor_frame)
            bos.pack(fill="x")
            ctk.CTkLabel(
                bos,
                text="Sistemde henüz etkinlik bulunmuyor.",
                font=ctk.CTkFont(size=14),
                text_color=COLORS["text_muted"],
            ).pack(padx=22, pady=24)
            return

        for e_id, etkinlik in self.etkinlikler.items():
            katilan = len(etkinlik.kayitli_katilimcilar)
            bos_yer = etkinlik.kapasite - katilan
            oran = katilan / etkinlik.kapasite if etkinlik.kapasite else 0

            kart = self._kart(self.rapor_frame)
            kart.pack(fill="x", pady=6)

            ust = ctk.CTkFrame(kart, fg_color="transparent")
            ust.pack(fill="x", padx=22, pady=(16, 8))
            sol = ctk.CTkFrame(ust, fg_color="transparent")
            sol.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(sol, text=etkinlik.ad, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(sol, text=f"ID: {e_id}  ·  {etkinlik.tarih}", font=ctk.CTkFont(size=12), text_color=COLORS["text_muted"]).pack(anchor="w")

            yuzde = int(oran * 100)
            renk = COLORS["danger"] if oran >= 1 else COLORS["warning"] if oran >= 0.8 else COLORS["success"]
            ctk.CTkLabel(ust, text=f"%{yuzde}", font=ctk.CTkFont(size=22, weight="bold"), text_color=renk).pack(side="right")

            bar_outer = ctk.CTkFrame(kart, height=10, fg_color=COLORS["border"], corner_radius=5)
            bar_outer.pack(fill="x", padx=22, pady=(0, 12))
            bar_outer.pack_propagate(False)
            ctk.CTkFrame(bar_outer, height=10, fg_color=renk, corner_radius=5).place(relwidth=min(1.0, oran), relheight=1)

            alt = ctk.CTkFrame(kart, fg_color="transparent")
            alt.pack(fill="x", padx=22, pady=(0, 16))
            for label, val, color in [
                ("Kapasite", str(etkinlik.kapasite), COLORS["text"]),
                ("Katılan", str(katilan), COLORS["accent"]),
                ("Boş Yer", str(bos_yer), COLORS["success"] if bos_yer > 0 else COLORS["danger"]),
            ]:
                kutu = ctk.CTkFrame(alt, fg_color=COLORS["input_bg"], corner_radius=8)
                kutu.pack(side="left", fill="x", expand=True, padx=(0, 8))
                ctk.CTkLabel(kutu, text=label, font=ctk.CTkFont(size=11), text_color=COLORS["text_muted"]).pack(pady=(10, 0))
                ctk.CTkLabel(kutu, text=val, font=ctk.CTkFont(size=20, weight="bold"), text_color=color).pack(pady=(2, 10))

            if etkinlik.kayitli_katilimcilar:
                ctk.CTkLabel(
                    kart,
                    text="Katılımcılar: " + ", ".join(k.ad for k in etkinlik.kayitli_katilimcilar),
                    font=ctk.CTkFont(size=12),
                    text_color=COLORS["text_muted"],
                    wraplength=900,
                    justify="left",
                ).pack(anchor="w", padx=22, pady=(0, 14))

    def _entry_temizle(self, *entries):
        for e in entries:
            e.delete(0, "end")

    def _veri_guncelle(self):
        self._etkinlik_liste_guncelle()
        self._katilimci_liste_guncelle()
        self._bilet_liste_guncelle()
        if self.aktif_sayfa == "panel":
            self._panel_guncelle()
        elif self.aktif_sayfa == "rapor":
            self._rapor_guncelle()

    def etkinlik_ekle_cmd(self):
        e_id = self.entry_etkinlik_id.get().strip()
        ad = self.entry_etkinlik_ad.get().strip()
        tarih = self.entry_etkinlik_tarih.get().strip()
        kapasite = self.entry_etkinlik_kapasite.get().strip()

        if e_id and ad and tarih and kapasite.isdigit():
            self.etkinlikler[e_id] = Etkinlik(e_id, ad, tarih, kapasite)
            messagebox.showinfo("Başarılı", f"{ad} etkinliği sisteme eklendi.")
            self._entry_temizle(
                self.entry_etkinlik_id,
                self.entry_etkinlik_ad,
                self.entry_etkinlik_tarih,
                self.entry_etkinlik_kapasite,
            )
            self._veri_guncelle()
        else:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doğru doldurun (Kapasite sayı olmalı).")

    def katilimci_ekle_cmd(self):
        k_id = self.entry_katilimci_id.get().strip()
        ad = self.entry_katilimci_ad.get().strip()
        email = self.entry_katilimci_email.get().strip()

        if k_id and ad and email:
            self.katilimcilar[k_id] = Katilimci(k_id, ad, email)
            messagebox.showinfo("Başarılı", f"{ad} adlı katılımcı sisteme eklendi.")
            self._entry_temizle(self.entry_katilimci_id, self.entry_katilimci_ad, self.entry_katilimci_email)
            self._veri_guncelle()
        else:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")

    def bilet_olustur_cmd(self):
        b_id = self.entry_bilet_id.get().strip()
        e_id = self.entry_bilet_etkinlik_id.get().strip()
        k_id = self.entry_bilet_katilimci_id.get().strip()

        if b_id and e_id and k_id:
            if e_id in self.etkinlikler and k_id in self.katilimcilar:
                etkinlik = self.etkinlikler[e_id]
                katilimci = self.katilimcilar[k_id]
                yeni_bilet = Bilet.bilet_olustur(b_id, etkinlik, katilimci)

                if yeni_bilet:
                    self.biletler.append(yeni_bilet)
                    messagebox.showinfo(
                        "Başarılı",
                        f"Bilet kesildi! {katilimci.ad}, {etkinlik.ad} etkinliğine kaydedildi.",
                    )
                    self._entry_temizle(
                        self.entry_bilet_id,
                        self.entry_bilet_etkinlik_id,
                        self.entry_bilet_katilimci_id,
                    )
                    self._veri_guncelle()
                else:
                    messagebox.showerror("Hata", "Bu etkinliğin kapasitesi dolmuştur!")
            else:
                messagebox.showerror("Hata", "Geçersiz Etkinlik ID veya Katılımcı ID.")
        else:
            messagebox.showwarning("Hata", "Lütfen bilet için tüm alanları doldurun.")


if __name__ == "__main__":
    app = EtkinlikUygulamasi()
    app.mainloop()
