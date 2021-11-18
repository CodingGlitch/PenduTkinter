#-*- coding: utf-8 -*-
from random import randint
import tkinter as tk

#Vous allez voir beaucoup de self.<variable>. C'est parce que j'utilise une classe. C'est plus simple après pour le côté graphique

class Pendu : #Ne vous embêter pas avec une classe. C'est juste pour le côté graphique.
    def __init__(self) :
        self.essaies = 10 #Le nombre d'essaies restant

        file = open("words.txt", 'r', encoding='UTF-8') # On ouvre le fichier contenant les mots avec l'encodage UTF-8, sinon c'est pas bon

        self.mots = [] #La liste des mots

        for i in file :
            self.mots.append(i.rstrip()) #On rajoute chaque mots dans le fichier directement dans la liste (après avoir retiré les \n)

        file.close() #On ferme le fichier car on a finit

        self.motC = self.mots[randint(0, len(self.mots)-1)] #On choisit un mot aléatoire
        self.lettresTrouves = [] #La liste pour les lettres trouvées
        
        #SAUTER CETTE PARTIE !!!! C'est le code graphique.
        self.win = False
        self.root = tk.Tk()
        self.root.title("Pendu")
        self.root.geometry("325x500")
        self.root.grid()
        self.root.bind('<Return>', self.penduTick)

        self.canvas = tk.Canvas(self.root, width = 300, height = 300, background='white')
        self.canvas.grid(column = 0, row = 0, columnspan = 2, padx = 10, pady = 10)

        self.guessEntry = tk.Entry(self.root)
        self.guessEntry.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

        self.entryButton = tk.Button(self.root, text = "Enter", command = self.penduTick)
        self.entryButton.grid(column=1, row=2, padx = 10, pady = 5)

        self.restartButton = tk.Button(self.root, text = "Restart", command = self.restart)
        self.restartButton.grid(column = 1, row = 3, padx=10, pady=5)

        self.wordLabel = tk.Label(self.root, text = "", font = ("Arial", 15))
        self.wordLabel.grid(column = 0, row = 1, columnspan = 2, padx = 10, pady = 10, sticky = "NS")

        self.triesLabel = tk.Label(self.root, text = "")
        self.triesLabel.grid(column = 0, row = 3, padx = 10, pady = 10)

        self.congratsLabel = tk.Label(self.root, text = "")
        self.congratsLabel.grid(column = 0, row = 4, padx = 10, pady = 10)

    def restart(self) : #On démarre une nouvelle partie
        self.win = False #Comme on démarre une nouvelle partie, le joueur n'a pas encore gagné
        
        #On choisit un nouveau mot (qui ne correspond pas au mot précédent)
        i = randint(0, len(self.mots)-1) 
        while self.motC == self.mots[i] :
            i = randint(0, len(self.mots)-1)
        self.motC = self.mots[i]
        
        #On remet tout les paramètres de la partie à 0 : les lettres trouvées, le nombre d'essais restant, le dessin du pendu...
        self.lettresTrouves = []
        self.essaies = 10
        self.canvas.delete('all')
        self.wordLabel.configure(text = " _ "*(len(self.motC)))
        self.triesLabel.configure(text = "You have 10 tries left")
        self.congratsLabel.configure(text = "")
        self.root.update_idletasks()

    def penduTick(self, event = None) : #Le code principale quand on clique sur le boutton Entrée

        if self.essaies > 0 and not self.win: #Si on a encore des essaies et qu'on n'a pas encore gagné
            
            #On récupère ce que le joueur à entrée
            self.congratsLabel.configure(text = "")
            guess = self.guessEntry.get()
            self.guessEntry.delete(0, len(guess))
            if len(guess) != 1 :
                guess = ""
                self.congratsLabel.configure(text = "Input only 1 character")
            for c in guess.lower() : #On vérifie si la lettre correspond à une lettre du mot (les lettres qui correspondent ne font pas perdre d'essaies)
                #On peut rentré plusieurs lettres d'un coup: si le joueur rentre "abcdefg", sa va regarder pour toutes ces lettre si elle est dans le mot.
                #On perd aussi plus d'essaies si on met plein de lettres qui ne sont pas dans le mot.
                if c in self.motC.lower() :
                    if c not in self.lettresTrouves : #Si la lettre est dans le mot, 
                        self.lettresTrouves.append(c)
                else : 
                    self.essaies -= 1 #Mauvaise lettre ? Un essaie en moins et on dessine le pendu un peu plus
                    self.drawNext()
                    
                if self.essaies > 0 : #Si on a encore des essaies (donc on peut pas tricher en mettant toutes les lettres de l'alphabet d'un coup)
                    complete = True #On vérifie si le mot est complété par le joueur
                    for c in self.motC.lower() :
                        if c not in self.lettresTrouves :
                            complete = False #Si le mot ne l'est pas, on continue

                    if complete : #Si le mot est complété, alors on annonce la victoire du joueur.
                        self.win = True
                        self.congratsLabel.configure(text = "You won !")
                        break
            
            
            #C'est juste pour mettre à jour l'interface graphique
            #Pour le mot, on l'affiche avec des "_" pour les lettres inconnues
            newText = ""
            for i in self.motC :
                if i.lower() in self.lettresTrouves : #Si la lettre du mot est connue
                    newText += i #Alors on l'affiche directement
                else :
                    newText += " _ " #Sinon on affiche un "_"
            
            #Ici on met à jour le texte. Considéré ça comme des prints versions graphiques
            self.wordLabel.configure(text = newText)
            
            if self.essaies <= 0 :
                self.wordLabel.configure(text = self.motC)
                self.congratsLabel.configure(text = "You lost...")
            
            self.triesLabel.configure(text = "You have " + str(self.essaies) + " tries left")
            self.root.update_idletasks()

    def start(self) : #Ne vous intéressez pas à cette fonction
        self.restart()
        self.root.mainloop()

    def drawNext(self):
        #Commentaire anglais pour ceux qui comprennent
        #On dessine le pendu en fonction du nombre d'essaies restants.
        #Ne restez pas plantez ici à essayez de comprendre, je l'ai fait trop rapidement pour le faire de manière compréhensible
        #Time for a LOT of specific drawing calls
        self.canvas.delete('all')
        if self.essaies < 10 :
            self.canvas.create_line(10, 290, 280, 290, width=10)
        if self.essaies < 9 :
            self.canvas.create_line(30, 290, 30, 40, width=10)
        if self.essaies < 8 :
            self.canvas.create_line(30, 45, 200, 45, width=8)
        if self.essaies < 7 :
            self.canvas.create_line(180, 45, 180, 120, width=8)
        if self.essaies < 6 :
            self.canvas.create_oval(170, 120, 190, 140, width=4)
        if self.essaies < 5 :
            self.canvas.create_line(180, 140, 180, 200, width=4)
        if self.essaies < 4 :
            self.canvas.create_line(180, 200, 160, 240, width=4)
        if self.essaies < 3 :
            self.canvas.create_line(180, 200, 200, 240, width=4)
        if self.essaies < 2 :
            self.canvas.create_line(180, 150, 160, 190, width=4)
        if self.essaies < 1 :
            self.canvas.create_line(180, 150, 200, 190, width=4)
            
            



#Graphical stuff with tkinter
#Et ici on lance le jeu. Oui c'est ici qu'il se lance. C'est pas avant.
#Le code qu'il y a avant c'est juste pour pouvoir faire l'initialisation graphique et me faciliter la vie
#Pour tout ce qui est dessin à l'écran. C'était soit ça, soit un code qui fait 30-40 lignes de plus pour rien.
pendu = Pendu()
pendu.start()

