'''import tkinter
fenetre = tkinter.Tk()
menu = tkinter.Menu(fenetre)
menu_fichier = tkinter.Menu(menu)
menu_edition = tkinter.Menu(menu)
menu.add_cascade(label="Fonctionnalités", menu = menu_fichier)
fenetre.config(menu= menu)
fenetre.mainloop()'''
import main

# Afficher la liste des mots les moins importants dans le corpus de documents.
print(main.mots_score_tfidf_nul('cleaned'))

# Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé
print(main.mots_max_tfidf('cleaned'))

# Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac hormis les mots dits « non importants »
print(main.mots_max_Chirac('cleaned'))

# Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois
print(main.nation('cleaned','nation'))

#Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé du climat et/ou de l’écologie
print(main.climat('cleaned'))