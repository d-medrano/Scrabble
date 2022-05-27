from os import system, name

from ScrabbleModule import *


def clear_screen():
    if name == 'nt': _ = system('cls')
    else: _ = system('clear')

def welcome(word):
    clear_screen()
    with open('welcome_message.txt','r') as f:
        for line in f:
            print(line, end='')
    print('\n' + ' '*14 + 'Select {} option:'.format(word), end=' ')

def initialize_game():
    bag_of_pawns = Pawns()
    bag_of_pawns.createBag()
    player_pawns = Pawns()
    for _ in range(7):
        player_pawns.addPawn(bag_of_pawns.takeRandomPawn())
    board = Board()
    Board.score = 0
    return bag_of_pawns, player_pawns, board, 0

def main_screen(board, bag_of_pawns, player_pawns):
    clear_screen()
    board.showBoard()
    print(13*' '+7*'+---'+'+'+15*' '+'+'+17*'-'+'+'+11*'-'+'+'+17*'-'+'+'+20*'-'+'+'+15*'-'+'+')
    print('    Letters: | {} | {} | {} | {} | {} | {} | {} |\t'.format(player_pawns.letters[0], player_pawns.letters[1], player_pawns.letters[2], player_pawns.letters[3], player_pawns.letters[4], player_pawns.letters[5], player_pawns.letters[6])+
    'Options: |  1) Write word  |  2) Hint  |  3) Check word  |  4) Letter points  |  0) End game  |')
    print(13*' '+7*'+---'+'+'+15*' '+'+'+17*'-'+'+'+11*'-'+'+'+17*'-'+'+'+20*'-'+'+'+15*'-'+'+')
    remaining_letters = len(bag_of_pawns.letters)
    print(13*' '+'Remaining letters: {}{}/100'.format('' if remaining_letters >= 10 else ' ' , remaining_letters), end='')
    option = input(19*' '+'What do you want to do? ')
    while (option != '1') and (option != '2') and (option != '3') and (option != '4') and (option != '0'):
        option = input(57*' '+'Come on... what do you want to do? ')
    print('')
    return option

def write_word(board, bag_of_pawns, player_pawns):
    word = Word.readWord()
    if not Dictionary.validateWord(word):
        return 0
    while abs((x := int(input('- Position x (0-14): ')))-7) > 7:
        pass
    while abs((y := int(input('- Position y (0-14): ')))-7) > 7:
        pass
    while (direction := input('- Direction (horizontal - "H", vertical - "V"): ')) not in ['H', 'V', 'h', 'v']:
        pass
    needed_pawns = board.getPawns(word, x, y, direction)
    if not FrequencyTable.isSubset(needed_pawns.getFrequency(), player_pawns.getFrequency()):
        input('You do not have letters for that word...')
    else:
        validation = board.isPossible(word, x, y, direction)
        if not validation[0]:
            input('\n' + validation[1])
        else:
            board.placeWord(player_pawns, word, x, y, direction)
            if (7 - player_pawns.getTotalPawns()) < len(bag_of_pawns.letters):
                for _ in range(7 - player_pawns.getTotalPawns()):
                    player_pawns.addPawn(bag_of_pawns.takeRandomPawn())
            else:
                clear_screen()
                board.showBoard()
                print('Game Over! Your score is {}.'.format(board.score))
                input('\nPress ENTER to continue...')
                return 1
            input('\nPress ENTER to continue...')
    return 0

def hint(board, player_pawns):
    if board.totalWords == 0:
        print('- Valid words:')
        Dictionary.showWord(player_pawns)
        print('\n')
    else:
        c = input('- Choose a letter from the board: ').upper()
        print('- Valid words:')
        Dictionary.showWordPlus(player_pawns, c)
        print('\n')
    input('Press ENTER to continue...')

def check_word(board, player_pawns):
    word = Word.readWord()
    if Dictionary.validateWord(word):
        board.showWordPlacement(player_pawns, word)
        input('\nPress ENTER to continue...')

def letter_points():
    clear_screen()
    print('- Letter points:')
    with open('letter_points.txt','r') as f:
        for line in f:
            print(line, end='')
    input('\n\nPress ENTER to continue...')

def new_game():
    bag_of_pawns, player_pawns, board, game_over = initialize_game()
    while True:
        while (action := main_screen(board, bag_of_pawns, player_pawns)) != '0':
            if action == '1':
                game_over = write_word(board, bag_of_pawns, player_pawns)
                if game_over == 1: return 0
            elif action == '2':
                hint(board, player_pawns)
            elif action == '3':
                check_word(board, player_pawns)
            else:
                letter_points()
        ex = input('Are you sure? (y/n) ')
        if ex == 'n':
            continue
        elif ex == 'y':
            return 0
        else:
            print('Not a valid option!', end=' ')
            input('Press ENTER to continue...')
            continue


welcome('an')

while (option := input()) != '0':
    if option == '1':
        new_game()
        welcome('an')
        continue
    elif option == '2':
        break
    else:
        welcome('valid')

clear_screen()