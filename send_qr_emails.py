import smtplib
import ssl
from email.message import EmailMessage
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time 
import re

def normalize_filename(filename):
    filename = filename.replace('ı', 'i').replace('İ', 'i')
    filename = filename.replace('ğ', 'g').replace('Ğ', 'g')
    filename = filename.replace('ü', 'u').replace('Ü', 'u')
    filename = filename.replace('ş', 's').replace('Ş', 's')
    filename = filename.replace('ö', 'o').replace('Ö', 'o')
    filename = filename.replace('ç', 'c').replace('Ç', 'c')
    filename = filename.lower().strip()
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'[^a-z0-9_.]', '', filename)
    return filename

print("1. Program başlatıldı...")

try:
    # Google Sheets bağlantısı
    print("2. Google Sheets'e bağlanılıyor...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("qr-service-key.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Etkinlik Başvuru Formu").sheet1
    print("✅ Google Sheets bağlantısı başarılı!")

    print("3. Veriler okunuyor...")
    rows = [{k.strip(): v for k, v in row.items()} for row in sheet.get_all_records()]
    print(f"✅ Toplam {len(rows)} satır okundu.")

    # Onaylı başvurular - e-posta adreslerine göre benzersiz hale getir
    onayli_kayitlar = []
    seen_emails = set()
    for row in rows:
        if row["Onay Durumu"].strip().upper() == "EVET":
            email = row["Mail"].strip()
            if email not in seen_emails:
                onayli_kayitlar.append(row)
                seen_emails.add(email)
    
    print(f"\n5. Toplam benzersiz onaylı başvuru sayısı: {len(onayli_kayitlar)}")

    EMAIL_ADDRESS = "yapayzekaata@yandex.com"
    EMAIL_PASSWORD = "ekolxqaogstmvlfv"
    smtp_server = "smtp.yandex.com"
    port = 465

    print("\n4. Yandex SMTP bağlantısı test ediliyor...")
    context = ssl.create_default_context()
    failed_sends = []
    sent_emails = set()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("✅ Yandex SMTP bağlantısı başarılı!")

        print("\n6. Mail gönderme işlemi başlıyor...")

        for index, row in enumerate(onayli_kayitlar, 1):
            ad = row["Ad"].strip()
            soyad = row["Soyad"].strip()
            email = row["Mail"].strip()

            if email in sent_emails:
                print(f"🔁 Atlanıyor (zaten gönderildi): {email}")
                continue

            print(f"\n📨 [{index}/{len(onayli_kayitlar)}] İşleniyor: {email}")

            possible_filenames = [
                f"qr_{normalize_filename(ad)}_{normalize_filename(soyad)}.png",
                f"qr_{normalize_filename(ad + '_' + soyad)}.png"
            ]

            qr_file = next((f for f in possible_filenames if os.path.exists(f)), None)

            if qr_file:
                try:
                    msg = EmailMessage()
                    msg["Subject"] = "🎉 Etkinlik Başvurunuz Onaylandı!"
                    msg["From"] = EMAIL_ADDRESS
                    msg["To"] = email
                    msg.set_content(f"""
Merhaba {ad} {soyad},

🎉 Başvurunuz başarıyla onaylandı!

Etkinliğimiz 17-18 Mayıs günlerinde saat 10:00' da 15 Temmuz Milli İrade Salonu'nda başlayacaktır. 
Girişlerde kullanacağınız QR kodunuz ektedir 📎
Etkinlikte görüşmek üzere 💜
""", subtype='html')

                    print(f"  - QR kod dosyası okunuyor: {qr_file}")
                    with open(qr_file, "rb") as f:
                        qr_data = f.read()
                        msg.add_attachment(qr_data, maintype="image", subtype="png", filename=qr_file)

                    print("  - Mail gönderiliyor...")
                    server.send_message(msg)
                    print(f"✅ Gönderildi: {email}")
                    sent_emails.add(email)
                    time.sleep(7)

                except Exception as e:
                    print(f"❌ Mail gönderim hatası ({email}): {str(e)}")
                    failed_sends.append((email, str(e)))
            else:
                print("❌ QR kod dosyası bulunamadı. Denenen dosyalar:")
                for f in possible_filenames:
                    print(f"   - {f}")
                failed_sends.append((email, "QR kod dosyası bulunamadı"))

except Exception as e:
    print(f"❌ Genel hata: {str(e)}")

print("\n7. Program tamamlandı!")

# Başarısız gönderim raporu
if failed_sends:
    print("\n❌ Gönderilemeyen mailler:")
    for email, reason in failed_sends:
        print(f"- {email}: {reason}")

    with open("failed_sends.txt", "w", encoding='utf-8') as f:
        f.write("Gönderilemeyen Mailler:\n")
        for email, reason in failed_sends:
            f.write(f"{email}: {reason}\n")
    print("\nDetaylı hata raporu 'failed_sends.txt' dosyasına kaydedildi.")