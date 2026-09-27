# Gezgin Satıcı Problemi İçin Sezgisel Algoritmayla Parametre Optimizasyonu

Pamukkale Üniversitesi, Endüstri Mühendisliği Bölümü — IENG435 Problem Çözmede Sezgisel Yöntemler dönem projesi.

**Hazırlayan:**  Dilara Şahbaz
**Öğretim Üyesi:** Prof. Dr. Can Berk Kalaycı
**Dönem:** Bahar, 2024-2025

## Proje Özeti

Bu proje, Gezgin Satıcı Problemi'ni (TSP) genetik algoritma ile çözerken algoritma parametrelerinin (popülasyon büyüklüğü, iterasyon sayısı, elitizm oranı, çaprazlama oranı, mutasyon oranı) çözüm kalitesine etkisini tam faktöriyel deneysel tasarım yöntemiyle incelemektedir. Çalışma iki aşamadan oluşur: popülasyon/iterasyon sayısını belirlemeye yönelik bir pilot çalışma, ve ardından elitizm/çaprazlama/mutasyon oranlarının test edildiği ana deney.

## Klasör İçeriği

- `kod.py` — Ana genetik algoritma ve tam faktöriyel deney kodu. Berlin52 veri setinde elitizm, çaprazlama ve mutasyon oranlarının tüm kombinasyonlarını 10 farklı seed ile dener, sonuçları Excel'e yazar.
- `pilot_calisma.py` — Pilot çalışma kodu. Farklı popülasyon büyüklüğü (30, 40, 50) ve iterasyon sayısı (10.000, 50.000, 100.000) kombinasyonlarını dener.
- `dataSets/` — TSPLIB formatında test veri setleri: `berlin52`, `att48`, `bays29`, `a280`, `ch150`, `eil51`.
- `Pilot_Study_Results.xlsx` — Pilot çalışma sonuçları.
- `TSP_Parameter_Optimization_Results*.xlsx` — Ana deneyin farklı veri setleri ve parametre koşulları için sonuç dosyaları.
- `Sezgisel_proje.docx` / `.pdf` — Proje raporu (yöntem, deney tasarımı, sonuçlar).
- `tam_faktoriye_tasarim.docx` — Tam faktöriyel deney tasarımı tablosu.

## Yöntem

Algoritma standart bir genetik algoritma iskeleti kullanır:

- **Başlangıç popülasyonu:** Rastgele permütasyonlar
- **Çaprazlama operatörleri:** OX (order crossover), edge recombination, ANX (alternating/neighbor-based)
- **Mutasyon operatörleri:** exchange, inversion, scramble, displacement, insert
- **Seçilim:** Fitness'e göre sıralama + elitizm

Her nesilde operatör seçimi rastgele olup, hangi çaprazlama/mutasyon türünün uygulanacağı rastgele bir sayı ile belirlenir.

### Test Edilen Parametreler (Ana Deney)

| Parametre | Değerler |
|---|---|
| Popülasyon büyüklüğü | 30 |
| İterasyon sayısı | 1e5 |
| Elitizm oranı (ER) | 0.1, 0.2, 0.3 |
| Çaprazlama oranı (CR) | 0.5, 0.7, 0.9 |
| Mutasyon oranı (MR) | 0.01, 0.05, 0.1 |
| Seed | 0-9 (10 tekrar) |
| Zaman limiti | 60 saniye/koşu |

### Sonuç

Berlin52 dahil test edilen veri setlerinde, popülasyon 30 ve iterasyon 1e5 sabit tutulduğunda elitizm oranı 0.1, çaprazlama oranı 0.5, mutasyon oranı 0.01 kombinasyonu genellikle en iyi sonuçları vermiştir. Detaylı tablo ve karşılaştırmalar `Sezgisel_proje.pdf içindedir.
