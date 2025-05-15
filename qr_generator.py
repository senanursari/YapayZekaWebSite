import gspread
from oauth2client.service_account import ServiceAccountCredentials
import qrcode
import re
import unicodedata

def normalize_filename(filename):
    # Türkçe karakterleri İngilizce karakterlere çevir
    filename = filename.replace('ı', 'i').replace('İ', 'i')
    filename = filename.replace('ğ', 'g').replace('Ğ', 'g')
    filename = filename.replace('ü', 'u').replace('Ü', 'u')
    filename = filename.replace('ş', 's').replace('Ş', 's')
    filename = filename.replace('ö', 'o').replace('Ö', 'o')
    filename = filename.replace('ç', 'c').replace('Ç', 'c')
    
    # Boşlukları kaldır ve küçük harfe çevir
    filename = filename.lower().strip()
    
    # Birden fazla boşluğu tek boşluğa çevir
    filename = re.sub(r'\s+', '_', filename)
    
    # Özel karakterleri kaldır
    filename = re.sub(r'[^a-z0-9_.]', '', filename)
    
    return filename

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("qr-service-key.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Etkinlik Başvuru Formu").sheet1

# Tüm hücreleri string yap + boşlukları temizle
rows = [{k.strip(): str(v).strip() for k, v in row.items()} for row in sheet.get_all_records()]

# Önce mevcut sütun başlıklarını görelim
print("\nMevcut sütun başlıkları:")
for key in rows[0].keys():
    print(f"- {key}")

print(f"\nToplam {len(rows)} kayıt bulundu.\n")

# Her onaylı kişi için QR oluştur
created_qrs = []
for i, row in enumerate(rows, 1):
    if row["Onay Durumu"].strip().upper() == "EVET":
        try:
            ad = row["Ad"].strip()
            soyad = row["Soyad"].strip()
            email = row["Mail"].strip()
            telefon = str(row.get("Telefon Numarası", "")).strip()
            uni = row["Okuduğunuz Üniversite / Okuduğunuz Lise"].strip()
            bolum = row["Bölüm"].strip()
            sinif = row["Sınıf"].strip()
            kaynak = row["Etkinliği nereden duydunuz?"].strip()
            # KVKK kontrolünü kaldırdık

            # QR verisi
            data = f"{ad.strip().lower()} {soyad.strip().lower()} {email.strip().lower()}"
            
            # Normalize edilmiş dosya adı
            filename = f"qr_{normalize_filename(ad)}_{normalize_filename(soyad)}.png"

            # QR kodu oluştur ve kaydet
            qr = qrcode.make(data)
            qr.save(filename)
            
            created_qrs.append(filename)
            print(f"✅ QR oluşturuldu ({i}/{len(rows)}): {filename}")
            
        except KeyError as e:
            print(f"❌ Hata: Sütun bulunamadı: {e}")
            continue
        except Exception as e:
            print(f"❌ Hata ({ad} {soyad}): {str(e)}")
            continue

print(f"\nToplam {len(created_qrs)} QR kod oluşturuldu.")
print("\nOluşturulan QR kodları:")
for qr in created_qrs:
    print(f"- {qr}")
