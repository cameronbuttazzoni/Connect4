from connect_4_stuff import *

class Bot2():
    def __init__(self):
        self.piece = ''
        self.name = "NoobGreedyBot"

    def move(self, piece, board):
        valid_moves = board.get_valid_moves()
        board.win_moves(piece, valid_moves) #if can win, remove all other moves
        if len(valid_moves) > 1:
            board.stop_loss(piece, valid_moves) #if will lose remove other moves
        if len(valid_moves) != 0:
            return valid_moves[random.randint(0, len(valid_moves)-1)]
        else:
            valid_moves = board.get_valid_moves()
            return random.randint(0, board.w-1)
