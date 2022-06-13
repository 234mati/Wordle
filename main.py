from faulthandler import disable
from turtle import color, width
from typing import Optional
import ReadingFile
import Node
import datetime
import random
import os
from timeit import default_timer as timer
import tkinter as tk
from tkinter import Button, Canvas, Frame, IntVar, Label, Toplevel, filedialog, Text
from tkinter import *  
'''
read = ReadingFile.ReadingFile()
configFile = read.getConfigFile()

minWordLength = int(configFile['base']['minWordLength'])
maxWordLength = int(configFile['base']['maxWordLength'])
treeDeep = int(configFile['base']['treeDeep'])
numberOfRounds = int(configFile['base']['numberOfRounds'])
'''

class Game():
    def __init__(self):
        self.wordLength = 5
        self.currentLetter = 0
        self.currentWordIndex = 0
        self.currentWord = ""
        self.colorInPlace = "#90EE90"
        self.colorKnown = "#F0E68C"
        self.colorOut = "#D3D3D3"
        self.colorLettersFrame  = "#E0FFFF"
        self.colorOptionFrame   = "#E0FFFF"
        self.colorWordsInPanel  = "#FFFAFA"
        self.roundHistory = []
        self.word = ""

        self.read = ReadingFile.ReadingFile()
        configFile = self.read.getConfigFile()

        self.minWordLength = int(configFile['base']['minWordLength'])
        self.maxWordLength = int(configFile['base']['maxWordLength'])
        self.treeDeep = int(configFile['base']['treeDeep'])
        self.numberOfRounds = int(configFile['base']['numberOfRounds'])
        self.dic = {
                 "ą":  "unknown",
                 "b":  "unknown",
                 "a":  "unknown",
                 "c":  "unknown",
                 "ć":  "unknown",
                 "d":  "unknown",
                 "e":  "unknown",
                 "ę":  "unknown",
                 "f":  "unknown",
                 "g":  "unknown",
                 "h":  "unknown",
                 "i":  "unknown",
                 "j":  "unknown",
                 "k":  "unknown",
                 "l":  "unknown",
                 "ł":  "unknown",
                 "m":  "unknown",
                 "n":  "unknown",
                 "ń":  "unknown",
                 "o":  "unknown",
                 "ó":  "unknown",
                 "p":  "unknown",
                 "r":  "unknown",
                 "s":  "unknown",
                 "ś":  "unknown",
                 "t":  "unknown",
                 "u":  "unknown",
                 "w":  "unknown",
                 "v":  "unknown",
                 "x":  "unknown",
                 "y":  "unknown",
                 "z":  "unknown",
                 "ź":  "unknown",
                 "ż":  "unknown"
             } 


        self.readCheck = self.read.getCheckingTrees()
        self.readGuess = self.read.getGuessWords()


    def check_words(self, word, guess):
        resultOfComparison = []
        for i in range(len(word)):
            resultOfComparison.append([guess[i],"unknown"])
            for j in range(len(word)):
                if i == j and guess[i] == word[j]:
                    resultOfComparison[i][1] = "inplace"
                elif i != j and guess[i] == word[j] and resultOfComparison[i][1] != "inplace":
                    resultOfComparison[i][1] = "known"
                elif resultOfComparison[i][1] != "inplace" and resultOfComparison[i][1] != "known":
                    resultOfComparison[i][1] = "out"   
                else:
                    pass    
        return resultOfComparison

    def update_dictionary(self, resultOfComparison):
        for i in self.dic.keys():
            for j in resultOfComparison:
                if i == j[0].lower():
                    self.dic[i] = j[1]     

    def play(self):
        
        def delete():
            if self.currentLetter > 0:
                self.currentLetter -= 1 
                self.currentWord = self.currentWord[0:-1]
                labels[self.currentWordIndex][self.currentLetter].config(text="  ")
                
        def letter(letter):
            if self.currentLetter < self.wordLength:
                labels[self.currentWordIndex][self.currentLetter].config(text=letter)
                self.currentLetter += 1
                self.currentWord += letter
            
        def enter():
            #print(self.currentWord, " ", self.wordLength, " ", self.readCheck[self.wordLength + self.minWordLength - self.maxWordLength-1].search_for_word(self.currentWord.lower()))
            if len(self.currentWord) == self.wordLength and self.readCheck[self.wordLength + self.minWordLength - self.maxWordLength-1].search_for_word(self.currentWord.lower()):
                resultOfComparison = self.check_words(self.word.lower(), self.currentWord.lower())    
                for i in range(len(resultOfComparison)):
                    if resultOfComparison[i][1] == "inplace":
                        labels[self.currentWordIndex][i].config(bg=self.colorInPlace)
                    elif resultOfComparison[i][1] == "known":
                        labels[self.currentWordIndex][i].config(bg=self.colorKnown)
                    else:
                        labels[self.currentWordIndex][i].config(bg=self.colorOut)    
                self.roundHistory.append(resultOfComparison) 
                if self.word.lower() == self.currentWord.lower():
                    comunicatLabel.config(text="WYGRAŁEŚ!!!")
                    clear_dic_and_variables()
                    self.read.add_scores(True,len(self.word))
                    saveResultButton.config(state="normal")
                    playAgainButton.config(state="normal")
                else:
                    self.currentWordIndex += 1
                    self.currentLetter = 0
                    self.currentWord = ""
                    self.update_dictionary(resultOfComparison)
                    for i in self.dic.items():
                        if i[1].__eq__("inplace"):
                            buttonDic[i[0]].config(bg=self.colorInPlace)
                        elif i[1].__eq__("known"):
                            buttonDic[i[0]].config(bg=self.colorKnown)
                        elif i[1].__eq__("out"):
                            buttonDic[i[0]].config(bg=self.colorOut)   
                        else:
                            pass
                if self.currentWordIndex>=self.numberOfRounds:
                    self.read.add_scores(False,len(self.word))
                    playAgainButton.config(state="normal")
                    comunicatLabel.config(text="PRZEGRAŁEŚ!!!")

        def exit_play():
            clear_dic_and_variables()
            game.destroy()

        def clear_dic_and_variables():
            self.currentWord = ""
            self.currentLetter = 0
            self.currentWordIndex = 0
    
            for key in self.dic.keys():
                self.dic[key] = "unknown"

        def play_again():
            clear_dic_and_variables()
            self.roundHistory.clear()
            set_new_word()
            print(self.word)
            for i in labels:
                for j in i:
                    j.config(text=str(" "),bg=self.colorWordsInPanel)

            for button in buttonDic.values():
                button.config(bg="#FFFAFA")  
            saveResultButton.config(state="disabled")
            playAgainButton.config(state="disabled")
            comunicatLabel.config(text="")
        
        def save_result():
            saveResultButton.config(state="disabled")
            self.read.save_game(self.roundHistory)

        def set_new_word():
            self.word = self.readGuess[self.wordLength + self.minWordLength - self.maxWordLength-1][random.randrange(0,len(self.readGuess[self.wordLength + self.minWordLength - self.maxWordLength-1]))]

        game = Toplevel(bg="#E0FFFF")
        game.geometry("400x400")
        game.title("Wordle")
        self.roundHistory = []
        set_new_word()
        print(self.word)
  
        framePanel   = Frame(game)
        framePanel.pack()
        labels = []
        for i in range(self.numberOfRounds):
            labels.append([])
            for j in range(self.wordLength):
                labels[i].append(tk.Button(framePanel,text=str(" "),bg=self.colorWordsInPanel,state="disabled",height=1,width=2))
                labels[i][j].grid(row=i,column=j)
        frameLetters = Frame(game, bg=self.colorLettersFrame )
        frameLetters.pack(padx=5,pady=5)

        frameLetters1 = Frame(frameLetters, bg=self.colorLettersFrame )
        frameLetters1.pack()
        frameLetters2 = Frame(frameLetters, bg=self.colorLettersFrame )
        frameLetters2.pack()
        frameLetters3 = Frame(frameLetters, bg=self.colorLettersFrame )
        frameLetters3.pack()
        frameLetters4 = Frame(frameLetters, bg=self.colorLettersFrame )
        frameLetters4.pack()
        
        frameOptions = Frame(game, bg=self.colorOptionFrame )
        frameOptions.pack()
        frameButtonsOptions = Frame(frameOptions, bg=self.colorOptionFrame )
        frameButtonsOptions.pack()
        
        exitButton = Button(frameButtonsOptions, text="Powrót",padx=5,pady=10,command=exit_play)
        exitButton.grid(row=0,column=0)

        saveResultButton = Button(frameButtonsOptions, text="Zapisz wynik",padx=5,pady=10,command=save_result,state="disabled")
        saveResultButton.grid(row=0,column=1)

        playAgainButton = Button(frameButtonsOptions, text="Zagraj ponownie",padx=5,pady=10,command=play_again,state="disabled")
        playAgainButton.grid(row=0,column=2)

        font=("Arial", 25)
        comunicatLabel = Label(frameOptions, text="",padx=5,pady=10,bg=self.colorLettersFrame,font=font)
        comunicatLabel.pack()
       
        
     
        buttonDic = {
        "q" :   tk.Button( frameLetters1, text="Q",command=lambda temp="Q" : letter(temp),bg="#FFFAFA"),
        "w" :   tk.Button( frameLetters1, text="W",command=lambda temp="W" : letter(temp),bg="#FFFAFA"),
        "e" :   tk.Button( frameLetters1, text="E",command=lambda temp="E" : letter(temp),bg="#FFFAFA"),
        "r" :   tk.Button( frameLetters1, text="R",command=lambda temp="R" : letter(temp),bg="#FFFAFA"),
        "t" :   tk.Button( frameLetters1, text="T",command=lambda temp="T" : letter(temp),bg="#FFFAFA"),
        "y" :   tk.Button( frameLetters1, text="Y",command=lambda temp="Y" : letter(temp),bg="#FFFAFA"),
        "u" :   tk.Button( frameLetters1, text="U",command=lambda temp="U" : letter(temp),bg="#FFFAFA"),
        "i" :   tk.Button( frameLetters1, text="I",command=lambda temp="I" : letter(temp),bg="#FFFAFA"),
        "o" :   tk.Button( frameLetters1, text="O",command=lambda temp="O" : letter(temp),bg="#FFFAFA"),
        "p" :   tk.Button( frameLetters1, text="P",command=lambda temp="P" : letter(temp),bg="#FFFAFA"),

        "a" :    tk.Button( frameLetters2, text="A",command=lambda temp="A" : letter(temp),bg="#FFFAFA"),
        "s" :    tk.Button( frameLetters2, text="S",command=lambda temp="S" : letter(temp),bg="#FFFAFA"),
        "d" :    tk.Button( frameLetters2, text="D",command=lambda temp="D" : letter(temp),bg="#FFFAFA"),
        "f" :    tk.Button( frameLetters2, text="F",command=lambda temp="F" : letter(temp),bg="#FFFAFA"),
        "g" :    tk.Button( frameLetters2, text="G",command=lambda temp="G" : letter(temp),bg="#FFFAFA"),
        "h" :    tk.Button( frameLetters2, text="H",command=lambda temp="H" : letter(temp),bg="#FFFAFA"),
        "j" :    tk.Button( frameLetters2, text="J",command=lambda temp="J" : letter(temp),bg="#FFFAFA"),
        "k" :    tk.Button( frameLetters2, text="K",command=lambda temp="K" : letter(temp),bg="#FFFAFA"),
        "l" :    tk.Button( frameLetters2, text="L",command=lambda temp="L" : letter(temp),bg="#FFFAFA"),
        "m" :    tk.Button( frameLetters2, text="M",command=lambda temp="M" : letter(temp),bg="#FFFAFA"),

        "Del" :    tk.Button( frameLetters3, text="Del",command=delete,bg="#FFFAFA"),
        "z" :  tk.Button( frameLetters3, text="Z",command=lambda temp="Z" : letter(temp),bg="#FFFAFA"),
        "x" :  tk.Button( frameLetters3, text="X",command=lambda temp="X" : letter(temp),bg="#FFFAFA"),
        "c" :  tk.Button( frameLetters3, text="C",command=lambda temp="C" : letter(temp),bg="#FFFAFA"),
        "v" :  tk.Button( frameLetters3, text="V",command=lambda temp="V" : letter(temp),bg="#FFFAFA"),
        "b" :  tk.Button( frameLetters3, text="B",command=lambda temp="B" : letter(temp),bg="#FFFAFA"),
        "n" :  tk.Button( frameLetters3, text="N",command=lambda temp="N" : letter(temp),bg="#FFFAFA"),
        "Enter" :    tk.Button( frameLetters3, text="Enter",command=enter,bg="#FFFAFA"),

        "ą" :    tk.Button( frameLetters4, text="Ą",command=lambda temp="Ą" : letter(temp),bg="#FFFAFA"),
        "ć" :    tk.Button( frameLetters4, text="Ć",command=lambda temp="Ć" : letter(temp),bg="#FFFAFA"),
        "ę" :    tk.Button( frameLetters4, text="Ę",command=lambda temp="Ę" : letter(temp),bg="#FFFAFA"),
        "ł" :    tk.Button( frameLetters4, text="Ł",command=lambda temp="Ł" : letter(temp),bg="#FFFAFA"),
        "ń" :    tk.Button( frameLetters4, text="Ń",command=lambda temp="Ń" : letter(temp),bg="#FFFAFA"),
        "ó" :    tk.Button( frameLetters4, text="Ó",command=lambda temp="Ó" : letter(temp),bg="#FFFAFA"),
        "ś" :    tk.Button( frameLetters4, text="Ś",command=lambda temp="Ś" : letter(temp),bg="#FFFAFA"),
        "ź" :    tk.Button( frameLetters4, text="Ź",command=lambda temp="Ź" : letter(temp),bg="#FFFAFA"),
        "ż" :    tk.Button( frameLetters4, text="Ż",command=lambda temp="Ż" : letter(temp),bg="#FFFAFA")
        }
        
        buttonDic["q"].grid(row=0,column=0)
        buttonDic["w"].grid(row=0,column=1)
        buttonDic["e"].grid(row=0,column=2)
        buttonDic["r"].grid(row=0,column=3)
        buttonDic["t"].grid(row=0,column=4)
        buttonDic["y"].grid(row=0,column=5)
        buttonDic["u"].grid(row=0,column=6)
        buttonDic["i"].grid(row=0,column=7)
        buttonDic["o"].grid(row=0,column=8)
        buttonDic["p"].grid(row=0,column=9)
        buttonDic["a"].grid(row=0,column=0)
        buttonDic["s"].grid(row=0,column=1)
        buttonDic["d"].grid(row=0,column=2)
        buttonDic["f"].grid(row=0,column=3)
        buttonDic["g"].grid(row=0,column=4)
        buttonDic["h"].grid(row=0,column=5)
        buttonDic["j"].grid(row=0,column=6)
        buttonDic["k"].grid(row=0,column=7)
        buttonDic["l"].grid(row=0,column=8)
        buttonDic["m"].grid(row=0,column=9)
        buttonDic["Del"].grid(row=0,column=0)
        buttonDic["z"].grid(row=0,column=1)
        buttonDic["x"].grid(row=0,column=2)
        buttonDic["c"].grid(row=0,column=3)
        buttonDic["v"].grid(row=0,column=4)
        buttonDic["b"].grid(row=0,column=5)
        buttonDic["n"].grid(row=0,column=6)
        buttonDic["Enter"].grid(row=0,column=8)
        buttonDic["ą"].grid(row=0,column=0)
        buttonDic["ć"].grid(row=0,column=1)
        buttonDic["ę"].grid(row=0,column=2)
        buttonDic["ł"].grid(row=0,column=3)
        buttonDic["ń"].grid(row=0,column=4)
        buttonDic["ó"].grid(row=0,column=5)
        buttonDic["ś"].grid(row=0,column=6)
        buttonDic["ź"].grid(row=0,column=7)
        buttonDic["ż"].grid(row=0,column=8)

    def results(self):

        def show_statistics():
            changeButton.config(text="Scores", command = show_games)
            myFrame.pack_forget()
            statFrame.pack()

        def show_games():    
            changeButton.config(text="Games", command=show_statistics)
            statFrame.pack_forget()
            myFrame.pack()
                 

        resultPanel = Toplevel(bg="#E0FFFF")
        resultPanel.resizable(False, False)
        resultPanel.geometry("400x300")
        resultPanel.title("Wordle:   results") 

        buttonFrame = Frame(resultPanel, bg="#E0FFFF")
        buttonFrame.pack(pady=2)

        changeButton = Button(buttonFrame, text="Games", command=show_statistics)
        changeButton.grid(row=0, column=0)

        exitButton = Button(buttonFrame, text="Exit", command=resultPanel.destroy)
        exitButton.grid(row=0, column=1)


        results = self.read.read_result()
        statistics = self.read.read_statistics()
        frames = []

        myFrame = Frame(resultPanel, bg="#E0FFFF")
        myFrame.pack(fill=BOTH, expand=1)

        statFrame = Frame(resultPanel, bg="#E0FFFF")
        for stat in statistics:
            Label(statFrame, text=stat[0]+":  "+stat[1],font=("Arial", 12), bg="#E0FFFF").pack()

        myCanvas = Canvas(myFrame, bg="#E0FFFF")
        myCanvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = tk.Scrollbar(myFrame, orient=VERTICAL, command=myCanvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        myCanvas.configure(yscrollcommand=scrollbar.set)
        myCanvas.bind('<Configure>', lambda e: myCanvas.configure(scrollregion=myCanvas.bbox("all")))

        secondFrame = Frame(myCanvas, bg="#E0FFFF")

        myCanvas.create_window((200,0), window=secondFrame,anchor="center")

        
        for i in range(len(results)):
            frames.append(Frame(secondFrame,bg="#E0FFFF"))
            frames[i].pack()
            data =  Frame(frames[i],bg="#E0FFFF")
            data.pack()
            scenario = Frame(frames[i],bg="#E0FFFF")
            scenario.pack()
            Label(data,text = "\nGra - "+str(i), font=("Arial", 15),bg="#E0FFFF").pack()
            #Label(data,text = str(results[i][1]), font=("Arial", 12)).pack()
            Label(data,text = str(results[i][2]), font=("Arial", 12),bg="#E0FFFF").pack()
            for round in range(len(results[i][0])):
                for j in range(len(results[i][0][round])):
                    if results[i][0][round][j][1] == "inplace":
                        Button(scenario,bg=self.colorInPlace, text=results[i][0][round][j][0].capitalize(),state="disabled",height=2,width=2).grid(row=round, column=j)
                    elif  results[i][0][round][j][1] == "known":
                        Button(scenario,bg=self.colorKnown, text=results[i][0][round][j][0].capitalize(),state="disabled",height=2,width=2).grid(row=round, column=j,)
                    else:
                        Button(scenario,bg=self.colorOut, text=results[i][0][round][j][0].capitalize(),state="disabled",height=2,width=2).grid(row=round, column=j)

       

    def options(self):
        options = Toplevel(bg="#E0FFFF")
        options.geometry("200x200")
        options.title("Wordle:   options")

        def out_of_options():
            self.wordLength = wordLength.get()
            options.destroy()

            
        wordLength = IntVar()
        wordLength.set(self.wordLength)
        
        Label(options,text="Długość słowa w grze: ").pack(anchor="w")
        for i in range(self.minWordLength,self.maxWordLength+1):
            tk.Radiobutton(options, text=str(i), variable=wordLength, value=i).pack(anchor='w')

        Button(options,text="Wyjdź i zapisz",command=out_of_options,bg="#F08080",height = 1,width=10).pack(anchor='sw', pady=30)

        
        

    def start_screen(self):
        root = tk.Tk()
        root.title("Wordle:   menu")
        root.geometry("300x400")

        canvas = tk.Canvas(root, height=400, width=300 , bg = "#B0C4DE")
        canvas.pack(padx=10,pady=10)

        frame = tk.Frame(canvas, height=400 , width=300,bg="#B0C4DE") 
        frame.pack(padx=75,pady=50)
    
        startButton = tk.Button(frame, bg="#4682B4", text  = "Start game", padx=20,pady=10,command=self.play)
        startButton.pack(padx=5,pady=5)

        resultsButton = tk.Button(frame, bg="#4682B4", text  = "Results", padx=30,pady=10, command=self.results)
        resultsButton.pack(padx=5,pady=5)

        optionsButton = tk.Button(frame, bg="#4682B4", text  = "Options", padx=30,pady=10,command=self.options)
        optionsButton.pack(padx=5,pady=5)

        endButton = tk.Button(frame, bg="#4682B4", text  = "Exit", padx=40, pady=10, command=root.destroy)
        endButton.pack(padx=5,pady=5)

        root.mainloop()

game = Game()
game.start_screen()    

#start(readCheck,readGuess)


''''''