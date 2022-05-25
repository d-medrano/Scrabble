class Pawns():

    points = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,
        'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1,
        'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
    }
    '''Letter points'''

    def __init__(self):
        self.letters = []
    
    def __str__(self):
        return ''.join(self.letters)
    
    def addPawn(self, c):
        '''
        Appends a new letter
            Args:
                c (str): new letter
        '''
        self.letters.append(c)

    def addPawns(self, c, n):
        '''
        Appends "n" times the same new letter "c"
            Args:
                c (str): new letter
                n (int): total number of inclusions
        '''
        for _ in range(n):
            self.addPawn(c)
     
    def createBag(self):
        '''
        Appends the total amount of letters in the game
        '''
        import pandas as pd
        all_pawns = pd.read_csv('bag_of_pawns.csv')
        for item in all_pawns.itertuples():
            self.addPawns(item[1], item[2])

    def getFrequency(self):
        '''
        Creates a "FrequencyTable" object with the letter content
            Returns:
                (FrequencyTable): frequencies for each letter
        '''
        fq = FrequencyTable()
        for letter in self.letters:
            fq.update(letter)
        return fq

    def showPawns(self):
        '''
        Prints the list of letters and their frequencies
        '''
        self.getFrequency().showFrequency()
    
    def takeRandomPawn(self):
        '''
        Takes a random pawns out of the letter content
            Returns:
                (str): extracted letter
        '''
        from numpy import random
        extracted = random.choice(self.letters)
        self.letters.remove(extracted)
        return extracted
    
    def takePawn(self, c):
        '''
        Removes letter "c"
            Args:
                c (str): letter to be removed
        '''
        self.letters.remove(c)
    
    def getTotalPawns(self):
        '''
        Total number of letters
            Returns:
                (int): Total number of letters
        '''
        return len(self.letters)
    
    @staticmethod
    def getPoints(c):
        '''
        Score of a single letter "c"
            Args:
                c (str): letter
            Returns:
                (int): Letter score
        '''
        return Pawns.points[c]
    
    @staticmethod
    def showPawnsPoints():
        print("Pawns' points:")
        i = 1
        for c in Pawns.points:
            c_points = Pawns.getPoints(c)
            print('"{}": {}{}'.format(c, ' ' if c_points < 10 else '', c_points),
                end = '    ' if i % 3 != 0 else '\n')
            i += 1


class Word():

    def __init__(self):
        self.word = []
    
    def __str__(self):
        return ''.join(self.word)
    
    def areEqual(self, w):
        '''
        Checks whether a word is equal to the object
            Args:
                w (Word): word to check
            Returns:
                (bool): True/False
        '''
        if self.getLengthWord() != w.getLengthWord():
            return False
        else:
            for i in range(self.getLengthWord()):
                if self.word[i] != w.word[i]:
                    return False
        return True
    
    def isEmpty(self):
        '''
        Checks whether the length of a word is 0 or not
            Returns:
                (bool): True/False
        '''
        return not bool(self.getLengthWord())
    
    def getFrequency(self):
        '''
        Creates a "FrequencyTable" object with the letter content of the word
            Returns:
                (FrequencyTable): frequencies for each letter
        '''
        fq = FrequencyTable()
        for letter in self.word:
            fq.update(letter)
        return fq
    
    @classmethod
    def readWord(cls):
        '''
        Reads a word from user input
            Returns:
                (Word): input word
        '''
        w = cls()
        while len(input_word := input('- Word: ').upper()) == 0:
            print('Please, introduce a word...\n')
        w.word.extend(list(input_word))
        return w
    
    @classmethod
    def readWordFromFile(cls, f):
        '''
        Reads a word from a file
            Args:
                f (file): file with some word content
            Returns:
                (Word): read word
        '''
        w = cls()
        w.word.extend(list(f.readline()[:-1]))
        return w
    
    def getLengthWord(self):
        '''
        Gets the length of a word
            Returns:
                (int): length of the word
        '''
        return len(self.word)


class Dictionary():

    filepath = 'dictionary.txt'
    '''Full path with the dictionary filename'''

    @staticmethod
    def validateWord(word):
        '''
        Checks whether a particular word is contained in the dictionary
            Args:
                word (Word): word to be searched on the dictionary
            Returns:
                (bool): True / False
        '''
        with open(Dictionary.filepath, 'r') as f:
            while not (line := Word.readWordFromFile(f)).isEmpty():
                if word.areEqual(line):
                    return True
            print(f'"{word}" not in dictionary!')
            return False
    
    @staticmethod
    def showWord(pawns):
        '''
        Prints all possible words in the dictionary that can be formed with the letters in pawns
            Args:
                pawns (Pawns): set of letters
        '''
        freq_pawns = pawns.getFrequency()
        with open(Dictionary.filepath, 'r') as f:
            i = 1
            while not (line := Word.readWordFromFile(f)).isEmpty():
                if FrequencyTable.isSubset(line.getFrequency(), freq_pawns):
                    print(line, end = (' '*(10-line.getLengthWord()) if i % 6 != 0 else '\n'))
                    i += 1

    @staticmethod
    def showWordPlus(pawns, c):
        '''
        Prints all possible words in the dictionary that can be formed with the letters in "pawns" and contains an additional letter "c" of the board
            Args:
                pawns (Pawns): set of letters
                c (str): additional letter of the board
        '''
        freq_pawns = pawns.getFrequency()
        freq_pawns.update(c)
        with open(Dictionary.filepath, 'r') as f:
            i = 1
            while not (line := Word.readWordFromFile(f)).isEmpty():
                if FrequencyTable.isSubset(line.getFrequency(), freq_pawns) and c in line.word:
                    print(line, end = (' '*(10-line.getLengthWord()) if i % 6 != 0 else '\n'))
                    i += 1


class FrequencyTable():

    def __init__(self):
        import pandas as pd
        letters = pd.read_csv('bag_of_pawns.csv')['Letter'].values.tolist()
        self.letters = letters
        self.frequencies = [0 for _ in range(len(letters))]
    
    def showFrequency(self):
        '''
        Prints the list of letters and frequencies
        '''
        for i in range(len(self.letters)):
            if self.frequencies[i] != 0:
                print(f'{self.letters[i]}: {self.frequencies[i]}')
    
    def update(self, c):
        '''
        Updates the list of frequencies by +1 to the corresponding letter
            Args:
                c (str): letter to be updated
        '''
        self.frequencies[self.letters.index(c)] += 1
    
    @staticmethod
    def isSubset(obj1, obj2):
        '''
        Checks whether the set of letters on the first object is a subset of the second object
            Args:
                obj1 (FrequencyTable): first object - smaller set
                obj2 (FrequencyTable): second object - bigger set
            Returns:
                (bool): True / False
        '''
        for i in range(len(obj1.frequencies)):
            if obj1.frequencies[i] > obj2.frequencies[i]:
                return False
        return True


class Board():

    score = 0
    '''Total score of the game board'''

    def __init__(self):
        import numpy as np
        self.board = [[' ' for _ in range(15)] for _ in range(15)]
        self.totalWords = 0
        self.totalPawns = 0

    def showBoard(self):
        '''
        Prints the board grid with its letter content included
        '''
        print('\n   ', end='')
        for i in range(len(self.board)):
            print('  {}{}'.format(0 if i <= 9 else '', i), end='')
        print('   (Score: {})'.format(Board.score), end='')
        for i in range(len(self.board)):
            print('\n   ', end='')
            for _ in range(len(self.board)):
                print('+---', end='')
            print('+\n   ', end='')
            for j in range(len(self.board)):
                print('| {} '.format(self.board[i][j]), end='')
            print('| {}{}'.format(0 if i <= 9 else '', i), end='')
        print('\n   ', end='')
        for _ in range(len(self.board)):
            print('+---', end='')
        print('+\n')
    
    def placeWord(self, player_pawns, word, x, y, direction):
        '''
        Includes a new word on a given location of the game board and updates de score and the number of total words. Removes the corresponding letters from the player pawns.
            Args:
                player_panws (Pawns):
                word (Word): new word to introduce
                x (int): vertical position on the board (0-14)
                y (int): horizontal position on the board (0-14)
                direction (str): orientation of the word (horizontal - "H", vertical - "V")
        '''
        if direction.upper() == 'H':
            for i in range(word.getLengthWord()):
                letter = word.word[i]         
                if self.board[x][y+i] == ' ':
                    player_pawns.takePawn(letter)
                    self.board[x][y+i] = letter
                    Board.score += Pawns.getPoints(letter)
                    self.totalPawns += 1
        elif direction.upper() == 'V':
            for i in range(word.getLengthWord()):
                letter = word.word[i]
                if self.board[x+i][y] == ' ':
                    player_pawns.takePawn(letter)
                    self.board[x+i][y] = letter
                    Board.score += Pawns.getPoints(letter)
                    self.totalPawns += 1
        self.totalWords += 1
    
    def isPossible(self, word, x, y, direction):
        '''
        Checks whether a given word in a given position of the board can be placed.
            Args:
                word (Word): word to check
                x (int): horizontal position on the board (0-14)
                y (int): vertical position on the board (0-14)
                direction (str): orientation of the word (horizontal - "H", vertical - "V")
            Returns:
                (bool, str): True/False, message with a reason
        '''
        positions = []
        if direction.upper() == 'H':
            for i in range(word.getLengthWord()):
                positions.append((x, y+i))
            positions.extend([(x, y-1), (x, y+word.getLengthWord())])
        elif direction.upper() == 'V':
            for i in range(word.getLengthWord()):
                positions.append((x+i, y))
            positions.extend([(x-1, y), (x+word.getLengthWord(), y)])
        if self.totalWords == 0:
            if (7, 7) not in positions[:-2]:
                return False, 'No letter placed on the central square'
        else:
            if positions[-1][0] > 14 or positions[-1][1] > 14:
                return False, 'Word out of the board'
            for i in range(word.getLengthWord()):
                if self.board[positions[i][0]][positions[i][1]] != ' ':
                    break
            else:
                return False, 'Your word must include a previous existing letter on the board'
            for i in range(word.getLengthWord()):
                if self.board[positions[i][0]][positions[i][1]] != ' ' and self.board[positions[i][0]][positions[i][1]] != word.word[i]:
                    return False, 'There already exists a different word in these positions'
            added_pawns = []
            for i in range(word.getLengthWord()):
                if self.board[positions[i][0]][positions[i][1]] == ' ':
                    added_pawns.append(word.word[i])
            if len(added_pawns) == 0:
                return False, 'You are not adding a single letter to the board'
            if ((positions[-2][0] != -1 and positions[-2][1] != -1 and self.board[positions[-2][0]][positions[-2][1]] != ' ') 
                or (positions[-1][0] != 15 and positions[-1][1] != 15 and self.board[positions[-1][0]][positions[-1][1]] != ' ')):
                return False, 'There are additional letters at the beginning or ending of your word'
        return True, 'You can add your word'

    def getPawns(self, word, x, y, direction):
        '''
        Creates and object with the needed letters to place a given word on the board on a specific location
            Args:
                word (Word): word to include on the board
                x (int): horizontal position on the board (0-14)
                y (int): vertical position on the board (0-14)
                direction (str): orientation of the word (horizontal - "H", vertical - "V")
            Returns:
                (Pawns): letters needed to include the new word
        '''    
        letters = Pawns()
        if direction.upper() == 'H':
            for i in range(word.getLengthWord()):
                if word.word[i] != self.board[x][y+i]:
                    letters.addPawn(word.word[i])
        elif direction.upper() == 'V':
            for i in range(word.getLengthWord()):
                if word.word[i] != self.board[x+i][y]:
                    letters.addPawn(word.word[i])
        return letters
    
    def showWordPlacement(self, pawns, word):
        '''
        Prints all valid placements for a given word on the board
            Args:
                pawns (Pawns): available player letters to form the word
                word (Word): given word to place on the board
        '''
        freq_pawns = pawns.getFrequency()
        n_words = {'H': 0, 'V': 0}
        for d in ['H', 'V']:
            print('{} positions:'.format('- Horizontal' if d == 'H' else '- Vertical'))
            for i in range(15):
                for j in range(15):
                    if self.isPossible(word, i, j, d)[0]:
                        needed_pawns = self.getPawns(word, i, j, d)
                        if FrequencyTable.isSubset(needed_pawns.getFrequency(), freq_pawns):
                            print('(x = {}, y = {})'.format(i, j))
                            n_words[d] +=1
            if n_words[d] == 0: print('  (None)')