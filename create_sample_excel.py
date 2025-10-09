# create_sample_excel.py
import pandas as pd
from pathlib import Path

Path("data").mkdir(exist_ok=True)

rows = [
    {
        "code": "VP199",
        "title": "No customer master record exists for sold-to party",
        "context": "SD/VA01 sipariş girişinde Sold-to partner eksik ya da hatalı.",
        "solution": "1) SP (Sold-to Party) partner rolü müşteri kartında tanımlı mı kontrol et (XD03/VD03). 2) Partner determination prosedürü ve hesap ataması doğru mu? 3) VA01 içinde partner fonksiyonları otomatik doluyor mu; gerekiyorsa customizing düzelt.",
        "source_link": "https://community.sap.com/ (vp199 araması)"
    },
    {
        "code": "ME045",
        "title": "Purchase order already closed",
        "context": "MM/ME22N; kapatılmış PO yeniden işleme alınmak isteniyor.",
        "solution": "1) ME22N ile kalem/doküman statüsünü kontrol et; gerekirse reopen. 2) GR/IR farklarını MIRO/MRBR ile kapat. 3) Release strategy ve tolerans ayarlarını gözden geçir.",
        "source_link": ""
    },
    {
        "code": "F5153",
        "title": "Posting not allowed to this account",
        "context": "FI; F-02 vb. kayıt sırasında hesap postalamaya kapalı.",
        "solution": "1) FS00’dan ilgili hesabın ‘Postings allowed’ ayarını aç. 2) Dönem kilidi (OB52/OBR1) uygun mu kontrol et. 3) Alan durumu grubu ve belge türü uyumlu mu kontrol et.",
        "source_link": ""
    },
    {
        "code": "M7149",
        "title": "Transfer posting from storage type blocked",
        "context": "WM/EWM; transfer posting sırasında depolama türü bloklu.",
        "solution": "1) Storage Type Control’de ‘Block’ işareti var mı kaldır. 2) LT01 veya /SCWM/ hareketleriyle doğru depolama türüne taşı. 3) Stok türü (unrestricted/QI) uygun mu kontrol et.",
        "source_link": ""
    },
    {
        "code": "ME083",
        "title": "Purchase order already exists",
        "context": "MM; aynı koşullar ile PO tekrarlanıyor.",
        "solution": "1) Mevcut PO numaralarını kontrol et. 2) Referans dokümanları (PR/RFQ) doğru bağlanmış mı? 3) Kopyalama kontrolü ve numaralandırma aralıklarını incele.",
        "source_link": ""
    },
    {
        "code": "ME545",
        "title": "No plant assigned to company code",
        "context": "MM Organizational data eksik; plant-company code bağı eksik.",
        "solution": "1) SPRO: Enterprise Structure → Assignment → Plant to Company Code ataması yap. 2) Satınalma organizasyonu eşleşmeleri tam mı kontrol et.",
        "source_link": ""
    },
    {
        "code": "M7022",
        "title": "Deficit of stock",
        "context": "MM/IM; stok yetersiz.",
        "solution": "1) MMBE ile mevcut stok ve rezervasyonları kontrol et. 2) Stok transferi yap veya tedarik süreci başlat. 3) Negatif stok izni varsa ayarını gözden geçir.",
        "source_link": ""
    },
    {
        "code": "ME059",
        "title": "Account assignment mandatory for material",
        "context": "MM; malzeme için hesap ataması zorunlu.",
        "solution": "1) Malzeme tipinde ve satınalma doküman tipinde AA kategorisi zorunlu mu kontrol et. 2) Doğru AA kategorisini gir (K, F vb.).",
        "source_link": ""
    },
    {
        "code": "F5152",
        "title": "Account requires open item management",
        "context": "FI; hesap açık kalem yönetimi gerektiriyor.",
        "solution": "1) FS00’dan Open Item Management açık mı; eğer kapalı ise dönem sonu etkilerini değerlendirerek aç. 2) Mevcut kalemleri temizlemeden ayar değişikliği yapma.",
        "source_link": ""
    },
    {
        "code": "M7034",
        "title": "Material not maintained",
        "context": "MM; malzeme uzantısı veya temel veri eksik.",
        "solution": "1) MM01/MM02 ile gerekli görünümleri (Purchasing/Accounting/Plant) oluştur. 2) Organizasyon atamalarını tamamla.",
        "source_link": ""
    },
]

df = pd.DataFrame(rows, columns=["code","title","context","solution","source_link"])
df.to_excel("data/sap_errors.xlsx", index=False)
print("✅ data/sap_errors.xlsx oluşturuldu.")
