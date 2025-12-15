# YOLOv8 Object Detection with PyQt5 GUI

Bu projede, **YOLOv8 (You Only Look Once v8)** nesne tespit algoritması kullanılarak
**Ayakkabı** ve **Bot** nesnelerinin görüntüler üzerinde tespiti gerçekleştirilmiştir.
Eğitilen derin öğrenme modeli, **PyQt5** kullanılarak geliştirilen bir masaüstü
uygulamasına entegre edilmiştir.

Proje kapsamında hem **model eğitimi** hem de **gerçek zamanlıya yakın bir GUI
uygulaması** geliştirilmiş ve uçtan uca bir nesne tespit sistemi oluşturulmuştur.

---

## Proje Amacı

Bu projenin temel amacı:

- YOLOv8 kullanarak **kendi veri seti** üzerinde nesne tespiti yapmak
- Eğitilen modeli bir **masaüstü GUI uygulaması** ile kullanılabilir hale getirmek
- Bounding box çizimi, sınıflandırma ve nesne sayımı işlemlerini kullanıcıya görsel
  olarak sunmaktır.

---

## Veri Seti

- Veri seti **kendi oluşturulan görüntülerden** meydana gelmektedir.
- Toplamda **200+ etiketli görüntü** bulunmaktadır.
- Veri seti **YOLOv8 formatına uygun** olacak şekilde etiketlenmiştir.
- Etiketleme işlemleri **Roboflow** aracı kullanılarak yapılmıştır.
- Her görüntüde bir veya birden fazla nesne (Ayakkabi / Bot) bulunabilmektedir.

Veri seti yapısı aşağıdaki gibidir:

dataset/
├── images/
│ ├── train/
│ ├── val/
│ └── test/
├── labels/
│ ├── train/
│ ├── val/
│ └── test/
└── data.yaml


---

## Model Eğitimi (YOLOv8)

- YOLOv8 modeli **Ultralytics** kütüphanesi kullanılarak eğitilmiştir.
- Eğitim süreci `yolov8.ipynb` dosyasında detaylı şekilde gösterilmiştir.
- Eğitim sonunda aşağıdaki metrikler raporlanmıştır:
  - Precision
  - Recall
  - mAP@50
  - mAP@50–95
- En iyi sonuç veren model ağırlıkları **best.pt** dosyası olarak kaydedilmiştir.

---

## PyQt5 GUI Uygulaması

Geliştirilen masaüstü uygulama aşağıdaki özelliklere sahiptir:

### Arayüz Özellikleri
- **Original Image Paneli**: Kullanıcının seçtiği görüntü gösterilir.
- **Tagged Image Paneli**: YOLOv8 tarafından analiz edilen ve üzerinde
  bounding box çizilmiş görüntü gösterilir.

### Fonksiyonel Özellikler
- **Select Image**: Bilgisayardan bir görüntü seçme
- **Test Image**: Seçilen görüntü üzerinde nesne tespiti yapma
- **Save Image**: Bounding box çizilmiş görüntüyü kaydetme
- **Nesne Sayımı**: Tespit edilen Ayakkabi ve Bot nesnelerinin sayısının gösterilmesi

GUI uygulaması `gui_app.py` dosyasında yer almaktadır.

---

## Dosya Yapısı

├── dataset/
├── yolov8.ipynb
├── gui_app.py
├── best.pt
└── README.md

Kullanılan Teknolojiler

Python 3.11

YOLOv8 (Ultralytics)

PyQt5

OpenCV

NumPy