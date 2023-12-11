from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QLabel, QDialog
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen
import sys
from IHM.deuxième_page import ImageReviewPage
from IHM.troisième_page import ImageDifferencePage
from pypylon import pylon
import os
import cv2


def show_difference_page(image_path, positions, scores, different_words):
    difference_page = ImageDifferencePage(image_path, positions, scores, different_words)
    difference_page.exec()


class ImageCaptureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Capture d'Images")
        self.setGeometry(100, 100, 800, 400)

        self.capture_label_button = QPushButton("Capturer l'étiquette")
        self.capture_label_button.clicked.connect(self.start_countdown_label)

        self.capture_product_button = QPushButton("Capturer le produit")
        self.capture_product_button.clicked.connect(self.start_countdown_product)

        # Créez un layout vertical pour les boutons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.capture_label_button)
        button_layout.addWidget(self.capture_product_button)

        self.image_label = QLabel(self)  # QLabel pour afficher le flux vidéo
        self.image_label.setFixedSize(800, 600)

        self.camera = pylon.InstantCamera()
        self.camera.Attach(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)
        self.timer.start(50)  # Mettre à jour l'affichage toutes les 100 ms

        self.show()

        # Créez un layout horizontal pour les boutons et l'image
        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_label)

        self.setLayout(main_layout)

        self.product_captured = False
        self.label_captured = False

        self.timer_label = QTimer(self)
        self.timer_label.timeout.connect(self.update_countdown_label)
        self.countdown_label = 0

        self.timer_product = QTimer(self)
        self.timer_product.timeout.connect(self.update_countdown_product)
        self.countdown_product = 0

        self.capture_state = "live"  # Initial state is live

    def update_video(self):
        if self.camera.IsOpen():  # Vérifiez si la caméra est encore ouverte
            grab = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            if grab.GrabSucceeded():
                image = grab.Array

                height, width = image.shape
                bytes_per_line = 1 * width

                # Convertir l'image en format QImage
                image_qt = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

                # Afficher l'image dans le QLabel en ajustant son échelle pour s'adapter à la taille du QLabel
                pixmap = QPixmap.fromImage(image_qt)

                # Ajouter un rectangle rouge au milieu de l'image
                painter = QPainter()
                painter.begin(pixmap)
                painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine))

                # Calculez les coordonnées du coin supérieur gauche du rectangle au milieu
                center_x = width // 2
                center_y = height // 2
                rect_size = 500  # Ajustez la taille du rectangle selon vos besoins

                top_left_x = center_x - (rect_size // 2)
                top_left_y = center_y - (rect_size // 2)

                painter.drawRect(top_left_x, top_left_y, rect_size, rect_size)

                painter.end()

                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
                self.image_label.setScaledContents(True)

            grab.Release()
        else:
            self.camera = pylon.InstantCamera()
            self.camera.Attach(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.camera.Open()
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            grab = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            if grab.GrabSucceeded():
                image = grab.Array

                height, width = image.shape
                bytes_per_line = 1 * width

                # Convertir l'image en format QImage
                image_qt = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

                # Afficher l'image dans le QLabel en ajustant son échelle pour s'adapter à la taille du QLabel
                pixmap = QPixmap.fromImage(image_qt)

                # Ajouter un rectangle rouge au milieu de l'image
                painter = QPainter()
                painter.begin(pixmap)
                painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine))

                # Calculez les coordonnées du coin supérieur gauche du rectangle au milieu
                center_x = width // 2
                center_y = height // 2
                longueur = 700  # Ajustez la taille du rectangle selon vos besoins
                largeur = 500

                top_left_x = center_x - (longueur // 2)
                top_left_y = center_y - (largeur // 2)

                painter.drawRect(top_left_x, top_left_y, longueur, largeur)

                painter.end()

                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
                self.image_label.setScaledContents(True)

            grab.Release()

    def start_countdown_label(self):
        if self.capture_state == "live":
            self.capture_state = "label"  # Switch to label capture mode
            self.countdown_label = 3  # Set the initial countdown value
            self.timer_label.start(1000)  # Start the timer with a 1-second interval
        else:
            # Handle the case when already in label capture mode
            pass

    def start_countdown_product(self):
        if self.capture_state == "live":
            self.capture_state = "product"  # Switch to label capture mode
            self.countdown_product = 3  # Set the initial countdown value
            self.timer_product.start(1000)  # Start the timer with a 1-second interval
        else:
            # Handle the case when already in label capture mode
            pass

    def update_countdown_label(self):
        if self.countdown_label > 0:
            self.countdown_label -= 1
            self.capture_label_button.setText(f"Prise d'image dans {self.countdown_label}s")
        else:
            self.timer_label.stop()
            self.capture_label_button.setText("Autre prise d'image de l'étiquette")
            self.basler_etiquette()
            self.capture_state = "live"

    def update_countdown_product(self):
        if self.countdown_product > 0:
            self.countdown_product -= 1
            self.capture_product_button.setText(f"Prise d'image dans {self.countdown_product}s")
        else:
            self.timer_product.stop()
            self.capture_product_button.setText("Autre prise d'image du produit")
            self.basler_produit()
            self.capture_state = "live"

    def show_image_review_page(self, image1, image2):
        review_page = ImageReviewPage(image1, image2)
        review_page.exec()
        # Ici, vous pouvez ajouter un code pour revenir à la première page après la fermeture de la deuxième page
        if review_page.result() == QDialog.DialogCode.Accepted:
            # Si l'utilisateur a accepté, vous pouvez revenir à la première page
            self.show()

    def basler_produit(self):
        grab = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
        image_folder = "acquisition_image"
        if grab.GrabSucceeded():
            image = grab.Array
            height, width = image.shape
            center_x = width // 2
            center_y = height // 2
            crop_size = 1500  # Taille du rectangle central en pixels (ajustez selon vos besoins)

            # Calculez les coordonnées du coin supérieur gauche du rectangle
            top_left_x = center_x - (crop_size // 2)
            top_left_y = center_y - (crop_size // 2)

            # Recadrez l'image au milieu
            cropped_image = image[top_left_y:top_left_y + crop_size, top_left_x:top_left_x + crop_size]

            # Enregistrez l'image sous format PNG en utilisant OpenCV
            image_path = os.path.join(image_folder, "produit_basler.png")
            #cv2.imwrite(image_path, cropped_image)
            cv2.imwrite(image_path, image)

            self.product_captured = True

            if self.label_captured and self.product_captured:
                self.show_image_review_page("etiquette_basler.png", "produit_basler.png")

                grab.Release()
                self.camera.Close()

    def basler_etiquette(self):
        grab = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
        image_folder = "acquisition_image"
        if grab.GrabSucceeded():
            image = grab.Array

            # Ajoutez l'impression de la forme de l'image
            print("Shape de l'image :", image.shape)

            height, width = image.shape
            center_x = width // 2
            center_y = height // 2
            crop_size = 1500  # Taille du rectangle central en pixels (ajustez selon vos besoins)

            # Calculez les coordonnées du coin supérieur gauche du rectangle
            top_left_x = center_x - (crop_size // 2)
            top_left_y = center_y - (crop_size // 2)

            # Recadrez l'image au milieu
            cropped_image = image[top_left_y:top_left_y + crop_size, top_left_x:top_left_x + crop_size]

            # Enregistrez l'image sous format PNG en utilisant OpenCV
            image_path = os.path.join(image_folder, "etiquette_basler.png")
            # cv2.imwrite(image_path, cropped_image)
            cv2.imwrite(image_path, image)

            self.label_captured = True

        if self.label_captured and self.product_captured:
            self.show_image_review_page("etiquette_basler.png", "produit_basler.png")

            grab.Release()
            self.camera.Close()
