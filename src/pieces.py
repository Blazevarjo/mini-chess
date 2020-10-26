import pygame


class Piece(pygame.sprite.Sprite):
    board_margin_x = 18
    board_margin_y = 23
    square_side_length = 80

    symbol = None
    piece_name = None

    def __init__(self, color, x, y):
        super().__init__()
        self.color = color
        self.x = x
        self.y = y
        self.image = pygame.image.load(
            f"assets/pieces/{self.piece_name}{self.color}.png")
        self.rect = self.image.get_rect()

        self.set_rect_position()

    def __str__(self):
        return f'{self.piece_name} x:{self.x} y:{self.y}'

    def set_rect_position(self):
        self.rect.x = self.board_margin_x + self.square_side_length * self.x
        self.rect.y = self.board_margin_y + self.square_side_length * self.y

    # set new position for piece (x, y) and rect (x, y)
    def set_new_position(self, board):
        # get values from center of field
        x = round((self.rect.x - 18) / 80)
        y = round((self.rect.y - 23) / 80)
        if (x, y) in self.valid_moves(board):
            self.x = x
            self.y = y

        self.set_rect_position()

    def valid_moves(self, board):
        pass

    def valid_moves_position(self, board):
        positions = []
        for square in self.valid_moves(board):
            x = self.board_margin_x + self.square_side_length * square[0]
            y = self.board_margin_y + self.square_side_length * square[1]
            positions.append((x, y))

        return positions


def is_valid_attack(x, y, color, chessboard_array):
    check_square = chessboard_array[y][x]

    if isinstance(check_square, Piece):
        if check_square.color == color:
            return False
        return True

    return False


def is_valid_inbound(x, y, color, chessboard_array):
    if x >= 0 and x <= 5 and y >= 0 and y <= 5:
        check_square = chessboard_array[y][x]
        if check_square is None:
            return True
        if is_valid_attack(x, y, color, chessboard_array):
            return True

    return False


def valid_lane_moves(x, y, color, chessboard_array):
    valid_moves = set()
    for i in (-1, 1):
        x_try = x
        while(True):
            x_try += i
            if is_valid_inbound(x_try, y, color, chessboard_array):
                if is_valid_attack(x_try, y, color, chessboard_array):
                    valid_moves.add((x_try, y))
                    break
                valid_moves.add((x_try, y))
            else:
                break

    for i in (-1, 1):
        y_try = y
        while(True):
            y_try += i
            if is_valid_inbound(x, y_try, color, chessboard_array):
                if is_valid_attack(x, y_try, color, chessboard_array):
                    valid_moves.add((x, y_try))
                    break
                valid_moves.add((x, y_try))
            else:
                break

    return valid_moves


class Bishop(Piece):
    symbol = 'B'
    piece_name = "Bishop"


class King(Piece):
    symbol = 'K'
    piece_name = 'King'


class Knight(Piece):
    symbol = 'N'
    piece_name = 'Knight'


class Pawn(Piece):
    symbol = 'P'
    piece_name = 'Pawn'


class Queen(Piece):
    symbol = 'Q'
    piece_name = 'Queen'


class Rook(Piece):
    symbol = 'R'
    piece_name = 'Rook'

    def valid_moves(self, board):
        return valid_lane_moves(self.x, self.y, self.color, board)
