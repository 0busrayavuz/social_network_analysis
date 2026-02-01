# Türkiye'de Sosyal Medya Üzerinden Kadın Cinayetleri Hakkında Yapılan Yorumların Duygu Analizi

**Proje Grubu:** EmpaTech
**Konu:** Sosyal Ağ Analizi ve Doğal Dil İşleme ile Toplumsal Tepki Analizi

Bu proje, Türkiye'de yaşanan kadın cinayetlerine karşı sosyal medya platformlarında (X) gösterilen toplumsal tepkileri, kullanıcı etkileşim ağlarını ve duygu durumlarını analiz etmek amacıyla geliştirilmiştir.

Proje kapsamında kullanılan **tüm veriler araştırma ekibimiz tarafından özgün olarak toplanmış ve etiketlenmiştir.** Herhangi bir hazır veri seti kullanılmamış olup; paylaşımlar ve bu paylaşımlara gelen yorumlar arasındaki etkileşim ağları haritalandırılmış, içerikler Temel Duygular (Pozitif, Negatif, Nötr) ve Alt Duygular (Öfke, Empati, Umutsuzluk, İğrenme vb.) bazında sınıflandırılarak görselleştirilmiştir.

## Proje Kapsamı ve Özellikleri

### 1. Özgün Veri Toplama
* Veriler, ekibimiz tarafından belirlenen anahtar kelimeler, hashtag'ler ve güncel olaylar üzerinden toplanmıştır.
* Duygu etiketlemeleri (Sentiment Labeling) proje ekibi tarafından manuel ve yarı-otomatik yöntemlerle titizlikle gerçekleştirilmiştir.

### 2. Veri İşleme
* Ham verilerin temizlenmesi, gereksiz karakterlerin (URL, kullanıcı etiketleri vb.) ayıklanması ve doğal dil işleme teknikleri ile analize hazır hale getirilmesi sağlanmıştır.

### 3. Gelişmiş Ağ Analizi
* **Radial (Yıldız) Ağ Yapısı:** Merkezde ana gönderilerin, çevresinde yorumların konumlandırıldığı hiyerarşik ağ görselleştirmesi kullanılmıştır.
* **Metrik Hesaplamaları:** Ağ yoğunluğu, derece dağılımı, modülarite, arasındalık merkeziliği ve topluluk tespiti (Community Detection) analizleri yapılmıştır.

### 4. Görselleştirme
* **Özel Renk Paleti:** Duyguların anlamlarına uygun renk kodları kullanılmıştır (Örn: Öfke için Kırmızı, Empati için Pembe, Umutsuzluk için Koyu Lacivert).
* **Detaylı Grafikler:** Alt duygu kırılımları (Pasta ve Bar grafikleri) ve toplulukların duygu dağılımları analiz edilmiştir.
* **İnteraktif Ağ Haritası:** PyVis kütüphanesi kullanılarak yakınlaştırılıp uzaklaştırılabilen dinamik bir ağ haritası oluşturulmuştur.

## Proje Dosya Yapısı

```text
social-network-analysis/
├── data/               # (Erişim İzne Tabidir - Detaylar aşağıdadır)
├── src/                # Kaynak kod dosyaları
│   ├── __init__.py     # Modül yöneticisi
│   ├── data_loader.py  # Veri yükleme ve temizleme işlemleri
│   ├── analysis.py     # Ağ metrikleri ve hesaplamalar
│   └─ visualization.py # Grafik çizimleri ve ağ görselleştirme
├── main.py             # Projeyi başlatan ana dosya
├── requirements.txt    # Gerekli Python kütüphaneleri
└── README.md           # Proje dokümantasyonu
```

## Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

**1. Projeyi İndirin:**
```
bash
git clone [https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ.git](https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ.git)
cd REPO_ADINIZ
```
**2. Sanal Ortamı Kurun (Önerilen):**
```
python -m venv .venv
# Windows için:
.\.venv\Scripts\activate
# Mac/Linux için:
source .venv/bin/activate
```
**3. Gerekli Kütüphaneleri Yükleyin:**
```
pip install -r requirements.txt
```
**4. Analizi Başlatın:**
```
python main.py
```

🔒 Veri Setine Erişim ve Etik Politikası
Bu projede kullanılan veri seti, Kişisel Verilerin Korunması Kanunu (KVKK) ve etik kurallar gereği herkese açık olarak paylaşılmamıştır. Veri seti, X kullanıcılarının kadın cinayetleri postlarındaki yorumlarını ve kullanıcı adlarını içermektedir.

Akademik araştırmalar veya doğrulama çalışmaları için veri setine ihtiyaç duyan araştırmacılar, aşağıdaki bağlantı üzerinden erişim izni talep edebilirler:

🔗 https://drive.google.com/file/d/1q-fu7W6_pm-YOcXy_cs-Ac1SQNsGI5_2/view?usp=drive_link

Not: Veri seti yalnızca akademik/bilimsel amaçlı kullanımlar için, kullanıcı isimleri anonimleştirilerek paylaşılabilir.

**Çıktılar**
Kod başarıyla çalıştığında outputs/ klasörü altında şu sonuçlar üretilir:
|  **plots/**  |  **reports/**  |
| :--- | :--- |
| • Temel ve Alt Duygu Dağılım Grafikleri<br>• Topluluk Analiz Grafikleri<br>• **EmpaTech_ozel_ag.html** (İnteraktif Ağ Haritası) | • **Ag_Analiz_Raporu.txt**<br>(Toplam düğüm, kenar, yoğunluk ve topluluk sayısı analiz raporu) |


## Proje Ekibi

Bu çalışma, **EmpaTech** araştırma grubu tarafından gerçekleştirilmiştir.

|   |   
| :---: | 
| **Büşra Yavuz** |
|**Osman Arı** |
| **Rabia Özdemir** |
|**Şerife Enginar** |
