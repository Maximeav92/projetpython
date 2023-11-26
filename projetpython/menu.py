import tkinter
fenetre = tkinter.Tk()
menu = tkinter.Menu(fenetre)
menu_fichier = tkinter.Menu(menu)
menu_edition = tkinter.Menu(menu)
menu.add_cascade(label="Fonctionnalités", menu = menu_fichier)
fenetre.config(menu= menu)
fenetre.mainloop()