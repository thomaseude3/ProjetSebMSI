from ultralytics import YOLO
import cv2
import shutil

def modele_yolo(image1, image2):
    # load a pretrained YOLOv8n model
    model = YOLO("../models/best (1).pt", "v8")

    nouveau_dossier = '../../acquisition_image/yolo_frames/'

    model.predict(source=image1, conf=0.25, save=True, project="../../")
    model.predict(source=image2, conf=0.25, save=True, project="../../")

    path1 = "../../predict/produit1.png"
    path2 = "../../predict2/produit2.png"

    # Déplacer l'image vers le nouveau dossier
    shutil.move(path1, nouveau_dossier + "etiquette_analysee.png")
    shutil.move(path2, nouveau_dossier + "produit_analyse.png")

    # Supprimer le dossier "predict"
    shutil.rmtree("../../predict")
    shutil.rmtree("../../predict2")
