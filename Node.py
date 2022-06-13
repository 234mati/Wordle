
class Node():
    def __init__(self, counter):
        self.counter = counter
        if counter == 0:
            self.isLeaf = True
            self.words = []
        else:
            self.isLeaf = False    
            self.children = {}
            
    def add_word_help(self, fullWord, cutWord):
        if self.isLeaf:
            self.words.append(fullWord)
        else:
            if cutWord[0] in self.children.keys():
                self.children[cutWord[0]].add_word_help(fullWord, cutWord[1:])
            else:
                self.children[cutWord[0]] = Node(self.counter-1)
                self.children[cutWord[0]].add_word_help(fullWord, cutWord[1:])

    def add_word(self, word):
        self.add_word_help(word,word)

    def search_for_word_help(self, fullWord, cutWord):
        if self.isLeaf:
            #zmienić contains na fullWord in words
            return fullWord in self.words
        elif cutWord!="" and cutWord[0] in self.children.keys():
            return self.children[cutWord[0]].search_for_word_help(fullWord,cutWord[1:])
        else:
            return False
    
    def search_for_word(self, word):
        return self.search_for_word_help(word,word)      

    def __str__(self) -> str:
        if self.isLeaf:
            return str(self.words)
        else:
            temp = ""
            for i in self.children.values():
                temp += str(i)
            return temp

