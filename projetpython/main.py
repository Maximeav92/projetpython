import os
import string
import math
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names
directory = "./speeches"
files_names = list_of_files(directory, "txt")
print(files_names)

def extraire_noms_presidents(fichier):
        parties = fichier.split("_")
        a = parties[1]
        parties = a.split(".")
        nom_president = parties[0]
        for i in nom_president:
            if i.isdigit() == True:
                nom_president = nom_president[0:-1]
        return nom_president
print(extraire_noms_presidents("Nomination_Chirac1.txt"))

def associer_prenom(str):
    if str == 'Macron':
        return 'Emmanuel'
    if str == 'Sarkozy' or 'Hollande' or 'Mitterand':
        return 'François'
    if str == 'Chirac':
        return 'Jacques'
    if str == 'Giscard dEstaing':
        return 'Valery'
    else:
        return 'non reconnu'
print(associer_prenom('Macron'))

def liste_presidents():
    fichiers = os.listdir("speeches")
    noms_presidents = set()
    for fichier in fichiers:
        parties = fichier.split("_")
        a = parties[1]
        parties = a.split(".")
        nom_president = parties[0]
        for i in nom_president:
            if i.isdigit() == True:
                nom_president = nom_president[0:-1]
        noms_presidents.add(nom_president)
    print("Noms des présidents :", list(noms_presidents))
print(liste_presidents())


'''dossier_cleaned = "cleaned"
os.mkdir(dossier_cleaned)'''
def minuscules():
    fichiers = os.listdir("speeches")
    for fichier in fichiers:
        with open(f'speeches/{fichier}', 'r', encoding='utf-8') as firstfile, open(f'cleaned/{fichier}_min.txt', 'w', encoding='utf-8') as secondfile:
            firstfile_min = firstfile.read().lower()
            secondfile.write(firstfile_min)
minuscules()

def ponctuation():
    fichiers_min = os.listdir("cleaned")
    for fichier_min in fichiers_min:
        with open(f'cleaned/{fichier_min}', 'r', encoding='utf-8') as f:
            texte = f.read()
            texte = texte.replace("'", ' ')
            texte = texte.replace('-', ' ')
            res = "".join([i for i in texte if i not in string.punctuation])
        with open(f'cleaned/{fichier_min}', 'w', encoding='utf-8') as f:
            f.write(res)
ponctuation()


#Écrire une fonction qui prend en paramètre une chaine de caractères et qui retourne un dictionnaire associant à chaque mot le nombre de fois qu’il apparait dans la chaine de caractères.
def TF(chaine):
    occurrences = {}
    mots = chaine.split()
    for mot in mots:
        occurrences[mot] = occurrences.get(mot, 0) + 1
    return occurrences
print(TF('Bonjour mot mot comment ca va'))


#Écrire une fonction qui prend en paramètre le répertoire où se trouve l’ensemble des fichiers du corpus et qui retourne un dictionnaire associant à chaque mot son score IDF.
def IDF(repertoire):
    fichiers = os.listdir(repertoire)
    nbfichiers = len(fichiers)
    fichier_mot = {}
    for fichier in fichiers:
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            mots_uniques = set(contenu.split())
            for mot in mots_uniques:
                fichier_mot[mot] = fichier_mot.get(mot, 0) + 1
    score_idf = {mot: math.log(nbfichiers / occurrences + 1) for mot, occurrences in fichier_mot.items()}
    return score_idf
print(IDF('cleaned'))


#Écrire une fonction qui prend en paramètre le répertoire où se trouvent les fichiers à analyser et qui retourne au minimum la matrice TF-IDF.
def TFIDF(repertoire):
    scores_tf_fichiers = {}
    scores_idf = IDF(repertoire)
    vecteurs_tfidf_fichiers = []
    fichiers = os.listdir(repertoire)
    for fichier in fichiers:
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            scores_tf_fichiers[fichier] = TF(contenu)
    for fichier, scores_tf_fichiers in scores_tf_fichiers.items():
        vecteur_tfidf = [scores_tf_fichiers.get(mot,0) * scores_idf.get(mot,0) for mot in scores_idf]
        vecteurs_tfidf_fichiers.append(vecteur_tfidf)
    return vecteurs_tfidf_fichiers
resultat_tfidf = (TFIDF('cleaned'))
for vecteur_tfidf in resultat_tfidf:
    print(vecteur_tfidf)


#calculer le score d'un mot
def mot_TFIDF(mot,repertoire):
    TF = 0
    dico_idf = IDF(repertoire)
    fichiers = os.listdir(repertoire)
    for fichier in fichiers:
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            mots_uniques = set(contenu.split())
            for mot_texte in mots_uniques:
                if mot_texte == mot:
                    TF = TF + 1
    score_tf = TF
    score_idf = dico_idf.get(mot)
    score_tfidf = score_tf * score_idf
    return score_tfidf
print(mot_TFIDF("france","cleaned"))


#Afficher la liste des mots les moins importants dans le corpus de documents
def mots_non_importants(repertoire):
    res = []
    scores_tf_fichiers = {}
    dico_idf = IDF(repertoire)
    fichiers = os.listdir(repertoire)
    for fichier in fichiers:
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            mots_uniques = set(contenu.split())
            for mot in mots_uniques:
                contenu = f.read()
                scores_tf_fichiers[fichier] = TF(contenu)
                score_idf = dico_idf.get(mot,0)
                score_tf = scores_tf_fichiers.get(mot,0)
                score_tfidf = score_tf * score_idf
                if score_tfidf == 0.0:
                    res.append(mot)
    return res
print(mots_non_importants('cleaned'))


#Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé
"""def mots_max_tfidf(repertoire):
    mots_max=[]
    matrice_tfidf = TFIDF(repertoire)
    score_max = max(matrice_tfidf)
    fichiers = os.listdir(repertoire)
    for fichier in fichiers:
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            mots_uniques = set(contenu.split())
            for mot in mots_uniques:
                score_mot = mot_TFIDF(mot,repertoire)
                if score_mot == score_max:
                    mots_max.append(mot)
    return mots_max
print(mots_max_tfidf("cleaned"))"""


#Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac
def mots_max_Chirac(repertoire):
    mots_max = []
    fichiers = ['Nomination_Chirac1.txt_min.txt', 'Nomination_Chirac2.txt_min.txt']
    for fichier in fichiers:
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            occurences = TF(contenu)
            max_occurence = occurences.get(max(occurences))
            mots_uniques = set(contenu.split())
            for mot in mots_uniques:
                if occurences.get(mot) == max_occurence:
                    mots_max.append(mot)
    return mots_max
print(mots_max_Chirac("cleaned"))


#Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois
def nation(repertoire):
    noms_president = []
    fichiers = os.listdir(repertoire)
    for fichier in fichiers:
        president = extraire_noms_presidents(fichier)
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            occurences = TF(contenu)
            mots_uniques = set(contenu.split())
            for mot in mots_uniques:
                if occurences.get(mot) == 'Nation' or 'nation':
                    noms_president.append(president)
                    break
    return noms_president
print(nation('speeches'))

















    























