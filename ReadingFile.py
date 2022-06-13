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
        self.numberOfRounds = int(self.configFile['base']['numberOfRounds'])
 

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
                f.write('Total Win Score = 0\n')
                f.write('Total Lose Score = 0\n')
                for i in range(self.minWordLength,self.maxWordLength+1):
                    f.write(str(i)+' Letter Words Win = 0\n')
                    f.write(str(i)+' Letter Words Lose = 0\n')

        scores = ConfigParser()
        scores.read(os.path.join(self.scriptDir, fileName))

        if isWin:
            scores['Scores']['Total Win Score']  = str(int(scores['Scores']['Total Win Score'])  + 1)
            scores['Scores'][str(numberOfLettersInWord)+' Letter Words Win']  = str( int(scores['Scores'][str(numberOfLettersInWord)+' Letter Words Win'])  + 1)
        else:
            scores['Scores']['Total Lose Score']  = str(int(scores['Scores']['Total Lose Score'])  + 1)
            scores['Scores'][str(numberOfLettersInWord)+' Letter Words Lose'] = str( int(scores['Scores'][str(numberOfLettersInWord)+' Letter Words Lose']) + 1)   
        
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
            savedGames.set("Game - "+ str(len(savedGames.sections())),"round "+str(i), str(listOfGuesses[i]))  
        savedGames.set("Game - "+ str(len(savedGames.sections())),"number of needed words", str(len(listOfGuesses)))     
        savedGames.set("Game - "+ str(len(savedGames.sections())),"date ", datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S") )
        with open(os.path.join(self.scriptDir, fileName),'w+') as gamesFile:
            savedGames.write(gamesFile)


    def read_config(self):
        fileName = "Config.ini"
        config = ConfigParser()
        config.read(os.path.join(self.scriptDir, fileName))
        return config
            

    def changeStringForList(self, w: str):
        sp = w.split("'")
        temp = []
        iter = 0
  
        for i in range(len(sp)):
            if i % 2 != 0 and iter % 4 == 1:
                temp.append(["",""])
                temp[int(i//4)][0] = sp[i]
            elif i % 2 != 0 and iter % 4 == 3:
                temp[int(i//4)][1] = sp[i]
            iter += 1
        return temp

    
    def read_statistics(self):
        fileName = self.scoresPath
        statistics = ConfigParser()
        statistics.read(os.path.join(self.scriptDir, fileName))
        outputTabel = []
        for i in statistics["Scores"].keys():
            outputTabel.append((i,statistics["Scores"][i]))   
        return outputTabel


    def read_result(self):
        fileName = self.savedGamesPath
        savedGames = ConfigParser()
        savedGames.read(os.path.join(self.scriptDir, fileName))
        outputTabel = []
        for game in savedGames.values():
            if game.name != "DEFAULT":
                numberOfNeededWords = int(game["number of needed words"])
                roundScenario = [self.changeStringForList(game["round " + str(i)]) for i in range(numberOfNeededWords)]
                outputTabel.append((roundScenario, numberOfNeededWords , game["date"]))
        return outputTabel 



    def getConfigFile(self):
        return self.configFile
