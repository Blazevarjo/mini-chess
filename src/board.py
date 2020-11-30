import pygame
import copy

from pieces import (
    King,
    Knight,
    Pawn, Piece,
    Rook,
    Queen,
    WHITE, BLACK
)


class Board(pygame.Surface):
    def __init__(self):
        BOARD_SIZE = 520

        super().__init__([BOARD_SIZE, BOARD_SIZE])

        self.COLOR_RED = [255, 0, 0]
        self.PADDING = 10
        self.BOX_SIDE_LENGTH = 60
        self.BOX_BORDER_RADIUS = 5

        self.image = pygame.image.load('assets/Chess_Board.png')
        self.blit(self.image, [0, 0])

        # board but in matrix 6x6
        self.array = [
            [Rook(BLACK, 0, 0), Knight(BLACK, 1, 0), King(BLACK, 2, 0),
             Queen(BLACK, 3, 0), Knight(BLACK, 4, 0), Rook(BLACK, 5, 0)],
            [Pawn(BLACK, x, 1) for x in range(6)],
            [None for x in range(6)],
            [None for x in range(6)],
            [Pawn(WHITE, x, 4) for x in range(6)],
            [Rook(WHITE, 0, 5), Knight(WHITE, 1, 5), King(WHITE, 2, 5),
             Queen(WHITE, 3, 5), Knight(WHITE, 4, 5), Rook(WHITE, 5, 5)]
        ]

        # flatten 2d array and get only valid pieces to draw (delete None values)
        self.pieces = [
            piece for row in self.array for piece in row if piece is not None]

        # generate valid moves for white player
        self.generate_valid_moves_for_player_pieces(WHITE, BLACK)

        self.sprites_group = pygame.sprite.Group()
        self.sprites_group.add(self.pieces)

    # update sprites on screen and draw them
    def blit_self(self):
        self.blit(self.image, [0, 0])

    def update(self):
        self.sprites_group.draw(self)

    # bring piece up, to a first layer
    def move_up(self, piece):
        self.sprites_group.remove(piece)
        self.sprites_group.add(piece)

    def pawn_promotion(self, pawn, promotion_piece):

        promoted_piece = None
        if promotion_piece == 'N':
            promoted_piece = Knight(pawn.color, pawn.x, pawn.y)
        elif promotion_piece == 'R':
            promoted_piece = Rook(pawn.color, pawn.x, pawn.y)
        elif promotion_piece == 'Q':
            promoted_piece = Queen(pawn.color, pawn.x, pawn.y)
        else:
            ValueError("Wrong piece")
        self.array[pawn.y][pawn.x] = promoted_piece
        self.set_piece_position(promoted_piece)
        self.pieces.remove(pawn)
        self.pieces.append(promoted_piece)
        pawn.kill()
        self.sprites_group.add(promoted_piece)

    # checking all pieces which can collide with given coords
    # and color (only one player can play at the same time!)

    def get_collided_piece(self, pos, color):
        for piece in self.pieces:
            if piece.rect.collidepoint(pos) and piece.color == color:
                return piece

        return None

    def set_piece_position(self, focused_piece, is_not_fake=True, board=None):
        if board is None:
            board = self.array

        old_y, old_x = focused_piece.y, focused_piece.x

        # assign new position of piece to board array
        focused_piece.set_new_position()

        attacked_piece = board[focused_piece.y][focused_piece.x]

        # when the piece didn't move
        if attacked_piece is board[old_y][old_x]:
            return False

        # set old position to None
        board[old_y][old_x] = None

        # remove attacked piece
        # in real game (not in checking all possibly position for pieces)
        if is_not_fake and attacked_piece is not None and attacked_piece is not focused_piece:
            attacked_piece.kill()
            self.pieces.remove(attacked_piece)

        board[focused_piece.y][focused_piece.x] = focused_piece

        # generate valid moves on new position
        focused_piece.generate_valid_moves(board)

        # when the piece moved
        return True

    # draw rectangles on legal moves for single piece
    def draw_valid_moves(self, piece):
        for x, y in piece.valid_moves_position():
            pygame.draw.rect(self, self.COLOR_RED,
                             [x + self.PADDING, y + self.PADDING,
                              self.BOX_SIDE_LENGTH, self.BOX_SIDE_LENGTH],
                             self.BOX_BORDER_RADIUS)

    # draw a rectangle on checked king
    def draw_check_warning(self, color):
        for row in self.array:
            for piece in row:
                if piece is not None and piece.color == color and piece.piece_name == "King":
                    pygame.draw.rect(self, self.COLOR_RED,
                                     [piece.rect.x + self.PADDING, piece.rect.y + self.PADDING,
                                      self.BOX_SIDE_LENGTH, self.BOX_SIDE_LENGTH],
                                     self.BOX_BORDER_RADIUS)
                    return

    def is_check(self, current_player, opponent_color, board=None):
        if board is None:
            board = self.array

        # get all pieces with given color
        player_pieces = [
            piece for row in board for piece in row if piece is not None and piece.color == current_player]

        moves = set()

        # get all unique moves from current player
        for piece in player_pieces:
            piece.generate_valid_moves(board)
            moves.update(piece.list_of_valid_moves)

        for row in board:
            for piece in row:
                if isinstance(piece, King) and piece.color == opponent_color:
                    # check if opponent can KILL current player's king
                    return (piece.x, piece.y) in moves

    # generate valid moves for all pieces

    def generate_valid_moves_for_player_pieces(self, current_player, opponent_color):
        moves = set()

        for piece in self.pieces:
            if piece.color == current_player:
                piece.generate_valid_moves(self.array)

                temp_valid_moves = piece.list_of_valid_moves.copy()

                for move in temp_valid_moves:
                    copy_piece = copy.copy(piece)
                    copy_piece.rect = piece.rect.copy()

                    # "move" copy_piece on selected position
                    copy_piece.rect.x = move[0] * \
                        Piece.square_side_length + Piece.board_margin_x
                    copy_piece.rect.y = move[1] * \
                        Piece.square_side_length + Piece.board_margin_y

                    # create copy of board to create a "simulation"
                    temp_board = [row[:] for row in self.array]

                    self.set_piece_position(copy_piece, False, temp_board)

                    # if after the move king is still is checked
                    # it's illegal move then
                    if self.is_check(opponent_color, current_player, temp_board):
                        piece.list_of_valid_moves.remove(move)

                # save all unique position to move
                moves.update(piece.list_of_valid_moves)

        # return false when player can't move
        return moves == set()

    def is_stalemate(self, current_player_color, next_player_color):
        return not self.is_check(current_player_color, next_player_color)
