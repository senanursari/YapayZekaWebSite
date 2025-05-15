Yapay Zeka  Web Sitesi
================================

Bu proje, Atatürk Üniversitesi Yapay Zeka Topluluğu için geliştirilmiş resmi bir web sitesidir.
Site; topluluğumuzu tanıtmak, etkinlikleri duyurmak, başvuru toplamak ve QR kod entegrasyonu ile etkinlik girişlerini yönetmek amacıyla hazırlanmıştır.

----------------------------
Özellikler
----------------------------
- Topluluk tanıtım sayfası
- Etkinlik duyuruları ve başvuru formları
- QR kod ile etkinlik katılım kontrolü
- Mobil uyumlu ve sade tasarım

----------------------------
Proje Yapısı
----------------------------

YapayZekaWebSite/
├── index.html           → Ana sayfa
├── style.css            → Sayfa stili
└── README.txt           → Proje açıklamaları (bu dosya)

----------------------------
Kullanım
----------------------------

1. Web Sitesi:

Projeyi bilgisayarınıza klonlayın ve "index.html" dosyasını çift tıklayarak açın.

2. QR Kod Oluşturmak:

Python terminalinde çalıştırın:
    python qr_generator.py

3. QR Kod Doğrulamak:

Python terminalinde çalıştırın:
    python qr_check.py

Gereken kütüphaneleri yüklemek için:

    pip install qrcode opencv-python pyzbar


----------------------------
Katkı ve İletişim
----------------------------

Projeye katkı sunmak isterseniz GitHub üzerinden pull request gönderebilir ya da bizimle iletişime geçebilirsiniz.

GitHub: https://github.com/senanursari/YapayZekaWebSite

----------------------------
Lisans
----------------------------

Bu proje MIT lisansı ile açık kaynak olarak sunulmuştur.

----------------------------
Hazırlayan
----------------------------

Senanur Sarı  
Atatürk Üniversitesi - Yapay Zeka Topluluğu
