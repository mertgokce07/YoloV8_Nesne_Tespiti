# 👟 Ayakkabı ve Bot Nesne Tespit Modeli

Bu proje, görüntüler üzerinden gerçek zamanlı olarak **Ayakkabı** ve **Bot** tespiti yapmak amacıyla eğitilmiş yüksek doğruluklu bir derin öğrenme modelidir.

## 📊 Performans Özet Tablosu

Model, eğitim sonunda elde edilen verilere göre aşağıdaki metriklerde üstün başarı göstermiştir:

| Metrik | Değer | Açıklama |
| :--- | :--- | :--- |
| **Precision (Kesinlik)** | %98.06 | Doğru tahmin oranı |
| **Recall (Duyarlılık)** | %96.21 | Nesneleri yakalama oranı |
| **mAP50** | %97.33 | Genel model doğruluğu |
| **mAP50-95** | %86.44 | Kutu hassasiyeti ve konum doğruluğu |
| **Hız (Inference)** | 7.56 ms | Görüntü başına işlem süresi (~130 FPS) |

## 🚀 Modelin Güçlü Yönleri

* **Yüksek Doğruluk:** %98'e varan kesinlik oranıyla yanlış pozitif (yanlış alarm) oranı minimuma indirilmiştir.
* **Gerçek Zamanlı Çalışma:** Saniyede 130 kare işleme hızıyla canlı video akışlarında sorunsuz çalışabilir.
* **Dengeli Öğrenme:** Ayakkabı ve Bot sınıfları arasında dengeli bir başarı dağılımı sağlanmıştır.

## 📂 Sınıf Bilgileri
Model aşağıdaki iki sınıfı tanımak üzere özelleştirilmiştir:
1.  **Ayakkabı** (Shoe)
2.  **Bot** (Boot)

