import time
import sys

# --- SİSTEM AYARLARI ---
TRAFO_KAPASITESI = 100.0
BINA_YUKU = 40.0
MEVCUT_KAPASITE = TRAFO_KAPASITESI - BINA_YUKU # 60 kW Net Kapasite
MIN_GARANTI_HIZ = 4.0 # Standart kullanıcıya verdiğimiz en kötü durum sözü (kW)

bagli_araclar = []

def sure_formatla(saat_ondalik):
    """Saat formatını düzenler"""
    if saat_ondalik > 50: return "-"
    saat = int(saat_ondalik)
    dakika = int((saat_ondalik - saat) * 60)
    if saat > 0: return f"{saat} sa {dakika} dk"
    else: return f"{dakika} dk"

def raporu_yazdir():
    print("\n" + "="*118)
    print(f"⚡ VOLTSYNC CANLI PANEL (Kullanılabilir Güç: {MEVCUT_KAPASITE:.1f} / 60.0 kW)")
    print("="*118)
    print(f"{'İsim':<12} | {'Mod':<10} | {'Güç (kW)':<10} | {'Ücret':<15} | {'Gerçekleşen Süre':<18} | {'DURUM'}")
    print("-" * 118)
    
    toplam_guc = 0
    for arac in bagli_araclar:
        durum = ""
        fiyat = f"{arac['baz_fiyat']} TL"
        sure_str = sure_formatla(arac['tahmini_sure'])
        
        if arac['anlik_guc'] == 0:
            if arac['mod_adi'] == "Eco":
                durum = "🌙 Gece Modu (02:00)"
                fiyat = "-" 
            else:
                durum = f"⏳ SIRADA (Bekliyor: {arac['bekleme_suresi_str']})"
                fiyat = "-"
                sure_str = "-"
        elif arac['mod_adi'] == "ACİL":
            durum = "🚀 VIP HIZ"
        elif arac['mod_adi'] == "Standart":
            # Kullanıcıya sürpriz yapıyoruz: Garantiden hızlıysa belirt
            if arac['anlik_guc'] > MIN_GARANTI_HIZ:
                durum = "🟢 HIZLI ŞARJ (Garanti Üstü)"
            elif arac['anlik_guc'] < 5.0:
                durum = "⚠️ MİNİMUM HIZ"
                fiyat = "4 TL (İndirimli)"
            else:
                durum = "🟢 NORMAL HIZ"

        print(f"{arac['isim']:<12} | {arac['mod_adi']:<10} | {arac['anlik_guc']:.1f} kW    | {fiyat:<15} | {sure_str:<18} | {durum}")
        toplam_guc += arac['anlik_guc']

    print("-" * 118)
    doluluk = int((toplam_guc / (TRAFO_KAPASITESI - BINA_YUKU)) * 100)
    print(f"TRAFO YÜKÜ: %{doluluk} Dolu")
    print("="*118 + "\n")

def en_erken_musaitlik_hesapla():
    aktif_aciller = [a for a in bagli_araclar if a['mod_tipi'] == 3 and a['anlik_guc'] > 0]
    if not aktif_aciller: return 0
    sureler = [a['tahmini_sure'] for a in aktif_aciller]
    return min(sureler)

def algoritma_calistir():
    kullanilabilir = MEVCUT_KAPASITE
    for arac in bagli_araclar: 
        if arac['durum_kodu'] == 'AKTIF': arac['anlik_guc'] = 0 

    # 1. ACİL (VIP)
    aciller = [a for a in bagli_araclar if a['mod_tipi'] == 3 and a['durum_kodu'] == 'AKTIF']
    for arac in aciller:
        verilen = min(22.0, kullanilabilir)
        arac['anlik_guc'] = verilen
        kullanilabilir -= verilen

    # 2. STANDART
    standartlar = [a for a in bagli_araclar if a['mod_tipi'] == 2 and a['durum_kodu'] == 'AKTIF']
    if standartlar and kullanilabilir > 0:
        kisi_basi = kullanilabilir / len(standartlar)
        for arac in standartlar:
            arac['anlik_guc'] = min(kisi_basi, 11.0)

    # SÜRE GÜNCELLEME
    for arac in bagli_araclar:
        if arac['anlik_guc'] > 0:
            kalan = arac['hedef'] - arac['mevcut']
            arac['tahmini_sure'] = kalan / arac['anlik_guc']

# --- SİMÜLASYON ---

print("#################################################")
print("##   VOLTSYNC - GARANTİLİ ŞARJ SİSTEMİ v7.0    ##")
print("#################################################")
time.sleep(1)

while True:
    print("\n>>> YENİ ARAÇ GİRİŞİ (Çıkış için 'q')")
    isim = input("Sürücü Adı: ")
    if isim == 'q': break
    if not isim: isim = "Misafir"

    print("1. ECO (Gece) | 2. STANDART (Garanti Süre) | 3. ACİL (VIP)")
    secim = input("Seçim (1-3): ")
    
    mod_tipi = 2; mod_adi = "Standart"; fiyat = 7
    if secim == '1': mod_tipi=1; mod_adi="Eco"; fiyat=4
    elif secim == '3': mod_tipi=3; mod_adi="ACİL"; fiyat=15

    # --- 1. STANDART MOD (KÖTÜ GÜN SENARYOSU HESABI) ---
    if mod_tipi == 2:
        # Mevcut yoğunluğa bakmadan, EN KÖTÜ ihtimali hesapla
        kalan_sarj_ihtiyaci = 60.0 # Varsayılan (kW)
        garanti_sure_saat = kalan_sarj_ihtiyaci / MIN_GARANTI_HIZ
        garanti_str = sure_formatla(garanti_sure_saat)
        
        print(f"\n🔎 SİSTEM ANALİZİ VE GARANTİ HESAPLAMASI...")
        time.sleep(0.5)
        print(f"ℹ️ Şebeke yoğunluğuna karşı size 'Minimum Hız' garantisi veriyoruz.")
        print(f"🛡️ EN GEÇ DOLUM SÜRESİ: {garanti_str} (Garanti Edilen)")
        print(f"⚡ (Not: Şebeke müsaitse çok daha erken biter)")
        print(f"💰 Tarife: {fiyat} TL / kWh")
        
        onay = input(">> Onaylıyor musunuz? (E/H): ")
        if onay.lower() != 'e':
            print("❌ İptal edildi.")
            continue

    # --- 2. ACİL MOD KONTROLÜ (Sıra var mı?) ---
    elif mod_tipi == 3:
        aktif_yuk = sum(a['anlik_guc'] for a in bagli_araclar)
        bos_yer = MEVCUT_KAPASITE - aktif_yuk
        
        if bos_yer < 20.0: 
            bekleme = en_erken_musaitlik_hesapla()
            bk_str = sure_formatla(bekleme)
            print(f"\n⛔ VIP KONTENJANI DOLU!")
            print(f"ℹ️ Sizi sıraya alabiliriz. En erken başlama: {bk_str} sonra.")
            
            onay = input(">> Sıraya girmeyi onaylıyor musunuz? (E/H): ")
            if onay.lower() != 'e':
                print("❌ İptal edildi.")
                continue
            else:
                yeni_arac = {
                'isim': isim, 'mod_tipi': mod_tipi, 'mod_adi': mod_adi, 'baz_fiyat': fiyat,
                'mevcut': 20, 'hedef': 80, 'anlik_guc': 0, 'tahmini_sure': 0,
                'durum_kodu': 'SIRADA', 'bekleme_suresi_str': bk_str
                }
                bagli_araclar.append(yeni_arac)
                print("✅ Sıraya alındınız.")
                raporu_yazdir()
                continue

    # --- 3. ECO MOD KONTROLÜ ---
    elif mod_tipi == 1:
        print(f"\nℹ️ Eco Mod seçtiniz. Araç gece 02:00'den sonra şarj olacak.")
        onay = input(">> Onaylıyor musunuz? (E/H): ")
        if onay.lower() != 'e':
            print("❌ İptal edildi.")
            continue

    # --- LİSTEYE EKLE ---
    yeni_arac = {
        'isim': isim, 'mod_tipi': mod_tipi, 'mod_adi': mod_adi, 'baz_fiyat': fiyat,
        'mevcut': 20, 'hedef': 80, 'anlik_guc': 0, 'tahmini_sure': 0,
        'durum_kodu': 'AKTIF', 'bekleme_suresi_str': '-'
    }
    if mod_tipi == 1: yeni_arac['durum_kodu'] = 'BEKLEMEDE'

    bagli_araclar.append(yeni_arac)
    print("\n✅ Araç Sisteme Eklendi.")
    time.sleep(0.5)
    algoritma_calistir()
    raporu_yazdir()