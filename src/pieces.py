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
    def set_new_position(self):
        # get values from center of field        
        self.x = round((self.rect.x - 18) / 80)
        self.y = round((self.rect.y - 23) / 80)
        self.set_rect_position()


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
