import random

mots = ["homme", "femme","chien","atletico","madrid","voyage","element","anticonstitutionellement"]
vies = 10

mot_choisi = random.choice(mots)
def nb_lettres_mot(self):
    nb_lettres = len(mot_choisi)
    return nb_lettres


nb_de_lettres = nb_lettres_mot(mot_choisi)
print("Le mot", mot_choisi, "a", nb_de_lettres, "lettres")

def nombre_de___():
    for i in range(nb_de_lettres):
        print("_")

test=nombre_de___()
print(test)