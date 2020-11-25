import pygame

WHITE = "W"
BLACK = "B"


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

        self.list_of_valid_moves = set()

    def __str__(self):
        return f'{self.piece_name} x:{self.x} y:{self.y}'

    def set_rect_position(self):
        self.rect.x = self.board_margin_x + self.square_side_length * self.x
        self.rect.y = self.board_margin_y + self.square_side_length * self.y

    # set new position for piece (x, y) and rect (x, y)
    def set_new_position(self):
        # get values from center of field
        x = round((self.rect.x - self.board_margin_x) /
                  self.square_side_length)
        y = round((self.rect.y - self.board_margin_y) /
                  self.square_side_length)

        if (x, y) in self.list_of_valid_moves:
            self.x = x
            self.y = y

        self.set_rect_position()

    def generate_valid_moves(self, board):
        self.list_of_valid_moves = self.valid_moves(board)

    def valid_moves(self, board):
        pass

    def valid_moves_position(self):
        positions = []
        for square in self.list_of_valid_moves:
            x = self.board_margin_x + self.square_side_length * square[0]
            y = self.board_margin_y + self.square_side_length * square[1]
            positions.append((x, y))

        return positions


def is_valid_attack(x, y, color, chessboard_array):
    check_square = chessboard_array[y][x]
    # check if square contains piece and if it does it checks
    # if it's the same color as yours, if not you can attack
    if isinstance(check_square, Piece):
        return not (check_square.color == color)

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


def valid_diagonal_moves(x, y, color, chessboard_array):
    valid_moves = set()
    for i in (-1, 1):
        for z in (-1, 1):
            x_try = x
            y_try = y
            while(True):
                x_try += i
                y_try += z
                if is_valid_inbound(x_try, y_try, color, chessboard_array):
                    if is_valid_attack(x_try, y_try, color, chessboard_array):
                        valid_moves.add((x_try, y_try))
                        break
                    valid_moves.add((x_try, y_try))
                else:
                    break

    return valid_moves


class Bishop(Piece):
    symbol = 'B'
    piece_name = "Bishop"

    def valid_moves(self, board):
        return valid_diagonal_moves(self.x, self.y, self.color, board)


class King(Piece):
    symbol = 'K'
    piece_name = 'King'

    def valid_moves(self, board):
        valid_moves = set()

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == j == 0:
                    continue
                x_try = self.x + i
                y_try = self.y + j

                if is_valid_inbound(x_try, y_try, self.color, board):
                    valid_moves.add((x_try, y_try))

        return valid_moves


class Knight(Piece):
    symbol = 'N'
    piece_name = 'Knight'

    def valid_moves(self, board):
        valid_moves = set()

        for i in (-1, 1):
            for j in (-2, 2):
                x_try = self.x + i
                y_try = self.y + j
                if is_valid_inbound(x_try, y_try, self.color, board):
                    valid_moves.add((x_try, y_try))

        for i in (-2, 2):
            for j in (-1, 1):
                x_try = self.x + i
                y_try = self.y + j
                if is_valid_inbound(x_try, y_try, self.color, board):
                    valid_moves.add((x_try, y_try))

        return valid_moves


class Pawn(Piece):
    symbol = 'P'
    piece_name = 'Pawn'

    def valid_moves(self, board):
        valid_moves = set()

        if self.color == WHITE:
            y_try = self.y - 1

            # pawn is on the edge of board
            if y_try < 0:
                return valid_moves

            if board[y_try][self.x] is None:
                valid_moves.add((self.x, y_try))

            if self.x - 1 >= 0 and board[y_try][self.x - 1] is not None and board[y_try][self.x - 1].color == BLACK:
                valid_moves.add((self.x - 1, y_try))

            if self.x + 1 < 6 and board[y_try][self.x + 1] is not None and board[y_try][self.x + 1].color == BLACK:
                valid_moves.add((self.x + 1, y_try))

        elif self.color == BLACK:
            y_try = self.y + 1

            # pawn is on the edge of board
            if y_try > 5:
                return valid_moves

            if board[y_try][self.x] is None:
                valid_moves.add((self.x, y_try))

            if self.x - 1 >= 0 and board[y_try][self.x - 1] is not None and board[y_try][self.x - 1].color == WHITE:
                valid_moves.add((self.x - 1, y_try))

            if self.x + 1 < 6 and board[y_try][self.x + 1] is not None and board[y_try][self.x + 1].color == WHITE:
                valid_moves.add((self.x + 1, y_try))

        return valid_moves


class Queen(Piece):
    symbol = 'Q'
    piece_name = 'Queen'

    def valid_moves(self, board):
        diagonal_moves = valid_diagonal_moves(
            self.x, self.y, self.color, board)
        lane_moves = valid_lane_moves(self.x, self.y, self.color, board)

        return diagonal_moves.union(lane_moves)


class Rook(Piece):
    symbol = 'R'
    piece_name = 'Rook'

    def valid_moves(self, board):
        return valid_lane_moves(self.x, self.y, self.color, board)
