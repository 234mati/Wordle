from typing import Optional
from fastapi import FastAPI
import ReadingFile
import Node
import datetime
from timeit import default_timer as timer


minWordLength = 4
maxWordLength = 7
treeDeep = 3

read = ReadingFile.ReadingFile(minWordLength, maxWordLength, treeDeep)
readCheck = read.getCheckingTrees()
#print(readCheck[0])
readGuess = read.getGuessWords()

start1 = timer()
readCheck[1].search_for_word("chlew")
end1 = timer()

start2 = timer()
read.listWordsToGuess[1].__contains__("chlew")
end2 = timer()


print("Struktura drzewiasta:  ", (end1 - start1)*1000," sekund")

print("Lista               :  ", (end2 - start2)*1000," sekund")




#print(readGuess)