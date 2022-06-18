
class NODE():
    """
    A class to represent a node use to collecting and easily accessing words from dictionary.

    ...

    Attributes
    ----------
    counter : str
        determin how close it is to the end of the tree
    is_leaf : bool
        determin if Node is leaf or not
    words : list[str]    (excist only in leaf)
        list of words that are collected in the leaf
    children : dict{str : Node.Node()}    (excist only in not leaf)
        dictionary of children (Nodes)
    
    Methods
    -------
    add_word_help(self, full_word: str, cut_word: str) -> None
        Add word to tree.
    -------    
    add_word(self, word: str) -> None    
        Execute add_word_help function.
    -------    
    search_for_word_help(self, full_word: str, cut_word: str) -> bool
        Find out if word excist in tree.
    -------    
    search_for_word(self, word: str) -> bool
        Execute search_for_word_help function.
    -------    
    __str__(self) -> str
        Change Node and it children into a string.
    """

    def __init__(self, counter: int) -> None: 
        """
        Constructs all the necessary attributes for the Node object.

        Parameters
        ----------
            counter : str
                determin how close it is to the end of the tree
        """
        self.counter = counter
        if counter == 0:
            self.is_leaf = True
            self.words = []
        else:
            self.is_leaf = False    
            self.children = {}
            
    def add_word_help(self, full_word: str, cut_word: str) -> None:
        """
        Add word to tree.

        Parameters
        ----------
            full_word: str
                Word that will be add to tree in leaf.
            cut_word: str
                Word with cutted begin, to add full_word in correct leaf.
        Returns
        -------
        None
        """
        if self.is_leaf and not full_word in self.words:
            self.words.append(full_word.lower())
        elif not self.is_leaf:
            if cut_word[0] in self.children.keys():
                self.children[cut_word[0]].add_word_help(full_word, cut_word[1:])
            else:
                self.children[cut_word[0]] = NODE(self.counter-1)
                self.children[cut_word[0]].add_word_help(full_word, cut_word[1:])

    def add_word(self, word: str) -> None:
        """
        Execute add_word_help function.

        Parameters
        ----------
            word: str
                Word that will be add to tree in leaf.
        Returns
        -------
        None
        """
        self.add_word_help(word,word)

    def search_for_word_help(self, full_word: str, cut_word: str) -> bool:
        """
        Find out if word excist in tree.

        Parameters
        ----------
            full_word: str
                Word thar we are looking for.
            cut_word: str
                Word with cutted begin, to search in tree.
        Returns
        -------
        bool
        """
        if self.is_leaf:
            return full_word in self.words
        elif cut_word!="" and cut_word[0] in self.children.keys():
            return self.children[cut_word[0]].search_for_word_help(full_word,cut_word[1:])
        else:
            return False
    
    def search_for_word(self, word: str) -> bool:
        """
        Execute search_for_word_help function.

        Parameters
        ----------
            word: str
                Word that is searched in tree.
        Returns
        -------
        bool
        """
        return self.search_for_word_help(word,word)      

    def __str__(self) -> str:
        """
        Change Node and Node's children into a string.

        Parameters
        ----------

        Returns
        -------
        str
        """
        if self.is_leaf:
            return str(self.words)
        else:
            build_string = ""
            for i in self.children.values():
                build_string += str(i)
            return build_string

