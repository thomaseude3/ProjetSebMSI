import cv2
from pypylon import pylon
from ultralytics import YOLO

# Charger le modèle YOLO pré-entraîné
model = YOLO("best.pt", "v8")

# Connexion à la première caméra trouvée
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# Configuration de la caméra
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Taille arbitraire pour la redimensionnement
target_height, target_width = 416, 416

# Boucle de capture et de prédiction
while True:
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        # Récupérer l'image et la redimensionner
        image = cv2.resize(grabResult.Array, (target_width, target_height))

        # Prédiction sur l'image redimensionnée
        detection_output = model.predict(source=image, conf=0.25, save=True)
        print(detection_output)  # Afficher les prédictions
    grabResult.Release()
