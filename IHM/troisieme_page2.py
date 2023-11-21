from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage

class Analyse_Review(QDialog):
    def __init__(self, image1_path, image2_path):
        super().__init__()

        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle("Analysed frames")

        layout = QVBoxLayout()

        # Chargez les images à partir des fichiers PNG
        self.pixmap1 = QPixmap(image1_path)
        self.pixmap2 = QPixmap(image2_path)

        # Créez des QLabel pour afficher les images
        self.label1 = QLabel()
        self.label2 = QLabel()

        # Redimensionnez les images pour qu'elles correspondent à la taille souhaitée
        scaled_pixmap1 = self.pixmap1.scaledToWidth(700)  # Ajustez la largeur selon vos besoins
        scaled_pixmap2 = self.pixmap2.scaledToWidth(700)  # Ajustez la largeur selon vos besoins

        # Affichez les images dans les QLabel
        self.label1.setPixmap(scaled_pixmap1)
        self.label2.setPixmap(scaled_pixmap2)

        # Créez un widget pour contenir les images côte à côte
        image_container = QWidget()
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.label1)
        image_layout.addWidget(self.label2)
        image_container.setLayout(image_layout)

        layout.addWidget(image_container)
        self.setLayout(layout)