# Etkinlik Kayıt Sistemi — Kullanım Kılavuzu

Bu belge, masaüstü uygulamasının nasıl çalıştırılacağını ve ekrandaki her bölümün ne işe yaradığını adım adım anlatır.

---

## 1. Program ne işe yarar?

**Etkinlik Kayıt Sistemi**, etkinlikleri tanımlamanıza, katılımcıları kaydetmenize ve bir katılımcıyı belirli bir etkinliğe **bilet / kayıt** ile bağlamanıza olanak veren basit bir yönetim aracıdır. Ayrıca her etkinlik için **kapasite, katılan sayısı ve boş yer** bilgisini özetleyen bir **katılım raporu** üretir.

Veriler uygulama açıkken **bilgisayar belleğinde** tutulur; programı kapatınca kayıtlar silinir (kalıcı dosya veya veritabanı yoktur).

---

## 2. Gereksinimler

| Bileşen | Açıklama |
|--------|----------|
| **Python 3** | Python yüklü olmalıdır (tercihen güncel bir 3.x sürümü). |
| **tkinter** | Grafik arayüz için kullanılır. Windows’ta Python ile birlikte çoğu kurulumda gelir. |

tkinter’in yüklü olup olmadığını terminalde şu komutla deneyebilirsiniz:

```bash
python -m tkinter
```

Küçük bir test penceresi açılıyorsa kurulum uygundur.

---

## 3. Programı nasıl çalıştırırım?

1. `etkinlik_kayit_sistemi.py` dosyasının bulunduğu klasöre gidin.
2. Terminal veya Komut İstemi’nde şunu çalıştırın:

```bash
python etkinlik_kayit_sistemi.py
```

Alternatif olarak dosyaya çift tıklayarak da açılabilir (sisteminizde `.py` dosyalarının Python ile ilişkilendirilmiş olması gerekir).

Pencere başlığı **“Etkinlik Kayıt Sistemi”** olmalıdır. Pencereyi kapatana kadar uygulama çalışmaya devam eder.

---

## 4. Önerilen kullanım sırası

İşlemler birbirine bağlıdır. Mantıklı sıra şöyledir:

1. **Önce etkinlik ekleyin** (en az bir etkinlik ve kapasitesi tanımlı olsun).
2. **Sonra katılımcı ekleyin** (bileti kesilecek kişiler sistemde kayıtlı olsun).
3. **Ardından bilet oluşturun** (etkinlik ID ve katılımcı ID ile eşleştirme).
4. İsterseniz **Katılım Raporunu Göster** ile özet görün.

Bilet aşamasında girilen **Etkinlik ID** ve **Katılımcı ID**, daha önce eklediğiniz kayıtlarla **birebir aynı** olmalıdır (büyük/küçük harf dahil).

---

## 5. Ekran bölümleri

### 5.1. Etkinlik Ekle

| Alan | Zorunlu | Açıklama |
|------|---------|----------|
| **Etkinlik ID** | Evet | Etkinliği sistemde tanımlayan benzersiz metin (ör. `E001`). Aynı ID ile tekrar eklerseniz önceki etkinlik **üzerine yazılır**; uyarı verilmez. |
| **Etkinlik Adı** | Evet | Etkinliğin görünen adı. |
| **Tarih** | Evet | Uygulama tarih biçimini zorlamaz; istediğiniz metni yazabilirsiniz (ör. `14.05.2026` veya `2026-05-14`). |
| **Kapasite** | Evet | Yalnızca **tam sayı** karakterleri kabul edilir (ör. `50`). Harf veya boş bırakma geçerli kayıt oluşturmaz. |

**Etkinlik Ekle** düğmesine bastığınızda alanlar doğruysa bilgi penceresi açılır ve form temizlenir. Eksik veya hatalı girişte uyarı mesajı görürsünüz.

---

### 5.2. Katılımcı Ekle

| Alan | Zorunlu | Açıklama |
|------|---------|----------|
| **Katılımcı ID** | Evet | Kişiyi tanımlayan benzersiz metin (ör. `K042`). Aynı ID tekrar eklenirse önceki kayıt üzerine yazılır. |
| **Ad Soyad** | Evet | Katılımcının adı. |
| **E-mail** | Evet | İletişim için e-posta (biçim doğrulaması yoktur; boş olmamalıdır). |

**Katılımcı Ekle** ile kayıt tamamlanır; başarılı olunca form temizlenir.

---

### 5.3. Bilet Kes / Kayıt Yap

Bu bölüm, bir katılımcıyı bir etkinliğe **kayıtlı katılımcı listesine** ekler ve geçerliyse bir **bilet** nesnesi oluşturur.

| Alan | Zorunlu | Açıklama |
|------|---------|----------|
| **Bilet ID** | Evet | Bu bileti ayırt etmek için verdiğiniz metin (ör. `B1001`). |
| **Etkinlik ID** | Evet | **Etkinlik Ekle** bölümünde kullandığınız ID ile aynı olmalıdır. |
| **Katılımcı ID** | Evet | **Katılımcı Ekle** bölümünde kullandığınız ID ile aynı olmalıdır. |

**Bilet Oluştur** düğmesi:

- ID’ler sistemde varsa ve etkinlikte **boş yer** varsa: katılımcı o etkinliğin listesine eklenir, bilet oluşturulur, başarı mesajı gösterilir.
- Etkinlik **doluysa**: hata mesajı — *“Bu etkinliğin kapasitesi dolmuştur!”*
- Yanlış veya hiç eklenmemiş ID’lerde: *“Geçersiz Etkinlik ID veya Katılımcı ID.”*
- Alanlardan biri boşsa: bilet için tüm alanların doldurulması istenir.

**Not:** Aynı kişi aynı etkinliğe birden fazla kez **bilet** ile eklenebilir; her seferinde liste uzar ve kapasite buna göre dolar. İş kuralları ihtiyacınıza göre farklı olabilir; uygulama şu an tekrarı engellemez.

---

### 5.4. Etkinlik Raporları

- **Katılım Raporunu Göster** düğmesine basınca alt metin kutusu güncellenir.
- Her etkinlik için şunlar yazılır:
  - Etkinlik adı ve ID
  - Tarih
  - **Kapasite**, **Katılan** (o etkinliğin kayıtlı katılımcı listesindeki kişi sayısı), **Boş Yer**

Henüz hiç etkinlik yoksa *“Sistemde henüz etkinlik bulunmuyor.”* mesajı görünür.

---

## 6. Sık karşılaşılan durumlar

| Durum | Ne yapmalıyım? |
|--------|----------------|
| Kapasite hatası | Etkinlik kapasitesini artırın veya başka etkinlik seçin; mevcut kayıtlar bellekte kalır. |
| Geçersiz ID | Etkinlik ve katılımcıyı önce eklediğinizden ve yazımın (boşluk, harf) aynı olduğundan emin olun. |
| Kapasite kabul edilmiyor | Kapasite alanına sadece rakam yazın (`50` gibi). |
| Program kapandı, veriler gitti | Normal davranıştır; kalıcı kayıt özelliği yoktur. |

---

## 7. Dosya yapısı (özet)

| Dosya | İşlev |
|--------|--------|
| `etkinlik_kayit_sistemi.py` | Uygulamanın tüm kodu ve arayüzü. |
| `KULLANIM_KILAVUZU.md` | Bu kullanım kılavuzu. |

---

## 8. Teknik not (kısa)

Uygulama **tkinter** ile masaüstü penceresi açar. Etkinlik ve katılımcılar Python **sözlük** yapısında ID ile saklanır; biletler bir **liste**de tutulur. Detaylı kod açıklamaları kaynak dosyadaki yorum satırlarında yer alır.

---

*Bu kılavuz, proje klasöründeki mevcut sürüme göre hazırlanmıştır.*
