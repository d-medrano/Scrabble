class Pawns():


    def __init__(self):
        self.letters = []
    

    def addPawn(self, c):
        self.letters.append(c)


    def addPawns(self, c, n):
        for _ in range(n):
            self.addPawn(c)
    

    def createBag(self):
        import pandas as pd
        all_pawns = pd.read_csv('bag_of_pawns.csv')
        for item in all_pawns.itertuples():
            self.addPawns(item[1], item[2])


    def getFrequency(self):
        fq = FrequencyTable()
        for letter in self.letters:
            fq.update(letter)
        return fq


    def showPawns(self):
    #    distinct_letters = []
    #    for l in self.letters:
    #        if l not in distinct_letters:
    #            distinct_letters.append(l)
    #            print(f"{l}: {self.letters.count(l)}")
        self.getFrequency().showFrequency()
    

    def takeRandomPawn(self):
        from numpy import random
        extracted = random.choice(self.letters)
        self.letters.remove(extracted)
        return extracted
    

    def takePawn(self, c):
        self.letters.remove(c)
    

    def getTotalPawns(self):
        return len(self.letters)



class Word():


    def __init__(self):
        self.word = []
    

    def __str__(self):
        return ''.join(self.word)
    

    def areEqual(self, w):
        if self.getLengthWord() != w.getLengthWord():
            return False
        else:
            for i in range(self.getLengthWord()):
                if self.word[i] != w.word[i]:
                    return False
        return True
    

    def isEmpty(self):
        return not bool(self.getLengthWord())
    

    def getFrequency(self):
        fq = FrequencyTable()
        for letter in self.word:
            fq.update(letter)
        return fq
    

    @classmethod
    def readWord(cls):
        w = cls()
        while len(input_word := input('Word: ').upper()) == 0:
            print('Please, introduce a word...')
        w.word.extend(list(input_word))
        return w
    

    @classmethod
    def readWordFromFile(cls, f):
        w = cls()
        w.word.extend(list(f.readline()[:-1]))
        return w
    

    def getLengthWord(self):
        return len(self.word)



class Dictionary():


    filepath = 'dictionary.txt'


    @staticmethod
    def validateWord(word):
        with open(Dictionary.filepath, 'r') as f:
            while not (line := Word.readWordFromFile(f)).isEmpty():
                if word.areEqual(line):
                    return True
            print(f'"{word}" not in dictionary!')
            return False



class FrequencyTable():


    def __init__(self):
        import pandas as pd
        letters = pd.read_csv('bag_of_pawns.csv')['Letter'].values.tolist()
        self.letters = letters
        self.frequencies = [0 for _ in range(len(letters))]
    

    def showFrequency(self):
        for i in range(len(self.letters)):
            if self.frequencies[i] != 0:
                print(f'{self.letters[i]}: {self.frequencies[i]}')
    

    def update(self, c):
        self.frequencies[self.letters.index(c)] += 1
    

    @staticmethod
    def isSubset(obj1, obj2):
        for i in range(len(obj1.frequencies)):
            if obj1.frequencies[i] > obj2.frequencies[i]:
                return False
        return True



class Board():


    def __init__(self):

        import numpy as np

        self.board = [[' ' for _ in range(15)] for _ in range(15)]
        self.totalWords = 0
        self.totalPawns = 0


    def showBoard(self):
        print('\n   ', end='')
        for i in range(len(self.board)):
            print('  {}{}'.format(0 if i <= 9 else '', i), end='')
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
        if direction == 'H':
            for i in range(word.getLengthWord()):            
                if self.board[x][y+i] == ' ':
                    player_pawns.takePawn(word.word[i])
                    self.board[x][y+i] = word.word[i]
                    self.totalPawns += 1
        elif direction == 'V':
            for i in range(word.getLengthWord()):
                if self.board[x+i][y] == ' ':
                    player_pawns.takePawn(word.word[i])
                    self.board[x+i][y] = word.word[i]
                    self.totalPawns += 1
        self.totalWords += 1
    

    def isPossible(self, word, x, y, direction):  

        positions = []
        if direction == 'H':
            for i in range(word.getLengthWord()):
                positions.append((x, y+i))
            positions.extend([(x, y-1), (x, y+word.getLengthWord())])
        elif direction == 'V':
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
            
            for i in range(word.getLengthWord()):
                added_pawns = []
                if self.board[positions[i][0]][positions[i][1]] == ' ':
                    added_pawns.append(word.word[i])
            if len(added_pawns) == 0:
                return False, 'You are not adding a single letter to the board'
            
            if ((positions[-2][0] != -1 and positions[-2][1] != -1 and self.board[positions[-2][0]][positions[-2][1]] != ' ') 
                or (positions[-1][0] != 15 and positions[-1][1] != 15 and self.board[positions[-1][0]][positions[-1][1]] != ' ')):
                return False, 'There are additional letters at the beginning or ending of your word'

        return True, 'You can add your word'


    def getPawns(self, word, x, y, direction):
        
        possible, message = self.isPossible(word, x, y, direction)
        letters = Word()

        if not possible:
            print(message)
        else:
            if direction == 'H':
                for i in range(word.getLengthWord()):
                    if word.word[i] != self.board[x][y+i]:
                        letters.word.append(word.word[i])
            elif direction == 'V':
                for i in range(word.getLengthWord()):
                    if word.word[i] != self.board[x+i][y]:
                        letters.word.append(word.word[i])
        
        return letters





