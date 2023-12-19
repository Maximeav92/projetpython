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
'''print(files_names)'''


def extraire_noms_presidents(fichier):
    parties = fichier.split("_")
    a = parties[1]
    parties = a.split(".")
    nom_president = parties[0]
    for i in nom_president:
        if i.isdigit() == True:
            nom_president = nom_president[0:-1]
    return nom_president
'''print(extraire_noms_presidents("Nomination_Chirac1.txt"))'''


def associer_prenom(str):
    if str == 'Macron':
        return 'Emmanuel'
    elif str == 'Sarkozy' or 'Hollande' or 'Mitterand':
        return 'François'
    elif str == 'Chirac':
        return 'Jacques'
    elif str == 'Giscard dEstaing':
        return 'Valery'
    else:
        return 'non reconnu'
'''print(associer_prenom('Macron'))'''


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
'''print(liste_presidents())'''


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

# Écrire une fonction qui prend en paramètre une chaine de caractères et qui retourne un dictionnaire associant à chaque mot le nombre de fois qu’il apparait dans la chaine de caractères.
def TF(chaine):
    occurrences = {}
    mots = chaine.split()
    for mot in mots:
        occurrences[mot] = occurrences.get(mot, 0) + 1
    return occurrences
'''print(TF('Bonjour mot mot comment ca va'))'''


# Écrire une fonction qui prend en paramètre le répertoire où se trouve l’ensemble des fichiers du corpus et qui retourne un dictionnaire associant à chaque mot son score IDF.
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
    score_idf = {mot: math.log10(nbfichiers / occurrences) for mot, occurrences in fichier_mot.items()}
    return score_idf
'''print(IDF('cleaned'))'''


# Écrire une fonction qui prend en paramètre le répertoire où se trouvent les fichiers à analyser et qui retourne au minimum la matrice TF-IDF.
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
        vecteur_tfidf = [scores_tf_fichiers.get(mot, 0) * scores_idf.get(mot, 0) for mot in scores_idf]
        vecteurs_tfidf_fichiers.append(vecteur_tfidf)
    return vecteurs_tfidf_fichiers
'''resultat_tfidf = (TFIDF('cleaned'))
for vecteur_tfidf in resultat_tfidf:
    print(vecteur_tfidf)'''


# Afficher la liste des mots les moins importants dans le corpus de documents
def mots_score_tfidf_nul(repertoire):
    scores_idf = IDF(repertoire)
    vecteurs_tfidf = TFIDF(repertoire)
    mots_uniques = set(mot for vecteur_tfidf in vecteurs_tfidf for mot, score_tfidf in zip(scores_idf, vecteur_tfidf) if score_tfidf == 0)
    return list(mots_uniques)
'''print(mots_score_tfidf_nul('cleaned'))'''


# Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé
def mots_max_tfidf(repertoire):
    scores_idf = IDF(repertoire)
    vecteurs_tfidf = TFIDF(repertoire)
    mots_uniques = list(scores_idf.keys())
    index_max_tfidf = [max(range(len(mots_uniques)), key=lambda i: vecteur_tfidf[i]) for vecteur_tfidf in vecteurs_tfidf]
    mots_max_tfidf = [mots_uniques[i] for i in index_max_tfidf]
    return mots_max_tfidf
'''print(mots_max_tfidf("cleaned"))'''


# Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac
def mots_max_Chirac(repertoire):
    mots_max = []
    mots_non_importants = mots_score_tfidf_nul(repertoire)
    contenu_total = ''
    fichiers = ['Nomination_Chirac1.txt_min.txt', 'Nomination_Chirac2.txt_min.txt']
    for fichier in fichiers:
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            contenu_total += contenu
    occurences = TF(contenu_total)
    max_occurences = max(occurences.values())
    for mot in occurences:
        if (occurences.get(mot) == max_occurences) and (occurences.get(mot) not in mots_non_importants):
            mots_max.append(mot)
    return mots_max
'''print(mots_max_Chirac("cleaned"))'''


# Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois
def nation(repertoire, mot_recherche):
    noms_president = []
    fichiers = os.listdir(repertoire)
    for fichier in fichiers:
        president = extraire_noms_presidents(fichier)
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            mots_uniques = set(contenu.split())
            for mot in mots_uniques:
                if mot == mot_recherche:
                    noms_president.append(president)
    # celui qui l'a répété le plus
    president_max = []
    occurences_max = 0
    for fichier in fichiers:
        president = extraire_noms_presidents(fichier)
        if president in noms_president:
            chemin_fichier = os.path.join(repertoire, fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                if mot_recherche in contenu :
                    occurences = TF(contenu)
                    occurences_mot = occurences.get(mot_recherche)
                    if occurences_mot is not None and occurences_mot > occurences_max:
                        occurences_max = occurences_mot
                        president_max = [president]
                    elif occurences_mot is not None and occurences_mot == occurences_max:
                        president_max.append(president)
    return list(set(noms_president)), president_max
'''print(nation('cleaned', 'nation'))'''


# Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé du climat et/ou de l’écologie
def climat(repertoire):
    noms_president = []
    fichiers = os.listdir(repertoire)
    for fichier in fichiers:
        president = extraire_noms_presidents(fichier)
        chemin_fichier = os.path.join(repertoire, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            mots_uniques = set(contenu.split())
            for mot in mots_uniques:
                if mot == ('climat' or 'écologie'):
                    noms_president.append(president)
    return list(set(noms_president))
'''print(climat('cleaned'))'''


# Partie 2

# Écrire une fonction qui prend en paramètre le texte de la question, et qui retourne la liste des mots qui composent la question.
def tokenisation(ch):
    ch_min = ch.lower()
    ch_final = ch_min.replace("'", ' ')
    ch_final = ch_final.replace('-', ' ')
    res = "".join([i for i in ch_final if i not in string.punctuation])
    mots = res.split()
    return mots
'''print(tokenisation('Bonjour, comment ça va?'))'''


# Écrire une fonction qui permet d’identifier les termes de la question qui sont également présents dans le corpus de documents.
def identification(question, repertoire):
    mot_identifies = []
    liste_mots = tokenisation(question)
    fichiers = os.listdir(repertoire)
    for mot in liste_mots:
        for fichier in fichiers:
            chemin_fichier = os.path.join(repertoire, fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                mots_texte = set(contenu.split())
                for mot_texte in mots_texte:
                    if (mot == mot_texte) and (mot not in mot_identifies):
                        mot_identifies.append(mot)
    return mot_identifies
'''print(identification('Bonjour, comment ça va ?','cleaned'))'''


# Calcul du vecteur TF-IDF pour les termes de la question
def tf_idf_question(question, repertoire):
    mots_question = tokenisation(question)
    mots_corpus = []
    for mot in IDF(repertoire):
        mots_corpus.append(mot)
    vecteur_tf_idf = [0] * len(mots_question)
    taille_question = len(mots_question)
    idf_mots = dict(IDF(repertoire))
    # Parcours de chaque mot de la question
    for i in range(taille_question):
        mot_question = mots_question[i]
        occurrences_mot = 0
        idf = 0
        # Vérification si le mot de la question est présent dans le dictionnaire des scores IDF
        if mot_question in idf_mots:
            idf = idf_mots[mot_question]
        else :
            idf = 0
        # Calcul l'occurrence de chaque mot dans la phrase
        for mot_corpus in mots_corpus:
            if mot_corpus == mot_question:
                occurrences_mot += 1
        '''print(f"Mot: {mot_question}, TF: {occurrences_mot}, IDF: {idf}")'''
        # Si des occurrences du mot ont été trouvées, calculer le score TF-IDF
        if occurrences_mot > 0 and idf > 0:
            vecteur_tf_idf[i] = idf * occurrences_mot
            '''print(f"Vecteur TF-IDF: {vecteur_tf_idf[i]}")'''
        else :
            vecteur_tf_idf[i] = 0
            '''print(f"Vecteur TF-IDF: {vecteur_tf_idf[i]}")'''
    return vecteur_tf_idf
'''print(tf_idf_question('Bonjour, comment ça va ?','cleaned'))'''


# Le produit scalaire :
def produit_scalaire(vecteur1, vecteur2):
    if len(vecteur1) != len(vecteur2):
        return ValueError("Les vecteurs doivent avoir la même dimension")
    resultat = sum(x * y for x, y in zip(vecteur1, vecteur2))
    return resultat
'''print(produit_scalaire([1, 2, 3], [4, 5, 6]))'''


# La norme d’un vecteur :
def norme_vecteur(vecteur):
    somme_carres = sum(x**2 for x in vecteur)
    norme = math.sqrt(somme_carres)
    return norme
'''print(norme_vecteur([3, 4]))'''


#Calcul de la similarité :
def similarite(vecteur_a, vecteur_b):
    produit = produit_scalaire(vecteur_a, vecteur_b)
    norme_a = norme_vecteur(vecteur_a)
    norme_b = norme_vecteur(vecteur_b)
    if norme_a == 0 or norme_b == 0:
        return 0
    return produit / (norme_a * norme_b)
'''print(similarite([1, 2, 3], [4, 5, 6]))'''


# Calcul du document le plus pertinent
def pertinence(matrice_tfidf_corpus, vecteur_tfidf_question, liste_fichiers):
    similarite_max = 0
    fichier_max = ""
    for i in range (len(matrice_tfidf_corpus)):
        fichier = liste_fichiers[i]
        vecteur_fichier = matrice_tfidf_corpus[i]
        similarite_vecteurs = similarite(vecteur_tfidf_question, vecteur_fichier)
        if similarite_vecteurs > similarite_max:
            similarite_max = similarite_vecteurs
            fichier_max = liste_fichiers[i]
    return fichier_max

#changer rep fichier
matrice = IDF('cleaned')
vecteur = tf_idf_question('Bonjour, comment ça va ?','cleaned')
liste_fichiers = list_of_files('./cleaned', 'txt')
print(pertinence(matrice, vecteur, liste_fichiers))
















