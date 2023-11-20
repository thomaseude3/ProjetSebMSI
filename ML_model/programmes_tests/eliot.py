import numpy
from ultralytics import YOLO
import os

# load a pretrained YOLOv8n model
model = YOLO('best.pt', "v8")

# spécifiez le chemin du dossier de sauvegarde
save_dir = "../../acquisition_image"

# assurez-vous que le dossier de sauvegarde existe
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# spécifiez le chemin complet pour l'enregistrement de l'image
image_name = "test_ml.png"
save_path = os.path.join(save_dir, image_name)

# prédisez sur une image et enregistrez les résultats
detection_output = model.predict(source=image_name, conf=0.25, save=True, save_dir=save_dir)

print("save_path:", save_path)

# affichez le tableau tensoriel
print(detection_output)

# affichez le tableau NumPy
print(detection_output[0].numpy())