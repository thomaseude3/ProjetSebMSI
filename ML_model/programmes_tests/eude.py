from ultralytics import YOLO
import cv2
import shutil

# load a pretrained YOLOv8n model
model = YOLO("../models/best (1).pt", "v8")

image1 = "produit1.png"
image2 = "produit2.png"
nouveau_dossier = '../../acquisition_image/yolo_frames/'


detection_output1 = model.predict(source=image1, conf=0.25, save=True, project="../../")
detection_output2 = model.predict(source=image2, conf=0.25, save=True, project="../../")

# Display tensor array
#print(detection_output)

path1 = "../../predict/produit1.png"
path2 = "../../predict2/produit2.png"


# Déplacer l'image vers le nouveau dossier
shutil.move(path1, nouveau_dossier + "image_analysee1.png")
shutil.move(path2, nouveau_dossier + "image_analysee2.png")


# Supprimer le dossier "predict"
shutil.rmtree("../../predict")
shutil.rmtree("../../predict2")