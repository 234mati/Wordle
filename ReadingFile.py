from gettext import find
import pandas as pand
import numpy as np
import random
import os
import Node



class ReadingFile():
    def __init__(self, minWordLength, maxWordLength, treeDeep):
        self.minWordLength = minWordLength
        self.maxWordLength = maxWordLength
        self.treeDeep = treeDeep
        
        scriptDir = os.path.dirname(__file__)
        textOpenForCheckingPath  = "Data/slowa.txt"
        textOpenGuessWordsPath  = "Data/DoWyboru.txt"

        f = open(os.path.join(scriptDir, textOpenForCheckingPath), encoding="utf8")
        textOpenForChecking = f.read()
        f.close()
        #with open(..) as f:
        f2 = open(os.path.join(scriptDir, textOpenGuessWordsPath), encoding="utf8")
        textOpenGuessWords = f2.read()
        f2.close()

        self.listWordsToCheck = self.unpack_words_collection(textOpenForChecking,"\n")
        self.listWordsToGuess = self.unpack_words_to_guess(textOpenGuessWords)
        self.trees = []

        for i in range(maxWordLength-minWordLength+1):
            self.trees.append(Node.Node(treeDeep))
            for j in self.listWordsToCheck[i]:
                self.trees[i].add_word(j)    


    def unpack_words_collection(self, words, separator):
        if separator != "":
            splittedWords = words.split(separator)
        else:
            splittedWords  = words
        list = []
        for i in range(self.maxWordLength-self.minWordLength+1):
            list.append([])   
        for i in splittedWords:
           if len(i) >= self.minWordLength and len(i) <= self.maxWordLength:
                list[self.minWordLength-self.maxWordLength+len(i)-1].append(i)
        return list


    def unpack_words_to_guess(self, words):
        guessWords = words.split(" ")
        guessWordsTemp = []
        for i in guessWords:
            equalIndeks = i.find('=')
            if equalIndeks != -1:
              guessWordsTemp.append(i[0:equalIndeks])
            else:
                guessWordsTemp.append(i)
        guessWordsTemp = self.unpack_words_collection(guessWordsTemp,"")
        return guessWordsTemp


    def getCheckingTrees(self):
        return self.trees

    def getGuessWords(self):
        return self.listWordsToGuess

