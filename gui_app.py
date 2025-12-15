# ============================
# 1) GEREKLİ KÜTÜPHANELER
# ============================

import sys                 # Uygulamayı çalıştırma/kapama (Qt event loop) gibi işlemler için
import cv2                 # OpenCV: görüntü işleme, renk dönüşümü, dosya kaydetme için
from ultralytics import YOLO  # YOLOv8 modelini yükleyip tahmin yapmak için

# PyQt5: Masaüstü arayüz (GUI) elemanları
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,  # temel pencere, yazı/alan, buton
    QFileDialog, QWidget, QHBoxLayout, QVBoxLayout     # dosya seçme penceresi, layoutlar
)
from PyQt5.QtGui import QPixmap, QImage  # QPixmap: ekranda resim göstermek, QImage: ham pixel -> Qt görsel
from PyQt5.QtCore import Qt             # hizalama, ölçekleme gibi Qt sabitleri (AlignCenter vb.)

# ============================
# 2) ANA PENCERE SINIFI
# ============================

class YOLOGui(QMainWindow):
    """
    Bu sınıf, PyQt5 ile bir ana pencere oluşturur.
    - Sol tarafta: Original Image (kullanıcının seçtiği görüntü)
    - Sağ tarafta: Tagged Image (YOLO çıktısı: bounding box çizilmiş görüntü)
    - Butonlar: Select Image, Test Image, Save Image
    - Etiket: Ayakkabi/Bot sayımı
    """

    def __init__(self):
        super().__init__()  # QMainWindow'un kendi kurulumlarını başlatır

        # Pencerenin başlığı ve boyutu
        self.setWindowTitle("YOLOv8 Object Detection GUI")
        self.setGeometry(100, 100, 1300, 700)  # (x, y, genişlik, yükseklik)

        # ============================
        # 2.1) MODELİ YÜKLEME
        # ============================
        # best.pt dosyası proje klasöründe olmalı.
        # YOLO("best.pt") => eğittiğin model ağırlıklarını yükler.
        self.model = YOLO("best.pt")

        # Kullanıcının seçtiği görselin dosya yolu burada tutulacak
        self.image_path = None

        # Arayüzü hazırlayan fonksiyon
        self.init_ui()

    # ============================
    # 3) ARAYÜZÜ OLUŞTURMA
    # ============================
    def init_ui(self):
        # Ana widget: QMainWindow içine yerleştirilen ana "container"
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Ana layout yatay: sol ve sağ tarafı yan yana koyacağız
        main_layout = QHBoxLayout()

        # Sol taraf (original image + select button)
        left_layout = QVBoxLayout()

        # Sağ taraf (tagged image + sayım + test + save)
        right_layout = QVBoxLayout()

        # ============================
        # 3.1) ORIGINAL IMAGE ALANI
        # ============================
        self.original_label = QLabel("Original Image")
        self.original_label.setAlignment(Qt.AlignCenter)  # ortala
        self.original_label.setFixedSize(500, 400)        # sabit boyut (UI düzenli kalsın diye)
        self.original_label.setStyleSheet(self.image_style())  # CSS benzeri stil

        # ============================
        # 3.2) TAGGED IMAGE ALANI
        # ============================
        self.tagged_label = QLabel("Tagged Image")
        self.tagged_label.setAlignment(Qt.AlignCenter)
        self.tagged_label.setFixedSize(500, 400)
        self.tagged_label.setStyleSheet(self.image_style())

        # ============================
        # 3.3) BUTONLAR
        # ============================
        # Select Image: kullanıcıdan resim seçtirir
        self.select_btn = QPushButton("Select Image")
        self.select_btn.clicked.connect(self.select_image)  # butona basılınca select_image() çalışır

        # Test Image: seçilen resimde YOLO tahmini yapar ve bounding box çizer
        self.test_btn = QPushButton("Test Image")
        self.test_btn.clicked.connect(self.test_image)

        # Save Image: tahminli (boxed) görüntüyü kaydeder
        self.save_btn = QPushButton("Save Image")
        self.save_btn.clicked.connect(self.save_image)

        # ============================
        # 3.4) SAYIM LABEL'I
        # ============================
        # YOLO çıktılarına göre kaç tane ayakkabı/bot tespit edildiğini göstereceğiz
        self.count_label = QLabel("Ayakkabi: 0 | Bot: 0")
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet(
            "color: yellow; font-size: 18px; font-weight: bold;"
        )

        # ============================
        # 3.5) BUTON STİLLERİ
        # ============================
        for btn in [self.select_btn, self.test_btn, self.save_btn]:
            btn.setFixedHeight(40)         # butonların yüksekliği aynı olsun
            btn.setStyleSheet(self.button_style())  # stil uygula

        # ============================
        # 3.6) LAYOUT'A ELEMAN EKLEME
        # ============================
        # Sol layout: üstte original image alanı, altında select butonu
        left_layout.addWidget(self.original_label)
        left_layout.addWidget(self.select_btn)

        # Sağ layout: üstte tagged image alanı, altında sayım, test ve save butonu
        right_layout.addWidget(self.tagged_label)
        right_layout.addWidget(self.count_label)
        right_layout.addWidget(self.test_btn)
        right_layout.addWidget(self.save_btn)

        # Ana layout: sol ve sağ layout'u yan yana koy
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # main_widget'in layout'unu ayarla
        main_widget.setLayout(main_layout)

        # Pencere arkaplan rengi
        main_widget.setStyleSheet("background-color: #0d1117;")

    # =============================
    # 4) FONKSİYONLAR
    # =============================

    def select_image(self):
        """
        Kullanıcıdan bir resim seçmesini ister.
        Seçilen resim:
          - self.image_path içine kaydedilir
          - Original Image panelinde gösterilir
        """

        # QFileDialog.getOpenFileName => kullanıcıya dosya seçme penceresi açar
        # Dönen: (dosya_yolu, seçilen_filter)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg)"  # sadece görseller listelensin
        )

        # Eğer kullanıcı bir dosya seçtiyse
        if file_path:
            self.image_path = file_path  # yolu sakla

            # QPixmap: Qt'nin resim gösterme formatı
            pixmap = QPixmap(file_path)

            # Resmi label boyutuna sığdır (oran bozulmasın)
            self.original_label.setPixmap(
                pixmap.scaled(
                    self.original_label.size(),
                    Qt.KeepAspectRatio,       # görüntüyü ezme, oranı koru
                    Qt.SmoothTransformation   # daha kaliteli ölçekleme
                )
            )

    def test_image(self):
        """
        Seçilen görsel üzerinde YOLO tahmini yapar.
        - Tespit edilen sınıfları sayar (Ayakkabi/Bot)
        - result.plot() ile bounding box çizilmiş çıktıyı üretir
        - Tagged Image panelinde gösterir
        - Save için last_result_image olarak saklar
        """

        # Eğer daha önce resim seçilmediyse tahmin yapma
        if self.image_path is None:
            return

        # ============================
        # 4.1) YOLO İLE TAHMİN
        # ============================
        # self.model(self.image_path) => dosya yolunu YOLO'ya verir
        # conf=0.25 => güven eşiği (0.25 altı tahminleri filtreler)
        results = self.model(self.image_path, conf=0.25)

        # YOLO bir liste döndürür (batch gibi düşün). Biz tek resim verdik: results[0]
        result = results[0]

        # ============================
        # 4.2) TESPİT SAYIMI
        # ============================
        ayakkabi = 0
        bot = 0

        # result.boxes.cls => tespit edilen her kutu için sınıf id listesi
        # Örn: [0,0,1] => 2 ayakkabi, 1 bot
        for cls_id in result.boxes.cls.tolist():
            if int(cls_id) == 0:
                ayakkabi += 1
            elif int(cls_id) == 1:
                bot += 1

        # GUI'de sayım label'ını güncelle
        self.count_label.setText(f"Ayakkabi: {ayakkabi} | Bot: {bot}")

        # ============================
        # 4.3) BOUNDING BOX ÇİZİMİ
        # ============================
        # result.plot() => kutuları ve sınıf etiketlerini çizilmiş şekilde görüntüyü üretir
        # Bu görüntü numpy array olarak gelir (OpenCV formatına yakın)
        plotted_img = result.plot()

        # OpenCV genelde BGR kullanır, Qt göstermek için RGB daha uygundur
        plotted_img = cv2.cvtColor(plotted_img, cv2.COLOR_BGR2RGB)

        # ============================
        # 4.4) NUMPY -> QIMAGE -> QPIXMAP
        # ============================
        h, w, ch = plotted_img.shape
        bytes_per_line = ch * w  # bir satırdaki byte sayısı

        # QImage: ham pixel verisini Qt görüntüsüne çevirir
        q_img = QImage(
            plotted_img.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        # QPixmap'e çevir, label'a koy
        pixmap = QPixmap.fromImage(q_img)
        self.tagged_label.setPixmap(
            pixmap.scaled(
                self.tagged_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        # Kaydetme işlemi için son çizilmiş görseli sakla
        self.last_result_image = plotted_img

    def save_image(self):
        """
        Tagged (kutu çizilmiş) görüntüyü dosyaya kaydeder.
        last_result_image yoksa (yani Test Image hiç yapılmadıysa) kaydetmez.
        """

        # Eğer henüz test edilmemişse kaydedilecek görüntü yok
        if not hasattr(self, "last_result_image"):
            return

        # Kullanıcıdan kayıt yeri ve adı al
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG (*.png);;JPG (*.jpg)"
        )

        # Eğer kullanıcı bir yol seçtiyse kaydet
        if save_path:
            # OpenCV BGR kaydettiği için tekrar RGB -> BGR çeviriyoruz
            cv2.imwrite(
                save_path,
                cv2.cvtColor(self.last_result_image, cv2.COLOR_RGB2BGR)
            )

    # =============================
    # 5) STİL FONKSİYONLARI
    # =============================

    def button_style(self):
        """
        Butonların görünümünü CSS benzeri Qt stylesheet ile belirliyoruz.
        """
        return """
        QPushButton {
            background-color: #238636;   /* normal durum */
            color: white;
            font-size: 15px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #2ea043;   /* üzerine gelince */
        }
        """

    def image_style(self):
        """
        Resim panellerinin görünümü.
        Kenarlık, yazı rengi, köşe oval vs.
        """
        return """
        QLabel {
            border: 2px dashed #30363d;
            border-radius: 10px;
            color: #8b949e;
            font-size: 16px;
        }
        """

# =============================
# 6) UYGULAMAYI ÇALIŞTIRMA
# =============================

if __name__ == "__main__":
    # QApplication: Qt uygulamasının kendisi (event loop burada döner)
    app = QApplication(sys.argv)

    # Ana pencereyi oluştur
    window = YOLOGui()

    # Pencereyi göster
    window.show()

    # Qt event loop'u başlat (uygulama burada çalışır)
    # Pencere kapanınca sys.exit ile programı düzgün kapatır
    sys.exit(app.exec_())
