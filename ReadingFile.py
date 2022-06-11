from gettext import find
import pandas as pand
import numpy as np
import random
import os
import Node
from configparser import ConfigParser
import datetime



class ReadingFile():
    def __init__(self):
        self.scriptDir = os.path.dirname(__file__)
        self.configFile = self.read_config()

        scriptDir = os.path.dirname(__file__)
        self.scoresPath = self.configFile['paths']['scoresPath']
        self.savedGamesPath = self.configFile['paths']['savedGamesPath']
        textOpenForCheckingPath  = self.configFile['paths']['checkWordsPath']
        textOpenGuessWordsPath  = self.configFile['paths']['guessWordsPath']

        self.minWordLength = int(self.configFile['base']['minWordLength'])
        self.maxWordLength = int(self.configFile['base']['maxWordLength'])
        self.treeDeep = int(self.configFile['base']['treeDeep'])
 

        with open(os.path.join(scriptDir, textOpenForCheckingPath), encoding="utf8") as f:
            textOpenForChecking = f.read()
        
        with open(os.path.join(scriptDir, textOpenGuessWordsPath), encoding="utf8") as f2:
            textOpenGuessWords = f2.read()


        self.listWordsToCheck = self.unpack_words_collection(textOpenForChecking,"\n")
        self.listWordsToGuess = self.unpack_words_to_guess(textOpenGuessWords)
        self.trees = []
        for i in range(self.maxWordLength-self.minWordLength+1):
            self.trees.append(Node.Node(self.treeDeep))
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

    def add_scores(self, isWin, numberOfLettersInWord):
        fileName = self.scoresPath
        if not os.path.exists(os.path.join(self.scriptDir, fileName)): 
            with open(os.path.join(self.scriptDir, fileName), 'x') as f:
                f.write('[Scores]\n')
                f.write('TotalWinScore = 0\n')
                f.write('TotalLoseScore = 0\n')
                for i in range(self.minWordLength,self.maxWordLength+1):
                    f.write(str(i)+'LetterWordsWin = 0\n')
                    f.write(str(i)+'LetterWordsLose = 0\n')

        scores = ConfigParser()
        scores.read(os.path.join(self.scriptDir, fileName))

        if isWin:
            scores['Scores']['TotalWinScore']  = str(int(scores['Scores']['TotalWinScore'])  + 1)
            scores['Scores'][str(numberOfLettersInWord)+'LetterWordsWin']  = str( int(scores['Scores'][str(numberOfLettersInWord)+'LetterWordsWin'])  + 1)
        else:
            scores['Scores']['TotalLoseScore']  = str(int(scores['Scores']['TotalLoseScore'])  + 1)
            scores['Scores'][str(numberOfLettersInWord)+'LetterWordsLose'] = str( int(scores['Scores'][str(numberOfLettersInWord)+'LetterWordsLose']) + 1)   
        
        with open(os.path.join(self.scriptDir, fileName),'w+') as scoreFile:
            scores.write(scoreFile)


    def save_game(self,listOfGuesses):
        fileName = self.savedGamesPath
        if not os.path.exists(os.path.join(self.scriptDir, fileName)): 
            open(os.path.join(self.scriptDir, fileName), 'x')
        savedGames = ConfigParser()
        savedGames.read(os.path.join(self.scriptDir, fileName))
        savedGames.add_section("Game - "+ str(len(savedGames.sections())+1))
        for i in range(len(listOfGuesses)):
            savedGames.set("Game - "+ str(len(savedGames.sections())),"Round "+str(i), str(listOfGuesses[i]))  
        savedGames.set("Game - "+ str(len(savedGames.sections())),"Number of needed words", str(len(listOfGuesses)))     
        savedGames.set("Game - "+ str(len(savedGames.sections())),"Date ", datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S") )
        with open(os.path.join(self.scriptDir, fileName),'w+') as gamesFile:
            savedGames.write(gamesFile)


    def read_config(self):
        fileName = "Config.ini"
        config = ConfigParser()
        config.read(os.path.join(self.scriptDir, fileName))
        return config
            

    def getConfigFile(self):
        return self.configFile
