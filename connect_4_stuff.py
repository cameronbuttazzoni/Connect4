import random
BOARD_HEIGHT = 6
BOARD_WIDTH = 7
CONNECT_NUM = 4 #need this many pieces in a row to win

class CentreBoard():
    def __init__(self, width, height):
        #board[x][y] x is horizontal and y is vertical
        self.board = [['' for y in range(height)] for x in range(width)]
        self.heights = [0 for x in range(width)] #height where next piece played
        self.h = height
        self.w = width
        self.height = height
        self.width = width
        self.moves = []

    def print(self):
        '''print the game board'''
        for x in range(self.h):
            height_ind = self.h - 1 - x
            print(' ', end="")
            for y in range(self.w):
                if y == 0: #first column
                    if self.board[y][height_ind] != '':
                        print('' + self.board[y][height_ind] + ' | ', end="")
                    else:
                        print(' ' + self.board[y][height_ind] + ' | ', end="")
                elif y == self.w - 1: #last column
                    print(self.board[y][height_ind] + ' ')
                else:
                    if self.board[y][height_ind] != '':
                        print('' + self.board[y][height_ind] + ' | ', end="")
                    else:
                        print(' ' + self.board[y][height_ind] + ' | ', end="")
            if x != self.h-1:
                print('-' * (self.w * 4 - 1))
        print('')

    
    def simulate_board(self, piece, x):
        '''Return copy of board with piece placed in position x'''
        new_board = CentreBoard(self.w, self.h)
        new_board.board = [[self.board[x][y] for y in range(self.h)]
                     for x in range(self.w)]
        new_board.heights = [self.heights[x] for x in range(self.w)]
        new_board.play_move(piece, x)
        return new_board
        

    def get_locations(self, piece):
        '''Return list of all coordinates where piece appears on board'''
        locations = []
        for x in range(self.w):
            for y in range(self.h):
                if self.board[x][y] == piece:
                    locations.append([x, y])
        return locations

    def check_row(self, piece, num):
        ''' Return True if any row has num of piece in a row
            else return False
        '''
        for y in range(0, self.h):
            count = 0
            for x in range(0, self.w):
                if self.board[x][y] == piece:
                    count += 1
                else:
                    count = 0
                if count == num:
                    return True
        return False

    def check_column(self, piece, num):
        ''' Return True if any column has num of piece in a row
            else return False
        '''
        for x in range(0, self.w):
            count = 0
            for y in range(0, self.h):
                if self.board[x][y] == piece:
                    count += 1
                else:
                    count = 0
                if count == num:
                    return True
        return False

    def check_diagonal_right(self, piece, num):
        ''' Return True if any diagonal right / has num of piece in a row
            else return False
        '''
        for x in range(0, self.w):
            y = 0
            count = 0
            for z in range(0, min(self.h, self.w)):
                if x+z >= self.w or y+z >= self.h:
                    break
                if self.board[x+z][y+z] == piece:
                    count += 1
                else:
                    count = 0
                if count == num:
                    return True
        for y in range(1, self.h):
            x = 0
            count = 0
            for z in range(0, min(self.h, self.w)):
                if x+z >= self.w or y+z >= self.h:
                    break
                if self.board[x+z][y+z] == piece:
                    count += 1
                else:
                    count = 0
                if count == num:
                    return True
        return False

    def check_diagonal_left(self, piece, num):
        ''' Return True if any diagonal left \ has num of piece in a row
            else return False
        '''
        for x in range(0, self.w):
            y = 0
            count = 0
            for z in range(0, min(self.h, self.w)):
                if x-z < 0 or y+z >= self.h:
                    break
                if self.board[x-z][y+z] == piece:
                    count += 1
                else:
                    count = 0
                if count == num:
                    return True
        for y in range(1, self.h):
            x = self.w - 1
            count = 0
            for z in range(0, min(self.h, self.w)):
                if x-z < 0 or y+z >= self.h:
                    break
                if self.board[x-z][y+z] == piece:
                    count += 1
                else:
                    count = 0
                if count == num:
                    return True
        return False

    def check_all_directions(self, piece, num):
        ''' Check for num piece in a row vertically, horizontally
           and diagonally
           Return True if found else return False
        '''
        r = self.check_row(piece, num)
        c = self.check_column(piece, num)
        dr = self.check_diagonal_right(piece, num)
        dl = self.check_diagonal_left(piece, num)
        #print(r, c, dr, dl)
        return r or c or dr or dl

    def insert_piece(self, piece, x, y):
        '''Places piece on board and records it in history'''
        self.board[x][y] = piece
        self.moves.append([piece, x])
        return 0
    
    def play_move(self, piece, x):
        y = self.heights[x]
        if y == self.h:
            return -1
        self.heights[x] += 1
        return self.insert_piece(piece, x, y)

    def get_piece(self, piece):
        if piece == '':
            return 'X'
        elif piece == 'X':
            return 'O'
        else:
            return 'X'

    def check_tie(self):
        if min(self.heights) == self.h:
            return True
        return False

    def check_finish(self, piece, num):
        if self.check_all_directions(piece, num):# win
            return 1
        if self.check_tie(): #Tie
            return 2
        return 0 #not done

    def get_valid_moves(self):
        valid_moves = []
        for x in range(self.w):
            if self.heights[x] != self.h:
                valid_moves.append(x)
        return valid_moves

            
    def check_move_win(self, x, y, piece):
        '''Return True if playing in this spot will result in a win
        '''
        #row
        self.board[x][y] = piece
        count = 0
        for a in range(2*CONNECT_NUM-1):
            if x-CONNECT_NUM+1+a < 0:
                continue
            if x-CONNECT_NUM+1+a >= self.width:
                break
            if self.board[x-CONNECT_NUM+1+a][y] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT_NUM:
                self.board[x][y] = ''
                return True

        #column
        count = 0
        for a in range(CONNECT_NUM):
            if y-a < 0:
                break
            if self.board[x][y-a] == piece:
                count += 1
            if count == CONNECT_NUM:
                self.board[x][y] = ''
                return True
            
        #diagonal right
        count = 0
        for a in range(2*CONNECT_NUM-1):
            if x-CONNECT_NUM+1+a < 0 or y-CONNECT_NUM+1+a < 0:
                continue
            if x-CONNECT_NUM+1+a >= self.w or y-CONNECT_NUM+1+a >= self.h:
                break
            if self.board[x-CONNECT_NUM+1+a][y-CONNECT_NUM+1+a] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT_NUM:
                self.board[x][y] = ''
                return True

        #diagonal left
        count = 0
        for a in range(2*CONNECT_NUM-1):
            if x+CONNECT_NUM-1-a < 0 or y-CONNECT_NUM+1+a < 0:
                continue
            if x+CONNECT_NUM-1-a >= self.w or y-CONNECT_NUM+1+a >= self.h:
                break
            if self.board[x+CONNECT_NUM-1-a][y-CONNECT_NUM+1+a] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT_NUM:
                self.board[x][y] = ''
                return True
        self.board[x][y] = ''
        return False

    def win_moves(self, piece, valid_moves):
        ''' If any move would cause a win, valid_moves removes all others
        '''
        for x in valid_moves:
            y = self.heights[x]
            if self.check_move_win(x, y, piece): #Winning Move Found
                if len(valid_moves) > 1:
                    valid_moves[0] = x
                    del valid_moves[1:]
                    return
        return 

    def stop_loss(self, piece, valid_moves):
        ''' If any move would stop an opponent loss, remove all others
        '''
        if piece == 'X':
            self.win_moves('O', valid_moves)
            return
        self.win_moves('X', valid_moves)
        return

    def prevent_free_win(self, piece, valid_moves):
        '''Remove any moves that would give opponent a win next_turn
        '''
        ind = 0
        opp_piece = self.get_piece(piece)
        while ind <  len(valid_moves):
            x = valid_moves[ind]
            y = self.heights[x] + 1
            if y >= self.h:
                ind += 1
                continue
            if self.check_move_win(x, y, opp_piece):
                del valid_moves[ind]
            else:
                ind += 1
        return

    def prevent_double(self, piece, valid_moves):
        ''' If the opponent can play a move so that their next turn they can
            win in two different ways, then remove all moves that don't stop
            this
        '''
        opp_piece = self.get_piece(piece)
        for x in valid_moves:
            if self.check_double(opp_piece, x):
                valid_moves[0] = x
                if len(valid_moves) > 1:
                    del valid_moves[1:]
        return

    def get_row_wins(self, piece, x, y):
        count = 0
        win_count = 0
        f_flag = False #If True, already found one winning move
        flag = False #If True, already counting empty in count count
        emp_dist = 0 #distance away from empty space used in last win
        for a in range(2*CONNECT_NUM-1):
            if x-CONNECT_NUM+1+a < 0:
                continue
            if x-CONNECT_NUM+1+a >= self.w:
                break
            new_piece = self.board[x-CONNECT_NUM+1+a][y]
            if new_piece == piece:
                count += 1
            elif not flag and new_piece == '':
                count += 1
                flag = True
            elif new_piece == '' and flag:
                emp_dist = 0
                if y - 1 >= 0:
                    if self.board[x-CONNECT_NUM+1+a][y-1] != '':
                        if count > 1:
                            if self.board[x-CONNECT_NUM+a][y] == piece:
                                count = 2
                                if self.board[x-CONNECT_NUM-1+a][y] == piece:
                                    count = 3
                        else:
                            count = 1
                else:
                    if count > 1:
                        if self.board[x-CONNECT_NUM+a][y] == piece:
                            count = 2
                            if self.board[x-CONNECT_NUM-1+a][y] == piece:
                                count = 3
                    else:
                        count = 1
            else:
                count = 0
                flag = False
            if flag:
                emp_dist += 1 #need to be CONNET_NUM-1 away
            if count == CONNECT_NUM:
                win_count += 1
                f_flag = True
            elif f_flag and count > CONNECT_NUM:
                if x-CONNECT_NUM+2+a >= self.w: #require next piece ours
                    break
                if self.board[x-CONNECT_NUM+2+a][y] in (piece, ''):
                    if y - 1 >= 0:
                        if self.board[x-CONNECT_NUM+2+a][y-1] != '':
                            win_count += 1
                    else:
                        win_count += 1
            elif f_flag and emp_dist == (CONNECT_NUM-1):
                if x-CONNECT_NUM+2+a >= self.w: #require next piece ours
                    break
                if self.board[x-CONNECT_NUM+2+a][y] == piece:
                    win_count += 1
        return win_count

    def get_column_wins(self, piece, x, y):
        count = 0
        for a in range(CONNECT_NUM):
            if y-a+1 < 0 or y-a+1 >= self.h:
                break
            if self.board[x][y-a+1] in (piece, ''):
                count += 1
            if count == CONNECT_NUM:
                return 1
        return 0

    def get_diagonal_right_wins(self, piece, x, y):
        count = 0
        win_count = 0
        f_flag = False #If True, already found one winning move
        flag = False #If True, already counting empty in count count
        emp_dist = 0 #distance away from empty space used in last win
        for a in range(2*CONNECT_NUM-1):
            if x-CONNECT_NUM+1+a < 0 or y-CONNECT_NUM+1+a < 0:
                continue
            if x-CONNECT_NUM+1+a >= self.w or y-CONNECT_NUM+1+a >= self.h:
                break
            new_piece = self.board[x-CONNECT_NUM+1+a][y-CONNECT_NUM+1+a]
            if new_piece == piece:
                count += 1
            elif not flag and new_piece == '':
                if y-CONNECT_NUM+a >= 0:
                    if self.board[x-CONNECT_NUM+1+a][y-CONNECT_NUM+a] != '':
                        count += 1
                        flag = True
                else:
                    count = 0
                    emp_dist = 0
            elif new_piece == '' and flag:
                if y-CONNECT_NUM+a >= 0 and x-CONNECT_NUM+a >= 0:
                    if self.board[x-CONNECT_NUM+a][y-CONNECT_NUM+a] != '':
                        emp_dist = 0
                        if count > 1:
                            if x-CONNECT_NUM-1+a >= 0 and y-CONNECT_NUM-1+a >=0:
                                new_piece2 = (self.board[x-CONNECT_NUM-1+a]
                                                  [y-CONNECT_NUM-1+a])
                                if new_piece2 == piece:
                                    count = 2
                            if x-CONNECT_NUM-2+a >= 0 and y-CONNECT_NUM-2+a >=0:
                                new_piece2 = (self.board[x-CONNECT_NUM-2+a]
                                                  [y-CONNECT_NUM-2+a])
                                if new_piece2 == piece and count == 2:
                                    count = 3
                        else:
                            count = 1
                else:
                    count = 0
                    flag = False
                    emp_dist = 0
                                    
            else:
                count = 0
                flag = False
            if flag:
                emp_dist += 1 #need to be CONNECT_NUM-1 away
            if count == CONNECT_NUM:
                win_count += 1
                f_flag = True
            elif f_flag and count > CONNECT_NUM:
                if x-CONNECT_NUM+2+a >= self.w: #require next piece ours
                    break
                if y-CONNECT_NUM+2+a >= self.h:
                    break
                new_piece2 = self.board[x-CONNECT_NUM+2+a][y-CONNECT_NUM+2+a]
                if new_piece2 in (piece, ''):
                    if self.board[x-CONNECT_NUM+2+a][y-CONNECT_NUM+1+a] != '':
                        win_count += 1
            elif f_flag and emp_dist == (CONNECT_NUM-1):
                if x-CONNECT_NUM+2+a >= self.w: #require next piece ours
                    break
                if y-CONNECT_NUM+2+a >= self.h:
                    break
                if self.board[x-CONNECT_NUM+2+a][y-CONNECT_NUM+2+a] == piece:
                    if self.board[x-CONNECT_NUM+2+a][y-CONNECT_NUM+1+a] != '':
                        win_count += 1
        return win_count

    def get_diagonal_left_wins(self, piece, x, y):
        count = 0
        win_count = 0
        f_flag = False #If True, already found one winning move
        flag = False #If True, already counting empty in count count
        emp_dist = 0 #distance away from empty space used in last win
        for a in range(2*CONNECT_NUM-1):
            if x+CONNECT_NUM-1-a < 0 or y-CONNECT_NUM+1+a < 0:
                continue
            if x+CONNECT_NUM-1-a >= self.w or y-CONNECT_NUM+1+a >= self.h:
                break
            new_piece = self.board[x+CONNECT_NUM-1-a][y-CONNECT_NUM+1+a]
            if new_piece == piece:
                count += 1
            elif not flag and new_piece == '':
                if y-CONNECT_NUM+a >= 0: #check their is a piece undearneath
                    if self.board[x+CONNECT_NUM-1-a][y-CONNECT_NUM+a] != '':
                        count += 1
                        flag = True
                else:
                    count = 0
                    emp_dist = 0
            elif new_piece == '' and flag:
                x_ind = x+CONNECT_NUM-a
                y_ind = y-CONNECT_NUM+a
                if x_ind >= 0 and y_ind >= 0:
                    if self.board[x_ind][y_ind] != '':
                        emp_dist = 0
                        if count > 1:
                            if x_ind+1 < self.w and y_ind-1 >= 0:
                                new_piece2 = self.board[x_ind+1][y_ind-1]
                                if new_piece2 == piece:
                                    count = 2
                            if x_ind+2 < self.w and y_ind-2 >= 0:
                                new_piece2 = self.board[x_ind+2][y_ind-2]
                                if new_piece2 == piece and count == 2:
                                    count = 3
                        else:
                            count = 1
                else:
                    count = 0
                    flag = False
                    emp_dist = 0
                                    
            else:
                count = 0
                flag = False
            if flag:
                emp_dist += 1 #need to be CONNECT_NUM-1 away
            if count == CONNECT_NUM:
                win_count += 1
                f_flag = True
            elif f_flag and count > CONNECT_NUM:
                if x+CONNECT_NUM-2-a >= self.w: #require next piece ours
                    break
                if y-CONNECT_NUM+2+a >= self.h:
                    break
                new_piece2 = self.board[x+CONNECT_NUM-2-a][y-CONNECT_NUM+2+a]
                if new_piece2 in (piece, ''):
                    if self.board[x+CONNECT_NUM-2-a][y-CONNECT_NUM+1+a] != '':
                        win_count += 1
            elif f_flag and emp_dist == (CONNECT_NUM-1):
                if x+CONNECT_NUM-2-a >= self.w: #require next piece ours
                    break
                if y-CONNECT_NUM+2+a >= self.h:
                    break
                if self.board[x+CONNECT_NUM-2-a][y-CONNECT_NUM+2+a] == piece:
                    if self.board[x+CONNECT_NUM-2-a][y-CONNECT_NUM+1+a] != '':
                        win_count += 1
        return win_count

    def check_double(self, piece, x, y=None):
        '''Check if playing in this position would result in a double next turn
        '''
        if y == None:
            y = self.heights[x]
        self.board[x][y] = piece
        win_count = self.get_row_wins(piece, x, y)
        win_count += self.get_column_wins(piece, x, y)
        win_count += self.get_diagonal_right_wins(piece, x, y)
        win_count += self.get_diagonal_left_wins(piece, x, y)
        self.board[x][y] = ''
        if win_count >= 2:
            return True
        return False

    def get_double(self, piece, valid_moves):
        for x in valid_moves:
            if self.check_double(piece, x):
                valid_moves[0] = x
                if len(valid_moves) > 1:
                    del valid_moves[1:]
        return

    def check_double_fast(self, piece, x, y=None):
        ''' Check if a play will result in a double
            Much faster than other function, but in rare cases will not find
            a double when one exists
        '''
        if y == None:
            y = self.heights[x]
        #NOT IMPLEMENTED
        return
    
    def check_future_double(self, piece, x, y=None):
        '''Check if playing in a position results in a potential double if more
           pieces were played
        '''
        if y == None:
            y = self.heights[x]
        return
    
    def check_nonblockable_three_row(self, piece, x, y=None):
        '''Check if playing in this spot will give three in a row that the
           opponent cannot block on at least one side
        '''
        if y == None:
            y = self.heights[x]
        ind1 = 0
        count = 0 #need 3 in row
        unblockable_num #sides if it is unblockable on how many sides
        self.board[x][y] = piece
        for ind in range(self.w):
            if board[ind][y] == piece:
                count += 1
            if count >= 3:
                if ind1-1 >= 0 and y-1 >= 0:
                    if self.board[ind1-1][y-1] == '':
                        unblockable_num += 1
                if ind+1 < self.w and y-1 >= 0:
                    if self.board[ind+1][y-1] == '':
                        unblockable_num += 1
                if unblockable_num > 0:
                    self.board[x][y] = ''
                    return unblockable_num           
        self.board[x][y] = ''
        return False

    def prevent_free_double(self, piece, valid_moves):
        '''Remove any moves from valid_moves that would allow the opponent to
           get a double by playing on top of you
        '''
        index = 0
        opp_piece = self.get_piece(piece)
        while index < len(valid_moves):
            x = valid_moves[index]
            y = self.heights[x]
            if y < self.h - 1: #otherwise no piece can be played on top of you
                self.board[x][y] = piece
                check = self.check_double(opp_piece, x, y+1)
                self.board[x][y] = ''
                if check:
                    del valid_moves[index]
                else:
                    index += 1
            else:
                index += 1
        return

    def check_stack_win(self, piece, valid_moves):
        '''Check if playing in a position would force opponent to play in same
           column to prevent losing, then again playing in same position would
           result in a win. Remove all other moves.
        '''
        for x in valid_moves:
            y = self.heights[x]
            if y >= self.h - 2: #too high up board
                continue
            self.board[x][y] = piece
            if self.check_move_win(x, y+1, piece):
                if self.check_move_win(x, y+2, piece):
                    valid_moves[0] = x
                    if len(valid_moves) > 1:
                        del valid_moves[1:]
                    self.board[x][y] = ''
                    return
            self.board[x][y] = ''
    
    def check_stack_double(self, piece, valid_moves):
        '''Check if playing in a position would force opponent to play in same
           column to prevent losing, then again playing in same position would
           result in a double
        '''
        for x in valid_moves:
            y = self.heights[x]
            if y >= self.h - 2: #too high up board
                continue
            self.board[x][y] = piece
            if self.check_move_win(x, y+1, piece):
                if self.check_double(piece, x, y+2):
                    valid_moves[0] = x
                    if len(valid_moves) > 1:
                        del valid_moves[1:]
                    self.board[x][y] = ''
                    return
            self.board[x][y] = ''

    def prevent_block(self, piece, board, valid_moves):
        ''' Dont play a move that will allow the opponent to block a win
        '''
        index = 0
        while index < len(valid_moves):
            x = valid_moves[index]
            y = board.heights[x] + 1
            if y >= board.height: #this move is top of board
                index += 1
                continue
            if board.check_move_win(x, y, piece):
                del valid_moves[index]
            else:
                index += 1 
        return
    
