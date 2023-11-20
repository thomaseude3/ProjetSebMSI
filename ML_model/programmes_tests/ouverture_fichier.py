import torch

# Spécifiez le chemin du fichier .pt
chemin_fichier_pt = "best.pt"

# Chargez le dictionnaire
dictionnaire = torch.load(chemin_fichier_pt)

# Imprimez les clés du dictionnaire
print("Clés du dictionnaire :", dictionnaire.keys())

# Extrait le modèle du dictionnaire (remplacez 'modele' par la clé réelle dans votre dictionnaire)
modele = dictionnaire['model']

# Convertissez le modèle en virgule flottante 32 bits
modele = modele.float()

# Remplacez cette ligne avec vos propres données d'entrée
vos_donnees_d_entree = torch.randn(1, 3, 224, 224).float()

# Utilisez le modèle pour effectuer une prédiction
resultat = modele(vos_donnees_d_entree)

# Imprimez le résultat (ajustez en fonction de la sortie de votre modèle)
print("Résultat de la prédiction :", resultat)

