from connect_4_stuff import *

class Bot1():
    def __init__(self):
        self.piece = ''
        self.name = "AlphaConnect"
        self.minmax_depth = 0 #minmax tree has this depth
        self.minmax_breadth = 0 #number of heatmap selections to take
        self.state_vectors = [] #Used to develop the heatmap
        self.my_benefit_matrix = [] #Used to find winchance, matrix of matrices
        self.their_benefit_matrix = [] #Used to find winchance, matrix of matrices
        self.PCA_win_matrix = [] #used to find winchance through pca
        self.games_analyzed = 0

    def get_winchance(self, board, cur_piece, opp_piece):
        '''Evaluates chance of winning from 0% to 100% given current board
        '''
        return 0

    def generate_int_board_copy(self, board, cur_piece, opp_piece):
        '''Produces Copy of board with cur_piece = 1, opp_piece = -1, '' = 0
        '''
        return []

    def generate_int_board(self, board, cur_piece, opp_piece):
        '''Changes board so that cur_piece = 1, opp_piece = -1, '' = 0
        '''
        return []

    def generate_posint_board_copy(self, board, cur_piece):
        '''Produces Copy of board with cur_piece = 1, opp_piece = 0, '' = 0
        '''
        return []

    def generate_posint_board(self, board, cur_piece):
        '''Changes board so that cur_piece = 1, opp_piece = 0, '' = 0
        '''
        return []

    def develop_heatmap(self, board, cur_piece_piece):
        '''find best moves to play given a board'''
        heat_map = []
        return heat_map

    def minmax(depth, board, cur_piece, opp_piece):
        ''' Find Optimal* move with depth of depth searched'''
        return

    def move(self, piece, board):
        '''Choose move'''
        return 0

    def self_learning(self, board):
        ''' Edits state vectors to make them more accurate at
            generating heat maps
        '''
        return

    def develop_state_vectors(self, file_name):
        '''develop state vectors from match history'''
        return
