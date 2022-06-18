from configparser import ConfigParser
import datetime
import Node
import os




class READING_FILE():
    """
    A class which access a other files, and prepare them to work in aplication.

    ...

    Attributes
    ----------
    script_dir : str
        path to file directory
    config_file : ConfigParser
        information from configuration file
    scores_path : str
        path to scores.txt file 
    saved_games_path : str
        path to savedGames.txt file  
    min_word_length : int
        minimum word length in game   
    min_word_length : int
        maximum word length in game       
    tree_deep : int
        how deep is tree that collects words
    number_of_rounds : int
        quantity of guesses that player have until he/she lost  
    list_words_to_check : list[list[str]]    
        list of list of words that will be used to check if word excist in language, every list of list take diffrent word length
    list_words_to_guess : list[list[str]]    
        list of list of words that player need to guess, every list of list take diffrent word length
    trees : list[Node.Node]
        trees with words to check, every tree take diffrent word length
    
    Methods
    -------
    unpack_words_collection(self, words: str, separator: str) -> list[list[str]]
        Take one string and change it to list of list of words, for the same word length in list. Used for words to check. 
    -------    
    unpack_words_to_guess(self, words: str) -> list[list[str]]  
        Take one string and change it to list of list of words, for the same word length in list. Used for words to guess.     
    -------    
    get_checking_trees(self) -> list[Node.Node]
        Return trees.   
    -------    
    get_guess_words(self) -> list[list[str]]
        Return list_words_to_guess.
    -------    
    add_scores(self, win: bool, number_of_letters_in_word: int) -> None
        Add win or lose, to your statistics in txt file.       
    -------
    save_options(self, word_length: int, show_letters: str) -> None
        Save options in config file.     
    ------- 
    save_game(self, list_of_guesses: list[list[str]]) -> None    
        Save your game, with all rounds, date, and number of rounds needed to win, in txt file.
    -------
    read_config(self) -> ConfigParser
        Open configuration file.
    -------
    change_string_for_list(self, words_from_file: str) -> list[list[str]]
        Translate one string to list of lists. Used for read round run from file.
    -------
    read_statistics(self) ->  list[tuple[str,str]]
        Read and process statistics from txt file.
    -------
    read_result(self) -> tuple((list[list[list[str]]],int, str))
        Read and process games/results from txt file.
    -------
    get_config_file(self) -> None
        Return config_file.
    """

    def __init__(self) -> None:
        """Constructs all the necessary attributes for the READING_FILE object, reading their vaules from files. """

        self.script_dir = os.path.dirname(__file__)
        self.config_file = self.read_config()

        self.scores_path = self.config_file['paths']['scoresPath']
        self.saved_games_path = self.config_file['paths']['savedGamesPath']
        words_for_checking_path  = self.config_file['paths']['checkWordsPath']
        guess_words_path  = self.config_file['paths']['guessWordsPath']

        with open(os.path.join(self.script_dir, words_for_checking_path), encoding="utf8") as f:
            text_open_for_checking = f.read()
        
        with open(os.path.join(self.script_dir, guess_words_path), encoding="utf8") as f2:
            text_open_guess_words = f2.read()

        self.min_word_length = int(self.config_file['base']['minWordLength'])
        self.max_word_length = int(self.config_file['base']['maxWordLength'])
        self.tree_deep = int(self.config_file['base']['treeDeep'])
        self.number_of_rounds = int(self.config_file['base']['numberOfRounds'])

        self.list_words_to_check = self.unpack_words_collection(text_open_for_checking,"\n")
        self.list_words_to_guess = self.unpack_words_to_guess(text_open_guess_words)
        self.trees = []

        for i in range(self.max_word_length-self.min_word_length+1):
            self.trees.append(Node.NODE(self.tree_deep))
            for j in self.list_words_to_check[i]:
                self.trees[i].add_word(j.lower())  

        for i in range(self.max_word_length-self.min_word_length+1):
            for j in self.list_words_to_guess[i]:
                self.trees[i].add_word(j.lower())  

 


    def unpack_words_collection(self, words: str, separator: str) -> list[list[str]]:
        """
        Take one string and change it to list of list of words, for the same word length in list. Used for words to check. 

        Parameters
        ----------
        words : str
            String that is seprate into words
        separator : str
            String that is used as seprator for words parameter    

        Returns
        -------
        list[list[str]]
        """
        if separator != "":
            splitted_words = words.split(separator)
        else:
            splitted_words  = words
        list = []
        for i in range(self.max_word_length-self.min_word_length+1):
            list.append([])   
        for i in splitted_words:
           if len(i) >= self.min_word_length and len(i) <= self.max_word_length:
                list[self.min_word_length-self.max_word_length+len(i)-1].append(i)
        return list


    def unpack_words_to_guess(self, words: str) -> list[list[str]]:
        """
        Take one string and change it to list of list of words, for the same word length in list. Used for words to guess.    

        Parameters
        ----------
        words : str
            String that is seprate into words  

        Returns
        -------
        list[list[str]]
        """
        guess_words = words.split(" ")
        guess_words_temp = []
        for i in guess_words:
            equalIndeks = i.find('=')
            if equalIndeks != -1:
              guess_words_temp.append(i[0:equalIndeks])
            else:
                guess_words_temp.append(i)
        guess_words_temp = self.unpack_words_collection(guess_words_temp,"")
        return guess_words_temp


    def get_checking_trees(self) -> list[Node.NODE]:
        """Return trees (words for checking)."""
        return self.trees

    def get_guess_words(self) -> list[list[str]]:
        """Return list_words_to_guess."""
        return self.list_words_to_guess

    def add_scores(self, win: bool, number_of_letters_in_word: int) -> None:
        """
        Add win or lose, to your statistics in txt file.    

        Parameters
        ----------
        win : bool
            If player guessed the word, or not 
        number_of_letters_in_word : int
            Number of letters in word
        Returns
        -------
        None
        """
        file_name = self.scores_path
        if not os.path.exists(os.path.join(self.script_dir, file_name)): 
            with open(os.path.join(self.script_dir, file_name), 'x') as f:
                f.write('[Scores]\n')
                f.write('Total Win Score = 0\n')
                f.write('Total Lose Score = 0\n')
                for i in range(self.min_word_length,self.max_word_length+1):
                    f.write(str(i)+' Letter Words Win = 0\n')
                    f.write(str(i)+' Letter Words Lose = 0\n')

        scores = ConfigParser()
        scores.read(os.path.join(self.script_dir, file_name))

        if win:
            scores['Scores']['Total Win Score']  = str(int(scores['Scores']['Total Win Score'])  + 1)
            scores['Scores'][str(number_of_letters_in_word)+' Letter Words Win']  = str( int(scores['Scores'][str(number_of_letters_in_word)+' Letter Words Win'])  + 1)
        else:
            scores['Scores']['Total Lose Score']  = str(int(scores['Scores']['Total Lose Score'])  + 1)
            scores['Scores'][str(number_of_letters_in_word)+' Letter Words Lose'] = str( int(scores['Scores'][str(number_of_letters_in_word)+' Letter Words Lose']) + 1)   
        
        with open(os.path.join(self.script_dir, file_name),'w+') as score_file:
            scores.write(score_file)

    def save_options(self, word_length: int, show_letters: str) -> None:
        """
        Save options in config file.      

        Parameters
        ----------
        word_length : int
            Word length while playing, will be saved in config file
        show_letters : str
            If show letters in games history, will be saved in config file
        Returns
        -------
        None
        """        
        file_name = "Config.ini"
        self.config_file['options']['wordLength'] = str(word_length)
        self.config_file['options']['showLetters'] = show_letters

        with open(os.path.join(self.script_dir, file_name),'w+') as config_file:
            self.config_file.write(config_file)

    def save_game(self, list_of_guesses: list[list[str]]) -> None:
        """
        Save your game, with all rounds, date, and number of rounds needed to win, in txt file.  

        Parameters
        ----------
        list_of_guesses : list[list[str]]
            All words in round that player tried, with information about certain letter if they were inplace, known or out
        Returns
        -------
        None
        """
        file_name = self.saved_games_path
        if not os.path.exists(os.path.join(self.script_dir, file_name)): 
            open(os.path.join(self.script_dir, file_name), 'x')
        saved_games = ConfigParser()
        saved_games.read(os.path.join(self.script_dir, file_name))
        saved_games.add_section("Game - "+ str(len(saved_games.sections())+1))
        for i in range(len(list_of_guesses)):
            saved_games.set("Game - "+ str(len(saved_games.sections())),"round "+str(i), str(list_of_guesses[i]))  
        saved_games.set("Game - "+ str(len(saved_games.sections())),"number of needed words", str(len(list_of_guesses)))     
        saved_games.set("Game - "+ str(len(saved_games.sections())),"date ", datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S") )
        with open(os.path.join(self.script_dir, file_name),'w+') as games_file:
            saved_games.write(games_file)


    def read_config(self) -> ConfigParser:
        """Open configuration file, and return this configuration"""
        file_name = "Config.ini"
        config = ConfigParser()
        config.read(os.path.join(self.script_dir, file_name))
        return config
            

    def change_string_for_list(self, words_from_file: str) -> list[list[str]]:
        """
        Translate one string to list of lists. Used for read round run from file.

        Parameters
        ----------
        words_from_file : str
            One string with combined infomration about the word that player guessed in rounds, and about letters, if they were inplace, known or out
        Returns
        -------
        None
        """
        sp = words_from_file.split("'")
        list_of_round_run = []
        iter = 0
  
        for i in range(len(sp)):
            if i % 2 != 0 and iter % 4 == 1:
                list_of_round_run.append(["",""])
                list_of_round_run[int(i//4)][0] = sp[i]
            elif i % 2 != 0 and iter % 4 == 3:
                list_of_round_run[int(i//4)][1] = sp[i]
            iter += 1
        return list_of_round_run

    
    def read_statistics(self) ->  list[tuple[str,str]]:
        """Read and process statistics from txt file, return list of tuples of str and str, that represents kind of score and score"""
        file_name = self.scores_path
        statistics = ConfigParser()
        statistics.read(os.path.join(self.script_dir, file_name))
        output_tabel = []
        for i in statistics["Scores"].keys():
            output_tabel.append((i,statistics["Scores"][i]))   
        return output_tabel


    def read_result(self) -> tuple((list[list[list[str]]],int, str)):
        """Read and process games/results from txt file, return tuple of list containing game run, with all player's gauesses, number of rounds needed to win, date of a win"""
        file_name = self.saved_games_path
        saved_games = ConfigParser()
        saved_games.read(os.path.join(self.script_dir, file_name))
        output_tabel = []
        for game in saved_games.values():
            if game.name != "DEFAULT":
                numberOfNeededWords = int(game["number of needed words"])
                roundScenario = [self.change_string_for_list(game["round " + str(i)]) for i in range(numberOfNeededWords)]
                output_tabel.append((roundScenario, numberOfNeededWords , game["date"]))
        return output_tabel 



    def get_config_file(self) -> ConfigParser:
        """Return config_file."""
        return self.config_file
