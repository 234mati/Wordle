from gettext import find
import pandas as pand
import numpy as np
import random


f = open("G:\Studia\JezykiSkryptowe\Projekt\slowa.txt", encoding="utf8")
textOpenForChecking = f.read()
f.close()
wordsForChecking = textOpenForChecking.split("\n")

f2 = open("G:\Studia\JezykiSkryptowe\Projekt\DoWyboru.txt", encoding="utf8")
textOpenGuessWords = f2.read()
f2.close()


minWordLength = 4
maxWordLength = 7


def unpack_words_collection(words, separator):
    if separator != "":
        splittedWords = words.split(separator)
    else:
        splittedWords  = words
    list = []
    for i in range(maxWordLength-minWordLength+1):
        list.append([])   
    for i in splittedWords:
        if len(i) >= minWordLength and len(i) <= maxWordLength:
            list[minWordLength-maxWordLength+len(i)-1].append(i)
    return list


def unpack_words_to_guess(words):
    guessWords = words.split(" ")
    guessWordsTemp = []
    for i in guessWords:
        equalIndeks = i.find('=')
        if equalIndeks != -1:
          guessWordsTemp.append(i[0:equalIndeks])
        else:
            guessWordsTemp.append(i)
    guessWordsTemp = unpack_words_collection(guessWordsTemp,"")
    return guessWordsTemp


listWordsToCheck = unpack_words_collection(textOpenForChecking,"\n")
listWordsToGuess = unpack_words_to_guess(textOpenGuessWords)

print(listWordsToGuess[0][random.randint(0, len(listWordsToGuess[0])-1)])
