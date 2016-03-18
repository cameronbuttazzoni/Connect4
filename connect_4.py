from connect_4_stuff import *
from connect_4_bot1 import Bot1
from connect_4_bot2 import Bot2
from connect_4_bot3 import Bot3
from connect_4_bot4 import Bot4
from connect_4_bot5 import Bot5
from connect_4_bot6 import Bot6
from connect_4_bot7 import Bot7

SAVE_HISTORY = False
SAVE_FINAL_STATE = False
SHOW_GAME = False


def select_AI(piece, board, next_AI, AI1, AI2):
    if next_AI == 1:
        return AI1.move(piece, board)
    return AI2.move(piece, board)


def play_game(num, width, height, against_AI):
    '''play connect num with board game of width and height given
       return the winner and the game history
    '''
    board = CentreBoard(width, height)
    piece = ''
    bot = Bot6()
    while 1:
        board.print()
        piece = board.get_piece(piece)
        while 1:
            try:
                move = int(input("Input: ").replace(' ', ''))
                if move < 0 or move >= width:
                    continue
                check = board.play_move(piece, move)
                if check == -1:
                    continue
                break
            except ValueError:
                continue
        if board.check_finish(piece, num):
            break
        if against_AI:
            piece = board.get_piece(piece)
            board.print()
            move = bot.move(piece, board)
            board.play_move(piece, move)
            if board.check_finish(piece, num):
                break
            
    board.print()
    return piece, board.moves

def AI_match(num, width, height, next_AI, AI1, AI2): #next_AI = 1 or 2
    board = CentreBoard(width, height)
    piece = ''
    check = 0
    while 1:
        piece = board.get_piece(piece)
        move = select_AI(piece, board, next_AI, AI1, AI2)
        board.play_move(piece, move)
        if next_AI == 1:
            next_AI = 2
        else:
            next_AI = 1
        if SHOW_GAME:
            if next_AI != 1: #already changed next_AI val
                print("AI: ", AI1.name)
            else:
                print("AI: ", AI2.name)
            board.print()
            junk = input('')
        check = board.check_finish(piece, num)
        if check != 0:
            break
    return piece, board.moves, check

def save_history(f, moves):
    for x in range(len(moves)):
        if x < len(moves) - 1:
            #f.write(str(moves[x][0]) + ',' + str(moves[x][1]) + ':')
            f.write(str(moves[x][1]) + ',')
        else:
            #f.write(str(moves[x][0]) + ',' + str(moves[x][1]) + '\n')
            f.write(str(moves[x][1]) + '\n')
    return

def save_final_state(f, moves):
    return

def battle_AI(rounds, filename):
    AI1_wins = 0
    AI2_wins = 0
    ties = 0
    AI1 = Bot6()
    AI2 = Bot7()
    if SAVE_HISTORY or SAVE_FINAL_STATE:
        f = open(filename, 'w')
    for x in range(int(rounds/2)):
        #print("Starting Round: ", 2 * x + 1)
        piece, moves, check = AI_match(CONNECT_NUM, BOARD_WIDTH, BOARD_HEIGHT, 1,
                                AI1, AI2)
        if SAVE_HISTORY:
            save_history(f, moves)
        elif SAVE_FINAL_STATE:
            save_final_state(f, moves)
        if piece == 'X' and check == 1:
            AI1_wins += 1
            if SHOW_GAME:
                print("AI1 " + AI1.name + " Wins!!!!")
        elif piece == 'O' and check == 1:
            AI2_wins += 1
            if SHOW_GAME:
                print("AI2 " + AI2.name + " Wins!!!!")
        else:
            if SHOW_GAME:
                print("Tie Game")
            ties += 1
        #print("Starting Round: ", 2 * x + 2)
        piece, moves, check = AI_match(CONNECT_NUM, BOARD_WIDTH, BOARD_HEIGHT, 2,
                                AI1, AI2)
        if SAVE_HISTORY:
            save_history(f, moves)
        elif SAVE_FINAL_STATE:
            save_final_state(f, moves)
        if piece == 'O' and check == 1:
            AI1_wins += 1
            if SHOW_GAME:
                print("AI1 " + AI1.name + " Wins!!!!")
        elif piece == 'X' and check == 1:
            AI2_wins += 1
            if SHOW_GAME:
                print("AI2 " + AI2.name + " Wins!!!!")
        else:
            if SHOW_GAME:
                print("Tie Game")
            ties += 1
    if SAVE_HISTORY or SAVE_FINAL_STATE:
        f.close()
    print("AI1 " + AI1.name + " Wins: ", AI1_wins)
    print("AI2 " + AI2.name + " Wins: ", AI2_wins)
    print("Ties: ", ties)
    games = AI1_wins + AI2_wins
    print("AI1 " + AI1.name + " Winrate: ", AI1_wins/games)
    print("AI2 " + AI2.name + " Winrate: ", AI2_wins/games)
    return

def bot_learninga():
    base_bot = Bot5()
    test_bot = Bot5()
    count = 0
    iterations = 0
    while 1:
        count += 1
        test_bot.change_slow()
        piece1, moves = AI_match(CONNECT_NUM, BOARD_WIDTH, BOARD_HEIGHT, 1,
                                test_bot, base_bot)
        piece2, moves = AI_match(CONNECT_NUM, BOARD_WIDTH, BOARD_HEIGHT, 2,
                                test_bot, base_bot)
        if piece1 == piece2 and piece1 == 'X':
            base_bot.update(test_bot)
            if count % 660 == 0:
                iterations += 10
                print("\nIterations: ", iterations, "\n")
                test_bot.print_weights()
        else:
            test_bot.update(base_bot)

        
def bot_learningb():
    base_bot = Bot5()
    test_bot = Bot5()
    noob_bot = Bot3()
    orig_bot = Bot5()
    vs_noob_winrate_max = 0.83
    vs_noob_winrate = 0.0
    ties = 0
    count = 0
    test = False
    rounds = 2500 #plays double this amount
    while 1:
        count += 1
        test_bot.change()
        if test:
            test = False
            for x in range(rounds):
                piece1, moves = AI_match(CONNECT_NUM, BOARD_WIDTH,
                                         BOARD_HEIGHT, 1, test_bot, noob_bot)
                if piece1 == 'X':
                    vs_noob_winrate += 1.0
                if piece1 == '':
                    ties += 1
                piece1, moves = AI_match(CONNECT_NUM, BOARD_WIDTH,
                                         BOARD_HEIGHT, 2, test_bot, noob_bot)
                if piece1 == 'O':
                    vs_noob_winrate += 1.0
                if piece1 == '':
                    ties += 1
            check = vs_noob_winrate / (2*rounds-ties) >= vs_noob_winrate_max
            print("Win Rate: ", vs_noob_winrate / (2*rounds-ties))
            vs_noob_winrate = 0.0
            if not check:
                test_bot.update(orig_bot)
                base_bot.update(orig_bot)
                continue
            else:
                orig_bot.update(test_bot)
                orig_bot.print_weights()
        piece1, moves = AI_match(CONNECT_NUM, BOARD_WIDTH, BOARD_HEIGHT, 1,
                                test_bot, base_bot)
        piece2, moves = AI_match(CONNECT_NUM, BOARD_WIDTH, BOARD_HEIGHT, 2,
                                test_bot, base_bot)
        if piece1 == piece2 and piece1 == 'X':
            base_bot.update(test_bot)
            if count % 500 == 0:
                test = True
        else:
            test_bot.update(base_bot)
        

def main():
    #piece, history = play_game(CONNECT_NUM, BOARD_WIDTH, BOARD_HEIGHT, True)
    battle_AI(20, "test.txt")
    #bot_learningb()
    return
                
                
        
if __name__ == '__main__':
    main()


