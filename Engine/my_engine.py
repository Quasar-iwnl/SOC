import copy
import math
import chess
from functools import cmp_to_key


def sortbyCond(a, b):
    if (a[0] != b[0]):
        return (a[0] - b[0])
    else:
        return b[1] - a[1]

W = chess.WHITE
B = chess.BLACK

PV = {
    'pawn': 100,
    'knight': 295,
    'bishop': 300,
    'rook': 500,
    'queen': 900,
    'king': 1000,

    # Pawn
    'doubled_pawn': 80,
    'isolated_pawn': 90,
    'protected_pawn': 105,
    'pawn_in_center': 110, # e4,d4,d5,e5
    'pawn_at_7': 300, # 7th rank
    'pawn_at_6': 150,
    'pawn_promotion': 900,

    # Bishop
    'fianchetto': 310,
    'bishop_in_center': 305,
    'back_rank_bishop': 290,

    # Knight
    'knight_in_center':  310,
    'corner_knight': 285,

    # Queen
    'early_queen_back_rank': 900,
    'early_queen_else': 880,

    # Rooks
    'connected_rooks': 515,
    'pig_rook': 518, # Pig is rook on the 7th rank
    'pig_connected': 570,

    # King
    'early_king_corner': 1050,
    'late_king_center': 1100
}

class Chess:
    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = chess.Board(fen)
        if self.board.turn:
            self.color = W
        else:
            self.color = B

    def get_position(self, piece):

        if piece == 'pawn':
            white_pawns = self.board.pieces(chess.PAWN, W)
            white_pawn_positions = ([square for square in white_pawns])

            black_pawns = self.board.pieces(chess.PAWN, B)
            black_pawn_positions = ([square for square in black_pawns])

            return white_pawn_positions, black_pawn_positions

        elif piece == 'knight':
            white_knights = self.board.pieces(chess.KNIGHT, W)
            white_knight_positions = ([square for square in white_knights])

            black_knights = self.board.pieces(chess.KNIGHT, B)
            black_knight_positions = ([square for square in black_knights])

            return white_knight_positions, black_knight_positions

        elif piece == 'bishop':
            white_bishops = self.board.pieces(chess.BISHOP, W)
            white_bishop_positions = ([square for square in white_bishops])

            black_bishops = self.board.pieces(chess.BISHOP, B)
            black_bishop_positions = ([square for square in black_bishops])

            return white_bishop_positions, black_bishop_positions

        elif piece == 'queen':
            white_queens = self.board.pieces(chess.QUEEN, W)
            white_queen_positions = ([square for square in white_queens])

            black_queens = self.board.pieces(chess.QUEEN, B)
            black_queen_positions = ([square for square in black_queens])

            return white_queen_positions, black_queen_positions

        elif piece == 'rook':
            white_rooks = self.board.pieces(chess.ROOK, W)
            white_rook_positions = ([square for square in white_rooks])

            black_rooks = self.board.pieces(chess.ROOK, B)
            black_rook_positions = ([square for square in black_rooks])

            return white_rook_positions, black_rook_positions

        elif piece == 'king':
            white_king = self.board.pieces(chess.KING, W)
            white_king_position = ([square for square in white_king])

            black_king = self.board.pieces(chess.KING, B)
            black_king_position = ([square for square in black_king])
            return white_king_position, black_king_position

        return -1

    def piece_evaluation(self):
        if self.board.is_insufficient_material():
            return 0

        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))

        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))

        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))

        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))

        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))

        value = (
                PV['pawn'] * (wp - bp) +
                PV['knight'] * (wn - bn) +
                PV['bishop'] * (wb - bb) +
                PV['rook'] * (wr - br) +
                PV['queen'] * (wq - bq)
        )

        if self.board.turn == chess.WHITE:
            return value
        return -value

    def total_material(self):
        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        value = (
                PV['pawn'] * wp + PV['knight'] * wn + PV['bishop'] * wb + PV['rook'] * wr + PV['queen'] * wq
        )
        return value

    def is_piece_attacked(self, square):
        """

        :param square: check if the piece at the given square is being attacked
        :return: -1 if no piece
                0 if piece exists but not being attacked
                n if n pieces are attacking
        """
        if self.board.piece_type_at(square) == None:
            return -1
        color = self.board.color_at(square)
        if color == W:
            attackers = self.board.attackers(B, square)
            defenders = self.board.attackers(W, square)
        else:
            attackers = self.board.attackers(W, square)
            defenders = self.board.attackers(B, square)

        return attackers, defenders

    def pawn_evaluate(self, position, pawn_position):

        piece = self.board.piece_at(position)
        attackers, defenders = self.is_piece_attacked(position)
        if len(attackers) > len(defenders):
            coeff = 0.35
        else:
            coeff = 1
        rank = chess.square_rank(position)
        file = chess.square_file(position)
        # Check if pawn is near the end
        if piece.color == W:
            if rank == 6:
                return coeff * PV['pawn_at_6']
            elif rank == 7:
                return coeff * PV['pawn_at_7']
            elif rank == 8:
                return coeff * PV['pawn_promotion']

        else:
            if rank == 2:
                return -coeff * PV['pawn_at_6']
            elif rank == 1:
                return -coeff * PV['pawn_at_7']
            elif rank == 8:
                return -coeff * PV['pawn_promotion']

        # Check for doubled pawns
        temp_rank = rank-1
        temp = 8*temp_rank + file
        if temp in pawn_position:
            if piece.color == W:
                return coeff * PV['doubled_pawn']
            else:
                return -coeff * PV['doubled_pawn']

        # Central Pawn
        if (file == 3 or file == 4) and (rank == 4 or rank == 5):
            if piece.color == W:
                return coeff * PV['pawn_in_center']
            else:
                return -coeff * PV['pawn_in_center']

        if piece.color == W:
            return coeff * PV['pawn']
        else:
            return -coeff * PV['pawn']

    def knight_evaluate(self, position):

        piece = self.board.piece_at(position)
        attackers, defenders = self.is_piece_attacked(position)
        if len(attackers) > len(defenders):
            coeff = 0.35
        else:
            coeff = 1

        rank = chess.square_rank(position)
        file = chess.square_file(position)

        # If knight is back rank
        if file == 0 or file == 7:
            if piece.color == W:
                return coeff * PV['corner_knight']
            else:
                return -coeff * PV['corner_knight']

        if (1 < rank < 6) and (1 < file < 6):
            if piece.color == W:
                return coeff * PV['knight_in_center']
            else:
                return -coeff * PV['knight_in_center']

        if piece.color == W:
            return coeff * PV['knight']
        else:
            return -coeff * PV['knight']

    def bishop_evaluate(self, position):

        piece = self.board.piece_at(position)
        attackers, defenders = self.is_piece_attacked(position)
        if len(attackers) > len(defenders):
            coeff = 0.35
        else:
            coeff = 1

        rank = chess.square_rank(position)
        file = chess.square_file(position)

        if piece.color == W:
            if (file == 2 or file == 6) and rank == 1:
                return coeff * PV['fianchetto']
            elif rank == 0:
                return coeff * PV['back_rank_bishop']
            elif 2 <= rank <= 5:
                return coeff * PV['bishop_in_center']
            else:
                return coeff * PV['bishop']
        else:
            if (file == 2 or file == 6) and rank == 6:
                return -coeff * PV['fianchetto']
            elif rank == 7:
                return -coeff * PV['back_rank_bishop']
            elif 4 <= rank <= 7:
                return -coeff * PV['bishop_in_center']
            else:
                return -coeff * PV['bishop']

    def is_draw(self):
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_fivefold_repetition():
            return True
        return False

    def rook_evaluate(self, position):

        piece = self.board.piece_at(position)
        attackers, defenders = self.is_piece_attacked(position)
        if len(attackers) > len(defenders):
            coeff = 0.35
        else:
            coeff = 1
        if piece.color == W:
            return coeff * PV['rook']
        else:
            return -coeff * PV['rook']


    def queen_evaluate(self, position):

        piece = self.board.piece_at(position)
        attackers, defenders = self.is_piece_attacked(position)
        if len(attackers) > len(defenders):
            coeff = 0.35
        else:
            coeff = 1

        rank = chess.square_rank(position)
        file = chess.square_file(position)
        if piece.color == W:
            return coeff*PV['queen']
        else:
            return -coeff*PV['queen']

    def king_evaluate(self, position):

        piece = self.board.piece_at(position)
        rank = chess.square_rank(position)
        file = chess.square_file(position)
        attackers, defenders = self.is_piece_attacked(position)
        if len(attackers) > 0:
            coeff = -1000
        else:
            coeff = 1
        if piece.color == W:
            # Check if it is late-game
            if self.total_material() < 15:
                return coeff * PV['king']
            else:
                if (file == 6 or file == 7) and rank == 0:
                    return coeff * PV['early_king_corner']
                else:
                    return coeff * PV['king']
        else:
            if self.total_material() < 15:
                return -coeff * PV['king']
            else:
                if (file == 6 or file == 7) and rank == 7:
                    return -coeff * PV['early_king_corner']
                else:
                    return -coeff * PV['king']

    def get_child(self, move):
        child = copy.deepcopy(self)
        child.board.push(move)
        child.color = child.board.turn
        return child

    def check_capture(self):
        legal_moves = list(self.board.legal_moves)

        if self.color == W:
            max_eval = -math.inf
            for move in legal_moves:
                prev_eval = self.piece_evaluation()
                child = self.get_child(move)
                next_eval = child.check_capture()
                if eval > max_eval:
                    max_eval = eval
            return max_eval
        else:
            min_eval = math.inf
            for move in legal_moves:
                child = self.get_child(move)
                eval = child.check_capture()
                if eval < min_eval:
                    min_eval = eval
            return min_eval

    def evaluate(self):
        if self.board.is_checkmate():
            if self.color == W:
                return math.inf
            else:
                return -math.inf
        if self.board.is_insufficient_material() or self.board.is_stalemate():
            return 0

        white_pawn_positions, black_pawn_positions = self.get_position('pawn')
        white_knight_positions, black_knight_positions = self.get_position('knight')
        white_bishop_positions, black_bishop_positions = self.get_position('bishop')
        white_rook_positions, black_rook_positions = self.get_position('rook')
        white_queen_positions, black_queen_positions = self.get_position('queen')
        white_king_position, black_king_position = self.get_position('king')

        # For knowing which part of the game it is (early, middle, late)
        half_moves = len(self.board.move_stack)
        no_of_minor_pieces = len(white_knight_positions) + len(white_bishop_positions) + len(
            black_bishop_positions) + len(black_knight_positions)

        white_eval = 0
        black_eval = 0

        for row in range(0, 8):
            for cell in range(0, 8):
                square = 8 * row + cell
                piece = self.board.piece_at(square)
                if piece is None:
                    pass
                elif piece.color == W:
                    if piece.piece_type == chess.PAWN:
                        white_eval = white_eval + self.pawn_evaluate(square, white_pawn_positions)
                    elif piece.piece_type == chess.KNIGHT:
                        white_eval = white_eval + self.knight_evaluate(square)
                    elif piece.piece_type == chess.BISHOP:
                        white_eval = white_eval + self.bishop_evaluate(square)
                    elif piece.piece_type == chess.ROOK:
                        white_eval = white_eval + self.rook_evaluate(square)
                    elif piece.piece_type == chess.QUEEN:
                        white_eval = white_eval + self.queen_evaluate(square)
                    elif piece.piece_type == chess.KING:
                        white_eval = white_eval + self.king_evaluate(square)
                elif piece.color == B:
                    if piece.piece_type == chess.PAWN:
                        black_eval = black_eval + self.pawn_evaluate(square, white_pawn_positions)
                    elif piece.piece_type == chess.KNIGHT:
                        black_eval = black_eval + self.knight_evaluate(square)
                    elif piece.piece_type == chess.BISHOP:
                        black_eval = black_eval + self.bishop_evaluate(square)
                    elif piece.piece_type == chess.ROOK:
                        black_eval = black_eval + self.rook_evaluate(square)
                    elif piece.piece_type == chess.QUEEN:
                        black_eval = black_eval + self.queen_evaluate(square)
                    elif piece.piece_type == chess.KING:
                        black_eval = black_eval + self.king_evaluate(square)

        return white_eval + black_eval

def basic_alpha_beta(engine, depth=3, alpha=-math.inf, beta=math.inf):
    best_move = None
    next_move = None
    if engine.board.is_checkmate():
        if engine.color == W:
            eval = int(-10000000)
        else:
            eval = int(10000000)
        return eval, None
    if engine.is_draw():
        return 0, None
    if depth == 0:
        # print(engine.board)
        # print(engine.evaluate())
        return engine.evaluate(), None
    if engine.color == W:
        max_eval = -math.inf
        moves = engine.board.legal_moves
        for move in moves:
            child = engine.get_child(move)
            # print(child.board)
            eval, next_move = basic_alpha_beta(child, depth-1, alpha, math.inf)
            alpha = max(alpha, eval)
            # print(move, eval, best_move, max_eval)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        moves = engine.board.legal_moves
        for move in moves:
            child = engine.get_child(move)
            eval, next_move = basic_alpha_beta(child, depth-1, -math.inf, beta)
            beta = min(beta, eval)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            if beta <= alpha:
                break
        return min_eval, best_move

# flag = 1
engine = Chess('rnbqkbnr/1pppp1pp/8/p7/4P3/1B3Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1')
engine.color = W
eval, move = basic_alpha_beta(engine, 3, -math.inf, math.inf)
print(move)
# while flag:
#     eval, move = basic_alpha_beta(engine, 3, -math.inf, math.inf)
#     print(move)
#     engine.board.push(move)
#     print(engine.board)
#     print(engine.board.legal_moves)
#     i = int(input())
#     j = int(0)
#     for move in engine.board.legal_moves:
#         if j == i:
#             engine.board.push(move)
#             break
#         j=j+1

    
