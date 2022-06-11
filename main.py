from typing import Optional
import ReadingFile
import Node
import datetime
import random
import os
from timeit import default_timer as timer


read = ReadingFile.ReadingFile()
configFile = read.getConfigFile()

minWordLength = int(configFile['base']['minWordLength'])
maxWordLength = int(configFile['base']['maxWordLength'])
treeDeep = int(configFile['base']['treeDeep'])
numberOfRounds = int(configFile['base']['numberOfRounds'])


readCheck = read.getCheckingTrees()
readGuess = read.getGuessWords()

#print(5 + minWordLength - maxWordLength - 1, "\t")
#print(readCheck[5 + minWordLength - maxWordLength- 1].search_for_word("łódka"))
'''
start1 = timer()
readCheck[1].search_for_word("chlew")
end1 = timer()

start2 = timer()
"chlew" in read.listWordsToGuess[1]
end2 = timer()
print("TreeDeep: ", treeDeep)
print("Struktura drzewiasta:  ", (end1 - start1)*1000," sekund")
print("Lista               :  ", (end2 - start2)*1000," sekund")
'''


def start(readCheck, readGuess):
    end = False
    while(not end):
        dic = {
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

        print("\n\n","---------------","Wordle","---------------","\n")
        print("MENU:","\n","1. Graj","\n","2. Wyjdź")

        decision = input()
        while(not decision.isdecimal() and (decision!=1 and decision!=2)):
            decision = input("Niepoprawne wprowadzenie, spróbuj ponownie:  ")

        if decision == "1":
            play_game(readCheck, readGuess, dic)
        else:
            end = True    



def play_game(readCheck, readGuess, dic):
    wordLength = 4
    word  = readGuess[wordLength + minWordLength - maxWordLength-1][random.randrange(0,len(readGuess[wordLength + minWordLength - maxWordLength-1]))]
    print("słow do zgadnięcia: ",word)

    i = 0
    end = False
    roundHistory = []
    while( i<numberOfRounds and not end ):
        print("\n")
        guess = input("Podaj słowo:    ")
        while(not readCheck[wordLength + minWordLength - maxWordLength-1].search_for_word(guess) or len(guess) != wordLength):
            guess = input("Błędne słowo, podaj słowo ponownie:    ")
        resultOfComparison = check_words(word, guess)    
        roundHistory.append(resultOfComparison) 
        if word == guess:
            print("WYGRAŁEŚ!!!")
            read.add_scores(True,len(word))
            read.save_game(roundHistory)
            end = True
        else:
            update_dictionary(dic,resultOfComparison)
        i += 1    
        print(dic)
    if end == False:
        read.add_scores(False,len(word))
        print("Przegrałeś!!!")


def update_dictionary( dic, resultOfComparison):
    for i in dic.keys():
        for j in resultOfComparison:
            if i == j[0]:
                dic[i] = j[1]     


def check_words(word, guess):
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


start(readCheck,readGuess)

