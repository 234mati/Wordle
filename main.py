from typing import Optional
from fastapi import FastAPI
import ReadingFile
import Node


minWordLength = 4
maxWordLength = 7
treeDeep = 3

read = ReadingFile.ReadingFile(minWordLength, maxWordLength, treeDeep)
readCheck = read.getCheckingTrees()
readGuess = read.getGuessWords()

print(readCheck[0].search_for_word("xxxx"))
print(readGuess)