import sys
import cv2
from pypylon import pylon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caméra Basler")
        self.setGeometry(100, 100, 800, 600)  # Ajustez les dimensions de la fenêtre ici

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(800, 600)  # Ajustez la taille du QLabel à la taille de la fenêtre

        self.capture_button = QPushButton("Prendre une photo")

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.capture_button)
        self.setLayout(layout)

        self.capture_button.clicked.connect(self.capture_image)

        self.camera = pylon.InstantCamera()
        self.camera.Attach(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)
        self.timer.start(100)  # Mettre à jour l'affichage toutes les 100 ms

        self.show()

    def update_video(self):
        grab = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
        if grab.GrabSucceeded():
            image = grab.Array

            height, width = image.shape
            bytes_per_line = 1 * width

            # Convertir l'image en format QImage
            image_qt = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

            # Afficher l'image dans le QLabel en ajustant son échelle pour s'adapter à la taille du QLabel
            pixmap = QPixmap.fromImage(image_qt)
            self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.video_label.setScaledContents(True)

        grab.Release()

    def capture_image(self):
        grab = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
        if grab.GrabSucceeded():
            image = grab.Array

            # Sauvegarder l'image capturée dans un fichier
            cv2.imwrite("captured_image.png", image)
            print("Image capturée")

        grab.Release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    sys.exit(app.exec())
