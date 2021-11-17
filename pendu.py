#-*- coding: utf-8 -*-
from random import randint
import tkinter as tk


class Pendu :
    def __init__(self) :
        self.essaies = 10

        file = open("words.txt", 'r', encoding='UTF-8')

        self.mots = []

        for i in file :
            self.mots.append(i.rstrip())

        file.close()

        self.motC = self.mots[randint(0, len(self.mots)-1)]
        self.lettresTrouves = []

        self.win = False
        self.root = tk.Tk()
        self.root.title("Pendu")
        self.root.geometry("325x450")
        self.root.grid()

        self.canvas = tk.Canvas(self.root, width = 300, height = 300, background='white')
        self.canvas.grid(column = 0, row = 0, columnspan = 2, padx = 10, pady = 10)

        self.guessEntry = tk.Entry(self.root)
        self.guessEntry.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

        self.entryButton = tk.Button(self.root, text = "Enter", command = self.penduTick)
        self.entryButton.grid(column=1, row=2, padx = 10, pady = 10)

        self.restartButton = tk.Button(self.root, text = "Restart", command = self.restart)
        self.restartButton.grid(column = 1, row = 3, padx=10, pady=10)

        self.wordLabel = tk.Label(self.root, text = "")
        self.wordLabel.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.triesLabel = tk.Label(self.root, text = "")
        self.triesLabel.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.congratsLabel = tk.Label(self.root, text = "")
        self.congratsLabel.grid(column = 0, row = 3, padx = 10, pady = 10)

    def restart(self) :
        self.win = False
        
        i = randint(0, len(self.mots)-1)
        while self.motC == self.mots[i] :
            i = randint(0, len(self.mots)-1)
        self.motC = self.mots[i]
        
        self.lettresTrouves = []
        self.essaies = 10
        self.canvas.delete('all')
        self.wordLabel.configure(text = "_"*(len(self.motC)))
        self.triesLabel.configure(text = "You have 10 tries left")
        self.congratsLabel.configure(text = "")
        self.root.update_idletasks()

    def penduTick(self) :

        if self.essaies > 0 and not self.win:
            
            guess = self.guessEntry.get()
            self.guessEntry.delete(0, -1)
            
            for c in guess.lower() :
                if c in self.motC.lower() :
                    if c not in self.lettresTrouves :
                        self.lettresTrouves.append(c)
                else :
                    self.essaies -= 1
                    self.drawNext()
                    
                if self.essaies > 0 :
                    complete = True
                    for c in self.motC.lower() :
                        if c not in self.lettresTrouves :
                            complete = False

                    if complete :
                        self.win = True
                        self.congratsLabel.configure(text = "You won !")
                        break

            newText = ""
            for i in self.motC :
                if i.lower() in self.lettresTrouves :
                    newText += i
                else :
                    newText += "_"
            
            self.wordLabel.configure(text = newText)
            
            if self.essaies <= 0 :
                self.wordLabel.configure(text = self.motC)
                self.congratsLabel.configure(text = "You lost...")
            
            self.triesLabel.configure(text = "You have " + str(self.essaies) + " tries left")
            self.root.update_idletasks()

    def start(self) :
        self.restart()
        self.root.mainloop()

    def drawNext(self):
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

pendu = Pendu()
pendu.start()


