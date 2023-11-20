import torch

# Spécifiez le chemin du fichier .pt
chemin_fichier_pt = "best.pt"

# Chargez le dictionnaire
dictionnaire = torch.load(chemin_fichier_pt)

# Imprimez les clés du dictionnaire
print("Clés du dictionnaire :", dictionnaire.keys())

train_args = dictionnaire.get('train_args', {})  # Assurez-vous de gérer le cas où 'train_args' est absent

project_value = train_args['project']
print("Valeur de 'project' :", project_value)

# Exploration des clés et de leurs valeurs
for cle, valeur in dictionnaire.items():
    print(f"Clé : {cle}")

    # Si la valeur est elle-même un dictionnaire, explorez ses clés
    if isinstance(valeur, dict):
        print("  Sous-clés : ", valeur.keys())

    # Imprimez la valeur (ajustez en fonction du type de données)
    print("  Valeur :", valeur)
    print("\n")