from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QLabel
from PyQt6.QtGui import QImage, QPixmap
import sys
from acquisition_image.capture_image import ImageCapture
from IHM.video_direct import CameraManager
from IHM.deuxième_page import ImageReviewPage
from IHM.troisième_page import ImageDifferencePage


def show_difference_page(image_path, positions, scores, different_words):
    difference_page = ImageDifferencePage(image_path, positions, scores, different_words)
    difference_page.exec()


class ImageCaptureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Capture d'Images")
        self.setGeometry(100, 100, 600, 300)

        self.capture_label_button = QPushButton("Capturer l'étiquette")
        self.capture_label_button.clicked.connect(self.start_countdown_label)

        self.capture_product_button = QPushButton("Capturer le produit")
        self.capture_product_button.clicked.connect(self.start_countdown_product)

        # Créez un layout vertical pour les boutons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.capture_label_button)
        button_layout.addWidget(self.capture_product_button)

        self.image_label = QLabel(self)  # QLabel pour afficher le flux vidéo
        self.image_capture = ImageCapture()

        # Créez un layout horizontal pour les boutons et l'image
        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_label)

        self.setLayout(main_layout)

        # Créez une instance de CameraManager
        self.camera_manager = CameraManager()
        self.camera_manager.frame_signal.connect(self.update_image_label)

        # Démarrez le thread de la caméra
        self.camera_manager.start()

        self.timer_label = QTimer(self)
        self.timer_label.timeout.connect(self.update_countdown_label)
        self.countdown_label = 0

        self.timer_product = QTimer(self)
        self.timer_product.timeout.connect(self.update_countdown_product)
        self.countdown_product = 0

    def update_image_label(self, frame):
        image_bytearray = bytearray(frame)

        # Mettez à jour l'image en direct dans le QLabel
        self.image_label.setPixmap(QPixmap.fromImage(QImage.fromData(image_bytearray)))
        self.image_label.setScaledContents(True)

    def start_countdown_label(self):
        self.countdown_label = 3  # Set the initial countdown value
        self.timer_label.start(1000)  # Start the timer with a 1-second interval

    def start_countdown_product(self):
        self.countdown_product = 3  # Set the initial countdown value
        self.timer_product.start(1000)  # Start the timer with a 1-second interval

    def update_countdown_label(self):
        if self.countdown_label > 0:
            self.countdown_label -= 1
            self.capture_label_button.setText(f"Prise d'image dans {self.countdown_label}s")
        else:
            self.timer_label.stop()
            self.capture_label_button.setText("Autre prise d'image de l'étiquette")
            self.image_capture.basler_etiquette()

    def update_countdown_product(self):
        if self.countdown_product > 0:
            self.countdown_product -= 1
            self.capture_product_button.setText(f"Prise d'image dans {self.countdown_product}s")
        else:
            self.timer_product.stop()
            self.capture_product_button.setText("Autre prise d'image du produit")
            self.image_capture.basler_produit()

    def show_image_review_page(self, image1, image2):
        review_page = ImageReviewPage(image1, image2)
        review_page.exec()
        # Ici, vous pouvez ajouter un code pour revenir à la première page après la fermeture de la deuxième page
        if review_page.result() == QDialog.DialogCode.Accepted:
            # Si l'utilisateur a accepté, vous pouvez revenir à la première page
            self.show()