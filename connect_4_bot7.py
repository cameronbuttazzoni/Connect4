from connect_4_stuff import *

class Bot7():
    def __init__(self):
        self.piece = ''
        self.name = "SimpleMinMaxBot"
        self.depth = 4

    def analyze_moves(self, piece, board, moves):
        ''' Return chance of winning based on current moves '''
        #moves = [valid_moves[x] for x in range(len(valid_moves))]
        #get_double, check_stack_win, etc.
        for x in moves:
            y = board.heights[x]
            if board.check_move_win(x, y, piece):
                return 100
        board.get_double(piece, moves)
        if len(moves) == 1:
            return 95
        board.check_stack_win(piece, moves)
        if len(moves) == 1:
            return 90
        board.check_stack_double(piece, moves)
        if len(moves) == 1:
            return 85
        board.prevent_free_double(piece, moves)
        if len(moves) == 0:
            return 30
        board.prevent_free_win(piece, moves)
        if len(moves) == 0:
            return 10
        return 50

    def select_move(self, piece, board, valid_moves, depth):
        ''' Uses minmax algorithm to find best move'''
        new_valid_moves = board.get_valid_moves()
        if depth == 0:
            val = self.analyze_moves(piece, board, new_valid_moves)
            if piece == self.piece:
                return val
            return 100.0-val
        else:
            opp_piece = board.get_piece(piece)
            if depth == self.depth:
                if piece == self.piece:
                    winrates = [0]
                else:
                    winrates = [100]
                for move in valid_moves:
                    board2 = board.simulate_board(opp_piece, move)
                    winrates.append(self.select_move(opp_piece, board2,
                                                    valid_moves, depth-1))
                m = max(winrates)
                best_inds = [i for i, j in enumerate(winrates) if j == m]
                #print(self.piece, piece, valid_moves, '\n', winrates)
                return valid_moves[random.randint(0, len(best_inds)-1)]
                #return valid_moves[winrates.index(max(winrates))]
            else:
                if piece == self.piece:
                    winrates = [0]
                else:
                    winrates = [100]
                for move in valid_moves:
                    board2 = board.simulate_board(opp_piece, move)
                    winrates.append(self.select_move(opp_piece, board2,
                                                    new_valid_moves, depth-1))
                val = self.analyze_moves(piece, board, new_valid_moves)
                #print(self == self.depth, valid_moves, '\n', winrates, val)
                if piece == self.piece:
                    return max(val, max(winrates))
                return min(val, min(winrates))

    def move(self, piece, board):
        self.piece = piece
        valid_moves = board.get_valid_moves()
        board.win_moves(piece, valid_moves) #if can win, remove all other moves
        if len(valid_moves) > 1:
            board.stop_loss(piece, valid_moves) #if will lose remove other moves
        if len(valid_moves) > 1:
            board.prevent_free_win(piece, valid_moves)
        if len(valid_moves) > 1:
            board.get_double(piece, valid_moves)
        if len(valid_moves) > 1:
            board.prevent_double(piece, valid_moves)
        if len(valid_moves) > 1:
            board.check_stack_win(piece, valid_moves)
        if len(valid_moves) > 1:
            board.check_stack_double(piece, valid_moves)
        if len(valid_moves) > 1:
            self.select_move(piece, board, valid_moves, self.depth)

        #WILL LOSE
        valid_moves = board.get_valid_moves()
        if len(valid_moves) > 1:
            board.win_moves(piece, valid_moves)
        if len(valid_moves) > 1:
            board.stop_loss(piece, valid_moves)
        if len(valid_moves) > 1:
            board.prevent_free_win(piece, valid_moves)
        if len(valid_moves) != 0:
            return valid_moves[random.randint(0, len(valid_moves)-1)]
        
        return random.randint(0, board.w-1)
