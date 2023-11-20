from ultralytics import YOLO

# Charger le modèle
model = YOLO("../models/last (1).pt", "v8")

# Liste des chemins vers les images à tester
image_paths = [
    "../../acquisition_image/etiquette_basler_binarisee.png",
    "../../acquisition_image/produit_basler_binarise.png"
]

# Résultats de détection pour chaque image
detection_results = []

# Effectuer la détection pour chaque image
for path in image_paths:
    # Prédire sur une image
    detection_output = model.predict(source=path, conf=0.50, save=True, project="../../")
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