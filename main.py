from tkinter import messagebox

import customtkinter as ctk


class Katilimci:
    def __init__(self, katilimci_id, ad, email):
        self.katilimci_id = katilimci_id
        self.ad = ad
        self.email = email


class Etkinlik:
    def __init__(self, etkinlik_id, ad, tarih, yer, kapasite):
        self.etkinlik_id = etkinlik_id
        self.ad = ad
        self.tarih = tarih
        self.yer = yer
        self.kapasite = int(kapasite)
        self.kayitli_katilimcilar = []

    def katilimci_ekle(self, katilimci):
        if len(self.kayitli_katilimcilar) < self.kapasite:
            self.kayitli_katilimcilar.append(katilimci)
            return True
        return False

    @property
    def dolu_sayisi(self):
        return len(self.kayitli_katilimcilar)

    @property
    def bos_yer(self):
        return self.kapasite - self.dolu_sayisi

    @property
    def dolu_mu(self):
        return self.dolu_sayisi >= self.kapasite


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


class VeriDeposu:
    """Organizatör ve katılımcı arayüzleri arasında paylaşılan veri."""

    def __init__(self):
        self.etkinlikler = {}
        self.katilimcilar = {}
        self.biletler = []

    def _sonraki_id(self, onek, mevcut_idler):
        max_num = 0
        for kid in mevcut_idler:
            if kid.startswith(onek) and kid[len(onek) :].isdigit():
                max_num = max(max_num, int(kid[len(onek) :]))
        return f"{onek}{max_num + 1:03d}"

    def sonraki_etkinlik_id(self):
        return self._sonraki_id("E", self.etkinlikler.keys())

    def sonraki_katilimci_id(self):
        return self._sonraki_id("K", self.katilimcilar.keys())

    def sonraki_bilet_id(self):
        return self._sonraki_id("B", [b.bilet_id for b in self.biletler])

    def musait_etkinlikler(self):
        return [e for e in self.etkinlikler.values() if not e.dolu_mu]


COLORS = {
    "bg": "#0f1117",
    "sidebar": "#161b26",
    "card": "#1c2333",
    "card_hover": "#242d42",
    "accent": "#6366f1",
    "accent_hover": "#818cf8",
    "accent_katilimci": "#14b8a6",
    "accent_katilimci_hover": "#2dd4bf",
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

        self.veri = VeriDeposu()
        self.aktif_rol = None
        self.aktif_sayfa = None
        self.oturum_katilimci_id = None
        self.profil_duzenle_aktif = False

        self.ana_konteyner = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        self.ana_konteyner.pack(fill="both", expand=True)

        self._giris_ekrani_olustur()

    # ── Yardımcı bileşenler ─────────────────────────────────────────────

    def _aktif_renk(self):
        if self.aktif_rol == "katilimci":
            return COLORS["accent_katilimci"], COLORS["accent_katilimci_hover"]
        return COLORS["accent"], COLORS["accent_hover"]

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

    def _birincil_buton(self, parent, metin, komut, renk=None):
        fg, hover = renk or self._aktif_renk()
        return ctk.CTkButton(
            parent,
            text=metin,
            command=komut,
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=fg,
            hover_color=hover,
        )

    def _ikincil_buton(self, parent, metin, komut):
        return ctk.CTkButton(
            parent,
            text=metin,
            command=komut,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=COLORS["card_hover"],
            hover_color=COLORS["border"],
            text_color=COLORS["text_muted"],
        )

    def _entry_temizle(self, *entries):
        for e in entries:
            e.delete(0, "end")

    def _etkinlik_etiket(self, etkinlik):
        return f"{etkinlik.ad} — {etkinlik.yer} ({etkinlik.tarih})"

    def _etkinlik_bilgi_satiri(self, etkinlik, e_id=None, ekstra=None):
        parcalar = [f"📅 {etkinlik.tarih}", f"📍 {etkinlik.yer}"]
        if e_id:
            parcalar.append(f"ID: {e_id}")
        if ekstra:
            parcalar.append(ekstra)
        return "  ·  ".join(parcalar)

    def _id_kutusu(self, parent, baslik, id_degeri, renk=None):
        kutu = ctk.CTkFrame(parent, fg_color=COLORS["input_bg"], corner_radius=10, border_width=1, border_color=renk or COLORS["border"])
        kutu.pack(fill="x", padx=22, pady=(0, 12))
        ctk.CTkLabel(
            kutu,
            text=baslik,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(12, 0))
        ctk.CTkLabel(
            kutu,
            text=id_degeri,
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=renk or COLORS["accent"],
        ).pack(anchor="w", padx=16, pady=(4, 14))

    def _doluluk_cubugu(self, parent, oran, height=8):
        renk = COLORS["danger"] if oran >= 1 else COLORS["warning"] if oran >= 0.8 else COLORS["success"]
        outer = ctk.CTkFrame(parent, height=height, fg_color=COLORS["border"], corner_radius=height // 2)
        outer.pack(fill="x")
        outer.pack_propagate(False)
        ctk.CTkFrame(outer, height=height, fg_color=renk, corner_radius=height // 2).place(
            relwidth=min(1.0, oran), relheight=1
        )
        return renk

    # ── Giriş ekranı ────────────────────────────────────────────────────

    def _giris_ekrani_olustur(self):
        self.giris_frame = ctk.CTkFrame(self.ana_konteyner, fg_color=COLORS["bg"])
        self.giris_frame.pack(fill="both", expand=True)

        merkez = ctk.CTkFrame(self.giris_frame, fg_color="transparent")
        merkez.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(merkez, text="🎫", font=ctk.CTkFont(size=48)).pack(pady=(0, 8))
        ctk.CTkLabel(
            merkez,
            text="Etkinlik Kayıt Sistemi",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color=COLORS["text"],
        ).pack()
        ctk.CTkLabel(
            merkez,
            text="Devam etmek için giriş türünüzü seçin",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=COLORS["text_muted"],
        ).pack(pady=(8, 36))

        kartlar = ctk.CTkFrame(merkez, fg_color="transparent")
        kartlar.pack()

        organizator = self._giris_karti(
            kartlar,
            "📅",
            "Etkinlik Organizatörü",
            "Etkinlik oluşturun, kapasite belirleyin\nve katılım raporlarını takip edin.",
            COLORS["accent"],
            lambda: self._rol_baslat("organizator"),
        )
        organizator.pack(side="left", padx=12)

        katilimci = self._giris_karti(
            kartlar,
            "🎟️",
            "Bilet Alan",
            "Mevcut etkinliklere göz atın,\nprofilinizi oluşturun ve bilet alın.",
            COLORS["accent_katilimci"],
            lambda: self._rol_baslat("katilimci"),
        )
        katilimci.pack(side="left", padx=12)

    def _giris_karti(self, parent, ikon, baslik, aciklama, renk, komut):
        kart = ctk.CTkFrame(
            parent,
            width=300,
            height=280,
            fg_color=COLORS["card"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        kart.pack_propagate(False)

        ctk.CTkLabel(kart, text=ikon, font=ctk.CTkFont(size=40)).pack(pady=(32, 12))
        ctk.CTkLabel(
            kart,
            text=baslik,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=COLORS["text"],
        ).pack()
        ctk.CTkLabel(
            kart,
            text=aciklama,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COLORS["text_muted"],
            justify="center",
        ).pack(pady=(10, 24), padx=20)

        ctk.CTkButton(
            kart,
            text="Giriş Yap →",
            command=komut,
            height=40,
            width=180,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=renk,
            hover_color=COLORS["accent_hover"] if renk == COLORS["accent"] else COLORS["accent_katilimci_hover"],
        ).pack(pady=(0, 28))

        return kart

    def _rol_baslat(self, rol):
        self.aktif_rol = rol
        self.giris_frame.destroy()

        self.rol_frame = ctk.CTkFrame(self.ana_konteyner, fg_color=COLORS["bg"], corner_radius=0)
        self.rol_frame.pack(fill="both", expand=True)
        self.rol_frame.grid_columnconfigure(1, weight=1)
        self.rol_frame.grid_rowconfigure(0, weight=1)

        if rol == "organizator":
            self._organizator_arayuz_olustur()
            self._sayfa_goster("panel")
        else:
            self._katilimci_arayuz_olustur()
            self._sayfa_goster("kesfet")

    def _rol_degistir(self):
        if hasattr(self, "rol_frame"):
            self.rol_frame.destroy()
        self.aktif_rol = None
        self.aktif_sayfa = None
        self.oturum_katilimci_id = None
        self.profil_duzenle_aktif = False
        self._giris_ekrani_olustur()

    # ── Ortak kabuk (sidebar + içerik) ──────────────────────────────────

    def _kabuk_olustur(self, logo_alt, nav_items):
        accent, accent_hover = self._aktif_renk()

        sidebar = ctk.CTkFrame(self.rol_frame, width=240, fg_color=COLORS["sidebar"], corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(28, 24))

        ctk.CTkLabel(logo_frame, text="🎫", font=ctk.CTkFont(size=28)).pack(anchor="w")
        ctk.CTkLabel(
            logo_frame,
            text="Etkinlik Kayıt",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w", pady=(6, 0))
        ctk.CTkLabel(
            logo_frame,
            text=logo_alt,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=accent,
        ).pack(anchor="w")

        self.nav_butonlar = {}
        nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=12, pady=(8, 0))

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

        self._ikincil_buton(sidebar, "← Rol Değiştir", self._rol_degistir).pack(
            side="bottom", fill="x", padx=16, pady=20
        )

        self.icerik = ctk.CTkFrame(self.rol_frame, fg_color=COLORS["bg"], corner_radius=0)
        self.icerik.grid(row=0, column=1, sticky="nsew")
        self.icerik.grid_columnconfigure(0, weight=1)
        self.icerik.grid_rowconfigure(1, weight=1)

    def _sayfa_baslik(self, baslik, alt):
        if hasattr(self, "sayfa_header") and self.sayfa_header.winfo_exists():
            self.sayfa_header.destroy()
        header = ctk.CTkFrame(self.icerik, fg_color=COLORS["bg"], height=80)
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 0))
        ctk.CTkLabel(
            header,
            text=baslik,
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=COLORS["text"],
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text=alt,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=COLORS["text_muted"],
            anchor="w",
        ).pack(anchor="w", pady=(4, 0))
        self.sayfa_header = header

    def _sayfa_goster(self, ad):
        basliklar = self._sayfa_basliklari()
        baslik, alt = basliklar[ad]
        self._sayfa_baslik(baslik, alt)

        accent, accent_hover = self._aktif_renk()
        for key, frame in self.sayfalar.items():
            frame.grid() if key == ad else frame.grid_remove()
        for key, btn in self.nav_butonlar.items():
            if key == ad:
                btn.configure(fg_color=accent, text_color="#ffffff", hover_color=accent_hover)
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_muted"],
                    hover_color=COLORS["card_hover"],
                )

        self.aktif_sayfa = ad
        self._sayfa_yenile(ad)

    def _sayfa_yenile(self, ad):
        yenileyiciler = {
            "panel": self._organizator_panel_guncelle,
            "etkinlik": self._organizator_etkinlik_liste_guncelle,
            "rapor": self._rapor_guncelle,
            "kesfet": self._kesfet_guncelle,
            "profil": self._profil_guncelle,
            "bilet_al": self._bilet_al_guncelle,
            "biletlerim": self._biletlerim_guncelle,
        }
        if ad in yenileyiciler:
            yenileyiciler[ad]()

    def _scroll_sayfa_olustur(self, sayfa_adlari):
        self.sayfalar = {}
        for ad in sayfa_adlari:
            frame = ctk.CTkScrollableFrame(
                self.icerik,
                fg_color=COLORS["bg"],
                scrollbar_button_color=self._aktif_renk()[0],
                scrollbar_button_hover_color=self._aktif_renk()[1],
            )
            frame.grid(row=1, column=0, sticky="nsew", padx=28, pady=(0, 24))
            frame.grid_columnconfigure(0, weight=1)
            self.sayfalar[ad] = frame

    # ═══════════════════════════════════════════════════════════════════
    #  ORGANİZATÖR
    # ═══════════════════════════════════════════════════════════════════

    def _sayfa_basliklari(self):
        if self.aktif_rol == "organizator":
            return {
                "panel": ("Organizatör Paneli", "Etkinliklerinizin genel durumu"),
                "etkinlik": ("Etkinlik Yönetimi", "Yeni etkinlik oluşturun ve mevcutları yönetin"),
                "rapor": ("Katılım Raporları", "Kayıt ve doluluk özeti"),
            }
        return {
            "kesfet": ("Etkinlikleri Keşfet", "Müsait etkinliklere göz atın"),
            "profil": ("Profilim", "Bilet alabilmek için profilinizi oluşturun"),
            "bilet_al": ("Bilet Al", "Seçtiğiniz etkinlik için kayıt olun"),
            "biletlerim": ("Biletlerim", "Aldığınız biletlerin listesi"),
        }

    def _organizator_arayuz_olustur(self):
        self._kabuk_olustur(
            "Organizatör Girişi",
            [
                ("panel", "📊  Panel"),
                ("etkinlik", "📅  Etkinliklerim"),
                ("rapor", "📋  Raporlar"),
            ],
        )
        self._scroll_sayfa_olustur(["panel", "etkinlik", "rapor"])
        self._organizator_panel_sayfasi()
        self._organizator_etkinlik_sayfasi()
        self._organizator_rapor_sayfasi()

    def _organizator_panel_sayfasi(self):
        p = self.sayfalar["panel"]
        p.grid_columnconfigure((0, 1, 2), weight=1)

        self.org_statlar = {}
        toplam_kayit = sum(len(e.kayitli_katilimcilar) for e in self.veri.etkinlikler.values())
        stats = [
            ("etkinlik", str(len(self.veri.etkinlikler)), "Etkinlik", "📅", COLORS["accent"]),
            ("kayit", str(toplam_kayit), "Toplam Kayıt", "👥", COLORS["success"]),
            ("bilet", str(len(self.veri.biletler)), "Satılan Bilet", "🎟️", COLORS["warning"]),
        ]
        for i, (key, _, label, icon, renk) in enumerate(stats):
            kart = ctk.CTkFrame(
                p, fg_color=COLORS["card"], corner_radius=14, border_width=1, border_color=COLORS["border"]
            )
            kart.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0), pady=(0, 16))
            ctk.CTkLabel(kart, text=icon, font=ctk.CTkFont(size=28)).pack(anchor="w", padx=20, pady=(20, 0))
            sayi = ctk.CTkLabel(
                kart, text="0", font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"), text_color=renk
            )
            sayi.pack(anchor="w", padx=20, pady=(8, 0))
            ctk.CTkLabel(kart, text=label, font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"]).pack(
                anchor="w", padx=20, pady=(4, 20)
            )
            self.org_statlar[key] = sayi

        bilgi = self._kart(p, "Organizatör olarak yapabilecekleriniz")
        bilgi.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 16))
        for metin in [
            "• Yeni etkinlik tanımlayın (ad, tarih, yer, kapasite)",
            "• Etkinliklerinizin doluluk durumunu izleyin",
            "• Katılımcı listelerini rapor ekranından görüntüleyin",
        ]:
            ctk.CTkLabel(
                bilgi, text=metin, font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"], anchor="w"
            ).pack(anchor="w", padx=22, pady=4)
        ctk.CTkLabel(bilgi, text="").pack(pady=8)

        self.org_panel_liste = self._kart(p, "Etkinlikleriniz")
        self.org_panel_liste.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.org_panel_icerik = ctk.CTkFrame(self.org_panel_liste, fg_color="transparent")
        self.org_panel_icerik.pack(fill="x", padx=22, pady=(0, 18))

    def _organizator_panel_guncelle(self):
        toplam_kayit = sum(len(e.kayitli_katilimcilar) for e in self.veri.etkinlikler.values())
        self.org_statlar["etkinlik"].configure(text=str(len(self.veri.etkinlikler)))
        self.org_statlar["kayit"].configure(text=str(toplam_kayit))
        self.org_statlar["bilet"].configure(text=str(len(self.veri.biletler)))

        for w in self.org_panel_icerik.winfo_children():
            w.destroy()
        if not self.veri.etkinlikler:
            ctk.CTkLabel(
                self.org_panel_icerik, text="Henüz etkinlik oluşturmadınız.", text_color=COLORS["text_muted"]
            ).pack(anchor="w")
            return
        for e_id, etkinlik in self.veri.etkinlikler.items():
            self._etkinlik_ozet_satiri(self.org_panel_icerik, e_id, etkinlik)

    def _etkinlik_ozet_satiri(self, parent, e_id, etkinlik):
        oran = etkinlik.dolu_sayisi / etkinlik.kapasite if etkinlik.kapasite else 0
        satir = ctk.CTkFrame(parent, fg_color=COLORS["input_bg"], corner_radius=10)
        satir.pack(fill="x", pady=4)
        sol = ctk.CTkFrame(satir, fg_color="transparent")
        sol.pack(side="left", fill="x", expand=True, padx=16, pady=12)
        ctk.CTkLabel(sol, text=etkinlik.ad, font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(anchor="w")
        ctk.CTkLabel(
            sol,
            text=self._etkinlik_bilgi_satiri(etkinlik, e_id, f"{etkinlik.dolu_sayisi}/{etkinlik.kapasite} kişi"),
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"],
            anchor="w",
        ).pack(anchor="w", pady=(2, 0))
        bar_wrap = ctk.CTkFrame(sol, fg_color="transparent")
        bar_wrap.pack(fill="x", pady=(6, 0))
        self._doluluk_cubugu(bar_wrap, oran, height=6)

    def _organizator_etkinlik_sayfasi(self):
        p = self.sayfalar["etkinlik"]
        ust = ctk.CTkFrame(p, fg_color="transparent")
        ust.pack(fill="both", expand=True)
        ust.grid_columnconfigure((0, 1), weight=1)

        form = self._kart(ust, "Yeni Etkinlik Oluştur")
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ctk.CTkLabel(
            form,
            text="Etkinlik ID sistem tarafından otomatik atanır.",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=22, pady=(0, 8))
        self.entry_etkinlik_ad = self._form_alani(form, "Etkinlik Adı", "ör. Python Atölyesi")
        self.entry_etkinlik_tarih = self._form_alani(form, "Tarih", "ör. 14.05.2026")
        self.entry_etkinlik_yer = self._form_alani(form, "Yer / Mekân", "ör. İstanbul Kongre Merkezi")
        self.entry_etkinlik_kapasite = self._form_alani(form, "Kapasite", "ör. 50")
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", padx=22, pady=(12, 8))
        self._birincil_buton(btn_frame, "Etkinlik Oluştur", self._etkinlik_ekle).pack(fill="x")
        self.org_son_etkinlik_id_frame = ctk.CTkFrame(form, fg_color="transparent")
        self.org_son_etkinlik_id_frame.pack(fill="x")

        liste = self._kart(ust, "Oluşturduğunuz Etkinlikler")
        liste.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.org_etkinlik_liste = ctk.CTkFrame(liste, fg_color="transparent")
        self.org_etkinlik_liste.pack(fill="both", expand=True, padx=22, pady=(0, 18))

    def _organizator_etkinlik_liste_guncelle(self):
        for w in self.org_etkinlik_liste.winfo_children():
            w.destroy()
        if not self.veri.etkinlikler:
            ctk.CTkLabel(self.org_etkinlik_liste, text="Henüz etkinlik yok.", text_color=COLORS["text_muted"]).pack(
                anchor="w"
            )
            return
        for e_id, etkinlik in self.veri.etkinlikler.items():
            self._etkinlik_ozet_satiri(self.org_etkinlik_liste, e_id, etkinlik)

    def _etkinlik_ekle(self):
        ad = self.entry_etkinlik_ad.get().strip()
        tarih = self.entry_etkinlik_tarih.get().strip()
        yer = self.entry_etkinlik_yer.get().strip()
        kapasite = self.entry_etkinlik_kapasite.get().strip()

        if ad and tarih and yer and kapasite.isdigit():
            e_id = self.veri.sonraki_etkinlik_id()
            self.veri.etkinlikler[e_id] = Etkinlik(e_id, ad, tarih, yer, kapasite)
            for w in self.org_son_etkinlik_id_frame.winfo_children():
                w.destroy()
            self._id_kutusu(self.org_son_etkinlik_id_frame, "Oluşturulan Etkinlik ID", e_id, COLORS["accent"])
            messagebox.showinfo(
                "Başarılı",
                f"{ad} etkinliği yayınlandı.\n\nEtkinlik ID: {e_id}\n\nKatılımcılar artık bilet alabilir.",
            )
            self._entry_temizle(
                self.entry_etkinlik_ad,
                self.entry_etkinlik_tarih,
                self.entry_etkinlik_yer,
                self.entry_etkinlik_kapasite,
            )
            self._organizator_veri_guncelle()
        else:
            messagebox.showwarning(
                "Hata", "Lütfen tüm alanları doldurun (Yer zorunludur, kapasite sayı olmalı)."
            )

    def _organizator_veri_guncelle(self):
        if self.aktif_sayfa:
            self._sayfa_yenile(self.aktif_sayfa)

    def _organizator_rapor_sayfasi(self):
        p = self.sayfalar["rapor"]
        ust = ctk.CTkFrame(p, fg_color="transparent")
        ust.pack(fill="x", pady=(0, 12))
        self._birincil_buton(ust, "Raporu Yenile", lambda: self._rapor_guncelle()).pack(side="left")
        self.rapor_frame = ctk.CTkFrame(p, fg_color="transparent")
        self.rapor_frame.pack(fill="both", expand=True)

    def _rapor_guncelle(self):
        for w in self.rapor_frame.winfo_children():
            w.destroy()
        if not self.veri.etkinlikler:
            bos = self._kart(self.rapor_frame)
            bos.pack(fill="x")
            ctk.CTkLabel(
                bos, text="Henüz etkinlik bulunmuyor.", font=ctk.CTkFont(size=14), text_color=COLORS["text_muted"]
            ).pack(padx=22, pady=24)
            return

        for e_id, etkinlik in self.veri.etkinlikler.items():
            oran = etkinlik.dolu_sayisi / etkinlik.kapasite if etkinlik.kapasite else 0
            kart = self._kart(self.rapor_frame)
            kart.pack(fill="x", pady=6)

            ust = ctk.CTkFrame(kart, fg_color="transparent")
            ust.pack(fill="x", padx=22, pady=(16, 8))
            sol = ctk.CTkFrame(ust, fg_color="transparent")
            sol.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(sol, text=etkinlik.ad, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(
                sol,
                text=self._etkinlik_bilgi_satiri(etkinlik, e_id),
                font=ctk.CTkFont(size=12),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w")

            renk = COLORS["danger"] if oran >= 1 else COLORS["warning"] if oran >= 0.8 else COLORS["success"]
            ctk.CTkLabel(ust, text=f"%{int(oran * 100)}", font=ctk.CTkFont(size=22, weight="bold"), text_color=renk).pack(
                side="right"
            )
            bar_wrap = ctk.CTkFrame(kart, fg_color="transparent")
            bar_wrap.pack(fill="x", padx=22, pady=(0, 12))
            self._doluluk_cubugu(bar_wrap, oran)

            alt = ctk.CTkFrame(kart, fg_color="transparent")
            alt.pack(fill="x", padx=22, pady=(0, 16))
            for label, val, color in [
                ("Kapasite", str(etkinlik.kapasite), COLORS["text"]),
                ("Katılan", str(etkinlik.dolu_sayisi), COLORS["accent"]),
                ("Boş Yer", str(etkinlik.bos_yer), COLORS["success"] if etkinlik.bos_yer > 0 else COLORS["danger"]),
            ]:
                kutu = ctk.CTkFrame(alt, fg_color=COLORS["input_bg"], corner_radius=8)
                kutu.pack(side="left", fill="x", expand=True, padx=(0, 8))
                ctk.CTkLabel(kutu, text=label, font=ctk.CTkFont(size=11), text_color=COLORS["text_muted"]).pack(
                    pady=(10, 0)
                )
                ctk.CTkLabel(kutu, text=val, font=ctk.CTkFont(size=20, weight="bold"), text_color=color).pack(
                    pady=(2, 10)
                )

            if etkinlik.kayitli_katilimcilar:
                ctk.CTkLabel(
                    kart,
                    text="Kayıtlı katılımcılar: " + ", ".join(k.ad for k in etkinlik.kayitli_katilimcilar),
                    font=ctk.CTkFont(size=12),
                    text_color=COLORS["text_muted"],
                    wraplength=900,
                    justify="left",
                ).pack(anchor="w", padx=22, pady=(0, 14))

    # ═══════════════════════════════════════════════════════════════════
    #  KATILIMCI (BİLET ALAN)
    # ═══════════════════════════════════════════════════════════════════

    def _katilimci_arayuz_olustur(self):
        self._kabuk_olustur(
            "Katılımcı Girişi",
            [
                ("kesfet", "🔍  Keşfet"),
                ("profil", "👤  Profilim"),
                ("bilet_al", "🎟️  Bilet Al"),
                ("biletlerim", "📋  Biletlerim"),
            ],
        )
        self._scroll_sayfa_olustur(["kesfet", "profil", "bilet_al", "biletlerim"])
        self._kesfet_sayfasi()
        self._profil_sayfasi()
        self._bilet_al_sayfasi()
        self._biletlerim_sayfasi()

    def _oturum_katilimci(self):
        if self.oturum_katilimci_id and self.oturum_katilimci_id in self.veri.katilimcilar:
            return self.veri.katilimcilar[self.oturum_katilimci_id]
        return None

    def _kesfet_sayfasi(self):
        p = self.sayfalar["kesfet"]
        self.kesfet_frame = ctk.CTkFrame(p, fg_color="transparent")
        self.kesfet_frame.pack(fill="both", expand=True)

    def _kesfet_guncelle(self):
        for w in self.kesfet_frame.winfo_children():
            w.destroy()

        if not self.veri.etkinlikler:
            bos = self._kart(self.kesfet_frame)
            bos.pack(fill="x")
            ctk.CTkLabel(
                bos,
                text="Henüz yayınlanmış etkinlik yok.\nOrganizatör bir etkinlik oluşturduğunda burada görünecek.",
                font=ctk.CTkFont(size=14),
                text_color=COLORS["text_muted"],
                justify="left",
            ).pack(padx=22, pady=24)
            return

        for e_id, etkinlik in self.veri.etkinlikler.items():
            oran = etkinlik.dolu_sayisi / etkinlik.kapasite if etkinlik.kapasite else 0
            kart = self._kart(self.kesfet_frame)
            kart.pack(fill="x", pady=8)

            ust = ctk.CTkFrame(kart, fg_color="transparent")
            ust.pack(fill="x", padx=22, pady=(16, 8))
            sol = ctk.CTkFrame(ust, fg_color="transparent")
            sol.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(sol, text=etkinlik.ad, font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(
                sol,
                text=f"📅 {etkinlik.tarih}  ·  📍 {etkinlik.yer}",
                font=ctk.CTkFont(size=13),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", pady=(4, 0))

            durum = "DOLU" if etkinlik.dolu_mu else f"{etkinlik.bos_yer} yer kaldı"
            durum_renk = COLORS["danger"] if etkinlik.dolu_mu else COLORS["success"]
            ctk.CTkLabel(ust, text=durum, font=ctk.CTkFont(size=13, weight="bold"), text_color=durum_renk).pack(
                side="right"
            )

            bar_wrap = ctk.CTkFrame(kart, fg_color="transparent")
            bar_wrap.pack(fill="x", padx=22, pady=(0, 12))
            self._doluluk_cubugu(bar_wrap, oran)

            alt = ctk.CTkFrame(kart, fg_color="transparent")
            alt.pack(fill="x", padx=22, pady=(0, 16))
            if not etkinlik.dolu_mu:
                ctk.CTkButton(
                    alt,
                    text="Bilet Al →",
                    height=36,
                    width=120,
                    corner_radius=8,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    fg_color=COLORS["accent_katilimci"],
                    hover_color=COLORS["accent_katilimci_hover"],
                    command=lambda eid=e_id: self._bilet_al_etkinlik_sec(eid),
                ).pack(side="right")
            else:
                ctk.CTkLabel(alt, text="Kapasite doldu", text_color=COLORS["danger"]).pack(side="right")

    def _bilet_al_etkinlik_sec(self, etkinlik_id):
        self._secili_etkinlik_id = etkinlik_id
        self._sayfa_goster("bilet_al")

    def _profil_sayfasi(self):
        p = self.sayfalar["profil"]
        self.profil_kart = self._kart(p, "Katılımcı Profili")
        self.profil_kart.pack(fill="x")
        self.profil_form_frame = ctk.CTkFrame(self.profil_kart, fg_color="transparent")
        self.profil_form_frame.pack(fill="x")

        self.profil_durum_kart = self._kart(p, "Oturum Durumu")
        self.profil_durum_kart.pack(fill="x", pady=(16, 0))
        self.profil_durum_label = ctk.CTkLabel(
            self.profil_durum_kart,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_muted"],
            justify="left",
        )
        self.profil_durum_label.pack(anchor="w", padx=22, pady=(0, 18))
        self.profil_son_id_frame = ctk.CTkFrame(self.profil_kart, fg_color="transparent")
        self.profil_son_id_frame.pack(fill="x")

    def _profil_guncelle(self):
        for w in self.profil_form_frame.winfo_children():
            w.destroy()

        k = self._oturum_katilimci()
        if k and self.profil_duzenle_aktif:
            self._id_kutusu(
                self.profil_form_frame,
                "Katılımcı ID'niz (değiştirilemez)",
                k.katilimci_id,
                COLORS["accent_katilimci"],
            )
            self.entry_profil_ad = self._form_alani(self.profil_form_frame, "Ad Soyad", "")
            self.entry_profil_email = self._form_alani(self.profil_form_frame, "E-posta", "")
            self.entry_profil_ad.insert(0, k.ad)
            self.entry_profil_email.insert(0, k.email)
            btn_frame = ctk.CTkFrame(self.profil_form_frame, fg_color="transparent")
            btn_frame.pack(fill="x", padx=22, pady=(12, 20))
            self._ikincil_buton(btn_frame, "İptal", self._profil_duzenle_iptal).pack(side="left", padx=(0, 8))
            self._birincil_buton(
                btn_frame,
                "Kaydet",
                self._profil_guncelle_kaydet,
                renk=(COLORS["accent_katilimci"], COLORS["accent_katilimci_hover"]),
            ).pack(side="left")
        elif k:
            ctk.CTkLabel(
                self.profil_form_frame,
                text=f"Hoş geldiniz, {k.ad}!",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=COLORS["accent_katilimci"],
            ).pack(anchor="w", padx=22, pady=(0, 4))
            self._id_kutusu(
                self.profil_form_frame,
                "Katılımcı ID'niz",
                k.katilimci_id,
                COLORS["accent_katilimci"],
            )
            ctk.CTkLabel(
                self.profil_form_frame,
                text=f"E-posta: {k.email}",
                font=ctk.CTkFont(size=13),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", padx=22, pady=(0, 8))
            btn_frame = ctk.CTkFrame(self.profil_form_frame, fg_color="transparent")
            btn_frame.pack(fill="x", padx=22, pady=(8, 20))
            self._ikincil_buton(btn_frame, "Profili Güncelle", self._profil_duzenle_modu).pack(side="left", padx=(0, 8))
            self._birincil_buton(
                btn_frame,
                "Bilet Al →",
                lambda: self._sayfa_goster("bilet_al"),
                renk=(COLORS["accent_katilimci"], COLORS["accent_katilimci_hover"]),
            ).pack(side="left")
            self.profil_durum_label.configure(
                text=f"✓ Oturum açık — {len(self._benim_biletlerim())} aktif biletiniz var."
            )
        else:
            ctk.CTkLabel(
                self.profil_form_frame,
                text="Bilet alabilmek için profilinizi oluşturun. ID sistem tarafından atanır.",
                font=ctk.CTkFont(size=13),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", padx=22, pady=(0, 12))
            self.entry_profil_ad = self._form_alani(self.profil_form_frame, "Ad Soyad", "ör. Ayşe Yılmaz")
            self.entry_profil_email = self._form_alani(self.profil_form_frame, "E-posta", "ör. ayse@mail.com")
            btn_frame = ctk.CTkFrame(self.profil_form_frame, fg_color="transparent")
            btn_frame.pack(fill="x", padx=22, pady=(12, 8))
            self._birincil_buton(
                btn_frame,
                "Profil Oluştur",
                self._profil_kaydet,
                renk=(COLORS["accent_katilimci"], COLORS["accent_katilimci_hover"]),
            ).pack(fill="x")
            self.profil_durum_label.configure(text="Henüz giriş yapılmadı.")

    def _profil_duzenle_modu(self):
        if self._oturum_katilimci():
            self.profil_duzenle_aktif = True
            self._profil_guncelle()

    def _profil_duzenle_iptal(self):
        self.profil_duzenle_aktif = False
        self._profil_guncelle()

    def _profil_guncelle_kaydet(self):
        k = self._oturum_katilimci()
        ad = self.entry_profil_ad.get().strip()
        email = self.entry_profil_email.get().strip()
        if k and ad and email:
            k.ad = ad
            k.email = email
            self.profil_duzenle_aktif = False
            messagebox.showinfo("Başarılı", "Profiliniz güncellendi.")
            self._profil_guncelle()
        else:
            messagebox.showwarning("Hata", "Ad ve e-posta alanlarını doldurun.")

    def _profil_kaydet(self):
        ad = self.entry_profil_ad.get().strip()
        email = self.entry_profil_email.get().strip()
        if ad and email:
            k_id = self.veri.sonraki_katilimci_id()
            self.veri.katilimcilar[k_id] = Katilimci(k_id, ad, email)
            self.oturum_katilimci_id = k_id
            for w in self.profil_son_id_frame.winfo_children():
                w.destroy()
            self._id_kutusu(
                self.profil_son_id_frame,
                "Size Atanan Katılımcı ID",
                k_id,
                COLORS["accent_katilimci"],
            )
            messagebox.showinfo(
                "Başarılı",
                f"Hoş geldiniz {ad}!\n\nKatılımcı ID'niz: {k_id}\n\nBu ID ile bilet alabilirsiniz.",
            )
            self.profil_duzenle_aktif = False
            self._profil_guncelle()
        else:
            messagebox.showwarning("Hata", "Ad ve e-posta alanlarını doldurun.")

    def _bilet_al_sayfasi(self):
        p = self.sayfalar["bilet_al"]
        self.bilet_al_icerik = ctk.CTkFrame(p, fg_color="transparent")
        self.bilet_al_icerik.pack(fill="both", expand=True)

    def _bilet_al_guncelle(self):
        for w in self.bilet_al_icerik.winfo_children():
            w.destroy()

        k = self._oturum_katilimci()
        if not k:
            uyari = self._kart(self.bilet_al_icerik)
            uyari.pack(fill="x")
            ctk.CTkLabel(
                uyari,
                text="Bilet almak için önce Profilim sayfasından kayıt olun.",
                font=ctk.CTkFont(size=14),
                text_color=COLORS["text_muted"],
            ).pack(padx=22, pady=20)
            self._birincil_buton(
                uyari,
                "Profile Git →",
                lambda: self._sayfa_goster("profil"),
                renk=(COLORS["accent_katilimci"], COLORS["accent_katilimci_hover"]),
            ).pack(padx=22, pady=(0, 20))
            return

        musait = self.veri.musait_etkinlikler()
        if not musait:
            bos = self._kart(self.bilet_al_icerik)
            bos.pack(fill="x")
            ctk.CTkLabel(
                bos,
                text="Şu an bilet alınabilecek müsait etkinlik yok.",
                font=ctk.CTkFont(size=14),
                text_color=COLORS["text_muted"],
            ).pack(padx=22, pady=24)
            return

        secili_id = getattr(self, "_secili_etkinlik_id", None)
        etkinlik_adlari = {self._etkinlik_etiket(e): e.etkinlik_id for e in musait}
        ad_listesi = list(etkinlik_adlari.keys())

        form = self._kart(self.bilet_al_icerik, "Bilet Satın Al")
        form.pack(fill="x")

        ctk.CTkLabel(
            form,
            text=f"Kayıtlı kullanıcı: {k.ad}  ·  ID: {k.katilimci_id}",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["accent_katilimci"],
        ).pack(anchor="w", padx=22, pady=(0, 12))

        satir = ctk.CTkFrame(form, fg_color="transparent")
        satir.pack(fill="x", padx=22, pady=6)
        ctk.CTkLabel(satir, text="Etkinlik", width=130, anchor="w", text_color=COLORS["text_muted"]).pack(side="left")

        baslangic = 0
        if secili_id and secili_id in self.veri.etkinlikler:
            hedef = self.veri.etkinlikler[secili_id]
            hedef_label = self._etkinlik_etiket(hedef)
            if hedef_label in ad_listesi:
                baslangic = ad_listesi.index(hedef_label)

        self.etkinlik_secim = ctk.CTkComboBox(
            satir,
            values=ad_listesi,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            button_color=COLORS["accent_katilimci"],
            button_hover_color=COLORS["accent_katilimci_hover"],
            dropdown_fg_color=COLORS["card"],
            command=self._bilet_al_etkinlik_onizleme,
        )
        self.etkinlik_secim.set(ad_listesi[baslangic])
        self.etkinlik_secim.pack(side="left", fill="x", expand=True)

        self.bilet_onizleme = ctk.CTkFrame(form, fg_color=COLORS["input_bg"], corner_radius=10)
        self.bilet_onizleme.pack(fill="x", padx=22, pady=16)

        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", padx=22, pady=(0, 20))
        self._birincil_buton(
            btn_frame,
            "Bileti Onayla ve Al",
            self._bilet_satin_al,
            renk=(COLORS["accent_katilimci"], COLORS["accent_katilimci_hover"]),
        ).pack(fill="x")

        self._bilet_al_etkinlik_onizleme(self.etkinlik_secim.get())
        self._secili_etkinlik_id = None

    def _bilet_al_etkinlik_onizleme(self, secim):
        for w in self.bilet_onizleme.winfo_children():
            w.destroy()
        e_id = None
        for label, eid in {self._etkinlik_etiket(e): e.etkinlik_id for e in self.veri.musait_etkinlikler()}.items():
            if label == secim:
                e_id = eid
                break
        if not e_id:
            return
        etkinlik = self.veri.etkinlikler[e_id]
        ctk.CTkLabel(
            self.bilet_onizleme,
            text=etkinlik.ad,
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(14, 4))
        ctk.CTkLabel(
            self.bilet_onizleme,
            text=f"📍 {etkinlik.yer}",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["accent_katilimci"],
        ).pack(anchor="w", padx=16, pady=(0, 4))
        ctk.CTkLabel(
            self.bilet_onizleme,
            text=f"📅 {etkinlik.tarih}  ·  Kalan yer: {etkinlik.bos_yer}/{etkinlik.kapasite}",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(0, 14))

    def _bilet_satin_al(self):
        k = self._oturum_katilimci()
        if not k:
            messagebox.showwarning("Hata", "Önce profil oluşturun.")
            return

        secim = self.etkinlik_secim.get()
        e_id = None
        for label, eid in {self._etkinlik_etiket(e): e.etkinlik_id for e in self.veri.musait_etkinlikler()}.items():
            if label == secim:
                e_id = eid
                break

        if not e_id:
            messagebox.showerror("Hata", "Geçersiz etkinlik seçimi.")
            return

        etkinlik = self.veri.etkinlikler[e_id]
        bilet_id = self.veri.sonraki_bilet_id()
        yeni_bilet = Bilet.bilet_olustur(bilet_id, etkinlik, k)

        if yeni_bilet:
            self.veri.biletler.append(yeni_bilet)
            messagebox.showinfo(
                "Bilet Alındı!",
                f"{etkinlik.ad} etkinliği için biletiniz oluşturuldu.\n"
                f"Yer: {etkinlik.yer}\nBilet No: {bilet_id}",
            )
            self._sayfa_goster("biletlerim")
        else:
            messagebox.showerror("Hata", "Bu etkinliğin kapasitesi dolmuştur!")

    def _biletlerim_sayfasi(self):
        p = self.sayfalar["biletlerim"]
        self.biletlerim_frame = ctk.CTkFrame(p, fg_color="transparent")
        self.biletlerim_frame.pack(fill="both", expand=True)

    def _benim_biletlerim(self):
        k = self._oturum_katilimci()
        if not k:
            return []
        return [b for b in self.veri.biletler if b.katilimci.katilimci_id == k.katilimci_id]

    def _biletlerim_guncelle(self):
        for w in self.biletlerim_frame.winfo_children():
            w.destroy()

        k = self._oturum_katilimci()
        if not k:
            uyari = self._kart(self.biletlerim_frame)
            uyari.pack(fill="x")
            ctk.CTkLabel(
                uyari, text="Biletlerinizi görmek için önce giriş yapın.", text_color=COLORS["text_muted"]
            ).pack(padx=22, pady=24)
            return

        biletler = self._benim_biletlerim()
        if not biletler:
            bos = self._kart(self.biletlerim_frame)
            bos.pack(fill="x")
            ctk.CTkLabel(
                bos, text="Henüz biletiniz yok. Keşfet sayfasından etkinlik seçin!", text_color=COLORS["text_muted"]
            ).pack(padx=22, pady=24)
            self._birincil_buton(
                bos,
                "Etkinliklere Git →",
                lambda: self._sayfa_goster("kesfet"),
                renk=(COLORS["accent_katilimci"], COLORS["accent_katilimci_hover"]),
            ).pack(padx=22, pady=(0, 20))
            return

        for b in reversed(biletler):
            kart = ctk.CTkFrame(
                self.biletlerim_frame, fg_color=COLORS["card"], corner_radius=14, border_width=1, border_color=COLORS["border"]
            )
            kart.pack(fill="x", pady=6)
            sol = ctk.CTkFrame(kart, fg_color="transparent")
            sol.pack(side="left", fill="x", expand=True, padx=20, pady=16)
            ctk.CTkLabel(sol, text=f"🎟️  {b.etkinlik.ad}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(
                sol,
                text=f"📅 {b.etkinlik.tarih}  ·  📍 {b.etkinlik.yer}",
                font=ctk.CTkFont(size=12),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", pady=(4, 0))
            ctk.CTkLabel(
                sol,
                text=f"Bilet No: {b.bilet_id}",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", pady=(2, 0))
            ctk.CTkLabel(
                kart, text="✓ Geçerli", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["success"]
            ).pack(side="right", padx=20)


if __name__ == "__main__":
    app = EtkinlikUygulamasi()
    app.mainloop()
