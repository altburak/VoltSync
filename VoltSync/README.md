# ⚡ VoltSync: Konut Siteleri İçin Akıllı Enerji & Şarj Yönetim Sistemi

VoltSync, elektrikli araç (EV) sayısının artmasıyla konut sitelerinde oluşacak altyapı yetersizliği ve enerji dalgalanmalarını önlemek için geliştirilmiş **Yapay Zeka Destekli Dinamik Yük Dengeleme (Dynamic Load Balancing)** simülasyonudur.

---

## 🎯 Projenin Amacı
Elektrikli araç sahipliği artarken, binaların mevcut elektrik altyapısı (trafolar) bu yükü kaldırmakta zorlanmaktadır. Altyapıyı yenilemek (trafo büyütmek) milyonlarca liralık maliyet gerektirir. 

**VoltSync**, donanım değiştirmeden, sadece **yazılım zekasıyla** mevcut kapasiteyi en verimli şekilde yönetir, araçları sıraya sokar ve herkesin şarj olmasını garanti eder.

## 🚀 Temel Özellikler (Simülasyon Yetenekleri)

Proje, `main.py` üzerinde çalışan bir terminal simülasyonudur. Aşağıdaki senaryoları başarıyla yönetir:

### 1. Dinamik Yük Dengeleme (Load Balancing)
* Bina elektrik tüketimi arttığında, araçların şarj hızını otomatik düşürür/dengeler.
* Bina tüketimi azaldığında (örn: gece), hızı maksimuma çıkarır.

### 2. Üç Farklı Kullanıcı Modu
* **🌙 ECO MOD (Gece):** "Acelem yok" diyen kullanıcı. Sistem bu araçları gece 02:00-06:00 arası (elektriğin en ucuz olduğu saatte) veya şebekenin müsait olduğu saatlerde şarj eder.
* **🟢 STANDART MOD (Garantili):** Sistem kullanıcıya **"En geç X saatte biter"** garantisi verir. Şebeke müsaitse daha hızlı bitirir.
* **🚀 ACİL MOD (VIP):** Yüksek ücret karşılığı öncelik alır. Diğer araçları gerekirse minimum sınıra kadar yavaşlatır, kendine yol açar.

### 3. Akıllı Kuyruk & Onay Sistemi
* Şebeke tamamen doluysa, yeni gelen kullanıcıya yalan söylemez.
* **"Şu an yer yok, tahmini mevcut araçların dolum süresine göre belirli bir süre beklersiniz. Onaylıyor musunuz?"** diye sorar.
* Onaylanırsa kullanıcıyı sanal kuyruğa alır ve yer açıldığı an otomatik başlatır.

---

## 🔮 Gelecek Planları ve Geliştirme Yol Haritası (Roadmap)

Bu proje şu an için algoritma mantığını kanıtlayan bir simülasyondur. Gerçek saha uygulaması için aşağıdaki geliştirmeler planlanmıştır:

1.  **Gerçek Veri Entegrasyonu:**
    * Binadaki enerji analizörlerinden **Modbus/TCP** protokolü ile anlık tüketim verisi çekilerek, simülasyondaki `BINA_YUKU` değişkeni gerçek zamanlı hale getirilecektir.

2.  **Yapay Zeka Destekli Tahminleme (AI Forecasting):**
    * Sadece anlık duruma değil, geçmiş tüketim verilerine bakarak **"1 saat sonra bina yükü artacak"** tahminini yapan LSTM (Long Short-Term Memory) modelleri entegre edilecektir.

3.  **Güneş Enerjisi (GES) Entegrasyonu:**
    * Gündüz saatlerinde Eco Mod kullanıcıları, şebeke yerine varsa binanın güneş panellerinden üretilen **bedava ve yeşil enerjiye** yönlendirilecektir (Green Charging). Böylelikle kar marjı artacaktır.

4.  **Mobil Uygulama ve Ödeme:**
    * Kullanıcıların mod seçimi yapabileceği ve kredi kartı ile ödeme yapabileceği (Iyzico/Masterpass entegreli) React Native mobil arayüzü geliştirilecektir.

5.  **Donanım Haberleşmesi (OCPP):**
    * Yazılımın şarj cihazlarıyla konuşması için **OCPP 1.6j / 2.0.1** protokolü entegre edilecektir.

---

## 🛠️ Nasıl Çalıştırılır?

Bu simülasyon saf **Python** ile yazılmıştır. Herhangi bir kütüphane kurulumu gerektirmez. Kod çalıştıktan sonra sırayla hayali kullanıcı isimleri girin, daha sonra 3 moddan birini seçin. Bu şekilde istediğiniz kadar kullanıcı ve kombinasyon seçerek tablodaki değişimi görün.

1. Repo'yu bilgisayarınıza indirin.
2. Terminali açın ve proje klasörüne gidin.
3. Aşağıdaki komutu çalıştırın:


```bash
python main.py

