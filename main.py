import random
import ReadingFile
from tkinter import *  


class GAME():
    """
    A class to represent a game with GUI.

    ...

    Attributes
    ----------
    read : READING_FILE
        give access to reading a configuration, words to guess and check, saving games and statistics
    MIN_WORD_LENGTH : int
        minimal word length thta user can choose in options
    MAX_WORD_LENGTH : int
        maximum word length thta user can choose in options
    NUMBER_OF_ROUNDS : int
        number of chances that have to guess a word
    COLOR_IN_PLACE  : str
        color of background behind letter if it stands in a correct place in word
    COLOR_KNOWN 
        color of background behind letter if it excist in word but stands in incorrect place
    COLOR_OUT : str
        color of background behind letter if it doesn't excist in word
    COLOR_LETTERS_FRAME : str
        color of background in letters frame
    COLOR_OPTION_FRAME : str  
        color of background in option frame
    COLOR_WORDS_IN_PANEL : str
        color of background in words panels
    COLOR_BACK_GROUND : str   
        color of background in options, result and game
    MESSAGE_FOR_WINNIG : str
        message that is display after user win
    MESSAGE_FOR_LOSING : str
        message that is display after user lose

    word_length : int
        word length correct with current options
    show_letters : str
        if show letters in games history or not
    current_letter_index : int
        amount of letters that user input 
    current_word_index : int
        amount of words that user input 
    current_word : str
        word that user currently typing 
    round_history : list[list[str]]                                                                                                             
        keep all words, that user input with specified if letter in the word was inplace, known or out
    guess_word : str
        random word that user need to guess
    read_check : list[NODE]
        trees for cheching if word excist in language
    read_guess : list[list[str]]
        list of list of words, grouped by word length 
    
    Methods
    -------
    check_words(self, word: str, guess: str) -> list[list[str]]
        Compare guess word with user guess, to check how similar they are, and to specifie if letters in user word are inplace, known or out. 
    play(self) -> None
        Open new window with a game, set all buttons and label, prepare for play.    
    results(self) -> None
        Open new window with all saved games and statistics from previous games.
    options(self) -> None
        Open new window with options, like length of word. 
    start_screen(self) -> None
        Open menu screen.
    """

    def __init__(self) -> None:
        """Constructs all the necessary attributes for the Game object."""
        self.read = ReadingFile.READING_FILE()
        config_file = self.read.get_config_file()

        self.MIN_WORD_LENGTH = self.read.min_word_length
        self.MAX_WORD_LENGTH = self.read.max_word_length
        self.NUMBER_OF_ROUNDS = self.read.number_of_rounds

        self.COLOR_IN_PLACE = config_file['colors']['colorInPlace']
        self.COLOR_KNOWN   = config_file['colors']['colorKnown']
        self.COLOR_OUT     = config_file['colors']['colorOut']
        self.COLOR_LETTERS_FRAME  = config_file['colors']['colorLettersFrame']
        self.COLOR_OPTION_FRAME   = config_file['colors']['colorOptionFrame']
        self.COLOR_WORDS_IN_PANEL  = config_file['colors']['colorWordsInPanel']
        self.COLOR_BACK_GROUND    = config_file['colors']['colorBackground']

        self.MESSAGE_FOR_WINNIG = config_file['messages']['messageForWinnig']
        self.MESSAGE_FOR_LOSING = config_file['messages']['messageForLossing']

        self.word_length =  int(config_file['options']['wordLength'])
        self.show_letters = config_file['options']['showLetters']

        self.current_letter_index = 0
        self.current_word_index = 0
        self.current_word = ""
        self.round_history = []
        self.guess_word = ""
        
       
        self.read_check = self.read.get_checking_trees()
        self.read_guess = self.read.get_guess_words()


    def compare_words(self, word: str, guess: str) -> list[list[str]]:
        """
        Compare guess word with user guess, to check how similar they are, and to specifie if letters in user word are inplace, known or out.

        Parameters
        ----------
        word : str
            Word that is base for comparement
        guess : str
            Word that is compared with word (user guess)
        Returns
        -------
        list[list[str]]
        """
        result_of_comparison = []
        for i in range(len(word)):
            result_of_comparison.append([guess[i],"unknown"])
            for j in range(len(word)):
                if i == j and guess[i] == word[j]:
                    result_of_comparison[i][1] = "inplace"
                elif i != j and guess[i] == word[j] and result_of_comparison[i][1] != "inplace":
                    result_of_comparison[i][1] = "known"
                elif result_of_comparison[i][1] != "inplace" and result_of_comparison[i][1] != "known":
                    result_of_comparison[i][1] = "out"   
                else:
                    pass    
        return result_of_comparison

    def play(self, frame_menu, root_menu) -> None:
        """
        Open window with game.

        Parameters
        ----------
        frame_menu : tk.Frame
            Define set of menu buttons
        root_menu : t.Tk 
            Main root of a gui.
        Returns
        -------
        None
        """ 
        def delete() -> None:
            """Delete letter from last word that user is typing, update current_letter_index, current_word, letters_buttons. Change label to normal state."""
            comunicat_label.config(text=" ")   
            if self.current_letter_index > 0:
                self.current_letter_index -= 1 
                self.current_word = self.current_word[0:-1]
                letters_buttons[self.current_word_index][self.current_letter_index].config(text="  ")
                
        def letter(letter: str) -> None:
            """
            Add letter from last word that user is typing, update current_letter_index, current_word, letters_buttons. Change label to normal state.
    
            Parameters
            ----------
            letter : str
                Define which letter shloud be add to a word
            Returns
            -------
            None
            """
            comunicat_label.config(text=" ")   
            if self.current_letter_index < self.word_length:
                letters_buttons[self.current_word_index][self.current_letter_index].config(text=letter)
                self.current_letter_index += 1
                self.current_word += letter
            
        def enter() -> None:
            """
            Check if current_word the same length as word_length require and word is excisting in language,
                if it is then compare those words, and define letters if they are inplace, known or out,
                then update letters_buttons and button_dic
                then check if user win 
                    if he/she did display a winning message, add scores and clear variables
                then check if user lost
                    if he/she did display a losing message and add scores  
                if it isn't it show comunicat what is wrong  
            """
            if len(self.current_word) == self.word_length and self.read_check[self.word_length + self.MIN_WORD_LENGTH - self.MAX_WORD_LENGTH-1].search_for_word(self.current_word.lower()):
                result_of_comparison = self.compare_words(self.guess_word.lower(), self.current_word.lower())    
                for i in range(len(result_of_comparison)):
                    if result_of_comparison[i][1] == "inplace":
                        letters_buttons[self.current_word_index][i].config(bg=self.COLOR_IN_PLACE)
                        button_dic[result_of_comparison[i][0]].config(bg=self.COLOR_IN_PLACE)
                    elif result_of_comparison[i][1] == "known":
                        letters_buttons[self.current_word_index][i].config(bg=self.COLOR_KNOWN)
                        button_dic[result_of_comparison[i][0]].config(bg=self.COLOR_KNOWN)
                    else:
                        letters_buttons[self.current_word_index][i].config(bg=self.COLOR_OUT) 
                        button_dic[result_of_comparison[i][0]].config(bg=self.COLOR_OUT)      

                self.round_history.append(result_of_comparison) 
                if self.guess_word.lower() == self.current_word.lower():
                    comunicat_label.config(text=self.MESSAGE_FOR_WINNIG)
                    clear_variables()
                    self.read.add_scores(True, len(self.guess_word))
                    save_result_button.config(state="normal")
                    play_again_button.config(state="normal")
                else:
                    self.current_word_index += 1
                    self.current_letter_index = 0
                    self.current_word = ""

                if self.current_word_index>=self.NUMBER_OF_ROUNDS:
                    self.read.add_scores(False, len(self.guess_word))
                    play_again_button.config(state="normal")
                    comunicat_label.config(text=self.MESSAGE_FOR_LOSING)
                    word_label.config(text=self.guess_word)
            elif len(self.current_word) != self.word_length:
                comunicat_label.config(text="Zbyt krótkie słowo")
            else:
                comunicat_label.config(text="Nie istnieje takie słowo")   

        def exit_play() -> None:
            """Clear variables and close the window"""
            clear_variables()
            frame_menu.pack(padx=75, pady=170)
            game.destroy()

        def clear_variables() -> None:
            """Clear variables that are used inside of a game"""
            self.current_word = ""
            self.current_letter_index = 0
            self.current_word_index = 0

        def play_again() -> None:
            """Clear variables, clear round history, set new word to geuss, prepare GUI"""
            clear_variables()
            self.round_history.clear()
            set_new_word()
            print(self.guess_word)
            for i in letters_buttons:
                for j in i:
                    j.config(text=str(" "),bg=self.COLOR_WORDS_IN_PANEL)

            for button in button_dic.values():
                button.config(bg="#FFFAFA")  
            save_result_button.config(state="disabled")
            play_again_button.config(state="disabled")
            comunicat_label.config(text="")
            word_label.config(text="")
        
        def save_result() -> None:
            """Save game history in file"""
            save_result_button.config(state="disabled")
            self.read.save_game(self.round_history)

        def set_new_word() -> None:
            """Set new word to guess"""
            self.guess_word = self.read_guess[self.word_length + self.MIN_WORD_LENGTH - self.MAX_WORD_LENGTH-1][random.randrange(0,len(self.read_guess[self.word_length + self.MIN_WORD_LENGTH - self.MAX_WORD_LENGTH-1]))]


        frame_menu.pack_forget()
        game = Frame(root_menu, bg=self.COLOR_BACK_GROUND)
        game.pack(padx=75, pady=25)

        self.round_history = []
        set_new_word()
        print(self.guess_word)

        self.current_letter_index = 0
        self.current_word = ""
        self.current_word_index = 0
  
        frame_panel = Frame(game, pady=20, bg = self.COLOR_BACK_GROUND)
        frame_panel.pack()
        letters_buttons = []
        for i in range(self.NUMBER_OF_ROUNDS):
            letters_buttons.append([])
            for j in range(self.word_length):
                letters_buttons[i].append(Button(frame_panel,text=str(" "),bg=self.COLOR_WORDS_IN_PANEL,state="disabled",height=1,width=2,font=("Arial", 15)))
                letters_buttons[i][j].grid(row=i,column=j)
        frame_letters_combined = Frame(game, bg=self.COLOR_LETTERS_FRAME )
        frame_letters_combined.pack(padx=5,pady=5)

        frame_letters_1 = Frame(frame_letters_combined, bg=self.COLOR_LETTERS_FRAME )
        frame_letters_1.pack()
        frame_letters_2 = Frame(frame_letters_combined, bg=self.COLOR_LETTERS_FRAME )
        frame_letters_2.pack()
        frame_letters_3 = Frame(frame_letters_combined, bg=self.COLOR_LETTERS_FRAME )
        frame_letters_3.pack()
        frame_letters_4 = Frame(frame_letters_combined, bg=self.COLOR_LETTERS_FRAME )
        frame_letters_4.pack()
        
        frame_options = Frame(game, bg=self.COLOR_OPTION_FRAME )
        frame_options.pack()
        frame_buttons_options = Frame(frame_options, bg=self.COLOR_OPTION_FRAME )
        frame_buttons_options.pack()
        
        exit_button = Button(frame_buttons_options, text="Powrót",padx=5,pady=10,command=exit_play)
        exit_button.grid(row=0,column=0)

        save_result_button = Button(frame_buttons_options, text="Zapisz wynik",padx=5,pady=10,command=save_result,state="disabled")
        save_result_button.grid(row=0,column=1)

        play_again_button = Button(frame_buttons_options, text="Zagraj ponownie",padx=5,pady=10,command=play_again,state="disabled")
        play_again_button.grid(row=0,column=2)


        comunicat_label = Label(frame_options, text="",padx=5,pady=10,bg=self.COLOR_LETTERS_FRAME,font=("Arial", 25))
        comunicat_label.pack()
        word_label = Label(frame_options, text="",padx=5,pady=10,bg=self.COLOR_LETTERS_FRAME,font=("Arial", 20))
        word_label.pack()
       
        
     
        button_dic = {
        "q" :   Button( frame_letters_1, text="Q",command=lambda temp="Q" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "w" :   Button( frame_letters_1, text="W",command=lambda temp="W" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "e" :   Button( frame_letters_1, text="E",command=lambda temp="E" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "r" :   Button( frame_letters_1, text="R",command=lambda temp="R" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "t" :   Button( frame_letters_1, text="T",command=lambda temp="T" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "y" :   Button( frame_letters_1, text="Y",command=lambda temp="Y" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "u" :   Button( frame_letters_1, text="U",command=lambda temp="U" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "i" :   Button( frame_letters_1, text="I",command=lambda temp="I" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "o" :   Button( frame_letters_1, text="O",command=lambda temp="O" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "p" :   Button( frame_letters_1, text="P",command=lambda temp="P" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),

        "a" :   Button( frame_letters_2, text="A",command=lambda temp="A" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "s" :   Button( frame_letters_2, text="S",command=lambda temp="S" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "d" :   Button( frame_letters_2, text="D",command=lambda temp="D" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "f" :   Button( frame_letters_2, text="F",command=lambda temp="F" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "g" :   Button( frame_letters_2, text="G",command=lambda temp="G" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "h" :   Button( frame_letters_2, text="H",command=lambda temp="H" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "j" :   Button( frame_letters_2, text="J",command=lambda temp="J" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "k" :   Button( frame_letters_2, text="K",command=lambda temp="K" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "l" :   Button( frame_letters_2, text="L",command=lambda temp="L" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "m" :   Button( frame_letters_2, text="M",command=lambda temp="M" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),

        "Del" :    Button( frame_letters_3, text="Del",command=delete,bg="#FFFAFA",font=("Arial", 12)),
        "z" :  Button( frame_letters_3, text="Z",command=lambda temp="Z" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "x" :  Button( frame_letters_3, text="X",command=lambda temp="X" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "c" :  Button( frame_letters_3, text="C",command=lambda temp="C" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "v" :  Button( frame_letters_3, text="V",command=lambda temp="V" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "b" :  Button( frame_letters_3, text="B",command=lambda temp="B" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "n" :  Button( frame_letters_3, text="N",command=lambda temp="N" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "Enter" :    Button( frame_letters_3, text="Enter",command=enter,bg="#FFFAFA",font=("Arial", 12)),

        "ą" :    Button( frame_letters_4, text="Ą",command=lambda temp="Ą" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "ć" :    Button( frame_letters_4, text="Ć",command=lambda temp="Ć" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "ę" :    Button( frame_letters_4, text="Ę",command=lambda temp="Ę" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "ł" :    Button( frame_letters_4, text="Ł",command=lambda temp="Ł" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "ń" :    Button( frame_letters_4, text="Ń",command=lambda temp="Ń" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "ó" :    Button( frame_letters_4, text="Ó",command=lambda temp="Ó" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "ś" :    Button( frame_letters_4, text="Ś",command=lambda temp="Ś" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "ź" :    Button( frame_letters_4, text="Ź",command=lambda temp="Ź" : letter(temp),bg="#FFFAFA",font=("Arial", 12)),
        "ż" :    Button( frame_letters_4, text="Ż",command=lambda temp="Ż" : letter(temp),bg="#FFFAFA",font=("Arial", 12))
        }
        
        button_dic["q"].grid(row=0,column=0)
        button_dic["w"].grid(row=0,column=1)
        button_dic["e"].grid(row=0,column=2)
        button_dic["r"].grid(row=0,column=3)
        button_dic["t"].grid(row=0,column=4)
        button_dic["y"].grid(row=0,column=5)
        button_dic["u"].grid(row=0,column=6)
        button_dic["i"].grid(row=0,column=7,ipadx=2)
        button_dic["o"].grid(row=0,column=8)
        button_dic["p"].grid(row=0,column=9)
        button_dic["a"].grid(row=0,column=0)
        button_dic["s"].grid(row=0,column=1)
        button_dic["d"].grid(row=0,column=2)
        button_dic["f"].grid(row=0,column=3)
        button_dic["g"].grid(row=0,column=4)
        button_dic["h"].grid(row=0,column=5)
        button_dic["j"].grid(row=0,column=6)
        button_dic["k"].grid(row=0,column=7)
        button_dic["l"].grid(row=0,column=8)
        button_dic["m"].grid(row=0,column=9)
        button_dic["Del"].grid(row=0,column=0)
        button_dic["z"].grid(row=0,column=1)
        button_dic["x"].grid(row=0,column=2)
        button_dic["c"].grid(row=0,column=3)
        button_dic["v"].grid(row=0,column=4)
        button_dic["b"].grid(row=0,column=5)
        button_dic["n"].grid(row=0,column=6)
        button_dic["Enter"].grid(row=0,column=8)
        button_dic["ą"].grid(row=0,column=0)
        button_dic["ć"].grid(row=0,column=1)
        button_dic["ę"].grid(row=0,column=2)
        button_dic["ł"].grid(row=0,column=3)
        button_dic["ń"].grid(row=0,column=4)
        button_dic["ó"].grid(row=0,column=5)
        button_dic["ś"].grid(row=0,column=6)
        button_dic["ź"].grid(row=0,column=7)
        button_dic["ż"].grid(row=0,column=8)

    def results(self, frame_menu, root_menu) -> None:
        """
        Open window with games history and statistics.

        Parameters
        ----------
        frame_menu : tk.Frame
            Define set of menu buttons
        root_menu : t.Tk 
            Main root of a gui.
        Returns
        -------
        None
        """

        def show_statistics():
            """Change view from games history to statistics"""
            change_button.config(text="Gry", command = show_games)
            frame_games.pack_forget()
            stat_frame.pack()

        def show_games(): 
            """"Change view from statistics to games history"""   
            change_button.config(text="Wyniki", command=show_statistics)
            stat_frame.pack_forget()
            frame_games.pack(fill=BOTH, expand=1)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((310,0), window=frame_games_2)



        def exit_result():
            result_panel.destroy()
            frame_menu.pack(padx=75, pady=170)         

        frame_menu.pack_forget()
        result_panel = Frame(root_menu, bg=self.COLOR_BACK_GROUND, height=600, width=400)
        result_panel.pack(padx=75, pady=100, fill=Y, ipadx= 50, ipady=100)

        button_frame = Frame(result_panel, bg=self.COLOR_BACK_GROUND)
        button_frame.pack(pady=2)

        change_button = Button(button_frame, text="Wyniki", command=show_statistics)
        change_button.grid(row=0, column=0, ipadx=10)

        exit_button = Button(button_frame, text="Wyjdź", command=exit_result)
        exit_button.grid(row=0, column=1,ipadx=2)

        results = self.read.read_result()
        statistics = self.read.read_statistics()
        frames = []

        frame_games = Frame(result_panel, bg=self.COLOR_BACK_GROUND)
        frame_games.pack(fill=BOTH, expand=1) 

        stat_frame = Frame(result_panel, bg=self.COLOR_BACK_GROUND)
        for stat in statistics:
            Label(stat_frame, text=stat[0]+":  "+stat[1],font=("Arial", 14), bg=self.COLOR_BACK_GROUND).pack()

        canvas = Canvas(frame_games, bg=self.COLOR_BACK_GROUND)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = Scrollbar(frame_games, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        frame_games_2 = Frame(canvas, bg=self.COLOR_BACK_GROUND)

        canvas.create_window((220,0), window=frame_games_2)
        
        for i in range(len(results)):
            frames.append(Frame(frame_games_2,bg=self.COLOR_BACK_GROUND))
            frames[i].pack()
            data =  Frame(frames[i],bg=self.COLOR_BACK_GROUND)
            data.pack()
            scenario = Frame(frames[i],bg=self.COLOR_BACK_GROUND)
            scenario.pack()
            Label(data,text = "\nGra - "+str(i), font=("Arial", 15),bg=self.COLOR_BACK_GROUND).pack()
            Label(data,text = str(results[i][2]), font=("Arial", 12),bg=self.COLOR_BACK_GROUND).pack()
            for round in range(len(results[i][0])):
                for j in range(len(results[i][0][round])):
                    if results[i][0][round][j][1] == "inplace":
                        if self.show_letters.__eq__("Tak"):
                            Button(scenario,bg=self.COLOR_IN_PLACE, text=results[i][0][round][j][0].capitalize(),state="disabled",height=2,width=2).grid(row=round, column=j)
                        else:
                            Button(scenario,bg=self.COLOR_IN_PLACE, state="disabled",height=2,width=2).grid(row=round, column=j)
                    elif  results[i][0][round][j][1] == "known":
                        if self.show_letters.__eq__("Tak"):
                            Button(scenario,bg=self.COLOR_KNOWN, text=results[i][0][round][j][0].capitalize(),state="disabled",height=2,width=2).grid(row=round, column=j,)
                        else:
                            Button(scenario,bg=self.COLOR_KNOWN, state="disabled",height=2,width=2).grid(row=round, column=j,)
                    else:
                        if self.show_letters.__eq__("Tak"):
                            Button(scenario,bg=self.COLOR_OUT, text=results[i][0][round][j][0].capitalize(),state="disabled",height=2,width=2).grid(row=round, column=j)
                        else:
                            Button(scenario,bg=self.COLOR_OUT, state="disabled",height=2,width=2).grid(row=round, column=j)


       

    def options(self, frame_menu, root_menu) -> None:
        """
        Open window with options.

        Parameters
        ----------
        frame_menu : tk.Frame
            Define set of menu buttons
        root_menu : t.Tk 
            Main root of a gui.
        Returns
        -------
        None
        """

        frame_menu.pack_forget()
        options = Frame(root_menu, bg=self.COLOR_BACK_GROUND, height=400 , width=300)
        options.pack(padx=90, pady=120)

        def out_of_options():
            """Save changes and close window"""
            self.word_length = word_length.get()
            self.show_letters = show_letters.get()
            self.read.save_options(self.word_length, self.show_letters)
            options.destroy()
            frame_menu.pack(padx=75, pady=170)

            
        word_length = IntVar()
        word_length.set(self.word_length)
        
        Label(options,text="Długość słowa w grze: ",bg=self.COLOR_BACK_GROUND, font=("Arial", 10)).pack(anchor="w")
        for i in range(self.MIN_WORD_LENGTH,self.MAX_WORD_LENGTH+1):
            Radiobutton(options, text=str(i), variable=word_length, value=i, bg=self.COLOR_BACK_GROUND).pack(anchor='w')

        show_letters = StringVar()
        show_letters.set(self.show_letters)
        
        Label(options,text="Pokazuj litery przy wynikach: ",bg=self.COLOR_BACK_GROUND, font=("Arial", 10)).pack(anchor="w")
        Radiobutton(options, text="Tak", variable=show_letters, value="Tak", bg=self.COLOR_BACK_GROUND).pack(anchor='w')
        Radiobutton(options, text="Nie", variable=show_letters, value="Nie", bg=self.COLOR_BACK_GROUND).pack(anchor='w')

        Button(options,text="Zapisz i wyjdź",command=out_of_options,bg="#F08080",height = 1,width=10).pack(anchor='sw', pady=30)

        
        

    def start_screen(self) -> None:
        """Open menu screen"""
        root = Tk()
        root.title("Wordle")
        root.geometry("600x600")
        root.config(bg=self.COLOR_BACK_GROUND)
        #root.resizable(False, False)

        frame_menu = Frame(root, height=500 , width=400, bg=self.COLOR_BACK_GROUND) 
        frame_menu.pack(padx=75,pady=170)

        start_button = Button(frame_menu, bg="#87CEFA", text  = "Rozpocznij grę", padx=17, pady=10, command=lambda frame=frame_menu, rt=root : self.play(frame, rt))
        start_button.pack(padx=5,pady=5)

        results_button = Button(frame_menu, bg="#87CEFA", text  = "Wyniki", padx=37, pady=10, command=lambda frame=frame_menu, rt=root : self.results(frame, rt))
        results_button.pack(padx=5,pady=5)

        options_button = Button(frame_menu, bg="#87CEFA", text  = "Opcje", padx=40, pady=10,command=lambda frame=frame_menu, rt=root : self.options(frame, rt))
        options_button.pack(padx=5,pady=5)

        end_button = Button(frame_menu, bg="#87CEFA", text  = "Wyjdź", padx=40, pady=10, command=root.destroy)
        end_button.pack(padx=5,pady=5)

        root.mainloop()

game = GAME()
game.start_screen()    
