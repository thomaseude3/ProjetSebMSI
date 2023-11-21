from ultralytics import YOLO
import os

# Charger le modèle
model = YOLO("../models/best (1).pt", "v8")

# Chemin du dossier contenant les images à tester
images_folder_path = "../../images_ia"

# Résultats de détection pour chaque image
detection_results = []

# Liste des chemins vers les images à tester
image_paths = [os.path.join(images_folder_path, image_file) for image_file in os.listdir(images_folder_path)]

# Effectuer la détection pour chaque image
for i, path in enumerate(image_paths):
    # Prédire sur une image
    detection_output = model.predict(source=path, conf=0.50, save=True, project=f"../predict_{i+1}")
    detection_results.append(detection_output)

# Comparaison des classes détectées pour chaque image avec un seuil de confiance < 0.5
for i, result in enumerate(detection_results):
    print(f"Résultats pour l'image {i + 1}:")
    classes_detected = []
    for detection in result:
        boxes = detection.boxes
        confs = boxes.data[:, 4:6]  # Confiance et ID de classe des objets détectés

        # Filtrer les prédictions avec un seuil de confiance inférieur à 0.5
        filtered_classes = [int(confs[j, 1]) for j in range(len(confs)) if confs[j, 0] < 0.5]
        classes_detected.extend(filtered_classes)

    unique_classes_detected = list(set(classes_detected))  # Supprimer les doublons

    print(f"Classes détectées avec seuil de confiance < 0.5 : {unique_classes_detected}")
