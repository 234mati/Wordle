
class Node():
    def __init__(self, counter):
        if counter == 0:
            self.isLeaf = True
            self.words = []
        else:
            self.isLeaf = False    
            self.children = {
            "a":  Node(counter-1),
            "ą":  Node(counter-1),
            "b":  Node(counter-1),
            "c":  Node(counter-1),
            "ć":  Node(counter-1),
            "d":  Node(counter-1),
            "e":  Node(counter-1),
            "ę":  Node(counter-1),
            "f":  Node(counter-1),
            "g":  Node(counter-1),
            "h":  Node(counter-1),
            "i":  Node(counter-1),
            "j":  Node(counter-1),
            "k":  Node(counter-1),
            "l":  Node(counter-1),
            "ł":  Node(counter-1),
            "m":  Node(counter-1),
            "n":  Node(counter-1),
            "ń":  Node(counter-1),
            "o":  Node(counter-1),
            "ó":  Node(counter-1),
            "p":  Node(counter-1),
            "r":  Node(counter-1),
            "s":  Node(counter-1),
            "ś":  Node(counter-1),
            "t":  Node(counter-1),
            "u":  Node(counter-1),
            "w":  Node(counter-1),
            "v":  Node(counter-1),
            "x":  Node(counter-1),
            "y":  Node(counter-1),
            "z":  Node(counter-1),
            "ź":  Node(counter-1),
            "ż":  Node(counter-1),
        }
        
            
    def add_word_help(self, fullWord, cutWord):
        if self.isLeaf:
            self.words.append(fullWord)
        else:
            self.children[cutWord[0]].add_word_help(fullWord, cutWord[1:])

    def add_word(self, word):
        self.add_word_help(word,word)

    def search_for_word_help(self, fullWord, cutWord):
        if self.isLeaf:
            return self.words.__contains__(fullWord) 
        else:
            return self.children[cutWord[0]].search_for_word_help(fullWord,cutWord[1:])
    
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
        
